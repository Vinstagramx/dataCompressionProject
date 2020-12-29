# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 11:44:38 2020

@author: Ronan
"""
import numpy as np

def load_data(path):
    data = np.loadtxt(path).T
    fixed_x = [x for x in data[1]]; fixed_y = [y for y in data[2]]; fixed_z = [z for z in data[3]]
    fixed_array = np.array([fixed_x, fixed_y, fixed_z], dtype = np.float) #does this round down or nearest - if we can't reconstruct data look at this 
    return fixed_array

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
            names.append(temp[0]+".FS.UNCAL.FULLRES")
            cavity_indices.append(int(temp[1].strip("\n")))
    return (names, cavity_indices)

def expo_decay(b):
    cavity_data=[]
    times = np.array([i*(1/22) for i in range(2640)])
    cavity_data = b*np.exp(-1*times) #turns out this is independent of sign of b
    cavity_data = [round(i,2) for i in cavity_data]
    return cavity_data

def main():
    file_data = load_files()
    names = file_data[0]
    cavity_indices = file_data[1]
    print(cavity_indices)
    for n in range(0,len(names)):
        data = load_data(names[n])
        print(names[n])
        out_data = [[],[]]
        for direction in range(3):
            dir_data = data[direction][:cavity_indices[n]]
            cavity_data = expo_decay(dir_data[-1])
            out_dir = np.concatenate((dir_data, cavity_data))
            print(out_dir)
            out_data[1].append(out_dir)
        
        time = np.array([i for i in range(len(out_data[1][1]))])*(1/22)
        out_data[0] = time
        print(out_data)
        save(out_data, names[n][:9]+"_cavity.txt")

main()
        