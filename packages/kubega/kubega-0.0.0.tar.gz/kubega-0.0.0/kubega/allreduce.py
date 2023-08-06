"""
This module contains simple collective communications primitives which operate
on arbitrary python objects. It is meant to be general but *non-performant*.
Only use these primitives if you are synchronizing *small* objects which can be
efficiently pickled and operated on. For larger objects, use framework-specific
functions, such as those provided by `torch.distributed`.

The functions in this module should be invoked *in the same order* across all
replicas in the current job. Otherwise, their behavior is undefined, and you may
encounter unexpected bugs and errors.
"""
import logging
import pickle
import socket
import sys
import threading
import time
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def default_reduce_fn(a, b):
    a += b
    return a


class Reducer:
    """
    Simple asynchronous allreduce operations on python objects.
    The replica with rank 0 is selected as the root pod, the left replicas are worker pods.

    Assume all invocations to allreduce, allreduce_async, and ``Future.result`` happen in the
    same order across all processes.
    """

    def __init__(self, rank, replicas, root_host, root_port):
        self._root_port = root_port
        self._result_map = {}
        self._next_key = 0
        self._rank = rank

        if rank == 0:
            # this is the root pod, start server on it
            self._reduce_fn_map = {}
            threading.Thread(target=self._run_server,
                             args=(self._root_port, replicas),
                             daemon=True).start()
        # Keep retrying connection, because
        # (1) the root pod might not have a registered domain name yet, and
        # (2) the root server socket might not be bound yet.
        exception_cnt = 0
        while True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if exception_cnt > 25:
                logger.error("Could not connect to root after max retries, exiting...")
                break
            try:
                if self._root_port == 0:
                    # waiting for server to get a valid port in local mode
                    raise ConnectionRefusedError
                logger.info(f"rank {rank} of {replicas} connecting to "
                            f"{root_host} on port {self._root_port}")
                sock.connect((root_host, self._root_port))
            except ConnectionRefusedError:
                logger.warning("Could not connect to root, trying again...")
                exception_cnt += 1
                time.sleep(5)
            else:
                # if no error happens
                break
        self._sockfile = sock.makefile("rwb")
        pickle.dump(rank, self._sockfile)
        self._sockfile.flush()

    def _run_server(self, port, replicas):
        try:
            listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listener.bind(("0.0.0.0", port))
            if port == 0:
                # local mode
                self._root_port = listener.getsockname()[1]
            listener.listen(replicas)
            # wait for connections from all clients
            logger.info(f"Master waiting for connections on {port}")
            clients = [None] * replicas
            while None in clients:
                client = listener.accept()[0].makefile("rwb")
                rank = pickle.load(client)
                assert clients[rank] is None
                clients[rank] = client

            # All connected. Now start the main loop.
            key = 0
            while True:
                # allreduce: reduce the result from root pod
                # reduce is implemented based on the received obj which are sent from clients
                for rank, client in enumerate(clients):
                    obj = pickle.load(client)
                    if rank == 0:
                        result = obj
                        reduce_fn = self._reduce_fn_map.pop(key)
                    else:
                        result = reduce_fn(result, obj)
                # Respond to clients in reverse order, with rank 0 last.
                # Prevent deadlocks where the rank 0 client gets unblocked
                # first and grab the GIL in a later operation, blocking this
                # server from responding to the remaining replicas.
                for client in reversed(clients):
                    pickle.dump((key, result), client)
                    client.flush()
                key += 1

        except Exception as e:
            traceback.print_exception(*sys.exc_info())
            logger.error(f"reducer server failed because of {e}")
            exit(1)

    def allreduce_async(self, obj, reduce_fn=default_reduce_fn):
        key = self._next_key
        self._next_key += 1
        try:
            self._reduce_fn_map[key] = reduce_fn
        except AttributeError:
            pass
        pickle.dump(obj, self._sockfile)
        self._sockfile.flush()
        return Future(self, key)

    def allreduce(self, obj, reduce_fn=default_reduce_fn):
        future = self.allreduce_async(obj, reduce_fn)
        return future.result()

    def broadcast(self, obj):
        """
        Use left projection to implement broadcast
        (Broadcast the reduced result from root pod to all work pods).
        """
        return self.allreduce(obj, lambda x, y: x)

    @property
    def result_map(self):
        return self._result_map

    @property
    def sockfile(self):
        return self._sockfile

    @property
    def rank(self):
        return self._rank


class Future:
    def __init__(self, reducer: Reducer, key):
        self._reducer = reducer
        self._key = key
        self._result = None

    def result(self):
        if self._result is None:
            while self._key not in self._reducer.result_map:
                try:
                    key, result = pickle.load(self._reducer.sockfile)
                    self._reducer.result_map[key] = result
                except Exception as e:
                    logger.error(f"reducer._rank = {self._reducer.rank} "
                                 f"is exiting unexpectedly because of {e}")
                    raise
            self._result = self._reducer.result_map.pop(self._key)
        return self._result
