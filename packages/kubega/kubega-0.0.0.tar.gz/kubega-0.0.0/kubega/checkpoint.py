"""
This module provides functionality to save and load arbitrary state as part of
checkpoint-restart elasticity. The `State` class can be subclassed to define
how to save/load any state to/from persistent storage, so it can be restored
after the current job restarts and resumed from where it left off.
"""
import logging
import os
import shutil

import kubega.env as env

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

CKPT_DIR_PREFIX = "checkpoint-"

# FIXME: Keeping global state like this will result in memory leaks for
#  applications which do not restart too often.
_STATES2NAMES = {}
_NAMES2STATES = {}


class State:
    """
    This class implements an arbitrary piece of state which can be saved and
    loaded as part of a checkpoint, and synchronized across all replicas.
    Should be sub-classed to define custom save, load, and sync logic.
    """

    def __init__(self, name):
        """
        Initialize the state object with a unique identifier `name`, which is
        used to refer to the saved object in persistent storage. No two `State`
        objects may share the same `name`.

        Arguments:
            name (str): Unique name of this `State` object.

        Raises:
            ValueError: If a `State` object with the given name already exists.
        """
        if name in _NAMES2STATES:
            raise ValueError("State '{}' already exists".format(name))
        _NAMES2STATES[name] = self
        _STATES2NAMES[self] = name

    def save(self, fileobj):
        """
        This method should be overridden by subclasses to define how the state
        is saved. It is invoked by `save_all_states` and `save_state` to save the
        state into persistent storage.

        Arguments:
            fileobj (BinaryIO): A binary writable file object.
        """
        pass

    def load(self, fileobj):
        """
        This method should be overridden by subclasses to define how the state
        is loaded. It is invoked by `load_state` to load the state from persistent
        storage.

        Arguments:
            fileobj (BinaryIO): A binary readable file object.
        """
        pass

    def sync(self):
        """
        This method should be overridden by subclasses to define how the state
        is synchronized across replicas. This might be necessary to make sure
        the state is consistent before saving it to persistent storage. It is
        invoked by `save_state` before saving the state.
        """
        pass


def _get_tmp_ckpt_dir(checkpoint_path):
    if checkpoint_path is None:
        return None

    tmp_dir = os.path.join(checkpoint_path, "_checkpoint")
    os.makedirs(tmp_dir, exist_ok=True)
    return tmp_dir


def save_state(state, checkpoint_dir, sync=True):
    """
    Saves a `State` object to persistent storage. First invokes `State.sync` on
    all replicas if `sync` is `True` (default), and then invokes `State.save`
    on the replica of rank 0 only. Note that we save state to a temporary
    folder first. Then, it will be renamed to the formal checkpoint folder
    after all states are saved.

    Arguments:
        state (State): The `State` object to save to persistent storage.
        checkpoint_dir (string): The directory of checkpoint.
        sync (bool): Whether `State.sync` should be invoked.
    """
    if sync:
        state.sync()
    if env.replica_rank() == 0 and checkpoint_dir is not None:
        name = _STATES2NAMES[state]
        file = os.path.join(_get_tmp_ckpt_dir(checkpoint_dir), name)
        with open(file, "wb") as f:
            state.save(f)


def save_all_states():
    """
    Invokes `save_state` on all `State` objects for which `State.skip` is True.
    This function can be used to trigger a global checkpoint and save every
    `State` in the current job.
    """
    if env.from_ray():
        from ray.tune.trainable import TrainableUtil
        checkpoint_dir = TrainableUtil.make_checkpoint_dir("/tmp", index=None, override=True)
    else:
        checkpoint_dir = env.checkpoint_path()

    for state in _STATES2NAMES:
        save_state(state, checkpoint_dir)

    # Prevent corrupting original state files in case the process got killed
    # during state file writing.
    if env.replica_rank() == 0 and checkpoint_dir is not None:
        tmp_ckpt_dir = _get_tmp_ckpt_dir(checkpoint_dir)
        ckpt_dir = os.path.join(checkpoint_dir, f"{CKPT_DIR_PREFIX}{env.num_restarts()}")
        os.rename(tmp_ckpt_dir, ckpt_dir)  # atomic, rename(src, dst)
        for dir_name in os.listdir(checkpoint_dir):
            dir_path = os.path.join(checkpoint_dir, dir_name)
            if dir_name.startswith(CKPT_DIR_PREFIX) and dir_path != ckpt_dir:
                shutil.rmtree(dir_path)
        return checkpoint_dir


def load_state(state):
    """
    Load the given `State` object from persistent storage. If the object was
    previously saved, then `State.load()` will be invoked with a readable file
    object to load from.

    Arguments:
        state (State): `State` object to load from persistent storage.

    Returns:
        `True` if state was previously saved and `State.load` was invoked,
        `False` otherwise.
    """
    if env.from_ray():
        from ray.tune import session
        # TODO: Check this. get_checkpoint() --> loaded_checkpoint()?
        checkpoint_dir = session.get_session().loaded_checkpoint()
    else:
        checkpoint_dir = env.checkpoint_path()
    if checkpoint_dir is None:
        return False

    ckpt_dirs = os.listdir(checkpoint_dir)
    if not ckpt_dirs:
        LOG.info(f"No checkpoint found in {checkpoint_dir}.")
        return False

    latest_restart_id = 0
    for dir_name in ckpt_dirs:
        if dir_name.startswith(CKPT_DIR_PREFIX):
            restart_id = int(dir_name[len(CKPT_DIR_PREFIX):])
            latest_restart_id = max(latest_restart_id, restart_id)

    if latest_restart_id != env.num_restarts() - 1:
        LOG.warning("Cannot find checkpoint from the last restart. "
                    f"Loading checkpoint from restart {latest_restart_id}.")

    ckpt_dir = os.path.join(checkpoint_dir, f"{CKPT_DIR_PREFIX}{latest_restart_id}")
    name = _STATES2NAMES[state]
    state_file = os.path.join(ckpt_dir, name)
    if not os.path.isfile(state_file):
        LOG.warning(f"Cannot find state file {state_file}.")
        return False

    with open(state_file, "rb") as f:
        state.load(f)

    return True
