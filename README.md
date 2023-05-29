# Diploma_2023

This repository was created in addition to Ivanov Danila's diploma: 

**"Development of the AutoML Algorithm for Fast Automatic Search of Optimal Hyperparameters with the External Hardware Constraints".**

## Abstract

The search for optimal hyperparameters is the main part of local optimization of neural network architecture.

Computational power and specifics of hardware impose strict external constraints on neural networks. This forms a complicated multidimensional hyperparameter search space. This paper proposes methods to modify known hyperparameter optimization techniques to use them on spaces defined by a complicated limitation black-box-type function. Using these modifications, we were able to find hyperparameters that satisfy the hardware constraints and maximize the quality of the neural network from Huawei

## Files Description
### PBL
PBLmain.py is the main file for PBL algorithm running. There are full pipeline of the algorithm with different stages. Comment \# $\textit{Huawei NDA}$ shows that I cannot publish these parts of project because of my NDA. Other files are supported:

$\cdot$ Huperparams.py contains all functions of hyperparameters as get_area, get_name and other.

$\cdot$ Mutation.py contains the custom mutations function.

$\cdot$ Global.py defines all global params of PBL algorithm, for example, number of workers $n\_
workers = 18$

### GPO
GPOmain.py is the main file for GPO algorithm running. There are the definition of the GPOoptimazer class and example how to use it.

$\cdot$ BiSearch.py contains a function of binary search points on the border of search space. It uses functions is_satisfy and get_params from Huperparams.py
