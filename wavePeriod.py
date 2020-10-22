import numpy as np


stat = []

numbers = [[170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181], [239, 240, 241, 242, 243], [249, 250, 251, 252, 253, 254, 255, 256, 257], [268, 269, 270, 271, 272, 273, 274, 275, 276], [281, 282, 283, 284, 285, 286, 287, 288, 289], [291, 292, 293, 294, 295, 296, 297, 298]]

for gr in numbers:
    for i in gr:
        data = np.loadtxt('данные для обработки/WFM'+str(i) + '.CSV', skiprows=1, delimiter=',')
        pos = data[0, 2] > 0
        beg = -10
        end = -10
        n = -1
        for j in range(1, len(data)):
            if not pos and (data[j, 2] > 0):
                n += 1
                if n == 0:
                    beg = j
                end = j
            pos = data[j, 2] > 0
        print(i, end='\t')
        print((end-beg)/n)
