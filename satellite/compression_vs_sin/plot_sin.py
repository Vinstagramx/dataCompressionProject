#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 15:57:31 2020

@author: ronan
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

compression_data_strings = open("temp_compression_data.txt").readlines()
compression_data = np.array([float(i.strip("\n")) for i in compression_data_strings])
compression_data = compression_data.reshape((90, 3))
means = np.mean(compression_data, axis=1)
data = means.reshape(15, 6)

fig = plt.figure()
ax = fig.gca(projection='3d')

X = np.arange(1,31, step=2)
Y = np.arange(0,6, step=1)
X,Y = np.meshgrid(Y,X)
Z = data

surf = ax.plot_trisurf(X, Y, Z, cmap=cm.coolwarm, \
                       linewidth=0, antialiased=False)