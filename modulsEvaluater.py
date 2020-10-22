import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from sympy import *

from scipy.optimize import curve_fit


def func(x, a, b):
    return x * a + b

def countModules(ks, ksErr):

    vx, vy, vz, ro, h, u, l, v, m, n, kx, ky, kz, dvx, dvy, dvz, dkx, dky, dkz = symbols(
        'vx vy vz ro h u l v m n kx ky kz dvx dvy dvz dkx dky dkz')
    values = [(vx, sound_velocity[0]), (vy, sound_velocity[1]), (vz, sound_velocity[2]), (kx, ks[0]), (ky, ks[1]), (kz, ks[2]), (ro, 1060)]
    err = [(dvx, 1), (dvy, 1), (dvz, 1), (dkx, ksErr[0]), (dky, ksErr[1]), (dkz, ksErr[2])]

    nVal = (4 * ro * vy ** 2 * (-ky + kz - 1)).subs(values)
    mVal = (ro * (-vx ** 2 * (2 * ky + kz + 1) + 2 * vy ** 2 * (ky + kz))).subs(values)
    lVal = (-ro * (vx ** 4 * (4 * ky + 2 * kz + 1) - vy ** 2 * (
                vx ** 2 * (-3 * kx + 12 * ky + 8 * kz + 2) + 4 * vy ** 2 * (kx - 2 * ky - 2 * kz))) / (
                        2 * vy ** 2)).subs(values)
    nerr, merr, lerr = (4*dky*Abs(ro*vy**2) + 4*dkz*Abs(ro*vy**2) + 8*dvy*Abs(ro*vy*(ky - kz + 1)),
        dky*Abs(ro*(2*vx**2 - 2*vy**2)) + dkz*Abs(ro*(vx**2 - 2*vy**2)) + 2*dvx*Abs(ro*vx*(2*ky + kz + 1)) + 4*dvy*Abs(ro*vy*(ky + kz)),
        dkx*Abs(ro*(3*vx**2 - 4*vy**2))/2 + dky*Abs(ro*(4*vx**4 - vy**2*(12*vx**2 - 8*vy**2))/vy**2)/2 + dkz*Abs(ro*(2*vx**4 - vy**2*(8*vx**2 - 8*vy**2))/vy**2)/2 + dvx*Abs(ro*(4*vx**3*(4*ky + 2*kz + 1) - 2*vx*vy**2*(-3*kx + 12*ky + 8*kz + 2))/vy**2)/2 + dvy*Abs(-ro*(-8*vy**3*(kx - 2*ky - 2*kz) - 2*vy*(vx**2*(-3*kx + 12*ky + 8*kz + 2) + 4*vy**2*(kx - 2*ky - 2*kz)))/(2*vy**2) + ro*(vx**4*(4*ky + 2*kz + 1) - vy**2*(vx**2*(-3*kx + 12*ky + 8*kz + 2) + 4*vy**2*(kx - 2*ky - 2*kz)))/vy**3)
    )
    return ([nVal, mVal, lVal], [i.subs(values).subs(err) for i in [nerr, merr, lerr]])


srcTables = 'comfortableDataDifferentFreqs'
srcWFM = 'данные SiO2 на нескольких частотах'
output = 'nonlinear_moduls.csv'
evaluated_table_path = 'comfortableDataComputationResult'

rho = 1060
length = 0.05
time_scale = 0.0000000008
sound_velocity = [2349, 1158, 1158]         # скорость звука без давления  x, y, z метры в секунду
pres_coef = 1000*10000/3                                # коэффициент связывающий силу с давлением

result = pd.DataFrame(index=range(6), columns=['freq_str', 'freq_MHz', 'n', 'm','l', 'En', 'Em', 'El', 'kx', 'ky', 'kz', 'err_kx', 'err_ky', 'err_kz', 'rel_er_kx', 'rel_er_ky', 'rel_er_kz'])
freq_number = 0

for freq in os.listdir(srcTables):

    path = os.path.join(srcTables, freq)
    ks = []     # kx, ky, kz
    ksErr = []  # the same order
    for dir in range(3):
        axis = ['x', 'y', 'z'][dir]
        df = pd.read_csv(os.path.join(srcTables, freq, axis + '.csv'), index_col=0)
        if df.shape[0] == 0:
            ks.append(None)
            ksErr.append(None)
            continue
        deltasFFT = [0]

        base = np.loadtxt(os.path.join(srcWFM, df['file_name'][0]), skiprows=1, delimiter=',')
        baseFFT = np.fft.rfft(base[:, 1])

        maxk = np.abs(baseFFT).argmax()

        for secondI in range(1, len(df['file_name'])):
            shifted = np.loadtxt(os.path.join(srcWFM, df['file_name'].iloc[secondI]), skiprows=1, delimiter=',')
            shFFT = np.fft.rfft(shifted[:, 1])
            delta = ((np.angle(shFFT[maxk]) - np.angle(baseFFT[maxk]) + np.pi/4)%(2*np.pi)-np.pi/4) * len(base) / maxk / 2 / np.pi
            deltasFFT.append(delta)

        df['deltaFFT'] = deltasFFT

        df['G'] = rho*(length/(length/sound_velocity[dir] - df['deltaFFT']*time_scale))**2      # Эффективный модуль упругости
        df['pressure'] = pres_coef*df['сила']

        df.to_csv(os.path.join(evaluated_table_path, freq, axis + '.csv'))
        incr_end = df['сила'].argmax()+1

        popt, pcov = curve_fit(func, df['pressure'][:incr_end], df['G'][:incr_end], p0=[4.77129651e-01, 9.21051620e+08])

        plt.plot(df['pressure'][:incr_end], df['G'][:incr_end], '-o')
        plt.plot(df['pressure'][:incr_end], func(df['pressure'][:incr_end], *popt))
        plt.title(axis + ' effective M from pressure')
        plt.xlabel('pressure, Pa')
        plt.ylabel('G, Pa')
        plt.savefig(os.path.join(evaluated_table_path, freq, axis + '.png'), dpi=300)
        plt.close()

        ks.append(popt[0])
        ksErr.append(np.sqrt(np.diag(pcov)[0]))
    print(ks)
    print([0 if ks[i] == None else ksErr[i]/ks[i] for i in range(3)])
    print()
    if None not in ks:
        vals, errors = countModules(ks, ksErr)
    else:
        vals, errors = ([None for i in range(3)] for j in range(2))
    result.iloc[freq_number] = [freq, float(freq[:-3].replace(',', '.'))] + vals + errors + ks + ksErr + [None if ks[i] == None else ksErr[i]/ks[i] for i in range(3)]
    freq_number += 1
result.to_csv('modules.csv')



