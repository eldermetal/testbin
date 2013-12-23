# -*- coding: UTF-8 -*-

''' ORIGINAL '''

# import numpy as np


# def readslice(inputfilename, nx, ny, timeslice):
#     f = open(inputfilename, 'rb')
#     f.seek(8 * timeslice * nx * ny)
#     field = np.fromfile(f, dtype='float32', count=nx * ny)
#     field = np.reshape(field, (nx, ny))
#     f.close()
#     return field

# print readslice('tmax.01.2013121700.daily_1.0.dat', 2, 2, 1)

''' MODIFIED '''

import numpy as np
import math
from scipy import ndimage, interpolate
import matplotlib.pyplot as plt
from subprocess import call


def readslice(inputfilename, nx, ny):
    fd = open(inputfilename, 'rb')
    # shape = ((nx, ny), timeslice)
    # data = np.fromfile(file=fd, dtype=np.float32, count=nx * ny).reshape(nx, ny)
    data = np.fromfile(file=fd, dtype=np.float32)
    fd.close()
    return data


def latlon_to_grid(lat, lon):
    ylat = lat + 90.
    if lon > 0:
        xlon = lon
    else:
        xlon = lon + 360.
    return [round(xlon, 2), round(ylat, 2)]


def calcula_lapse_rate(dheight, prec, var):
    if dheight > 200.:
        if prec > 2.:
            return var - (dheight * 0.0065)
        else:
            return var - (dheight * 0.01)
    else:
        return var


""" Lendo da estac_total as listas das latlons e altitudes """

lat = []
latp = []
lon = []
lonp = []
# altr = []
# altm = []
cid = []
dheight = []

with open('estac_total', 'r') as latlonestac:
    latlon = latlonestac.readlines()
    for linha in latlon:
        linha_lixo = linha.split()
        lat.append(float(linha_lixo[0]))
        lon.append(float(linha_lixo[1]))

with open('estac_total_altitudes', 'r') as listaestac:
    lista = listaestac.readlines()
    for data in lista:
        data_lixo = data.split()
        dheight.append(abs(float(data_lixo[2]) - float(data_lixo[3])))
        # altr.append(int(data_lixo[2]))
        # altm.append(int(data_lixo[3]))
        cid.append(data_lixo[6])


"""PASSAR O COOR NA PORRA DO SCIPY INTERPOLATE CARAI DE ASA!!!"""

""" O CAVALINHO EH FODA!"""

coor = map(latlon_to_grid, lat, lon)

""""""""""""""""""""""""""""""""""""""
# DEFINICAO DE PARAMETROS DA GRADE
""""""""""""""""""""""""""""""""""""""
# Numero de pontos zonais LON - nx
nx = 360
# Numero de pontos meridionais lat - ny
ny = 180
# Longitude mais OESTE
rlonini = 0.
rlonfim = 360.
# Latitude mais SUL
rlatini = -89.
rlatfim = 90.

""""""""""""""""""""""""""""""""""""""
# tmax.01.2013121700.daily_1.0.dat
# tmax.01.2013120300.mensal_1.0.dat
teste = readslice('tmax.01.2013121700.daily_1.0.dat', nx, ny)
# print teste.shape
rec = teste.shape[0]
rec /= nx * ny
teste1 = teste.reshape(nx, ny, rec, order='F')
# print coor
testinho = np.array([[310.11], [75.93]])
testet1 = teste1[:, :, 0].T
print testet1
print ndimage.map_coordinates(testet1, testinho.T)
print teste1.shape
# teste1 = np.rollaxis(teste1, 0, 3)
# teste1 = np.rollaxis(teste1, 0, 2)
print teste1.shape
print teste1.shape[0]
# print teste1[1,1,1]

nrows = teste1.shape[1]
ncols = teste1.shape[0]



# print teste1
# print_slice('tmax.01.2013120300.mensal_1.0.dat', 30, 90)

""" IMPORTANTE >> teste1[:.:,1].T
 tranposta, fortran inverte os axis por default! """

# im = plt.imshow(testet1, origin='lower',
#                 interpolation='nearest', extent=[0, ncols, 0, nrows])
# plt.colorbar(im)
# plt.show()


# fd = open('tmax.01.2013120300.mensal_1.0.dat')

# print map(calcula_lapse_rate(dheight, 3, teste1[:, :, 5].T))