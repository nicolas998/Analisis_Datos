#!/usr/bin/env python

import datetime as dt
import os
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("template")
import matplotlib.pyplot as plt
import matplotlib.colors as colors

Path = '/mnt/ALMACENAMIENTO/radiometro/datos/'
ruta = '/home/ccuervo/Radiometer/'
# Path = '/Users/Usuario/Desktop/'
# ruta = '/Users/Usuario/Desktop/'



def listadorLV2(directorio, inicio):
    lf = []
    lista = os.listdir(directorio)
    for i in lista:
        if i.startswith(inicio) and i.endswith('lv2.csv'):
            lf.append(i)
    return lf


start = dt.datetime(2013, 01, 16)
today = dt.datetime(2016, 01, 16)
# start = dt.datetime(2015, 06, 23)
# today = dt.datetime(2015, 06, 23)
# today = dt.date.today() + dt.timedelta(hours=5)

dias = []
day = start
i = 0
while day.date() <= today.date():
    dias.append(day)
    i += 1
    day = start + dt.timedelta(days=i)

# =============================================================================
# =============================================================================
#	                                  Lectura
# =============================================================================
# =============================================================================


lv2 = [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.60, 0.70, 0.80, 0.90,
       1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.00, 2.25, 2.50, 2.75, 3.00, 3.25,
       3.50, 3.75, 4.00, 4.25, 4.50, 4.75, 5.00, 5.25, 5.50, 5.75, 6.00, 6.25, 6.50, 6.75, 7.00, 7.25,
       7.50, 7.75, 8.00, 8.25, 8.50, 8.75, 9.00, 9.25, 9.50, 9.75, 10.00]

record = []
date = []
GPS = []
ground = []
cloud = []
time = []

Temperature_Zenit = []
Temperature_15N = []
Temperature_15S = []
Temperature_15A = []

VaporDensity_Zenit = []
VaporDensity_15N = []
VaporDensity_15S = []
VaporDensity_15A = []

Liquid_Zenit = []
Liquid_15N = []
Liquid_15S = []
Liquid_15A = []

RelativeHumidity_Zenit = []
RelativeHumidity_15N = []
RelativeHumidity_15S = []
RelativeHumidity_15A = []

# Tiempos
t_Temperature_Zenit = []
t_Temperature_15N = []
t_Temperature_15S = []
t_Temperature_15A = []

t_VaporDensity_Zenit = []
t_VaporDensity_15N = []
t_VaporDensity_15S = []
t_VaporDensity_15A = []

t_Liquid_Zenit = []
t_Liquid_15N = []
t_Liquid_15S = []
t_Liquid_15A = []

t_RelativeHumidity_Zenit = []
t_RelativeHumidity_15N = []
t_RelativeHumidity_15S = []
t_RelativeHumidity_15A = []



def roundTime(dti=None, dateDelta=dt.timedelta(minutes=1)):
    """Round a datetime object to a multiple of a timedelta
    dt : datetime.datetime object, default now.
    dateDelta : timedelta object, we round to a multiple of this, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
            Stijn Nevens 2014 - Changed to use only datetime objects as variables
    """
    roundTo = dateDelta.total_seconds()

    if dti == None :
        dti = dt.datetime.now()
    seconds = (dti - dti.min).seconds
    # // is a floor division, not a comment on following line:
    rounding = (seconds+roundTo/2) // roundTo * roundTo
    return dti + dt.timedelta(0,rounding-seconds,-dti.microsecond)


