import pytest

from kubega.conftest import elastic_multiprocessing


@elastic_multiprocessing
def test_duplicate():
    from kubega.env import num_restarts
    from kubega.checkpoint import State
    s1 = State("state1")
    s2 = State("state2")
    with pytest.raises(ValueError):
        state_dup = State("state1")
    return [2, 0][num_restarts()]


@elastic_multiprocessing
def test_save_load():
    import pickle
    from kubega.checkpoint import State, save_all_states, load_state
    from kubega.env import replica_rank, num_restarts

    class TestState(State):
        def __init__(self, name):
            super().__init__(name)
            self.synced = False
            self.value = None

        def sync(self):
            self.synced = True

        def save(self, fileobj):
            assert replica_rank() == 0  # Should only be called from rank 0.
            pickle.dump(self.value, fileobj)

        def load(self, fileobj):
            # Should load the correct value.
            self.value = pickle.load(fileobj)

    s1 = TestState("state1")
    s2 = TestState("state2")

    if num_restarts() == 0:
        # Save all state.
        s1.value = 10
        s2.value = 20
        save_all_states()
        assert s1.synced and s2.synced
        return 2  # Restart with 2 replicas.
    elif num_restarts() == 1:
        # Load from checkpoints.
        load_state(s1)
        load_state(s2)
        assert s1.value == 10
        assert s2.value == 20
    else:
        assert False
