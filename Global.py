import copy
import numpy as np
import pandas as pd
from multiprocessing import Process, Queue

n = 8

n_workers = 18

myQueue = Queue()

df = pd.DataFrame(columns = ['name', 'worker_id', 'active', 'born', 'die', 'parent', 
                             'iter_999', 'iter_1999', 'iter_2999', 'iter_3999', 'iter_4999'])

rules = dict(
            FIR_outs = [2, 13],
            LowBitFIR_outs = [1, 7],
            LUT_dims = [0, 4],
            LUT_n_points = [2, 5],
            ClusterLUT_dims = [0, 2],
            n_clusters = [3, 11],
            ClusterLUT_n_points = [2, 6],
            LUT_mixer_outs = [2, 9]
            )

all_exp_params = []
for worker_id in range(n_workers):
    exp_params = dict(
                    worker_id = worker_id,
                    gpu_id = 2 + worker_id//3,
                    seed = 42,
                    n_epochs = 5000
                    )
    all_exp_params.append(exp_params)
