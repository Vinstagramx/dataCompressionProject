# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 12:05:08 2020

@author: Ronan
"""
import numpy as np
import matplotlib.pyplot as plt

import time
import os

cwd = os.getcwd()
parent = os.path.dirname(cwd)
PATH = os.path.join(parent, 'bscproject', 'C1_160308.FS.FULLRES.txt')


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

def binary(decimal):
    """
    Might need to change this depending on how we're actually meant to reverse/
    send the data (i.e 16 bit/signed or unsigned etc). Right now going for 
    smallest binary representation but that may not be right. Length of this 
    string should be # of bits needed.
    """
    if decimal >= 0:
        sign_bit = 0
    else:
        sign_bit = 1
    bin_string = str(sign_bit) + bin(abs(decimal)).replace("0b", "") 
    return bin_string

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
            compressed.append(deltas) #edited for ease of use w/ bit_difference()
    compressed = np.ndarray.flatten(np.asarray(compressed))
    return compressed
            
def golomb_encoding(n,b):
    q = n//b
    r = n - q*b
    quot = ["1" for i in range(0,q)] + ["0"]
    return ("".join(quot), r)

def golomb(buffer_length, data_list, rice = False):
    buffer_regions = [i*buffer_length for i in range(0, len(data_list)//buffer_length)]
    unaries, binaries, remainders = [], [], []
    for buffer_start in buffer_regions:
        #print(buffer_start)
        data = data_list[buffer_start:(buffer_start+buffer_length)]
        b = int(np.mean(data))
        golombs = [golomb_encoding(i, b) for i in data]
        remainders.append([len(binary(i[1])) for i in golombs])
        unaries.append([len(i[0]) for i in golombs])
        binaries.append(len(binary(b)))
    compressed = np.concatenate((binaries, remainders, unaries), axis = None) 
    return compressed
    
def bit_difference(buffer_length, data, scheme):
    """
    Calculates 'size' of uncompressed data by getting length of binary
    representation, then encodes data and calculatees 'size' in similar manner.
    Obvs will need to add more schemes to this at some point.
    """
    incoming_bits = sum([len(binary(i)) for i in data])
    if scheme == "delta":
        compressed = delta_data(buffer_length, data)
        compressed_bits = sum([len(binary(i)) for i in compressed])
    elif scheme == "golomb":
        compressed = golomb(buffer_length, data)
        compressed_bits = sum(compressed)
    else:
        raise Exception("Please supply an encoding scheme")
    compression_ratio = (1 - compressed_bits/incoming_bits) *100
    #compression_ratio = incoming_bits/compressed_bits
    return compression_ratio

def vary_buffer_size(scheme, data, min_max = (1,100)):
    buffer_sizes = range(min_max[0], min_max[1])
    ratios = []
    for i in buffer_sizes:
        print(i)
        ratios.append(bit_difference(i, data, scheme))
    plt.plot(buffer_sizes, ratios)




"""
When using the fixed_data array:
fixed_data[0], [1], [2] = x,y,z magnetic field reading
"""

#use bin() function to get binary equivalent - then use len ti find out # of bits
#any reason deltas + golomb can't be used?
#need to implement binary/huffman encoding for remainder of golob
data = load_data(PATH)

#%%
fixed_data = fix_data(data)

#%%
start = time.time()
#print(bit_difference(50, fixed_data[0], "delta"))
print(bit_difference(10, fixed_data[0], "delta"))
end = time.time()

time_taken = end-start
print(f'Time taken for compression : {time_taken}s')

#data = load_data(DATA_PATH)
#fixed_data = fix_data(data)
#%%
#use bin() function to get binary equivalent - then use len ti find out # of bits
#any reason deltas + golomb can't be used?
#need to implement binary/huffman encoding for remainder of golob
start = time.time()
#print(bit_difference(50, fixed_data[0], "delta"))
print(bit_difference(100, fixed_data[0], "golomb"))
end = time.time()

time_taken = end-start
print(f'Time taken for compression : {time_taken}s')

#%%
vary_buffer_size("golomb", fixed_data[0], (1, 100))


#print(bit_difference(100, fixed_data[0], "golomb"))
#print(delta_data(100, fixed_data[0], squared=False)[-1])
#print(golomb(100, fixed_data[0])[:4])

#plt.plot(raw_data[0], raw_data[1], label = "x-data")
#plt.plot(raw_data[0], raw_data[2], label = "y-data")
#plt.plot(raw_data[0], raw_data[3], label = "z-data")

#plt.xlabel("Time")
#plt.ylabel("Magnetic field strength (nT)")
#plt.legend()