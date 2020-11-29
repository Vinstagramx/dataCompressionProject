#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:31:19 2020

@author: ronan
"""

import numpy as np
import random
import sys

random.seed(1) #set seed for random generation

time_interval = 0.14866719 

def load_data(path):
        data = np.loadtxt(path).T
        fixed_x = [x for x in data[1]]; fixed_y = [y for y in data[2]]; fixed_z = [z for z in data[3]]
        fixed_array = np.array([fixed_x, fixed_y, fixed_z], dtype = np.float) #does this round down or nearest - if we can't reconstruct data look at this 
        return fixed_array


def dc_interference():
    """Simulate DC interference by generating random vector of magnitude 1 and 
    then multiplying by 200"""
    x_component = random.uniform(0, 1/np.sqrt(2))
    y_component = random.uniform(0, 1/np.sqrt(2))
    z_component = np.sqrt(1-(x_component**2 + y_component**2))
    magnitude = random.randint(100,200)
    vec = (magnitude*x_component, magnitude*y_component, magnitude*z_component)
    print("magnitude of vector: ", np.sqrt(vec[0]**2+vec[1]**2+vec[2]**2))
    return vec

def add_sin(freq, amplitude, data):
    modified_data = []
    for direction in range(3):
        dir_data = data[direction]
        temp_data = dir_data
        time = np.array([i for i in range(len(dir_data))])*time_interval
        sin_wave = amp*np.sin(2*np.pi*freq*time)
        temp_data = temp_data + sin_wave
        modified_data.append(temp_data)
    return (time, modified_data)

def save(data, out):
    time = data[0]
    f = open(out, "w")
    for i in range(len(time)):
        string = str(time[i]) + "  " + str(data[1][0][i]) + "  " + str(data[1][1][i]) + "  " + str(data[1][2][i]) + "\n"
        f.write(string)
    f.close()

#%%
if __name__ == "__main__":
    file_names = []
    #wave_data = gen_wave_data(8, 5, 1.5) #so we use the same interference for each wave, just adding a new one each time
    data = load_data(sys.argv[1])
    dc = dc_interference() #generate consistent dc interference
    for freq in np.arange(1,31, step=2):
        for amp in np.arange(0,6, step=1):
            i = str(freq) + "_" + str(amp)
            print("adding sin " +i)
    #    out_data = simulate_interference(wave_data[:i+1], data, dc) #only use i waves in the interference
            out_data= add_sin(freq, amp, data)
            outfile = sys.argv[1][:9] + "_modified_"+str(i)+".txt"
            save(out_data, outfile)
            file_names.append(sys.argv[1][:9]+ "_modified_"+str(i)+".txt")
    f = open("temp_file_list.txt", "w")
    for i in range(len(file_names)):
        f.write(file_names[i] + "\n")
    