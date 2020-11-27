# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 16:57:14 2020

@author: Ronan
"""
import numpy as np
import matplotlib.pyplot as plt

def load_data(path):
    data = np.loadtxt(path).T
    fixed_x = [x for x in data[1]]; fixed_y = [y for y in data[2]]; fixed_z = [z for z in data[3]]
    fixed_array = np.array([fixed_x, fixed_y, fixed_z], dtype = np.float) #does this round down or nearest - if we can't reconstruct data look at this 
    return fixed_array

data = load_data("C1_160309_cavity.txt")
time = np.array([i for i in range(len(data[1]))])*0.14866719
plt.plot(time, data[0])