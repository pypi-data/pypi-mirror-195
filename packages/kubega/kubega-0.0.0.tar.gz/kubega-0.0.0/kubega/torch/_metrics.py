import collections
import pickle
import time

import numpy as np

from kubega import checkpoint, env
from kubega.goodput import Goodput, fit_perf_params
from kubega.sched_hints import SCHED_HINTS, PERF_PARAMS, post_sched_hints

_METRICS_STATE = None
_GRAD_PARAM_DICT = {}
_PREV_REPORT_TIME = None


def _metrics_state():
    """
    Get metrics state from checkpoints.
    """
    global _METRICS_STATE
    if _METRICS_STATE is None:
        _METRICS_STATE = _MetricsState()
        checkpoint.load_state(_METRICS_STATE)
    return _METRICS_STATE


def _get_sched_hints():
    state = _metrics_state()
    if len(state.profile) == 0:
        return None
    _fit_perf_params()
    return _metrics_state()


def _post_sched_hints():
    assert env.replica_rank() == 0
    state = _metrics_state()
    sched_hints = SCHED_HINTS.copy()

    sched_hints["perfParams"] = {k: v for (k, v) in zip(PERF_PARAMS.keys(), state.perf_params)}
    sched_hints["maxBatchSize"] = state.max_batch_size
    sched_hints["localBszBounds"] = state.local_bsz_bounds
    sched_hints["initBatchSize"] = state.init_batch_size
    if state.grad_params:
        sched_hints["gradParams"] = {}
        sched_hints["gradParams"]["norm"] = state.grad_params[0]
        sched_hints["gradParams"]["var"] = state.grad_params[1]
    sched_hints["maxProfiledReplicas"] = max(key[1] for key in state.profile)
    sched_hints["gradientAccumulation"] = state.gradient_accumulation

    post_sched_hints(sched_hints, env.job_id())


def get_goodput():
    state = _metrics_state()
    if state.grad_params is None or state.perf_params is None:
        return None
    return Goodput(state.perf_params, state.grad_params, state.init_batch_size)


def profile_step_start(atomic_bsz):
    state = _metrics_state()

    state.atomic_bsz = atomic_bsz
    state.step_start = time.time()
    state.sync_time = 0.0


def update_batch_size(init_batch_size, max_batch_size, local_bsz_bounds, grad_accum):
    state = _metrics_state()

    state.init_batch_size = init_batch_size
    state.max_batch_size = max_batch_size
    state.local_bsz_bounds = local_bsz_bounds
    state.gradient_accumulation = grad_accum


def update_grad_params(edp_key, grad_norm_sqr, grad_variance):
    state = _metrics_state()

    global _GRAD_PARAM_DICT
    _GRAD_PARAM_DICT[edp_key] = np.asarray([grad_norm_sqr, grad_variance])
    grad_params = sum(_GRAD_PARAM_DICT.values())

    state.grad_params = (grad_params[0], grad_params[1])


def update_sync_time(sync_time):
    state = _metrics_state()
    state.sync_time += sync_time


def profile_step_commit(accum_step=False):
    global _PREV_REPORT_TIME
    state = _metrics_state()

    step_time = time.time() - state.step_start
    num_nodes = env.num_nodes()
    num_replicas = env.num_replicas()
    key = (num_nodes, num_replicas, state.atomic_bsz)
    if accum_step:
        state.profile[key]["accum_step_time"] += step_time
        state.profile[key]["accum_count"] += 1
    else:
        state.profile[key]["optim_step_time"] += step_time
        state.profile[key]["optim_sync_time"] += state.sync_time
        state.profile[key]["optim_count"] += 1
    del state.atomic_bsz
    del state.step_start
    del state.sync_time

    if not accum_step:
        if _PREV_REPORT_TIME is None:
            _PREV_REPORT_TIME = time.time()
        if env.replica_rank() == 0 and time.time() - _PREV_REPORT_TIME > 30:
            _fit_perf_params()
            _post_sched_hints()
            _PREV_REPORT_TIME = time.time()


def update_progress(progress):
    _metrics_state().progress = progress


def get_progress():
    return _metrics_state().progress


class _MetricsState(checkpoint.State):
    """
    The state to be saved into checkpoints in this design.
    """

    def __init__(self):
        super().__init__("kubega-metrics")
        self.profile = collections.defaultdict(collections.Counter)
        self.perf_params = None
        self.grad_params = None
        self.init_batch_size = None
        self.max_batch_size = None
        self.local_bsz_bounds = None
        self.gradient_accumulation = False
        self.progress = 0.0  # Progress in scale-invariant iterations.

    def save(self, fileobj):
        pickle.dump(self.profile, fileobj)
        pickle.dump(self.perf_params, fileobj)
        pickle.dump(self.grad_params, fileobj)
        pickle.dump(self.init_batch_size, fileobj)
        pickle.dump(self.max_batch_size, fileobj)
        pickle.dump(self.local_bsz_bounds, fileobj)
        pickle.dump(self.gradient_accumulation, fileobj)
        pickle.dump(self.progress, fileobj)

    def load(self, fileobj):
        self.profile = pickle.load(fileobj)
        self.perf_params = pickle.load(fileobj)
        self.grad_params = pickle.load(fileobj)
        self.init_batch_size = pickle.load(fileobj)
        self.max_batch_size = pickle.load(fileobj)
        self.local_bsz_bounds = pickle.load(fileobj)
        self.gradient_accumulation = pickle.load(fileobj)
        self.progress = pickle.load(fileobj)


def _fit_perf_params():
    """
    Load metrics from checkpoints and get the optimal resource allocation setting by fitting.
    """
    state = _metrics_state()
    profile = {k: v for k, v in state.profile.items() if v.get("optim_count")}
    num_nodes, num_replicas, atomic_bsz = (np.array(k) for k in zip(*profile.keys()))

    accum_step_time = np.array([v.get("accum_step_time", 0.0) for v in profile.values()])
    accum_count = np.array([v.get("accum_count", 0) for v in profile.values()])
    optim_step_time = np.array([v.get("optim_step_time", 0.0) for v in profile.values()])
    optim_sync_time = np.array([v.get("optim_sync_time", 0.0) for v in profile.values()])
    optim_count = np.array([v.get("optim_count", 0) for v in profile.values()])
    assert np.all(optim_count > 0)

    # Non-sync time during optimization steps should be approximately equal to
    # accumulation step time, combine those data points.
    assert np.all(optim_step_time >= optim_sync_time)
    accum_step_time += optim_step_time - optim_sync_time
    accum_count += optim_count
    accum_step_time /= accum_count
    optim_step_time /= optim_count
    state.perf_params = fit_perf_params(num_nodes, num_replicas, atomic_bsz,
                                        accum_step_time, optim_step_time)
