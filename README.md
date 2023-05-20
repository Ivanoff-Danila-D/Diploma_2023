# Diploma_2023

## Abstract

The search for optimal hyperparameters is the main part of local optimization of neural network architecture.

Computational power and specifics of hardware impose strict external constraints on neural networks. This forms a complicated multidimensional hyperparameter search space. This paper proposes methods to modify known hyperparameter optimization techniques to use them on spaces defined by a complicated limitation black-box-type function. Using these modifications, we were able to find hyperparameters that satisfy the hardware constraints and maximize the quality of the neural network from Huawei

## Files Description
PBLmain.py is the main file for PBL algorithm running. There are full pipeline of the algorithm with different stages. Comment \texttt{Huawei NDA} shows that i cannot publish these parts of project because of my NDA. Other files are supported:
\dot Huperparams.py contains all functions of hyperparameters as get_area, get_name and other. \\
\dot Mutation.py contains the custom mutations function.
