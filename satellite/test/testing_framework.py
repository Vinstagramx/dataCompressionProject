# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 10:42:19 2020

@author: Ronan
"""
#%% DEPENDENCIES
import matplotlib.pyplot as plt
from encoder import Delta, Golomb
import numpy as np
import os
import pandas as pd

cwd = os.getcwd()
cwd = os.path.dirname(cwd)
data_folder = os.path.join(cwd, 'data')
stats_file = os.path.join(cwd, 'test','stats_prime.csv')
#%% 
data_path = data_folder
csv = pd.read_csv(stats_file)

files = os.listdir(data_path)
#%%
means = []; stds = []
for filename in files:
    file_path = os.path.join(data_path, filename)
    dirs = ["x", "y", "z"]
    for direction in dirs:
        temp_encoder = Delta(file_path, 100, "all", direction = direction)
        mean = np.mean(temp_encoder._current_data)
        means.append(mean)
#%%
csv["Means"] = [i/10000 for i in means]
print(csv)


#%%
def check_for_max(ratios_list):
    max_ratio = max(ratios_list)
    for i in ratios_list[-10:] :
        if i >= max_ratio :
            return False
    if ratios_list[-1] < ratios_list[-2] and ratios_list[-2] < ratios_list[-3]:
        return True
    else:
        return False
        
def master_testing(encoder, indexes, arg_list):
    """
    Takes encoder (so pass Delta or Golomb into it), split: (start, end) and arg_list which should be list of format 
    [sample_size, bits, mode, any other valid optional arguments]
    """
    loop = 0; max_ratios = []; max_blocks = []
    for filename in files[indexes[0]:indexes[1]]:
        file_index = filename[:9]
        dirs = ["x", "y", "z"]
        file_path = os.path.join(data_path, filename)
        for direction in dirs:
            ratios = []
            print(file_index, loop)
            for i in range(2, 100 , 1):
                to_unpack = [file_path, i] + [arg_list[0]] + [direction] + arg_list[1:]
                temp_encoder = encoder(*to_unpack)
                temp_encoder.encode_data(stats=False)
                ratios.append(temp_encoder.get_spacesaving_ratio())
                if i > 10:
                    check = check_for_max(ratios)
                    if check:
                        print("Local max found, exiting")
                        break
            max_ratio = max(ratios); block_size = ratios.index(max_ratio) + 2
            print(max_ratio)
            max_ratios.append(max_ratio)
            max_blocks.append(block_size)
            loop+=1
    return (max_ratios, max_blocks)

#%%
max_ratios = []; max_blocks = []
for b in ["min", "max", "mean"]:
    temp = master_testing(Golomb, [0,6], [7000, 14, b])
    max_ratios.append(temp[0])
    max_blocks.append(temp[1])

np.save("max_golomb_ratios_to_18_b", max_ratios)
np.save("max_golomb_blocks_to_18_b", max_blocks)
#csv["Delta"] = max_ratios
#csv["Block"] = max_blocks
#csv.to_csv("stats_prime.csv")
#%%
up_to_18_ratios = list(np.load("max_ratios_to_18.npy"))
up_to_18_blocks = list(np.load("max_blocks_to_18.npy"))
from_19_csv = pd.read_csv("delta_compression_stats.csv")
from_19_ratios = list(from_19_csv["Max Compression Ratio (Delta)"])
from_19_blocks = list(from_19_csv["Block Size (Delta)"])
ratio_data = up_to_18_ratios + from_19_ratios
block_data = up_to_18_blocks + from_19_blocks

csv["Delta"] = ratio_data
csv["Block"] = block_data
#%%
csv.to_csv("stats_prime.csv")

