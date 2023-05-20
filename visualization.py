import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from math import isnan


handBaseline = ... #Huawei NDA
randomBaseline = ... #Huawei NDA

df = pd.read_csv('PBL_result.csv')

points = []

for i, row in df.iterrows():
    for x in range(row['born'], row['die']):
        if not isnan(row['iter_4999']):
            y = row['iter_4999']
        elif not isnan(row['iter_3999']):
            y = row['iter_3999']
        elif not isnan(row['iter_2999']):
            y = row['iter_2999']
        elif not isnan(row['iter_1999']):
            y = row['iter_1999']
        else:
            y = row['iter_999']
        points.append([int(x), y])

points = np.array(sorted(points, key=lambda x: x[0]))

means = np.zeros(14)
count = 0
current = 0
for item in points:
    if int(item[0]) != current:
        means[current] /= count
        count = 0
        current = int(item[0])
    means[current] += item[1]
    count += 1

means[-1] /= count
means

plt.figure(figsize=(10, 7))
plt.scatter(points[:, 0], points[:, 1], label='Tested sets of Hyperparams')
plt.plot([0, 13], [handBaseline, handBaseline], c='red', label='Baseline')
plt.plot([0, 13], [randomBaseline, randomBaseline], c='green', label='Best of Random Search')
plt.plot(means, c='blue', marker='*', label='Mean score per epoch' )
plt.xlabel('Epoch of optimization', size=16)
plt.grid()
plt.legend()