import numpy as np
import pandas as pd

import Global
from Hyperparams import is_satisfy, get_hparams, get_name, from_name_get_params

def mutation(params, r):
    global rules
    global df
    
    while True:
        seq = sorted(np.random.randint(low=0, high=r+1, size=n-1))
        diff = np.insert(seq, -1, r) - np.insert(seq, 0, 0)
        signs = np.random.choice([-1, 1], size=n)
        delta = diff * signs
        
        new_params = params.copy()
        flag = False
        
        for i, (key, value) in enumerate(params.items()):
            if key == 'ClusterLUT_dims' and new_params['LUT_dims'] == 0:
                new_params['ClusterLUT_dims'] = 1
            else:
                if value + delta[i] >= rules[key][0] and value + delta[i] < rules[key][1]:
                    new_params[key] = value + delta[i]
                elif value - delta[i] >= rules[key][0] and value - delta[i] < rules[key][1]:
                    new_params[key] = value - delta[i]
                else:
                    delta[i] //= 2
                    if value + delta[i] >= rules[key][0] and value + delta[i] < rules[key][1]:
                        new_params[key] = value + delta[i]
                    elif value - delta[i] >= rules[key][0] and value - delta[i] < rules[key][1]:
                        new_params[key] = value - delta[i]
                    else:
                        flag = True
                        break
                        
        name = get_name(new_params)
        if df['name'].isin([name]).any() or flag:
            continue
        else:
            return new_params

        
def get_mutation_satifying_hparams(params, r):
    _r = r
    count = 0
    while True:
        if count < 100:
            new_hparams = mutation(params, _r)
            if is_satisfy(new_hparams):
                return new_hparams
        else:
            _r -= 1
            count = 0
            if _r == 0:
                return None
        count += 1