import matplotlib.pyplot as plt
import numpy as np

numbers = [[170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181], [239, 240, 241, 242, 243], [249, 250, 251, 252, 253, 254, 255, 256, 257], [268, 269, 270, 271, 272, 273, 274, 275, 276], [281, 282, 283, 284, 285, 286, 287, 288, 289], [291, 292, 293, 294, 295, 296, 297, 298]]
for group in numbers:
    for i in group:
        file = np.loadtxt("исходные данные/WFM" + ' ' if i > 9 else '0' + str(i) + ".CSV", skiprows=1, delimiter=',')[:, [0, 2]]
        normN = 1000
        more = sum(file[range(normN), 1])/normN
        file[:, 1] -= more
        prop = max(abs(min(file[:, 1])), abs(max(file[:, 1])))
        file[:, 1] /= prop

        np.savetxt('нормированные данные/WFM'+ str(i) + '.CSV', file, delimiter='\t')


