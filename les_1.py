import numpy as np

# Topic 1

# 1
a = np.array([[1, 2, 3, 3, 1],
              [6, 8, 11, 10, 7]])
a.transpose()
mean_a = a.mean(axis=1)
print(mean_a)

# 2
a_centered = (a - mean_a[:, None]).transpose()
print(a_centered)

# 3
a_centered_sp = a_centered[:, 0].dot(a_centered[:, 1])
# число наблюдений 2
x = a_centered_sp / (2 - 1)
print(x)

# 4
print(np.cov(a)[0, 1])