def Read_CSV(filename):
    f = open(filename, "r")

    for line in f:
        # cortar caracteres
        c = line.split('\r\n')
        # separar en las primeras 3 entradas separadas por ','
        a = c[0].split(',', 3)

        record.append(a[0])
        date.append(a[1])

        if a[2] == '31':
            GPS.append(a[3].split(','))

            # organizar la fecha de cada trama de datos
            t = a[1]
            time.append(dt.datetime(2000 + int(t[6:8]), int(t[0:2]), int(t[3:5]),
                                    int(t[9:11]), int(t[12:14]), int(t[15:17]))
                        - dt.timedelta(hours=5))


        elif a[2] == '201':
            ground.append(a[3].split(','))

        elif a[2] == '301':
            cloud.append(a[3].split(',')[:-1])

        elif a[2] == '401':
            # if a[3].startswith('ZenithKV'):
            #     b = a[3].split(',', 1)
            #     Temperature_Zenit.append(b[1].split(',')[:-1])
            #     t = a[1]
            #     # t_Temperature_Zenit.append(dt.datetime(2000 + int(t[6:8]), int(t[0:2]), int(t[3:5]),
            #     #                                        int(t[9:11]), int(t[12:14])) - dt.timedelta(hours=5))
            #     t_Temperature_Zenit.append(roundTime(dt.datetime(2000+int(t[6:8]), int(t[0:2]), int(t[3:5]),
            #                                            int(t[9:11]), int(t[12:14]), int(t[15:17]))-dt.timedelta(hours=5)))
            #
            # if a[3].startswith('Angle15KV(N)'):
            #     b = a[3].split(',', 1)
            #     Temperature_15N.append(b[1].split(',')[:-1])
            #     t = a[1]
            #     # t_Temperature_15N.append(dt.datetime(2000 + int(t[6:8]), int(t[0:2]), int(t[3:5]),
            #     #                                      int(t[9:11]), int(t[12:14])) - dt.timedelta(hours=5))
            #     t_Temperature_15N.append(roundTime(dt.datetime(2000+int(t[6:8]), int(t[0:2]), int(t[3:5]),
            #                                            int(t[9:11]), int(t[12:14]), int(t[15:17]))-dt.timedelta(hours=5)))
            #
            # if a[3].startswith('Angle15KV(S)'):
            #     b = a[3].split(',', 1)
            #     Temperature_15S.append(b[1].split(',')[:-1])
            #     t = a[1]
            #     # t_Temperature_15S.append(dt.datetime(2000 + int(t[6:8]), int(t[0:2]), int(t[3:5]),
            #     #                                      int(t[9:11]), int(t[12:14])) - dt.timedelta(hours=5))
            #     t_Temperature_15S.append(roundTime(dt.datetime(2000+int(t[6:8]), int(t[0:2]), int(t[3:5]),
            #                                            int(t[9:11]), int(t[12:14]), int(t[15:17]))-dt.timedelta(hours=5)))

            if a[3].startswith('Angle15KV(A)'):
                b = a[3].split(',', 1)
                Temperature_15A.append(b[1].split(',')[:-1])
                t = a[1]
                # t_Temperature_15A.append(dt.datetime(2000 + int(t[6:8]), int(t[0:2]), int(t[3:5]),
                #                                      int(t[9:11]), int(t[12:14])) - dt.timedelta(hours=5))
                t_Temperature_15A.append(roundTime(dt.datetime(2000+int(t[6:8]), int(t[0:2]), int(t[3:5]),
                                                       int(t[9:11]), int(t[12:14]), int(t[15:17]))-dt.timedelta(hours=5)))


        elif a[2] == '402':
            # if a[3].startswith('ZenithKV'):
            #     b = a[3].split(',', 1)
            #     VaporDensity_Zenit.append(b[1].split(',')[:-1])
            #     t = a[1]
            #     # t_VaporDensity_Zenit.append(dt.datetime(2000 + int(t[6:8]), int(t[0:2]), int(t[3:5]),
            #     #                                         int(t[9:11]), int(t[12:14])) - dt.timedelta(hours=5))
            #     t_VaporDensity_Zenit.append(roundTime(dt.datetime(2000+int(t[6:8]), int(t[0:2]), int(t[3:5]),
            #                                            int(t[9:11]), int(t[12:14]), int(t[15:17]))-dt.timedelta(hours=5)))
            #
            # if a[3].startswith('Angle15KV(N)'):
            #     b = a[3].split(',', 1)
            #     VaporDensity_15N.append(b[1].split(',')[:-1])
            #     t = a[1]
            #     # t_VaporDensity_15N.append(dt.datetime(2000 + int(t[6:8]), int(t[0:2]), int(t[3:5]),
            #     #                                       int(t[9:11]), int(t[12:14])) - dt.timedelta(hours=5))
            #     t_VaporDensity_15N.append(roundTime(dt.datetime(2000+int(t[6:8]), int(t[0:2]), int(t[3:5]),
            #                                            int(t[9:11]), int(t[12:14]), int(t[15:17]))-dt.timedelta(hours=5)))
            #
            # if a[3].startswith('Angle15KV(S)'):
            #     b = a[3].split(',', 1)
            #     VaporDensity_15S.append(b[1].split(',')[:-1])
            #     t = a[1]
            #     # t_VaporDensity_15S.append(dt.datetime(2000 + int(t[6:8]), int(t[0:2]), int(t[3:5]),
            #     #                                       int(t[9:11]), int(t[12:14])) - dt.timedelta(hours=5))
            #     t_VaporDensity_15S.append(roundTime(dt.datetime(2000+int(t[6:8]), int(t[0:2]), int(t[3:5]),
            #                                            int(t[9:11]), int(t[12:14]), int(t[15:17]))-dt.timedelta(hours=5)))

            if a[3].startswith('Angle15KV(A)'):
                b = a[3].split(',', 1)
                VaporDensity_15A.append(b[1].split(',')[:-1])
                t = a[1]
                # t_VaporDensity_15A.append(dt.datetime(2000 + int(t[6:8]), int(t[0:2]), int(t[3:5]),
                #                                       int(t[9:11]), int(t[12:14])) - dt.timedelta(hours=5))
                t_VaporDensity_15A.append(roundTime(dt.datetime(2000+int(t[6:8]), int(t[0:2]), int(t[3:5]),
                                                       int(t[9:11]), int(t[12:14]), int(t[15:17]))-dt.timedelta(hours=5)))


        elif a[2] == '403':
            # if a[3].startswith('ZenithKV'):
            #     b = a[3].split(',', 1)
            #     Liquid_Zenit.append(b[1].split(',')[:-1])
            #     t = a[1]
            #     # t_Liquid_Zenit.append(dt.datetime(2000 + int(t[6:8]), int(t[0:2]), int(t[3:5]),
            #     #                                   int(t[9:11]), int(t[12:14])) - dt.timedelta(hours=5))
            #     t_Liquid_Zenit.append(roundTime(dt.datetime(2000+int(t[6:8]), int(t[0:2]), int(t[3:5]),
            #                                            int(t[9:11]), int(t[12:14]), int(t[15:17]))-dt.timedelta(hours=5)))
            #
            # if a[3].startswith('Angle15KV(N)'):
            #     b = a[3].split(',', 1)
            #     Liquid_15N.append(b[1].split(',')[:-1])
            #     t = a[1]
            #     # t_Liquid_15N.append(dt.datetime(2000 + int(t[6:8]), int(t[0:2]), int(t[3:5]),
            #     #                                 int(t[9:11]), int(t[12:14])) - dt.timedelta(hours=5))
            #     t_Liquid_15N.append(roundTime(dt.datetime(2000+int(t[6:8]), int(t[0:2]), int(t[3:5]),
            #                                            int(t[9:11]), int(t[12:14]), int(t[15:17]))-dt.timedelta(hours=5)))
            #
            # if a[3].startswith('Angle15KV(S)'):
            #     b = a[3].split(',', 1)
            #     Liquid_15S.append(b[1].split(',')[:-1])
            #     t = a[1]
            #     # t_Liquid_15S.append(dt.datetime(2000 + int(t[6:8]), int(t[0:2]), int(t[3:5]),
            #     #                                 int(t[9:11]), int(t[12:14])) - dt.timedelta(hours=5))
            #     t_Liquid_15S.append(roundTime(dt.datetime(2000+int(t[6:8]), int(t[0:2]), int(t[3:5]),
            #                                            int(t[9:11]), int(t[12:14]), int(t[15:17]))-dt.timedelta(hours=5)))

            if a[3].startswith('Angle15KV(A)'):
                b = a[3].split(',', 1)
                Liquid_15A.append(b[1].split(',')[:-1])
                t = a[1]
                # t_Liquid_15A.append(dt.datetime(2000 + int(t[6:8]), int(t[0:2]), int(t[3:5]),
                #                                 int(t[9:11]), int(t[12:14])) - dt.timedelta(hours=5))
                t_Liquid_15A.append(roundTime(dt.datetime(2000+int(t[6:8]), int(t[0:2]), int(t[3:5]),
                                                       int(t[9:11]), int(t[12:14]), int(t[15:17]))-dt.timedelta(hours=5)))


        elif a[2] == '404':
            # if a[3].startswith('ZenithKV'):
            #     b = a[3].split(',', 1)
            #     RelativeHumidity_Zenit.append(b[1].split(',')[:-1])
            #     t = a[1]
            #     # t_RelativeHumidity_Zenit.append(dt.datetime(2000 + int(t[6:8]), int(t[0:2]), int(t[3:5]),
            #     #                                             int(t[9:11]), int(t[12:14])) - dt.timedelta(hours=5))
            #     t_RelativeHumidity_Zenit.append(roundTime(dt.datetime(2000+int(t[6:8]), int(t[0:2]), int(t[3:5]),
            #                                            int(t[9:11]), int(t[12:14]), int(t[15:17]))-dt.timedelta(hours=5)))
            #
            # if a[3].startswith('Angle15KV(N)'):
            #     b = a[3].split(',', 1)
            #     RelativeHumidity_15N.append(b[1].split(',')[:-1])
            #     t = a[1]
            #     # t_RelativeHumidity_15N.append(dt.datetime(2000 + int(t[6:8]), int(t[0:2]), int(t[3:5]),
            #     #                                           int(t[9:11]), int(t[12:14])) - dt.timedelta(hours=5))
            #     t_RelativeHumidity_15N.append(roundTime(dt.datetime(2000+int(t[6:8]), int(t[0:2]), int(t[3:5]),
            #                                            int(t[9:11]), int(t[12:14]), int(t[15:17]))-dt.timedelta(hours=5)))
            #
            # if a[3].startswith('Angle15KV(S)'):
            #     b = a[3].split(',', 1)
            #     RelativeHumidity_15S.append(b[1].split(',')[:-1])
            #     t = a[1]
            #     # t_RelativeHumidity_15S.append(dt.datetime(2000 + int(t[6:8]), int(t[0:2]), int(t[3:5]),
            #     #                                           int(t[9:11]), int(t[12:14])) - dt.timedelta(hours=5))
            #     t_RelativeHumidity_15S.append(roundTime(dt.datetime(2000+int(t[6:8]), int(t[0:2]), int(t[3:5]),
            #                                            int(t[9:11]), int(t[12:14]), int(t[15:17]))-dt.timedelta(hours=5)))

            if a[3].startswith('Angle15KV(A)'):
                b = a[3].split(',', 1)
                RelativeHumidity_15A.append(b[1].split(',')[:-1])
                t = a[1]
                # t_RelativeHumidity_15A.append(dt.datetime(2000 + int(t[6:8]), int(t[0:2]), int(t[3:5]),
                #                                           int(t[9:11]), int(t[12:14])) - dt.timedelta(hours=5))
                t_RelativeHumidity_15A.append(roundTime(dt.datetime(2000+int(t[6:8]), int(t[0:2]), int(t[3:5]),
                                                       int(t[9:11]), int(t[12:14]), int(t[15:17]))-dt.timedelta(hours=5)))

    # borrar los tiempos de los headers de inicio y final
    del time[0]
    del time[-1]


