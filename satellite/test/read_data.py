# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 12:05:08 2020

@author: Ronan
"""
import pandas
import numpy as np
import matplotlib.pyplot as plt


DATA_PATH = "C:\\Users\\Ronan\\Documents\\uni_work\\physics\\third year\\project\\data\\test_data\\C1_160308.txt"

def load_data(path):
    raw_data = np.loadtxt(path).T #724662 entries
    return raw_data

def fix_data(data):
    """
    Convert all the floats to ints and store in an np array. If possible try
    and make the arrays 16 bit ints as they were originally.
    """
    fixed_x = data[1] * 10000
    fixed_y = data[2] * 10000
    fixed_z = data[3] * 10000
    fixed_array = np.array([fixed_x, fixed_y, fixed_z], dtype = np.int32)
    return fixed_array

def delta_encoding(data):
    ref_point = data[0]
    compressed = [(i- ref_point) for i in data[1:]]
    return [ref_point] + compressed

def delta_data(buffer_length, data_list, squared = False):
    buffer_regions = [i*buffer_length for i in range(0, len(data_list)//buffer_length)]
    compressed = []
    for buffer_start in buffer_regions:
        deltas = delta_encoding(data_list[buffer_start:(buffer_start+buffer_length)])
        if squared == True: #delta squared encoding, doesn't seem to be too useful for our data
            delta_squared = delta_encoding(deltas[1:])
            compressed.append(delta_squared)
        else:
            compressed.append(deltas)
    return compressed
            
def golomb_encoding(n,b):
    q = n//b
    r = n - q*b
    quot = ["1" for i in range(0,q)] + ["0"]
    return ("".join(quot), r)

def golomb(buffer_length, data_list, rice = False):
    buffer_regions = [i*buffer_length for i in range(0, len(data_list)//buffer_length)]
    compressed = []
    for buffer_start in buffer_regions:
        data = data_list[buffer_start:(buffer_start+buffer_length)]
        b = int(np.mean(data))
        golombs = [golomb_encoding(i, b) for i in data]
        remainders = [bin(i[1]) for i in golombs]
        unaries = [i[0] for i in golombs]
        compressed.append([(unaries[i], remainders[i]) for i in range(0, buffer_length)])
    return compressed
    
       

#use bin() function to get binary equivalent - then use len ti find out # of bits
#any reason deltas + golomb can't be used?
#need to implement binary/huffman encoding for remainder of golob
data = load_data(DATA_PATH)
fixed_data = fix_data(data)
#print(delta_data(100, fixed_data[0], squared=False)[-1])
print(golomb(100, fixed_data[0])[:4])

#plt.plot(raw_data[0], raw_data[1], label = "x-data")
#plt.plot(raw_data[0], raw_data[2], label = "y-data")
#plt.plot(raw_data[0], raw_data[3], label = "z-data")

#plt.xlabel("Time")
#plt.ylabel("Magnetic field strength (nT)")
#plt.legend()