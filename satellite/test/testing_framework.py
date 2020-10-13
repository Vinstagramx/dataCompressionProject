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

#%% 
data_path = "C:\\Users\\Ronan\\Documents\\github\\Physics2020\\satellite\\data"
csv = pd.read_csv("C:\\Users\\Ronan\\Documents\\github\\Physics2020\\satellite\\test\\stats.csv")
loop = 0; max_ratios = []; max_blocks = []

for filename in os.listdir(data_path):
    file_index = filename[:9]
    dirs = ["x", "y", "z"]
    for direction in dirs:
        ratios = []
        print(file_index, loop)
        for i in range(2, 3, 1):
            temp_encoder = Delta(data_path+"\\"+filename, i, 2, direction=direction)
            temp_encoder.encode_data(stats=False)
            ratios.append(temp_encoder.get_compression_ratio())
        max_ratio = max(ratios); block_size = ratios.index(max_ratio) + 2
        max_ratios.append(max_ratio)
        max_blocks.append(max_blocks)
        loop += 1
print(max_ratio)
print(max_blocks)
#%%
csv["Delta"] = max_ratios
csv["Block"] = max_blocks
csv.to_csv("stats_prime")
        
    
    
