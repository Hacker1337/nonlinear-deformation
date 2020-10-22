import numpy as np
import matplotlib.pyplot as plt


firstN, secondN = (170, 181)
shifting = 138

data1 = np.loadtxt("данные для обработки/WFM" + str(firstN) + ".csv", skiprows=1, delimiter=',')
data2 = np.loadtxt("данные для обработки/WFM" + str(secondN) + ".csv", skiprows=1, delimiter=',')

plt.plot((np.arange(len(data1))), data1[:, 2])
plt.plot((np.arange(len(data2)) + shifting), data2[:, 2])
# plt.plot((np.arange(len(data1)) + 470) % len(data1), data1[:, 1])
plt.show()
