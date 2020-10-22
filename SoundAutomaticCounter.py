from sympy import *


vx, vy, vz, ro, h, u, l, v, m, n, kx, ky, kz, dvx, dvy, dvz, dkx, dky, dkz = symbols('vx vy vz ro h u l v m n kx ky kz dvx dvy dvz dkx dky dkz')


# значения измеренных величин в СИ
# и их погрешности
values = [(vx, 22802.1), (vy, 1151.2), (vz, 1151.2), (kx, 1359.13411), (ky, 0.42303), (kz, 0.6779), (ro, 1060)]
err = [(dvx, 0.1), (dvy, 0.1), (dvz, 0.1), (dkx, 59.47512), (dky, 0.03609), (dkz, 0.0795)]

'''
errors for n, m, l respectively
[0, 8*dvy*Abs(ro*vy*(ky - kz + 1)), 0, 0, 4*dky*Abs(ro*vy**2), 4*dkz*Abs(ro*vy**2)]
[2*dvx*Abs(ro*vx*(2*ky + kz + 1)), 4*dvy*Abs(ro*vy*(ky + kz)), 0, 0, dky*Abs(ro*(2*vx**2 - 2*vy**2)), dkz*Abs(ro*(vx**2 - 2*vy**2))]
[dvx*Abs(ro*(4*vx**3*(4*ky + 2*kz + 1) - 2*vx*vy**2*(-3*kx + 12*ky + 8*kz + 2))/vy**2)/2, dvy*Abs(-ro*(-8*vy**3*(kx - 2*ky - 2*kz) - 2*vy*(vx**2*(-3*kx + 12*ky + 8*kz + 2) + 4*vy**2*(kx - 2*ky - 2*kz)))/(2*vy**2) + ro*(vx**4*(4*ky + 2*kz + 1) - vy**2*(vx**2*(-3*kx + 12*ky + 8*kz + 2) + 4*vy**2*(kx - 2*ky - 2*kz)))/vy**3), 0, dkx*Abs(ro*(3*vx**2 - 4*vy**2))/2, dky*Abs(ro*(4*vx**4 - vy**2*(12*vx**2 - 8*vy**2))/vy**2)/2, dkz*Abs(ro*(2*vx**4 - vy**2*(8*vx**2 - 8*vy**2))/vy**2)/2]

n = 4*ro*vy**2*(-ky + kz - 1)
m = ro*(-vx**2*(2*ky + kz + 1) + 2*vy**2*(ky + kz))
l = -ro*(vx**4*(4*ky + 2*kz + 1) - vy**2*(vx**2*(-3*kx + 12*ky + 8*kz + 2) + 4*vy**2*(kx - 2*ky - 2*kz)))/(2*vy**2)
'''
nerr = [0, 8*dvy*Abs(ro*vy*(ky - kz + 1)), 0, 0, 4*dky*Abs(ro*vy**2), 4*dkz*Abs(ro*vy**2)]
merr = [2*dvx*Abs(ro*vx*(2*ky + kz + 1)), 4*dvy*Abs(ro*vy*(ky + kz)), 0, 0, dky*Abs(ro*(2*vx**2 - 2*vy**2)), dkz*Abs(ro*(vx**2 - 2*vy**2))]
lerr = [dvx*Abs(ro*(4*vx**3*(4*ky + 2*kz + 1) - 2*vx*vy**2*(-3*kx + 12*ky + 8*kz + 2))/vy**2)/2, dvy*Abs(-ro*(-8*vy**3*(kx - 2*ky - 2*kz) - 2*vy*(vx**2*(-3*kx + 12*ky + 8*kz + 2) + 4*vy**2*(kx - 2*ky - 2*kz)))/(2*vy**2) + ro*(vx**4*(4*ky + 2*kz + 1) - vy**2*(vx**2*(-3*kx + 12*ky + 8*kz + 2) + 4*vy**2*(kx - 2*ky - 2*kz)))/vy**3), 0, dkx*Abs(ro*(3*vx**2 - 4*vy**2))/2, dky*Abs(ro*(4*vx**4 - vy**2*(12*vx**2 - 8*vy**2))/vy**2)/2, dkz*Abs(ro*(2*vx**4 - vy**2*(8*vx**2 - 8*vy**2))/vy**2)/2]

nVal = (4*ro*vy**2*(-ky + kz - 1)).subs(values)
dn = 0
print('n =', nVal)
print('Error of n defining in format: reason tab value')
for i in range(6):
    print(err[i][0], end='\t')
    if nerr[i] == 0:
        print(0)
    else:
        t = nerr[i].subs(values).subs(err[i][0], err[i][1])
        dn += t
        print(t)
print("Total n err =", dn)
print('Relative n error =', abs(dn/nVal))
print()
mVal = (ro*(-vx**2*(2*ky + kz + 1) + 2*vy**2*(ky + kz))).subs(values)
dm = 0
print('m =', mVal)
print('Error of m defining in format: reason tab value')
for i in range(6):
    print(err[i][0], end='\t')
    if merr[i] == 0:
        print(0)
    else:
        t = merr[i].subs(values).subs(err[i][0], err[i][1])
        dm += t
        print(t)
print("Total m err =", dm)
print('Relative m error =', abs(dm/mVal))
print()

lVal = (-ro*(vx**4*(4*ky + 2*kz + 1) - vy**2*(vx**2*(-3*kx + 12*ky + 8*kz + 2) + 4*vy**2*(kx - 2*ky - 2*kz)))/(2*vy**2)).subs(values)
dl = 0
print('l =', lVal)
print('Error of l defining in format: reason tab value')
for i in range(6):
    print(err[i][0], end='\t')
    if lerr[i] == 0:
        print(0)
    else:
        t = lerr[i].subs(values).subs(err[i][0], err[i][1])
        dl += t
        print(t)
print("Total l err =", dl)
print('Relative l error =', abs(dl/lVal))
print()


