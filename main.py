import itertools
import os
import sys

sys.path.append("../../")  # change this to the folder where your project's root is located

import copy
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from multiprocessing import Process, Queue

import Global
from Hyperparams import is_satisfy, get_hparams, get_name, from_name_get_params
from Mutation import get_mutation_satifying_hparams

iteration = 0

r = 15

processes = []

def build_model(...):
    pass #Huawei NDA


from tensorflow.keras.callbacks import Callback
class GetScore(Callback):
    def __init__(self, model_adapter, queue, exp_params, name):
        super().__init__()
        
        self.model_adapter = model_adapter
        self.queue = queue
        self.exp_params = exp_params
        self.name = name
        
    def on_epoch_end(self, epoch, logs=None):
        if epoch % 1000 == 999:
            score = abs(self.model_adapter.history[-1]['val_nmse_left'])
            result = dict(
                        exp_params = self.exp_params,
                        name = self.name,
                        epoch = epoch,
                        score = score)
            
            self.queue.put(result)


def run_exp(queue, exp_params, model_hparams=None):
    model = build_model(model_hparams)
    MyCallback = GetScore(model, queue, exp_params, name)
    model.add_callback(MyCallback)
    
    pass #Huawei NDA


def find_best_n_worst_models(iter_n='iter_999'):
    global df
    
    Best = (df.loc[df[iter_n].notna()]).sort_values(by=iter_n)
    best_index = np.array(Best.index)[-6:]
    
    Active = (df.loc[df['active'] == 1]).sort_values(by=iter_n)
    worst_index = np.array(Active.index)[:6]
    
    return best_index, worst_index


def exploit(strong_ind, weak_ind, new_hparams=None):
    global df
    global all_exp_params
    global processes
    global myQueue
    global r
    global iteration
    
    if new_hparams == None:
        strong_name = df['name'][strong_ind]
        strong_hparams = from_name_get_params(strong_name)
        new_hparams = get_mutation_satifying_hparams(strong_hparams, r)
        if new_hparams == None:
            return False
    else:
        strong_ind = -1

    new_name = get_name(new_hparams)
    
    weak_worker_id = df['worker_id'][weak_ind]
    weak_exp_params = all_exp_params[weak_worker_id]
    processes[weak_worker_id].terminate()
    
    df['die'][(df['worker_id'] == weak_worker_id) & (df['active'] == 1)] = iteration
    df['active'][(df['worker_id'] == weak_worker_id) & (df['active'] == 1)] = 0
    
    new_row = {'name': new_name, 'worker_id': weak_worker_id, 'active': 1, 'born': iteration, 'die': None, 'parent': strong_ind, 'iter_999': None, 'iter_1999': None, 'iter_2999': None, 'iter_3999': None, 'iter_4999': None}
    df = df.append(new_row, ignore_index=True)
    
    print(weak_worker_id, ': ', new_name)
    
    args = dict(queue = myQueue,
                exp_params = weak_exp_params,
                model_hparams = new_hparams)
    
    p = Process(target=run_exp, kwargs=args)
    processes[weak_worker_id] = p
    p.start()
    return True


for worker_id in range(n_workers):
    hparams = get_satifying_hparams()
    name = get_name(hparams)
            
    new_row = {'name': name, 'worker_id': worker_id, 'active': 1, 'born': iteration, 'die': None, 'parent': -1, 'iter_999': None, 'iter_1999': None, 'iter_2999': None, 'iter_3999': None, 'iter_4999': None}
    df = df.append(new_row, ignore_index=True)
    
    exp_params = all_exp_params[worker_id]
    args = dict(queue = myQueue,
                exp_params = exp_params,
                model_hparams = hparams)
    p = Process(target=run_exp, kwargs=args)
    processes.append(p)
    p.start()


stages = [{'start_r': 15, 'min_r': 8, 'r_step': 2, 'iter_n': 'iter_999'},
          {'start_r': 9, 'min_r': 4, 'r_step': 2, 'iter_n': 'iter_1999'},
          {'start_r': 3, 'min_r': 1, 'r_step': 1, 'iter_n': 'iter_2999'},
          {'start_r': 3, 'min_r': 1, 'r_step': 1, 'iter_n': 'iter_4999'}]

iteration += 1

level = n_workers + n_workers // 3
for stage in stages:
    r = stage['start_r']
    min_r = stage['min_r']
    step = stage['r_step']
    iter_n = stage['iter_n']
    print(f'NEW ITERATION IS STARTED! iteration={iteration}, r={r}')
    
    while r >= min_r:
        delay = 0
        while not myQueue.empty():
            delay += 1
            res = myQueue.get()
            name, epoch, score = res['name'], res['epoch'], res['score']
            df[f'iter_{epoch}'][(df['name'] == name)] = score

        if df.loc[(df['active'] == 1) & (df[iter_n])]['name'].count() == n_workers:
            print('change')
            best, worst = find_best_n_worst_models(iter_n)
            for best_ind, worst_ind in zip(best, worst):
                if not exploit(best_ind, worst_ind):
                    new_hparams = get_satifying_hparams()
                    exploit(best_ind, worst_ind, new_hparams=new_hparams)
            
            finish_indexes = df.loc[(df['active'] == 1) & (df['iter_4999'])].index
            for ind in finish_indexes:
                print('restart')
                if not exploit(ind, ind):
                    new_hparams = get_satifying_hparams()
                    exploit(ind, ind, new_hparams=new_hparams)

        if iter_n == 'iter_999' and delay >= n_workers//2:
            delay = 0
            finish_indexes = df.loc[(df['active'] == 1) & (df['iter_4999'])].index
            for ind in finish_indexes:
                print('restart')
                if not exploit(ind, ind):
                    new_hparams = get_satifying_hparams()
                    exploit(ind, ind, new_hparams=new_hparams)

        if df['name'].count() >= level:
            level = df['name'].count() + n_workers // 3
            r -= step
            iteration += 1
            if r >= min_r:
                print(f'NEW ITERATION IS STARTED! iteration={iteration}, r={r}')
            
for p in processes:
    p.join()
    
while not myQueue.empty():
    res = myQueue.get()
    name, epoch, score = res['name'], res['epoch'], res['score']
    df[f'iter_{epoch}'][(df['name'] == name)] = score

myQueue.close()

df['die'][df['die'].isna()] = iteration

df.to_csv('PBL_data.csv')