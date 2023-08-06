"""
A wrapper of allreduce primitives.
"""
from kubega import env
from kubega.allreduce import Reducer, default_reduce_fn

_REDUCER = None


def init(master_addr=None, master_port=None, replica_rank=None, num_replicas=None):
    """
    Initialize this module, must be invoked before calling any other functions.
    This function will block until it has been invoked from all replicas.

    Arguments:
        master_addr: address of the replica with rank 0.
        master_port: free port of the replica with rank 0.
        replica_rank: rank of the current replica.
        num_replicas: total number of replicas.

    Raises:
        RuntimeError: If this module had already been initialized.
    """
    global _REDUCER
    if replica_rank is None:
        replica_rank = env.replica_rank()
    if num_replicas is None:
        num_replicas = env.num_replicas()

    if _REDUCER is not None:
        raise RuntimeError("{} is already initialized".format(__name__))

    if master_addr is None:
        master_addr = env.master_addr()
    if master_port is None:
        master_port = env.master_port()
    _REDUCER = Reducer(replica_rank, num_replicas, master_addr, master_port)


def teardown():
    """
    Teardown this module, will block until this function has been invoked from
    all replicas.

    Raises:
        RuntimeError: If this module has not been initialized.
    """
    raise NotImplementedError


def allreduce(value, reduce_fn=default_reduce_fn):
    """
    Reduces a value across all replicas in such a way that they all get the
    final result. Blocks until this function is invoked by all replicas.

    Arguments:
        value (object): The object which will be reduced together with all
            other replicas.
        reduce_fn (Function): A reduction function which two objects as
            arguments, and returns the resulting reduced object.

    Returns:
        object: Resulting value after being reduced across all replicas.

    Raises:
        RuntimeError: If this module has not been initialized.
    """
    if _REDUCER is None:
        raise RuntimeError("{} has not been initialized".format(__name__))
    return _REDUCER.allreduce(value, reduce_fn)


def allreduce_async(value, reduce_fn=default_reduce_fn):
    """
    Asynchronous version of the `allreduce` function. Does not block, instead
    returns a future which can be used to obtain the result later.

    Arguments:
        value (object): The object which will be reduced together with all
            other replicas.
        reduce_fn (Function): A reduction function which two objects as
            arguments, and returns the resulting reduced object.

    Returns:
        Future: Object from which the result can be obtained later.

    Raises:
        RuntimeError: If this module has not been initialized.
    """
    if _REDUCER is None:
        raise RuntimeError("{} has not been initialized".format(__name__))
    return _REDUCER.allreduce_async(value, reduce_fn)


def broadcast(value):
    """
    Broadcasts a value from the replica of rank 0 to all replicas. Blocks until
    this function is invoked by all replicas.

    Arguments:
        value (object): The object which will be broadcasted from replica 0.
            Ignored on all other replicas.

    Returns:
        object: The value broadcasted from replica 0.

    Raises:
        RuntimeError: If this module has not been initialized.
    """
    if _REDUCER is None:
        raise RuntimeError("{} has not been initialized".format(__name__))
    return _REDUCER.broadcast(value)