def Read_bad():
    a = np.zeros(58)
    a[a == 0] = np.nan

    time.append(day)

    Temperature_Zenit.append(a)
    Temperature_15N.append(a)
    Temperature_15S.append(a)
    Temperature_15A.append(a)

    VaporDensity_Zenit.append(a)
    VaporDensity_15N.append(a)
    VaporDensity_15S.append(a)
    VaporDensity_15A.append(a)

    Liquid_Zenit.append(a)
    Liquid_15N.append(a)
    Liquid_15S.append(a)
    Liquid_15A.append(a)

    RelativeHumidity_Zenit.append(a)
    RelativeHumidity_15N.append(a)
    RelativeHumidity_15S.append(a)
    RelativeHumidity_15A.append(a)

    # Tiempos
    t_Temperature_Zenit.append(day)
    t_Temperature_15N.append(day)
    t_Temperature_15S.append(day)
    t_Temperature_15A.append(day)

    t_VaporDensity_Zenit.append(day)
    t_VaporDensity_15N.append(day)
    t_VaporDensity_15S.append(day)
    t_VaporDensity_15A.append(day)

    t_Liquid_Zenit.append(day)
    t_Liquid_15N.append(day)
    t_Liquid_15S.append(day)
    t_Liquid_15A.append(day)

    t_RelativeHumidity_Zenit.append(day)
    t_RelativeHumidity_15N.append(day)
    t_RelativeHumidity_15S.append(day)
    t_RelativeHumidity_15A.append(day)


# ==========================================================================
#                       Lectura de todos los archivos
# ==========================================================================

missed = []
corruted = []

# Lectura recursiva si hay fechas sin archivos o con archivos malos

