import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def func(x, a, b):
    return x * a + b


# xdata = np.array([0, 1075000, 2150000, 3050000, 4075000])
# ydata = np.array([970394214, 970852352, 971328705, 971559258, 971712612])

# popt, pcov = curve_fit(func, xdata, ydata, p0=[4.77129651e-01, 9.21051620e+08])  # popt - значения коэффициентов, pcov - ковариационная матрица
# print(popt)
# errors = np.sqrt(np.diag(pcov))
# print(errors)
# yteor = func(xdata, popt[0], popt[1])
# plt.plot(xdata, ydata)
# plt.plot(xdata, yteor)
# plt.show()

out = open('interp.txt', 'w')
data = open('phases.txt', 'r')
X = []
y = []
group = 0
s = data.readline()
while len(s) > 0:
    type, gr, pr, mod = s.split()
    if type == 'group':
        if gr != '170':
            print(group, end='\t', file=out)
            popt, pcov = curve_fit(func, np.array(X), np.array(y), p0=[4.77129651e-01, 9.21051620e+08])
            print(popt[0], np.sqrt(np.diag(pcov))[0], sep='\t', file=out)
            print(popt)
            X = []
            y = []
        group = gr
    X.append(int(pr))
    y.append(int(float(mod)))
    s = data.readline()

