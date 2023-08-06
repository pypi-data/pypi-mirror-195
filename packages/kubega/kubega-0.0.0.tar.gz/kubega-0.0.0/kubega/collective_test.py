from kubega.conftest import elastic_multiprocessing


@elastic_multiprocessing
def test_allreduce():
    import kubega.collective as collective
    import kubega.env as env

    collective.init("0.0.0.0")

    # allreduce with default reduce_fn (addition).
    result = collective.allreduce(env.replica_rank())
    assert result == sum(range(env.num_replicas()))

    # allreduce with custom reduce_fn (set union).
    result = collective.allreduce(
        {env.replica_rank()},
        reduce_fn=lambda a, b: a | b)
    assert result == set(range(env.num_replicas()))

    return [5, 0][env.num_restarts()]


@elastic_multiprocessing
def test_allreduce_async():
    import kubega.collective as collective
    import kubega.env as env

    collective.init("0.0.0.0")

    future_1 = collective.allreduce_async(1)
    future_2 = collective.allreduce_async(2)
    future_3 = collective.allreduce_async(3)
    assert future_2.result() == 2 * env.num_replicas()
    assert future_1.result() == 1 * env.num_replicas()
    assert future_3.result() == 3 * env.num_replicas()

    return [5, 0][env.num_restarts()]


@elastic_multiprocessing
def test_broadcast():
    import kubega.collective as collective
    import kubega.env as env

    collective.init("0.0.0.0")
    result = collective.broadcast(env.replica_rank())
    assert result == 0

    return [5, 0][env.num_restarts()]