for day in dias:
    print '******************************' + day.strftime('%Y-%m-%d') + '******************************'
    try:
        # existencia de archivos
        lista = listadorLV2(Path, day.strftime('%Y-%m-%d'))
        print lista
        a = lista[0]
        for archivo in lista:
            try:
                # lectura de cada archivo
                Read_CSV(Path + archivo)
                print 'Readed ' + archivo
            except:
                Read_bad()
                corruted.append(archivo)
                print 'file corruted', archivo
    except:
        Read_bad()
        print 'Day without flies'
        missed.append(day)

print '************************* lv2 files readed **************************'

print missed

print corruted

# Limpiar Variables

del Temperature_Zenit
del Temperature_15N
del Temperature_15S
# del Temperature_15A

del VaporDensity_Zenit
del VaporDensity_15N
del VaporDensity_15S
# del VaporDensity_15A

del Liquid_Zenit
del Liquid_15N
del Liquid_15S
# del Liquid_15A

del RelativeHumidity_Zenit
del RelativeHumidity_15N
del RelativeHumidity_15S
# del RelativeHumidity_15A

# Tiempos
del t_Temperature_Zenit
del t_Temperature_15N
del t_Temperature_15S
# del t_Temperature_15A

del t_VaporDensity_Zenit
del t_VaporDensity_15N
del t_VaporDensity_15S
# del t_VaporDensity_15A

del t_Liquid_Zenit
del t_Liquid_15N
del t_Liquid_15S
# del t_Liquid_15A

del t_RelativeHumidity_Zenit
del t_RelativeHumidity_15N
del t_RelativeHumidity_15S
# del t_RelativeHumidity_15A


print "variables cleared"


# =============================================================================
# CONVERTIR LOS DATOS EN MATRICES

def Matriciador(X):
    M = np.zeros((len(X), 58), dtype=float)

    for i in range(len(X)):
        for j in range(58):
            try:
                M[i, j] = float(X[i][j])
            except:
                M[i, j] = np.nan
                print i, t_VaporDensity_15A[i]

    return M


# np.array(record, dtype=float)
# np.array(date, dtype=float)
# np.array(GPS, dtype=float)

ground = np.array(ground, dtype=float)
cloud = np.array(cloud, dtype=float)

# Temperature_Zenit = np.array(Temperature_Zenit, dtype=float)
# Temperature_15N = Matriciador(Temperature_15N)
# Temperature_15S = Matriciador(Temperature_15S)
Temperature_15A = np.array(Temperature_15A, dtype=float)
print 'Temperature'

# Liquid_Zenit = np.array(Liquid_Zenit, dtype=float)
# Liquid_15N = Matriciador(Liquid_15N)
# Liquid_15S = Matriciador(Liquid_15S)
Liquid_15A = np.array(Liquid_15A, dtype=float)
print 'Liquid'

# RelativeHumidity_Zenit = np.array(RelativeHumidity_Zenit, dtype=float)
# RelativeHumidity_15N = Matriciador(RelativeHumidity_15N)
# RelativeHumidity_15S = Matriciador(RelativeHumidity_15S)
RelativeHumidity_15A = np.array(RelativeHumidity_15A, dtype=float)
print 'RelativeHumidity'

# VaporDensity_Zenit = Matriciador(VaporDensity_Zenit)
# VaporDensity_15N = Matriciador(VaporDensity_15N)
# VaporDensity_15S = Matriciador(VaporDensity_15S)
VaporDensity_15A = Matriciador(VaporDensity_15A)

# VaporDensity_15A = np.array(VaporDensity_15A, dtype=float)
print 'VaporDensity'


##Enmascarar datos malos
# Enmascarar datos malos
Temperature_15A = np.ma.masked_outside(Temperature_15A, 100, 350)
Temperature_15A = np.ma.array(Temperature_15A, mask=np.isnan(Temperature_15A))
Temperature_15A = np.ma.mask_rows(Temperature_15A)

# Humedad = np.ma.masked_outside(Temperature_15A, 100,350)
# Humedad = np.ma.masked_where(np.ma.getmask(Temperatura), RelativeHumidity_15A)
RelativeHumidity_15A = np.ma.masked_outside(RelativeHumidity_15A, 0, 100)
RelativeHumidity_15A = np.ma.array(RelativeHumidity_15A, mask=np.isnan(RelativeHumidity_15A))
RelativeHumidity_15A = np.ma.mask_rows(RelativeHumidity_15A)

Liquid_15A = np.ma.masked_outside(Liquid_15A, 0, 10)
Liquid_15A = np.ma.array(Liquid_15A, mask=np.isnan(Liquid_15A))
Liquid_15A = np.ma.mask_rows(Liquid_15A)

print 'Masked'

##Convetir a DataFrame
# T_Z = pd.DataFrame(Temperature_Zenit, index=t_Temperature_Zenit, columns=lv2)
# T_N = pd.DataFrame(Temperature_15N, index=t_Temperature_15N, columns=lv2)
# T_S = pd.DataFrame(Temperature_15S, index=t_Temperature_15S, columns=lv2)
T_A = pd.DataFrame(Temperature_15A, index=t_Temperature_15A, columns=lv2)
print 'Pandas Temperature'

# V_Z = pd.DataFrame(VaporDensity_Zenit, index=t_VaporDensity_Zenit, columns=lv2)
# V_N = pd.DataFrame(VaporDensity_15N, index=t_VaporDensity_15N, columns=lv2)
# V_S = pd.DataFrame(VaporDensity_15S, index=t_VaporDensity_15S, columns=lv2)
V_A = pd.DataFrame(VaporDensity_15A, index=t_VaporDensity_15A, columns=lv2)
print 'Pandas Vapor'

# L_Z = pd.DataFrame(Liquid_Zenit, index=t_Liquid_Zenit, columns=lv2)
# L_N = pd.DataFrame(Liquid_15N, index=t_Liquid_15N, columns=lv2)
# L_S = pd.DataFrame(Liquid_15S, index=t_Liquid_15S, columns=lv2)
L_A = pd.DataFrame(Liquid_15A, index=t_Liquid_15A, columns=lv2)
print 'Pandas Liquid'

