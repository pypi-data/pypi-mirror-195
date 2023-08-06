"""
Create a temporary local environment which mimics a real DL job.
"""
import functools
import multiprocessing as mp
import os
import signal
import tempfile

import portpicker


def elastic_multiprocessing(func):
    """
    Decorator which runs a function inside a temporary local environment
    which mimics a real DL job. Runs replicas of the decorated function
    in their own processes, and sets up the shared environment, including
    environment variables and shared directories. The decorated function is
    always started with a single replica, but can optionally return an integer
    number of replicas to trigger a restart using that many replicas.

    ```python
    @elastic_multiprocessing
    def test_my_stuff():
        from KUBEGA.env import num_replicas, num_restarts
        if num_restarts() == 0:
            print(num_replicas)  # Outputs '1'.
            return 5  # Restart using 5 replicas.
        if num_restarts() == 1:
            print(num_replicas)  # Outputs '5'.
        return 0  # No more restarts, this line can be omitted.
    ```

    .. warning::
       The replica processes are forked from the current main process. This
       means that mutations to global variables in the main process prior to
       calling the decorated function may be observed by the child processes!
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        num_restarts = 0
        num_replicas = 1
        with tempfile.TemporaryDirectory() as tmpdir:
            while num_replicas:
                assert isinstance(num_replicas, int)
                master_port = portpicker.pick_unused_port()
                queue = mp.Queue()  # For passing return values back.

                def run(rank):  # Invoked in each child process.
                    os.environ["KUBEGA_CHECKPOINT_PATH"] = str(tmpdir)
                    os.environ["KUBEGA_JOB_ID"] = "tmpjob"
                    os.environ["KUBEGA_MASTER_PORT"] = str(master_port)
                    os.environ["KUBEGA_REPLICA_RANK"] = str(rank)
                    os.environ["KUBEGA_NUM_REPLICAS"] = str(num_replicas)
                    os.environ["KUBEGA_NUM_NODES"] = "1"
                    os.environ["KUBEGA_NUM_RESTARTS"] = str(num_restarts)
                    res = None
                    try:
                        res = func(*args, **kwargs)
                    finally:
                        queue.put((rank, res))

                # Start each replica in a separate child process.
                procs = [mp.Process(target=run, args=(rank,))
                         for rank in range(num_replicas)]
                for proc in procs:
                    proc.start()

                try:  # Wait for results from child processes.
                    for i in range(num_replicas):
                        rank, result = queue.get()
                        procs[rank].join()
                        assert procs[rank].exitcode == 0
                        if i == 0:  # All return values should be the same.
                            num_replicas = result
                        assert num_replicas == result
                finally:
                    # Clean up any remaining child processes.
                    for proc in procs:
                        if proc.is_alive():
                            os.kill(proc.pid, signal.SIGKILL)
                        proc.join()
                    # Clean up the queue.
                    queue.close()
                num_restarts += 1

    return wrapper
