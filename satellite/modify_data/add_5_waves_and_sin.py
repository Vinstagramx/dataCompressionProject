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

time_interval = 1/22 #0.14866719 

def load_data(path):
        data = np.loadtxt(path).T
        fixed_x = [x for x in data[1]]; fixed_y = [y for y in data[2]]; fixed_z = [z for z in data[3]]
        fixed_array = np.array([fixed_x, fixed_y, fixed_z], dtype = np.float) #does this round down or nearest - if we can't reconstruct data look at this 
        return fixed_array

def square_wave(t, freq, offset=0, amplitude = 1):
    T = 1/freq
    period = t//T #function repeats so this is the number of cycles
    if t < (2*period+1)*T/2: #halfway point
        v_in = -amplitude/2
    else: #t < (period+1)*T and t > (2*period+1)*T/2:
        v_in = amplitude/2
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

def simulate_interference(wave_data, data, dc_offset = [0,0,0]):
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
        for wave in wave_data:
            sq_wave = np.array([square_wave(i, wave[0], wave[1], wave[2]) \
                                    for i in time])
            temp_data = temp_data + sq_wave
        modified_data.append(temp_data)
    return (time, modified_data)

def gen_wave_data(n, max_amp, max_freq):
    """Generate n-1 waves of random amplitude and frequency. At the start 
    generate 1 major wave that has a higher maximum possible amplitude distribution
    than the other waves."""
    wave_data = [(1,0,0)]
    #major_wave = (random.uniform(0.8,1.2), 0, random.uniform(3.5,5))
    #wave_data.append(major_wave)
    #wave_data.ppend((1,0,0))
    for i in range(n-1):
        temp_wave = (random.uniform(0.8,30), 0, random.uniform(0.25,3.5))
        wave_data.append(temp_wave)
    return wave_data

def add_sine_wave(time, max_amp = 10, max_freq = 10, random=True):
    """Generate a sinusoidal wave of a random amplitude and frequency, using an input array
    of data (for start and end values, and also number of samples of sine wave to take)
    --> Freq: up to 30Hz
    --> Amplitude: up to 10nT
    """
    #sample_num = len(array)
    #samples = np.linspace(array[0], array[1], num = sample_num)
    if random:
        amp = max_amp * np.random.random(size=None)
        freq = random.uniform(0.1, max_freq)
    else:
        amp = max_amp
        freq = max_freq
    sine_wave = amp * np.sin(2 * np.pi * freq * time)
    return sine_wave

def save(data, out):
    time = data[0]
    f = open(out, "w")
    for i in range(len(time)):
        string = str(time[i]) + "  " + str(data[1][0][i]) + "  " + str(data[1][1][i]) + "  " + str(data[1][2][i]) + "\n"
        f.write(string)
    f.close()

def load_files():
    names = []; cavity_indices = []
    with open("cavity_positions.txt") as f:
        data = f.readlines()#.split(" ")
        for i in data:
            temp = i.split(" ")
            names.append(temp[0]+"_cavity.txt")
            cavity_indices.append(int(temp[1].strip("\n")))
    return (names, cavity_indices)

if __name__ == "__main__":
    file_names = []
    wave_data = gen_wave_data(5, 5, 30) #so we use the same interference for each wave, just adding a new one each time
    names = load_files()[0]
    dc = dc_interference() #generate consistent dc interference
    for name in names:
        print(name)
        data = load_data(name)
        
        out_data = simulate_interference(wave_data, data, dc) #only use i waves in the interference
        for d in range(3):
            out_data[1][d] = out_data[1][d] + add_sine_wave(out_data[0], 6, 5, random=False)
        outfile = name[:9] + "_interference.txt"
        save(out_data, outfile)
        file_names.append(name[:9]+ "_interference.txt")
        f = open("temp_interference_file_list.txt", "w")
        for i in range(len(file_names)):
            f.write(file_names[i] + "\n")
    
