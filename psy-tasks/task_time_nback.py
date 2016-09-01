import importlib

import nengo
import numpy as np
from psyrun import Param

from gosmann_frontiers2016.benchmarks.benchmark import benchmark_time


pspace = (
    Param(model=['nback']) *
    Param(sd=[1, 16]))
pspace *= Param(backend=['reference', 'ocl_gpu', 'ocl_cpu', 'optimized'])
pspace *= Param(neuron_type=['LIF', 'LIFRate', 'Direct'])
pspace *= Param(trial=range(5))

min_items = 1
max_jobs = None


def execute(model, backend, neuron_type, trial, **kwargs):
    kwargs = {k: v for k, v in kwargs.items() if np.isfinite(v)}
    mod = importlib.import_module('gosmann_frontiers2016.benchmarks.' + model)
    with nengo.Config(nengo.Ensemble) as cfg:
        cfg[nengo.Ensemble].neuron_type = getattr(nengo.neurons, neuron_type)()
        model = getattr(mod, model)(**kwargs)
    return benchmark_time(model, backend)