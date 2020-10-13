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
"""
Vinnie path
"""
cwd = os.getcwd()
data_folder = os.path.join(cwd, 'data')
stats_file = os.path.join(cwd, 'test','stats.csv')
#%%
"""
Ronan path
"""
# cwd = os.getcwd()
# cwd = os.path.dirname(cwd)
# data_folder = os.path.join(cwd, 'data')
# stats_file = os.path.join(cwd, 'test','stats.csv')
#%%
'''
Vinnie path length split
'''
filenames = []
path_list = []


#%% 
data_path = data_folder
csv = pd.read_csv(stats_file)
loop = 0; max_ratios = []; max_blocks = []
files = os.listdir(data_path)

for file in os.listdir(data_path):
    if file.endswith(".txt"):
        filenames.append(file.split('.')[0])
        path_list.append(os.path.join(data_folder, file))
filenames_1 = filenames[:len(filenames)//2]
filenames_2 = filenames[len(filenames)//2:]

path_list_1 = path_list[:len(path_list)//2]
path_list_2 = path_list[len(path_list)//2:]

for index, filename in enumerate(path_list_2):
    dirs = ["x", "y", "z"]
    file_path = filename
    print(filenames_2[index])
    for direction in dirs:
        ratios = []
        for i in range(2, 100, 1):
            temp_encoder = Delta(file_path, i, "all", direction=direction)
            temp_encoder.encode_data(stats=False)
            ratios.append(temp_encoder.get_compression_ratio())
        max_ratio = max(ratios); block_size = ratios.index(max_ratio) + 2
        print(max_ratio)
        max_ratios.append(max_ratio)
        max_blocks.append(block_size)
        loop+=1
        print(loop)
#%%
d = {'Max Compression Ratio (Delta)' : max_ratios, 'Block Size (Delta)': max_blocks}
df = pd.DataFrame(data=d)
df.to_csv('delta_compression_stats.csv')
# np.save("max_ratios_to_18", max_ratios)
# np.save("max_blocks_to_18", max_blocks)
#csv["Delta"] = max_ratios
#csv["Block"] = max_blocks
#csv.to_csv("stats_prime.csv")

    
    
