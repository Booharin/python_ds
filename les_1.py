import numpy as np

a = np.array([[1, 2, 3, 3, 1], [6, 8, 11, 10, 7]])
a.transpose()
mean_a = a.mean(axis = 1)
print(mean_a)