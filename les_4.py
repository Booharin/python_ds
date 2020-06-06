import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import load_boston
from sklearn.manifold import TSNE
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 1

boston = load_boston()
data = boston["data"]
feature_names = boston["feature_names"]
target = boston["target"]

x = pd.DataFrame(data, columns=feature_names)
y = pd.DataFrame(target, columns=["price"])

x_train, x_test, y_train, y_test = train_test_split(x,
                                                    y,
                                                    test_size=0.2,
                                                    random_state=42)

scaler = StandardScaler(with_mean=False)

x_train_scaled = pd.DataFrame(scaler.fit_transform(x_train),
                              columns=x_train.columns)
x_test_scaled = pd.DataFrame(scaler.transform(x_test),
                             columns=x_test.columns)

tsne = TSNE(n_components=2, learning_rate=250, random_state=42)
x_train_tsne = tsne.fit_transform(x_train_scaled)
plt.scatter(x_train_tsne[:, 0], x_train_tsne[:, 1])

#plt.show()

# 2
kmeans = KMeans(n_clusters=3, max_iter=100, random_state=42)

labels_train = kmeans.fit_predict(x_train_scaled)

plt.scatter(x_train_tsne[:, 0], x_train_tsne[:, 1], c=labels_train)

#plt.show()

plt.hist(y_train[labels_train == 0], bins=20, density=True, alpha=0.5)
plt.hist(y_train[labels_train == 1], bins=20, density=True, alpha=0.5)
plt.hist(y_train[labels_train == 2], bins=20, density=True, alpha=0.5)

plt.legend(['Cluster_0', 'Cluster_1', 'Cluster_2'])
plt.xlabel('Price')

#plt.show()

plt.hist(x_train.loc[labels_train == 0, 'CRIM'], bins=20, density=True, alpha=0.5)
plt.hist(x_train.loc[labels_train == 1, 'CRIM'], bins=20, density=True, alpha=0.5)
plt.hist(x_train.loc[labels_train == 2, 'CRIM'], bins=20, density=True, alpha=0.5)

plt.xlim(0, 12)
plt.legend(['Cluster_0', 'Cluster_1', 'Cluster_2'])
plt.xlabel('CRIM')

#plt.show()

# 3

labels_test = kmeans.fit_predict(x_test_scaled)
x_test_tsne = tsne.fit_transform(x_test_scaled)
plt.scatter(x_test_tsne[:, 0], x_test_tsne[:, 1], c=labels_test)

#plt.show()

plt.hist(y_test[labels_test == 0], bins=20, density=True, alpha=0.5)
plt.hist(y_test[labels_test == 1], bins=20, density=True, alpha=0.5)
plt.hist(y_test[labels_test == 2], bins=20, density=True, alpha=0.5)

plt.legend(['Cluster_0', 'Cluster_1', 'Cluster_2'])
plt.xlabel('Price')

#plt.show()

plt.hist(x_test.loc[labels_test == 0, 'CRIM'], bins=20, density=True, alpha=0.5)
plt.hist(x_test.loc[labels_test == 1, 'CRIM'], bins=20, density=True, alpha=0.5)
plt.hist(x_test.loc[labels_test == 2, 'CRIM'], bins=20, density=True, alpha=0.5)

plt.xlim(0, 12)
plt.legend(['Cluster_0', 'Cluster_1', 'Cluster_2'])
plt.xlabel('CRIM')

plt.show()

