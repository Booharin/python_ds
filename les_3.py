from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import numpy as np
import pandas as pd

# 1

boston = load_boston()
data = boston["data"]
feature_names = boston["feature_names"]
target = boston["target"]

x = pd.DataFrame(data, columns=feature_names)
y = pd.DataFrame(target, columns=["price"])

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

lr = LinearRegression()
lr.fit(x_train, y_train)

y_predict = lr.predict(x_test)

print(r2_score(y_test["price"],
               y_predict.flatten()))
