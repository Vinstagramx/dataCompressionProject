# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 16:39:32 2020

@author: Ronan
"""

import matplotlib.pyplot as plt
from encoder import Delta, Golomb
import numpy as np

def pretty_graph(x_label, y_label, title, fontsize): #formatting graphs
    plt.xlabel(x_label,fontsize=fontsize)
    plt.title(title,fontsize=fontsize)
    plt.ylabel(y_label,fontsize=fontsize) 
    plt.tick_params(labelsize=fontsize)

#%%
DATA_PATH = "C:\\Users\\Ronan\\Documents\\uni_work\\physics\\third year\\project\\data\\test_data\\C1_160308.txt"

d = Delta(DATA_PATH, 11, 100)

#%%
d.encode_data()
#%%
raw_data = d._data
dirs = ["x", "y", "z"]
for index, i  in enumerate(raw_data):
    std = np.std(i)
    print("standard dev is: ", std)
    plt.figure("Raw data")
    plt.plot(range(len(i)), i, label = dirs[index])
    plt.legend()
    pretty_graph("Time (s)", "Magnetic Field (nT)", "Magnetic field as function of time", 20)
#%%
ratios = []
for i in range(2, 100, 2):
    print(i)
    temp_encoder = Delta(DATA_PATH, i, 100, direction="y")
    temp_encoder.encode_data(stats=False)
    ratios.append(temp_encoder.get_compression_ratio())
#%%
plt.figure("Compression ratios")
plt.plot(range(2, 100, 2), ratios)
pretty_graph("Block size", "Compression Ratio", "Compression Ratio vs Block size", 20)