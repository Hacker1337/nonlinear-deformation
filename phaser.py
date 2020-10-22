import numpy as np
import matplotlib.pyplot as plt

numbers = [[170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181], [239, 240, 241, 242, 243], [249, 250, 251, 252, 253, 254, 255, 256, 257], [268, 269, 270, 271, 272, 273, 274, 275, 276], [281, 282, 283, 284, 285, 286, 287, 288, 289], [291, 292, 293, 294, 295, 296, 297, 298]]

output = open('phasesIncorrect.csv', 'a')
for grn in range(len(numbers)):
    print("group", numbers[grn][0], sep='\t')
    output.write("group" + "\t" + str(numbers[grn][0]) + "\n")

    base = np.loadtxt('данные для обработки/WFM'+str(numbers[grn][0]) +'.CSV', skiprows=1, delimiter=',')
    baseFFT = np.fft.rfft(base[:, 2])

    maxk = 0
    for i in range(1, len(baseFFT)):
        if (np.abs(baseFFT[maxk]) < np.abs(baseFFT[i])):
            maxk = i


    for secondP in numbers[grn][1:]:
        shifted = np.loadtxt('данные для обработки/WFM'+str(secondP)+'.CSV', skiprows=1, delimiter=',')
        shFFT = np.fft.rfft(shifted[:, 2])
        delta = (np.angle(shFFT[maxk]) - np.angle(baseFFT[maxk]))*len(base)/maxk/2/np.pi
        output.write(str(secondP) + "\t" + str(delta) + "\n")
        print(secondP, delta, sep='\t')

        # plt.plot(np.fft.rfftfreq(len(base)), np.abs(baseFFT))
        # plt.plot(np.fft.rfftfreq(len(shifted)), np.abs(shFFT))
        # plt.plot(np.arange(len(shFFT)), np.abs(shFFT))
        # plt.show()
        # plt.plot(np.fft.rfftfreq(len(base)), np.angle(baseFFT))
        # plt.plot(np.fft.rfftfreq(len(base)), np.angle(shFFT))
        # plt.show()
        #
        # plt.plot(np.arange(len(shifted)), shifted[:, 2])
        # plt.plot(np.arange(len(shifted)), base[:, 2])
        # shFFT[14:] *= 0
        # shFFT[:13] *= 0
        # plt.plot(np.arange(len(shifted)-1), np.fft.irfft(shFFT))
        # plt.plot(np.arange(len(shifted)-1), np.fft.irfft(baseFFT))
        # plt.show()
