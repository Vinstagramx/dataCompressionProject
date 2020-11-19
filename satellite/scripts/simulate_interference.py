# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 22:44:07 2020

@author: Ronan
"""
import numpy as np
import os
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(os.path.abspath(__file__)))
cwd = os.getcwd()
parent_dir = os.path.dirname(cwd)
cwd = os.path.dirname(cwd)

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

def simulate_interference(wave_data, data):
    # wave data of form [(period, offset, amplitude), ...]
    modified_data = []
    for direction in range(3):
        dir_data = data[direction]
        temp_data = dir_data
        time = np.array([i for i in range(len(dir_data))])*time_interval
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


#plt.plot(mod[0], mod[1][0])
#data = load_data(DATAPATH)
#mod = simulate_interference([(100,0,5), data])
#plt.plot(mod[0], data[0])

#%%
file_list = open("file_list.txt", "r").readlines()
#print(file_list)
edited_file_list = [i[4:29].strip("/") for i in file_list]
print(edited_file_list)

for file in edited_file_list:
    #datafile = 'C4_160313.FS.FULLRES.txt'

    DATA_PATH = os.path.join(cwd, 'data', file)
    OUTFILE = file[:9]+"_modified.txt"
    print(OUTFILE)
    data = load_data(DATA_PATH)
    mod = simulate_interference([(1,0,5)], data)
    save(mod, OUTFILE)
    


        
