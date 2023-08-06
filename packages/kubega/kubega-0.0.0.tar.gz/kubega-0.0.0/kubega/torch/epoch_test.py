from kubega.conftest import elastic_multiprocessing


@elastic_multiprocessing
def test_epoch():
    import kubega.checkpoint
    from kubega.env import num_restarts
    from kubega.torch.epoch import (remaining_epochs_until,
                                    current_epoch, finished_epochs)
    total_epochs = 10
    restart_epoch = 5
    assert current_epoch() is None
    if num_restarts() == 0:
        assert finished_epochs() == 0
        expected_epochs = list(range(restart_epoch + 1))
    elif num_restarts() == 1:
        assert finished_epochs() == restart_epoch
        expected_epochs = list(range(restart_epoch, total_epochs))
    else:
        assert False
    for idx, epoch in enumerate(remaining_epochs_until(10)):
        assert epoch == expected_epochs[idx]
        assert current_epoch() == epoch
        assert finished_epochs() == epoch
        if num_restarts() == 0 and epoch == restart_epoch:
            kubega.checkpoint.save_all_states()
            return 5  # Restart with 5 replicas.
