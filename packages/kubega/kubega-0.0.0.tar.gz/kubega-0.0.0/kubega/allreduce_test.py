import collections
import faulthandler
import signal
from multiprocessing import Process

import numpy as np
import portpicker

from kubega.allreduce import Reducer

root_host = "127.0.0.1"
DEFAULT_REDUCER_PORT = portpicker.pick_unused_port()


def init(rank, replicas):
    faulthandler.enable(all_threads=True)
    faulthandler.register(signal.SIGTERM, all_threads=True, chain=False)

    reducer = Reducer(rank, replicas, root_host, DEFAULT_REDUCER_PORT)
    if rank == 0:
        batch_size = 64
        x = {"foo": 1}
    else:
        x = {"bar": 1}
        batch_size = 0

    # Test 1: do a bunch of broadcasts
    # Because broadcast is performed by master, thus the broadcasted ``batch_size`` is 64, rather than 0
    batch_size = reducer.broadcast(batch_size)
    batch_size = reducer.broadcast(batch_size)
    batch_size = reducer.broadcast(batch_size)
    assert batch_size == 64

    # Test 2: do allreduce on Counter
    # the all reduced x is {"foo": 1, "bar": replicas - 1}
    x = reducer.allreduce(collections.Counter(x))
    assert x["foo"] == 1
    assert x["bar"] == replicas - 1

    # Test 3: do an async allreduce operation
    all_reduced_x = reducer.allreduce_async(np.asarray([1, 1, 1]))
    all_reduced_x = all_reduced_x.result()
    assert np.allclose(all_reduced_x, replicas * np.asarray([1, 1, 1]))

    # Test 4: simulate a training loop
    x = None
    for _ in range(10):
        if x:
            x = x.result()
            assert np.allclose(x, replicas * np.asarray([1, 1, 1]))
        x = reducer.allreduce_async(np.asarray([1, 1, 1]))


def test_allreduce():
    _replicas = 3
    processes = []
    for _rank in range(_replicas):
        p = Process(target=init, args=(_rank, _replicas), daemon=True)
        p.start()
        processes.append(p)

    for p in processes[1:]:
        p.join()

    processes[0].join()

    for p in processes:
        assert not p.exitcode
