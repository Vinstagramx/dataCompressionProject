# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 22:44:07 2020

@author: Ronan
"""
import numpy as np
import os
import matplotlib.pyplot as plt
import random
import sys

random.seed(1)

time_interval = 0.14866719 

def load_data(path):
        data = np.loadtxt(path).T
        fixed_x = [x for x in data[1]]; fixed_y = [y for y in data[2]]; fixed_z = [z for z in data[3]]
        fixed_array = np.array([fixed_x, fixed_y, fixed_z], dtype = np.float) #does this round down or nearest - if we can't reconstruct data look at this 
        return fixed_array

def square_wave(t, T, offset=0, amplitude = 1):
    period = t//T #function repeats so this is the number of cycles
    if t < 0:
        v_in = 1
    else:
        if t < (2*period+1)*T/2: #halfway point
            v_in = 0
        elif t < (period+1)*T and t > (2*period+1)*T/2:
            v_in = amplitude
    return v_in

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
    
def gen_wave_data(n, max_amp, max_freq):
    """Generate n-1 waves of random amplitude and frequency. At the start 
    generate 1 major wave that has a higher maximum possible amplitude distribution
    than the other waves."""
    wave_data = []
    major_wave = (random.uniform(0.8,1.2), 0, random.uniform(3.5,5))
    wave_data.append(major_wave)
    for i in range(n-1):
        temp_wave = (random.uniform(0.8,1.2), 0, random.uniform(0.25,3.5))
        wave_data.append(temp_wave)
    return wave_data

def simulate_interference(wave_data, data, dc_offset = [0,0,0], dc_only = False):
    """Given an input list of thruples wave_data and the data to be modified,
    create n squares using wave_data to get their period, offset and amplitude.
    Then add these square waves to the data and save. If a dc offset is supplied,
    add this to the data as well.
    If dc_only == True, only DC interference is used.
    """

    modified_data = []
    for direction in range(3):
        dir_data = data[direction]
        temp_data = dir_data
        temp_data = temp_data + dc_offset[direction]
        time = np.array([i for i in range(len(dir_data))])*time_interval
        if dc_only == False:
            for wave in wave_data:
                sq_wave = np.array([square_wave(i, wave[0], wave[1], wave[2]) \
                                    for i in time])
                temp_data = temp_data + sq_wave
        modified_data.append(temp_data)
    return (time, modified_data)

def save(data, out):
    time = data[0]
    f = open(out, "w")
    for i in range(len(time)):
        string = str(time[i]) + "  " + str(data[1][0][i]) + "  " + str(data[1][1][i]) + "  " + str(data[1][2][i]) + "\n"
        f.write(string)
    f.close()

def manage_files(file, n, dc=False, dc_only = False):
    # If dc_only == True - i.e. for 0 waves added, then no square waves are added onto the data.
    wave_data = gen_wave_data(n, 5, 1.5)
    print(wave_data)
    if dc:
        dc_offset = dc_interference()
    else:
        dc_offset= [0,0,0]
    data = load_data(file)
    mod = simulate_interference(wave_data, data, dc_offset, dc_only)
    outfile = file[:9] + "_modified_"+str(n)+".txt"
    save(mod, outfile)
        
if __name__ == "__main__":
    file_names = []
    for i in range(0,8):
        if i == 0:
            manage_files(sys.argv[1], i, True, True)
        else:
            manage_files(sys.argv[1], i, True, False)
        file_names.append(sys.argv[1][:9]+ "_modified_"+str(i)+".txt")
    f = open("temp_file_list.txt", "w")
    for i in range(len(file_names)):
        f.write(file_names[i] + "\n")
    


        
