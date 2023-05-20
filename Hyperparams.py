import numpy as np

import Global

def get_area(params): #return chip area of the model with this params.
    area = 0
    pass #Huawei NDA
    return area    


def is_satisfy(params, limit):
    return get_area(params) <= limit


def get_hparams(rules):
    lut_dims = np.random.choice(np.arange(rules['LUT_dims'][0], rules['LUT_dims'][1]))
    hparams = dict()
    for key, limits in rules.items():
        if key == 'LUT_dims':
            hparams[key] = lut_dims
        elif key == 'ClusterLUT_dims' and lut_dims == 0:
            hparams['ClusterLUT_dims'] = 1
        else:
             hparams[key] = np.random.choice(np.arange(limits[0], limits[1]))
    return hparams


def get_name(params):
    name = ''
    for k, v in params.items():
        name += f'{k}={v},_'
    return name[0:-2]


def from_name_get_params(name):
    params = dict()
    for word in name.split(',_'):
        key, value = word.split('=')
        params[key] = int(value)
    return params