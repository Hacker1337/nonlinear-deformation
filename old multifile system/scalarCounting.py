import numpy as np
import matplotlib.pyplot as plt
import time

numbers = [[170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181],
           [239, 240, 241, 242, 243],
           [249, 250, 251, 252, 253, 254, 255, 256, 257],
           [268, 269, 270, 271, 272, 273, 274, 275, 276],
           [281, 282, 283, 284, 285, 286, 287, 288, 289],
           [291, 292, 293, 294, 295, 296, 297, 298]]

output = open('../correlations.txt', 'a')
for grn in range(len(numbers)):
    print("group", numbers[grn][0], sep='\t')
    output.write("group" + "\t" + str(numbers[grn][0]) + "\n")

    base = np.loadtxt('данные для обработки/WFM'+str(numbers[grn][0]) +'.CSV', skiprows=1, delimiter=',')
    for secondP in numbers[grn][1:]:
        shifted = np.loadtxt('данные для обработки/WFM'+str(secondP)+'.CSV', skiprows=1, delimiter=',')
        res = np.zeros((2*len(base)-1, 2))
        res[:, 0] = np.arange(-len(base)+1, len(base))
        res[:, 1] = np.correlate(base[:, 2], shifted[:, 2], mode='full')
        np.savetxt("correls/WFM" + str(secondP) + ".txt", res)
        maxi = 0
        for i in range(1, len(res)):
            if res[i, 1] > res[maxi, 1]:
                maxi = i
        output.write(str(secondP) + ", " + str(res[maxi, 0]) + "\n")
        print(secondP, res[maxi, 0], sep='\t')
        # plt.plot(res[:, 0], res[:, 1], 'red')
        # plt.show()
        # plt.plot(np.arange(len(base)), base[:, 1])
        # plt.plot((np.arange(len(base))+maxsh)%len(base), shifted[:, 1])
        # plt.show()

output.close()