# H_Z = pd.DataFrame(RelativeHumidity_Zenit, index=t_RelativeHumidity_Zenit, columns=lv2)
# H_N = pd.DataFrame(RelativeHumidity_15N, index=t_RelativeHumidity_15N, columns=lv2)
# H_S = pd.DataFrame(RelativeHumidity_15S, index=t_RelativeHumidity_15S, columns=lv2)
H_A = pd.DataFrame(RelativeHumidity_15A, index=t_RelativeHumidity_15A, columns=lv2)
print 'Pandas Humedad'




# =========================================================================
# =========================================================================
# =========================================================================

#                       Thermodinamic parameters

# =========================================================================
# =========================================================================
# =========================================================================

p0 = 1013.25
gM_RT = 9.80665 * 0.0289644 / (8.31447 * 295.15)

a = 0.3048 / 145366.45
b = 0.190284

Alt = np.array(lv2) * 1000


def Pressure(Alt, T):
    gM_R = 9.80665 * 0.0289644 / 8.31447
    temp = T.iloc[-1, :]
    Press = p0 * np.exp(-gM_R * (Alt + 1541) / temp)
    return np.array(Press)


# Press = Pressure(Alt, T_A)
# P = p0*np.exp(np.log(1-Alt*a)/b)
# P = p0*(1-Alt*a)/np.exp(b)
# Press = p0*np.exp(-gM_RT*(Alt+1541))
# Press = p0* (1 - (2.25577e-5 * (Alt + 1541))) ** 5.25588
# Press = 849.6*np.exp(-Alt/7000)

Press = [849.7, 844.8, 839.9, 835.0, 830.2, 825.4, 820.6, 815.8, 811.1, 806.4, 801.7, 792.3, 783.1,
         773.9, 764.9, 755.9, 747.0, 738.2, 729.5, 720.8, 712.3, 703.8, 695.4, 687.1, 678.9, 670.8,
         650.7, 631.2, 612.1, 593.4, 575.1, 557.4, 540.0, 523.1, 506.7, 490.7, 475.1, 459.9, 443.1,
         430.7, 416.8, 403.1, 389.9, 377.0, 364.5, 352.2, 340.3, 328.8, 317.5, 306.5, 295.9, 285.5,
         275.4, 265.6, 256.0, 246.8, 237.7, 229.0]

R = 287.05
cp = 1004
lv = 2260


def DewPoint(RH, T):
    # constantes
    # a = 6.1121 #mb
    # b = 18.678
    # c = 530.29
    # d = 507.65
    # Td = c*(np.log(RH/1000+np.exp((b-T/d)*(T/(c+T)))))/(b-(np.log(RH/1000+np.exp((b-T/d)*(T/(c+T))))))

    a = 17.625
    b = 243.04

    Num = (b * (np.log(RH / 100.) + ((a * (T - 273.15)) / (b + T - 271.15))))
    Den = a - np.log(RH / 100.) - (a * (T - 273.15) / (b + T - 273 - 15))
    Td = Num / Den

    return Td + 273.15


def Theta(T, P):
    Tp = T.copy()

    for i in range(58):
        Tp.iloc[:, i] = T.iloc[:, i] * (1000 / (Press[i])) ** (R / cp)

    return Tp


def MixingRatio(V, T, P):
    ##density dry air
    pdA = T.copy()
    q = V.copy()
    for i in range(58):
        # pasar hPa a Pa 100
        pdA.iloc[:, i] = 100 * Press[i] / (R * T.iloc[:, i])

    q = V / pdA

    return q/1000.


def MixRatioSat(q, RH):
    qs = 100 * q / RH
    return qs 


def TempV(T, q):
    Tv = T * (1+q*((1/0.622)-1))
    return Tv


def Theta_e(Theta, qs, T):
    O_e = Theta * np.exp(lv * qs / (cp * T))

    return O_e


def Theta_v(Tv, P):
    O_v = Tv.copy()

    for i in range(58):
        O_v.iloc[:, i] = Tv.iloc[:, i] * (1000 / Press[i]) ** (R / cp)

    return O_v


Td = DewPoint(H_A, T_A)
print Td
# O = Theta(T_A, Press)
q = MixingRatio(V_A, T_A, Press)
# ws = MixRatioSat(w, H_A)
Tv = TempV(T_A, q)
# Oe = Theta_e(O, ws, T_A)
# Ov = Theta_v(Tv, Press)
print Td
print Tv
print 'DewPoint and VirtualTemp'

# =========================================================================
#               Funciones termodinamicas
# =========================================================================
Rs_da       = 287.05    # Specific gas const for dry air, J kg^{-1} K^{-1}
Rs_v        = 461.51    # Specific gas const for water vapour, J kg^{-1} K^{-1}
Cp_da       = 1004.6    # Specific heat at constant pressure for dry air
Cv_da       = 719.      # Specific heat at constant volume for dry air
Cp_v        = 1870.     # Specific heat at constant pressure for water vapour
Cv_v        = 1410.     # Specific heat at constant volume for water vapour
Cp_lw       = 4218      # Specific heat at constant pressure for liquid water
Epsilon     = 0.622     # Epsilon=R_s_da/R_s_v; The ratio of the gas constants
degCtoK     = 273.15    # Temperature offset between K and C (deg C)
rho_w       = 1000.     # Liquid Water density kg m^{-3}
grav        = 9.81      # Gravity, m s^{-2}
Lv          = 2.5e6     # Latent Heat of vaporisation
boltzmann   = 5.67e-8   # Stefan-Boltzmann constant
mv          = 18.0153   # Mean molar mass of water vapor(g/mol)


