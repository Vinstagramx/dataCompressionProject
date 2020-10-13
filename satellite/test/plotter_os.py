"""
Created on Tue Oct  6 16:39:32 2020

@author: Ronan
Altered to use os package and to work with current working directories.
"""

import os
import matplotlib.pyplot as plt
from encoder import Delta, Golomb
import numpy as np
import pandas as pd

cwd = os.getcwd()

'''
Working with a singular file
'''

parent_dir = os.path.dirname(cwd)
datafile = 'C3_160313.FS.FULLRES.txt'
DATA_PATH = os.path.join(cwd, 'data', datafile)
plot_path = os.path.join(cwd, 'test', 'plots')
plt.clf()
figure = plt.gcf()  # get current figure
figure.set_size_inches(18, 10)

filename = datafile.split('.')[0]

def plot_settings(datalength, filename):
    plt.legend()
    if datalength != 0:
        plt.xlim(0, datalength)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.title(f"Compression ratio vs Block (buffer) size - {filename}", fontsize = 24)
    plt.ylabel("Compression Ratio (%)", fontsize = 22)
    plt.xlabel("Block size", fontsize = 22)

#%%
# dx = Delta(DATA_PATH, 20, 'all', direction="x")
# dx = Delta(DATA_PATH, 20, 'all', direction="x")
# dz = Delta(DATA_PATH, 20, 'all', direction="x")

#%%
# time_interval = 0.14866719 #time interval between every reading (in seconds) - FIXED
# raw_data = d._data
# dirs = ["x-direction", "y-direction", "z-direction"]
# for index, i  in enumerate(raw_data):
#     std = np.std(i)
#     print(dirs[index], " standard dev is: ", std)
#     timeseries = np.asarray(range(len(i))) * time_interval
#     maxval = max(timeseries)
#     plt.plot(timeseries, i, label = dirs[index])

# plot_settings(maxval, filename)   
# plt.savefig(f'{plot_path}/raw_data_{filename}.png', dpi = 200)
# plt.show() 

#%%
# dx.encode_data()
# dy.encode_data()
# dz.encode_data()
#%%
xratios, yratios, zratios = [], [], []
maxblocksize = 200
step = 2
for i in range(2, 200, 2):
    print(i)
    xtemp_encoder = Delta(DATA_PATH, i, 'all', direction="x")
    xtemp_encoder.encode_data(stats=False)
    ytemp_encoder = Delta(DATA_PATH, i, 'all', direction="y")
    ytemp_encoder.encode_data(stats=False)
    ztemp_encoder = Delta(DATA_PATH, i, 'all', direction="z")
    ztemp_encoder.encode_data(stats=False)
    xratios.append(xtemp_encoder.get_compression_ratio())
    yratios.append(ytemp_encoder.get_compression_ratio())
    zratios.append(ztemp_encoder.get_compression_ratio())
#%%
# plt.figure("Compression ratios")
plt.plot(range(2, maxblocksize, step), xratios, label = 'x-direction')
plt.plot(range(2, maxblocksize, step), yratios, label = 'y-direction')
plt.plot(range(2, maxblocksize, step), zratios, label = 'z-direction')
plot_settings(None, filename)
plt.savefig(f'{plot_path}/compression_ratio_xyz_{maxblocksize}_{filename}.png', dpi = 200)

# """
# Code to print raw data for multiple files
# """
# data_folder = os.path.join(cwd, 'data')
# path_list = []
# filenames = []
# for file in os.listdir(data_folder):
#     if file.endswith(".txt"):
#         filenames.append(file.split('.')[0])
#         path_list.append(os.path.join(data_folder, file))

# file_dir_list = []
# std_list = []
# rawdata_plotpath = os.path.join(plot_path, 'raw_data')
# csv_path = os.path.join(cwd, 'test')
# for ind, path in enumerate(path_list):
#     d = Delta(path, 20, 1000, direction="x")
#     time_interval = 0.14866719 #time interval between every reading (in seconds) - FIXED
#     raw_data = d._data
#     dirs = ["x-direction", "y-direction", "z-direction"]
#     coord = ['x', 'y', 'z']
#     for index, i  in enumerate(raw_data):
#         i = i / 10000
#         std = np.std(i)
#         print(f"{dirs[index]} standard dev is: {std}nT")
#         timeseries = np.asarray(range(len(i))) * time_interval
#         maxval = max(timeseries)
#         file_dir_list.append(f'{filenames[ind]} {coord[index]}')
#         std_list.append(std)
#         # plt.plot(timeseries, i, label = dirs[index])

#     # plot_settings(maxval, filenames[ind])   
#     # plt.savefig(f'{rawdata_plotpath}/raw_data_{filenames[ind]}.png', dpi = 200)
#     # plt.show() 
#     # plt.clf()
# g = {'File and Direction': file_dir_list, 'Standard Deviation (nT)': std_list}
# df = pd.DataFrame(data = g)
# df.to_csv(f'{csv_path}/stats.csv')
# print(path_list)