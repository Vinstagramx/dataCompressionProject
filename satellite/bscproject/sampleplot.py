#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 12:19:47 2020

@author: vwong
"""

# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

# #df = pd.read_csv('C1_160308.FS.FULLRES.txt', sep = '\s+', header = None, dtype = np.float64, engine = 'python')
# #df.columns = ["time", "x", "y", "z"]

# df['cortime'] = df['time'] - df['time'][0]
# plt.title('Magnetic field readings of ESA Cluster Probe')
# plt.xlabel('Time(s)')
# plt.ylabel('Magnetic Field Strength (nT)')
# plt.plot(df['cortime'], df['x'])
# plt.plot(df['cortime'], df['y'])
# plt.plot(df['cortime'], df['z'])

def power_two(param):
    power = 1
    while(power < param):
        power*=2
    print(f'closest exponent = {power}')
    return power

x = 200
power_two(x)