def SatVap(temp, phase="liquid"):
    """Calculate saturation vapour pressure over liquid water and/or ice.
    INPUTS:
    temp: (K)
    phase: ['liquid'],'ice'. If 'liquid', do simple dew point. If 'ice',
    return saturation vapour pressure as follows:
    Tc>=0: es = es_liquid
    Tc <0: es = es_ice

    RETURNS: e_sat  (hPa)

    SOURCE: http://cires.colorado.edu/~voemel/vp.html (#2:
    CIMO guide (WMO 2008), modified to return values in Pa)

    This formulation is chosen because of its appealing simplicity,
    but it performs very well with respect to the reference forms
    at temperatures above -40 C. At some point I'll implement Goff-Gratch
    (from the same resource).
    """

    if temp > 100:
        T = temp
    else:
        T = temp + 273.15

    Log10ew = 10.79574 * (1 - 273.16 / T) - 5.02800 * np.log10(T / 273.16) \
              + 1.50475E-4 * (1 - 10 * (-8.2969 * (T / 273.16 - 1))) \
              + 0.42873E-3 * (10 * (+4.76955 * (1 - 273.16 / T)) - 1) + 0.78614
    ew = 10 ** Log10ew

    return ew


# if temp >100:
#     tempc = temp-273.15
# else:
#     tempc=temp
# # tempc = temp+273.15
# over_liquid=6.112*np.exp(17.62*tempc/(tempc+243.12))*100.
# over_ice=6.112*np.exp(22.46*tempc/(tempc+272.62))*100.
# # return np.where(tempc<0,over_ice,over_liquid)
#
# if phase=="liquid":
#     # return 6.112*np.exp(17.67*tempc/(tempc+243.12))*100.
#     return over_liquid
# elif phase=="ice":
#     # return 6.112*np.exp(22.46*tempc/(tempc+272.62))*100.
#     return np.where(tempc<0,over_ice,over_liquid)
# else:
#     raise NotImplementedError

def MixRatio(e, p):
    """Mixing ratio of water vapour
    INPUTS
    e (Pa) Water vapor pressure
    p (Pa) Ambient pressure

    RETURNS
    qv (kg kg^-1) Water vapor mixing ratio`
    """

    return Epsilon * e / (p - e)


def Theta(tempk, pres, pref=100000.):
    """Potential Temperature
    INPUTS:
    tempk (K)
    pres (Pa)
    pref: Reference pressure (default 100000 Pa)
    OUTPUTS: Theta (K)
    Source: Wikipedia
    Prints a warning if a pressure value below 2000 Pa input, to ensure
    that the units were input correctly.
    """

    try:
        minpres = np.min(pres)
    except TypeError:
        minpres = pres

    if minpres < 2000:
        print "WARNING: P<2000 Pa; did you input a value in hPa?"

    return tempk * (pref / pres) ** (Rs_da / Cp_da)


def TempK(theta, pres, pref=100000.):
    """Inverts Theta function."""

    try:
        minpres = np.min(pres)
    except TypeError:
        minpres = pres

    if minpres < 2000:
        print "WARNING: P<2000 Pa; did you input a value in hPa?"

    return theta * (pres / pref) ** (Rs_da / Cp_da)



def ThetaV(tempk, pres, e):
    """Virtual Potential Temperature

    INPUTS
    tempk (K)
    pres (Pa)
    e: Water vapour pressure (Pa) (Optional)
    """

    mixr = MixRatio(e, pres)
    theta = Theta(tempk, pres)

    return theta * (1 + mixr / Epsilon) / (1 + mixr)


def GammaW(tempk, pres, e=None):
    """Function to calculate the moist adiabatic lapse rate (deg C/Pa) based
    on the temperature, pressure, and rh of the environment.
    INPUTS:
    tempk (K)
    pres (Pa)
    RH (%)
    RETURNS:
    GammaW: The moist adiabatic lapse rate (Dec K/Pa)
    """

    tempc = tempk - degCtoK
    es = SatVap(tempk) * 100
    ws = MixRatio(es, pres)

    if e is None:
        # assume saturated
        e = es

    w = MixRatio(e, pres)

    tempv = VirtualTempFromMixR(tempk, w)
    latent = Latentc(tempc)

    A = 1.0 + latent * ws / (Rs_da * tempk)
    B = 1.0 + Epsilon * latent * latent * ws / (Cp_da * Rs_da * tempk * tempk)
    Rho = pres / (Rs_da * tempv)
    Gamma = (A / B) / (Cp_da * Rho)
    return Gamma


def Density(tempk, pres, mixr):
    """Density of moist air"""

    virtualT = VirtualTempFromMixR(tempk, mixr)
    return pres / (Rs_da * virtualT)


def VirtualTemp(tempk, pres, e):
    """Virtual Temperature
    INPUTS:
    tempk: Temperature (K)
    e: vapour pressure (Pa)
    p: static pressure (Pa)
    OUTPUTS:
    tempv: Virtual temperature (K)
    SOURCE: hmmmm (Wikipedia)."""

    tempvk = tempk / (1 - (e / pres) * (1 - Epsilon))
    return tempvk


def VirtualTempFromMixR(tempk, mixr):
    """Virtual Temperature
    INPUTS:
    tempk: Temperature (K)
    mixr: Mixing Ratio (kg/kg)
    OUTPUTS:
    tempv: Virtual temperature (K)
    SOURCE: hmmmm (Wikipedia). This is an approximation
    based on a m
    """

    return tempk * (1.0 + 0.6 * mixr)


def Latentc(tempc):
    """Latent heat of condensation (vapourisation)
    INPUTS:
    tempc (C)
    OUTPUTS:
    L_w (J/kg)
    SOURCE:
    http://en.wikipedia.org/wiki/Latent_heat#Latent_heat_for_condensation_of_water
    """

    return 1000 * (2500.8 - 2.36 * tempc + 0.0016 * tempc ** 2 - 0.00006 * tempc ** 3)


