from kubega.conftest import elastic_multiprocessing
from kubega.torch.accumulator import Accumulator


@elastic_multiprocessing
def test_accumulator_restarts():
    import kubega.checkpoint
    import kubega.collective
    from kubega.env import num_restarts, replica_rank
    kubega.collective.init("0.0.0.0")
    accum = Accumulator()

    if num_restarts() == 0:
        accum["a"] += 15  # Idempotent.
    assert "a" not in accum
    with accum.synchronized():
        assert "a" in accum
        assert accum["a"] == 15
    assert "a" not in accum
    if num_restarts() == 0:
        accum["a"] -= 5  # Idempotent.
        kubega.checkpoint.save_all_states()
        return 4  # Restart with 4 replicas.

    if num_restarts() == 1:  # Idempotent.
        accum.update({"a": replica_rank(), "b": replica_rank()})
    assert len(accum) == 0
    with accum.synchronized():
        assert len(accum) == 2
        assert accum["a"] == 16
        assert accum["b"] == 6
    assert len(accum) == 0
    if num_restarts() == 1:
        kubega.checkpoint.save_all_states()
        return 2  # Restart with 2 replicas.

    if num_restarts() == 2:  # Idempotent.
        accum -= {"b": 5, "c": 5}
    with accum.synchronized():
        assert accum["a"] == 16
        assert accum["b"] == -4
        assert accum["c"] == -10
        accum.clear()
    with accum.synchronized():
        assert not accum
