# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 22:44:07 2020

@author: Ronan
"""
import numpy as np
import os
import matplotlib.pyplot as plt

cwd = os.getcwd()
parent_dir = os.path.dirname(cwd)
cwd = os.path.dirname(cwd)
datafile = 'C3_160313.FS.FULLRES.txt'
DATA_PATH = os.path.join(cwd, 'data', datafile)

time_interval = 0.14866719 

def load_data(path):
        data = np.loadtxt(path).T
        fixed_x = round(data[1]/7.8125e-3); fixed_y = round(data[2]/7.8125e-3); fixed_z = round(data[3]/7.8125e-3)
        fixed_array = np.array([fixed_x, fixed_y, fixed_z], dtype = np.int32) #does this round down or nearest - if we can't reconstruct data look at this 
        return fixed_array

def square_wave(t, T, offset=0):
    period = t//T #function repeats so this is the number of cycles
    if t < 0:
        v_in = 1
    else:
        if t < (2*period+1)*T/2: #halfway point
            v_in = 0
        elif t < (period+1)*T and t > (2*period+1)*T/2:
            v_in = 1
    return v_in

def simulate_interference(wave_data, data):
    # wave data of form [(period, offset, amplitude), ...]
    modified_data = []
    for direction in range(3):
        dir_data = data[direction]
        temp_data = dir_data
        time = np.array([i for i in range(len(dir_data))])*time_interval
        for wave in wave_data:
            sq_wave = np.array([square_wave(i, wave[0], wave[1]) \
                                for i in time])*wave[2]/7.8125e-3
            temp_data = temp_data + sq_wave
        modified_data.append(temp_data)
    return (time, modified_data)

data = load_data(DATA_PATH)
mod = simulate_interference([(1,0,5)], data)
plt.plot(mod[0], mod[1][0])
plt.plot(mod[0], data[0])