def MixRatio(e, p):
    """Mixing ratio of water vapour
    INPUTS
    e (Pa) Water vapor pressure
    p (Pa) Ambient pressure

    RETURNS
    qv (kg kg^-1) Water vapor mixing ratio`
    """

    return Epsilon * e / (p - e)


def MixR2VaporPress(qv, p):
    """Return Vapor Pressure given Mixing Ratio and Pressure
    INPUTS
    qv (kg kg^-1) Water vapor mixing ratio`
    p (Pa) Ambient pressure

    RETURNS
    e (Pa) Water vapor pressure
    """

    return qv * p / (Epsilon + qv)


def VaporPressure(dwpt):
    """Water vapor pressure
    INPUTS
    dwpt (C) Dew Point Temperature (for SATURATION vapor
         pressure use tempc)

    RETURNS
    e (Pa) Water Vapor Pressure
    SOURCE:
    Bolton, Monthly Weather Review, 1980, p 1047, eq. (10)
    """

    return 611.2 * np.exp(17.67 * dwpt / (243.5 + dwpt))


def DewPoint(e):
    """ Use Bolton's (1980, MWR, p1047) formulae to find tdew.
    INPUTS:
    e (Pa) Water Vapor Pressure
    OUTPUTS:
    Td (C)
      """

    ln_ratio = np.log(e / 611.2)
    Td = ((17.67 - ln_ratio) * degCtoK + 243.5 * ln_ratio) / (17.67 - ln_ratio)
    return Td - degCtoK


# =========================================================================
# =========================================================================
# =========================================================================

#                           Stability index

# =========================================================================
# =========================================================================
# =========================================================================

def lift_wet(start_t, pres):
    # --------------------------------------------------------------------
    # Lift a parcel moist adiabatically from startp to endp.
    # Init temp is startt in K, pressure levels are in hPa
    # --------------------------------------------------------------------

    temp = start_t
    t_out = np.zeros(pres.shape);
    t_out[0] = start_t
    for ii in range(pres.shape[0] - 1):
        delp = pres[ii] - pres[ii + 1]
        temp = temp - 100 * delp * GammaW(temp, (pres[ii] - delp / 2) * 100)
        t_out[ii + 1] = temp
    return t_out


def lifter(start_t, start_dp, start_p):
    """Lift a parcel to discover certain properties.
    INPUTS:
    startp:  Pressure (hPa)
    startt:  Temperature (K)
    startdp: Dew Point Temperature (K)
    """

    # assert start_t > start_dp, "Not a valid parcel. Check Td<Tc"
    try:
        Pres = np.linspace(start_p, 200, 100)

        # Lift the dry parcel
        T_dry = start_t * (Pres / start_p) ** (Rs_da / Cp_da)

        # Mixing ratio isopleth
        # revisar bien si lo hago con la relacion de mezcla del radiometro
        start_e = SatVap(start_dp) * 100
        start_w = MixRatio(start_e, start_p * 100)

        e = Pres * start_w / (.622 + start_w)
        T_iso = 243.5 / (17.67 / np.log(e / 6.112) - 1) + 273.15

        # Solve for the intersection of these lines (LCL)
        # interp requires the x argument (argument 2)
        # to be ascending in order!
        P_lcl = np.interp(0, T_iso - T_dry, Pres)
        T_lcl = np.interp(P_lcl, Pres[::-1], T_dry[::-1])

        # Now lift a wet parcel from the intersection point
        preswet = np.linspace(P_lcl, 200)
        tempwet = lift_wet(T_lcl, preswet)

        P_parcel = []
        T_parcel = []

        for i in range(len(Pres)):
            if Pres[i] > P_lcl:
                P_parcel.append(Pres[i])
                T_parcel.append(T_dry[i])

        for i in range(len(tempwet)):
            P_parcel.append(preswet[i])
            T_parcel.append(tempwet[i])

        return T_parcel, P_parcel, T_lcl, P_lcl
    except:
        return np.nan, np.nan, np.nan, np.nan


# T_parcel, P_parcel = lifter(T_A.iloc[-1, 0], Td.iloc[-1, 0], Press[0])


def Diferenciador(T, T_dp, Press, level, level0=0):
    """Calcula lifted Index.
    INPUTS:
    T     :  Temperature profile (K)
    T_dp  : Dew Point Temperature (K)
    Press : pressuere (hPa)
    level : comparation level (hPa)
    level0: ascend level (hPa)
    """
    try:
        # ascender la temperatura 50mb encima de la superficie
        start_P = np.ones(len(Press)) * Press[0]

        start_T = np.interp(level0, start_P - Press, T)
        start_Tdp = np.interp(level0, start_P - Press, T_dp)

        T_parcel, P_parcel, T_lcl, P_lcl = lifter(start_T, start_Tdp, Press[0] - 50)

        T_p_level = np.interp(level, P_parcel[::-1], T_parcel[::-1])
        T_level = np.interp(level, Press[::-1], T[::-1])

        return T_level - T_p_level

    except:
        return np.nan


def integral(x, y):
    s = 0
    for i in range(len(y)-1):
        a = (x[i+1]-x[i])*(y[i]+y[i+1])/2.
        s += a
    return s


