import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pylab import rcParams

# 1

x = [1, 2, 3, 4, 5, 6, 7]
y = [3.5, 3.8, 4.2, 4.5, 5, 5.5, 7.0]

# plt.plot(x, y)
# plt.show()

# plt.scatter(x, y)
# plt.show()

# 2

t = np.linspace(0, 10, 51)
f = [np.cos(element) for element in t]

title_font = {
    "fontsize": 15,
    "fontweight": "bold",
    "color": "#365587",
    "family": "serif",
}

label_font = {
    "fontsize": 9,
    "color": "#662c65",
    "family": "serif",
}

plt.plot(t, f, color="green")
plt.title("График f(t)", fontdict=title_font)
plt.xlabel("Переменная x", fontdict=label_font)
plt.ylabel("Функция f(x)", fontdict=label_font)

plt.axis([0.5, 9.5, -2.5, 2.5])

plt.show()