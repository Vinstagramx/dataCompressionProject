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
stats_file = os.path.join(cwd, 'test','stats.csv')
#%% 
data_path = data_folder
csv = pd.read_csv(stats_file)
loop = 0; max_ratios = []; max_blocks = []
files = os.listdir(data_path)

for filename in files[:6]:
    file_index = filename[:9]
    dirs = ["x", "y", "z"]
    file_path = os.path.join(data_path, filename)
    for direction in dirs:
        ratios = []
        print(file_index, loop)
        for i in range(2, 100 , 1):
            temp_encoder = Delta(file_path, i, "all", direction=direction)
            temp_encoder.encode_data(stats=False)
            ratios.append(temp_encoder.get_compression_ratio())
        max_ratio = max(ratios); block_size = ratios.index(max_ratio) + 2
        print(max_ratio)
        max_ratios.append(max_ratio)
        max_blocks.append(block_size)
        loop+=1
#%%
np.save("max_ratios_to_18", max_ratios)
np.save("max_blocks_to_18", max_blocks)
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
csv.to_csv("stats_prime.csv")

