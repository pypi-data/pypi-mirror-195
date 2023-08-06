import os
import sys

if "darwin" in sys.platform.lower():
    # To avoid multiple runs of the model code
    # https://pythonspeed.com/articles/python-multiprocessing/
    import multiprocessing

    multiprocessing.set_start_method('fork')

import logging
import portpicker
import requests
import torch.distributed
import pkg_resources
import kubega.collective
import kubega.env
import semver
from kubega.torch.epoch import current_epoch, finished_epochs, remaining_epochs_until
from kubega.torch.data import current_dataloader, AdaptiveDataLoader, ElasticSampler
from kubega.torch.parallel import AdaptiveDataParallel
from kubega.torch.accumulator import Accumulator

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

__all__ = [
    "init_process_group",
    "current_epoch",
    "finished_epochs",
    "remaining_epochs_until",
    "current_dataloader",
    "AdaptiveDataLoader",
    "ElasticSampler",
    "AdaptiveDataParallel",
    "Accumulator",
]


def version_check(version):
    if semver.VersionInfo.isvalid(version) and \
            version != "0.0.0":
        return True
    else:
        return False


def init_process_group(backend,
                       init_method=None,
                       world_size=None,
                       rank=None):
    """
    Initializes the default distributed process group and the kubeGA
    collectives module.

    Args:
        backend (str or Backend): The backend to use. Use "nccl" for multi-GPU
            training else "gloo".
        init_method (str, optional): URL specifying how to initialize the
                                     process group.
        world_size (int, optional): Number of processes participating in
                                    the job
        rank (int, optional): Rank of the current process (it should be a
                              number between 0 and ``world_size``-1).

    If init_method, world_size and rank is NOT provided, typically in the
    Kubernetes environment, kubeGA will try to infer them through environment
    variables KUBEGA_MASTER_ADDR, KUBEGA_NUM_REPLICAS and
    KUBEGA_REPLICA_RANK respectively.
    """
    if kubega.env.from_ray():
        from kubega_ray.kubega.utils import unique_nodes_pg
        assert init_method is not None
        assert world_size is not None
        assert rank is not None
        os.environ["kubega_NUM_NODES"] = str(unique_nodes_pg())
        os.environ["kubega_REPLICA_RANK"] = str(rank)
        os.environ["kubega_NUM_REPLICAS"] = str(world_size)

    url = kubega.env.supervisor_url()
    master_port = kubega.env.master_port()
    if rank is None:
        rank = kubega.env.replica_rank()

    if world_size is None:
        world_size = kubega.env.num_replicas()

    if init_method is not None:
        _, master_addr, master_port = init_method.split(":")
        master_addr = master_addr[2:]
        master_port = int(master_port)
    elif url:
        key = kubega.env.job_id()
        group = kubega.env.num_restarts()
        while True:
            response = requests.get(url=f"{url}/discover/{key}/{group}")
            if response.status_code != 408:  # Timeout.
                break
        response.raise_for_status()
        master_addr = response.json()[0]
        sched_version = kubega.env.kubega_sched_version()
        trainer_version = pkg_resources.get_distribution("kubega").version
        if version_check(sched_version) and version_check(trainer_version):
            trainer_ver_maj = semver.VersionInfo.parse(trainer_version).major
            sched_ver_maj = semver.VersionInfo.parse(sched_version).major
            if trainer_ver_maj != sched_ver_maj:
                raise Exception('kubega version {} is incompatible with'
                                'scheduler version {}'.format(trainer_version,
                                                              sched_version))
    else:
        master_addr = kubega.env.master_addr()

    # Initialize collective module.
    kubega.collective.init(master_addr, master_port, rank, world_size)

    # Initialize torch.distributed.
    torch_port = kubega.collective.broadcast(portpicker.pick_unused_port())
    init_method = "tcp://{}:{}?rank={}&world_size={}".format(
        master_addr, torch_port, rank, world_size)
    LOG.info("Initializing torch.distributed using %s", init_method)
    torch.distributed.init_process_group(backend, init_method)

    LOG.info("torch.distributed initialized")
