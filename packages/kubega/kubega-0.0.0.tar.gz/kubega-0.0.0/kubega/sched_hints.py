"""
This module provides a function to post the optimized scheduling hints
(resource allocation details for a job) to the supervisor.
"""
import json
import logging
from collections import OrderedDict
from types import MappingProxyType

import requests

from kubega import env
from kubega.goodput import PerfParams

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

PERF_PARAMS = MappingProxyType(OrderedDict({k: 0. for k in PerfParams._fields}))
SCHED_HINTS = MappingProxyType({'initBatchSize': 0,
                                'localBszBounds': None,  # [min, max]
                                'globalBatchSize': None,
                                'maxBatchSize': 0,
                                'maxProfiledReplicas': 0,
                                'gradientAccumulation': False,
                                'gradParams': None,
                                'perfParams': None})


def post_sched_hints(sched_hints, job_key):
    url = env.supervisor_url()
    if not url or url == "":
        return
    headers = {"Content-Type": "application/json"}
    try:
        for k in sched_hints:
            assert k in SCHED_HINTS

        response = requests.put(
            url=f"{url}/hints/{job_key}",
            data=json.dumps(sched_hints),
            headers=headers
        )
        if response.status_code != 200:
            LOG.warning(f"Received {response.status_code}")
    except Exception as e:
        LOG.warning(f"{e}")
