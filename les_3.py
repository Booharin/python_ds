from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

from matplotlib import pyplot as plt

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

# 2

model = RandomForestRegressor(n_estimators=1000,
                              max_depth=12,
                              random_state=42)
model.fit(x_train, y_train.values[:, 0])
y_predict_rfr = model.predict(x_test)

# the second model works more precisely
print(r2_score(y_test["price"],
               y_predict_rfr.flatten()))

# 3
print(sum(model.feature_importances_))

most_important = pd.DataFrame(model.feature_importances_,
                              index=x_train.columns,
                              columns=['importance']).sort_values('importance',
                                                                  ascending=False).head(2)
print(most_important)