def CAPE_CINE(T, P, T_parcel, P_parcel, T_lcl, P_lcl):
    try:
        # interp to accuracy in te integral
        T_interp = np.empty((len(P_parcel), ), dtype=float)
        H_interp = np.empty((len(P_parcel), ), dtype=float)
        T_interp[::-1] = np.interp(P_parcel[::-1], P[::-1], T[::-1])
        H_interp[::-1] = np.interp(P_parcel[::-1], P[::-1], lv2[::-1])*1000.

        T_dif = grav*(T_parcel - T_interp)/T_interp

        il = T_dif[(T_dif<0)&(T_interp>=T_lcl)] # T < T_parcel before LCL
        fc = T_dif[(T_dif>=0)&(T_interp<=T_lcl)] # T > T_parcel after LCL
        ie = T_dif[(T_dif<=0)&(T_dif<=fc[0])&(T_interp>=T_lcl-20)] # convective inhibition end
        el = T_dif[(T_dif<=0)&(T_interp<=T_lcl-20)] # T < T_parcel after LCL

        IL  = np.where(T_dif == il[0])[0][0] # inhibition of convection starts
        IE  = np.where(T_dif == ie[-1])[0][0] #inhibition of convection ends
        LFC = np.where(T_dif == fc[0])[0][0] # level of free convection
        try:
            EL  = np.where(T_dif == el[0])[0][0] # equilibrium level
        except:
            EL = len(T_dif)-1

        CINE = np.trapz(T_dif[IL:IE], H_interp[IL:IE])
        CAPE = np.trapz(T_dif[LFC:EL], H_interp[LFC:EL])
        # CINE = integral(T_dif[IL:IE], H_interp[IL:IE])
        # CAPE = integral(T_dif[LFC:EL], H_interp[LFC:EL])
        return CAPE, CINE
    except:
        print 'ClAMENT!!'
        return np.nan, np.nan

#obtener datos de el dato 1
T_parcel, P_parcel, T_lcl, P_lcl = lifter(Tv.iloc[-1, 1], Td.iloc[-1, 1], Press[1])

CAPE, CINE = CAPE_CINE(Tv.iloc[-1,:].values, Press, T_parcel, P_parcel, T_lcl, P_lcl)

print CAPE, CINE

# Historia del CAPE - CINE

cape = []; cine = []
for i in T_A.index:
    print i
    T_parcel, P_parcel, T_lcl, P_lcl = lifter(Tv[Tv.index == i].values[-1,1], Td.iloc[Td.index == i].values[-1,1], Press[1])
    cap, cin = CAPE_CINE(Tv[Tv.index == i].values[0,:], Press, T_parcel, P_parcel, T_lcl, P_lcl)
    cape.append(cap)
    cine.append(cin)

CAPE = pd.DataFrame(cape, index=t_Temperature_15A)
CINE = pd.DataFrame(cine, index=t_Temperature_15A)
CAPE.columns=['CAPE']
CINE.columns=['CINE']

CAPE = CAPE[(CAPE['CAPE']<3E4)&(CAPE['CAPE']>0)]
CINE = CINE[(CINE['CINE']>-1E4)&(CINE['CINE']<0)]

CAPE.to_csv(ruta+'CAPE.txt', sep='\t')
CINE.to_csv(ruta+'CINE.txt', sep='\t')


plt.figure()
CAPE.plot()
plt.savefig(ruta+'CAPE.png')

plt.figure()
CINE.plot()
plt.savefig(ruta+'CINE.png')
print CINE, CAPE


# Historia del LI
lifted = []
for i in T_A.index:
    print i
    li = Diferenciador(T_A[T_A.index == i].values[0,:], Td.iloc[Td.index == i].values[0,:], Press, 500, 50)
    lifted.append(li)

LI = pd.DataFrame(lifted, index=t_Temperature_15A)
LI.columns=['LI']
LI = LI[(LI['LI']<10.)&(LI['LI']>-20.)]

LI.to_csv(ruta+'LI.txt', sep='\t')

plt.figure()
LI.plot()
plt.xlabel('Time')
plt.ylabel('LI')
plt.savefig(ruta+'LI.png')
print LI



# ciclo diario


def DiurnalCycles(Index, label):
    "Grafica el ciclo diurno promedio y mensual de un indice"

    month_hour_means = Index.groupby(lambda x: (x.month, x.hour)).mean()
    hour_means = Index.groupby(lambda x: (x.hour)).mean()
    print hour_means
    print month_hour_means

    plt.figure()
    plt.plot(hour_means.values, label = 'Ciclo diurno')
    plt.xlabel('Hour')
    plt.ylabel(label)
    plt.legend(loc='best')
    plt.savefig(ruta+label+'_dirunal_cycle.png')

    meses = ['enero','febrero','marzo', 'abril', 'mayo','junio','julio',
             'agosto', 'septiembre','octubre','noviembre','diciembre']

    for i in range (1,13):
        plt.figure()
        plt.plot(month_hour_means.values[24*(i-1) : 24*(i)],label=meses[i-1])
        plt.xlabel('Hour')
        plt.ylabel(label)
        plt.legend(loc='best')
        plt.savefig(ruta+label+'_'+meses[i-1]+'_dirunal_cycle.png')

    # Todos los meses en una grafica

    import matplotlib.colors as colors
    import matplotlib.cm as cmx
    # define some random data that emulates your indeded code:
    NCURVES = 12
    # np.random.seed(101)
    # curves = [np.random.random(20) for i in range(NCURVES)]
    values = range(NCURVES)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    # replace the next line
    #jet = colors.Colormap('jet')
    # with
    jet = cm = plt.get_cmap('jet')
    cNorm  = colors.Normalize(vmin=0, vmax=values[-1])
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
    print scalarMap.get_clim()

    lines = []
    for idx in range(NCURVES):
        line = month_hour_means.values[24*(idx) : 24*(idx+1)]
        colorVal = scalarMap.to_rgba(values[idx])
        colorText = (meses[idx])
        retLine, = ax.plot(line,
                           color=colorVal,
                           label=colorText)
        lines.append(retLine)
    #added this to get the legend to work
    handles,labels = ax.get_legend_handles_labels()

    ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, -0.05),
              fancybox=True, shadow=True, ncol=5)
    ax.grid()
    plt.xlabel('Hour')
    plt.ylabel(label)
    plt.savefig(ruta+label+'_Month_dirunal_cycle.png')
    print 'Guardadas'


DiurnalCycles(LI, 'LI')
DiurnalCycles(CAPE, 'CAPE')
DiurnalCycles(CINE, 'CINE')


print 'Non clament finiti'
