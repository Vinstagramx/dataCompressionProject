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
    plt.title(f"Space Saving Ratio vs Block (buffer) size - {filename}", fontsize = 24)
    plt.ylabel("Space Saving Ratio (%)", fontsize = 22)
    plt.xlabel("Block size", fontsize = 22)
    
    
def pretty_graph(x_label, y_label, title, fontsize): #formatting graphs
    plt.xlabel(x_label,fontsize=fontsize)
    plt.title(title,fontsize=fontsize)
    plt.ylabel(y_label,fontsize=fontsize) 
    plt.tick_params(labelsize=fontsize)
    plt.legend()

#%%
# raise Exception("oops")
#%%
# dx = Delta(DATA_PATH, 20, 'all', direction="x")
# dx = Delta(DATA_PATH, 20, 'all', direction="x")
# dz = Delta(DATA_PATH, 20, 'all', direction="x")

#%%
#time_interval = 0.14866719 #time interval between every reading (in seconds) - FIXED
#raw_data = d._data
#dirs = ["x-direction", "y-direction", "z-direction"]
#stds = []; means = []
#for index, i  in enumerate(raw_data):
#    std = np.std(i); mean = np.mean(i)
#    print(dirs[index], " standard dev is: ", std, " mean is:", mean)
#    stds.append(std)
#    means.append(mean)
#    
#    


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
    xratios.append(xtemp_encoder.get_spacesaving_ratio())
    yratios.append(ytemp_encoder.get_spacesaving_ratio())
    zratios.append(ztemp_encoder.get_spacesaving_ratio())
#%%
# plt.figure("Compression ratios")
plt.plot(range(2, maxblocksize, step), xratios, label = 'x-direction')
plt.plot(range(2, maxblocksize, step), yratios, label = 'y-direction')
plt.plot(range(2, maxblocksize, step), zratios, label = 'z-direction')
plot_settings(None, filename)
plt.savefig(f'{plot_path}/spacesaving_ratio_xyz_{maxblocksize}_{filename}.png', dpi = 200)

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
#%%
stats_data = pd.read_csv("stats_prime.csv")
#%%
compression_data = stats_data["Max Compression Ratio (Delta)"] #Max Compression Ratio
x_data = []; y_data = []; z_data = []; data = [x_data, y_data, z_data]
for i in range(len(compression_data)):
    data[(i)%3].append(compression_data[i])

#%% HIST OF MAX COMPRESSION RATIOS
print("whole data: ", compression_data)
print("x data: ", x_data)
plt.figure("Distribution of maximum compression ratios over datasets")
n, bins, patches = plt.hist(data, 20, stacked=True) #12 seems cool
plt.gca().set_facecolor("#fffcf5")
pretty_graph("Maximum Compression Ratio (%)", "", "Distribution of Maximum Compression Ratio over datasets", 20)
plt.legend(["x", "y", "z"], fontsize = 18)
#%% MEAN VS MAX COMPRESSION
mean_data = stats_data["Means"]
x_means = []; y_means = []; z_means = []; mean_datas = [x_means, y_means, z_means]
for i in range(len(mean_data)):
    mean_datas[(i)%3].append(mean_data[i])

colours = ["C0", "C1", "C2"]
for i in range(3):
    plt.scatter(mean_datas[i], data[i], color = colours[i])

plt.gca().set_facecolor("#fffcf5")
pretty_graph("Mean of raw data (nT)", "Maximum Compression Ratio", "Maximum compression ratio vs mean of raw data", 20)
plt.legend(["x", "y", "z"], fontsize = 18)
#%% STD VS MAX COMPRESSION
std_data = stats_data["Standard Deviation (nT)"]
x_std_data = []; y_std_data = []; z_std_data = []; std_datas = [x_std_data, y_std_data, z_std_data]
for i in range(len(mean_data)):
    std_datas[(i)%3].append(std_data[i])

colours = ["C0", "C1", "C2"]
for i in range(3):
    plt.scatter(std_datas[i], data[i], color = colours[i])

plt.gca().set_facecolor("#fffcf5")
pretty_graph("Standard Deviation of raw data (nT)", "Maximum Compression Ratio", "Maximum compression ratio vs standard deviation of raw data", 20)
plt.legend(["x", "y", "z"], fontsize = 18)
#%% GOLOMB PLOTTING
colours = ["C0", "C1", "C2"]; ratios = []
plt.figure("Golomb b parameter efficiencies in z direction")
for index, mode in enumerate(["min", "max", "mean"]):
    ratios = []; buffer_sizes = range(2,70)
    for i in buffer_sizes:
        temp_encoder = Golomb(DATA_PATH, i, 1000, direction="z", mode=mode)
        temp_encoder.encode_data(stats=False)
        ratio = temp_encoder.get_spacesaving_ratio()
        ratios.append(ratio)
        print(i, ", ", ratio)
    plt.plot(buffer_sizes, ratios, color=colours[index], label ="b: "+ mode)
plt.legend(fontsize=20)
pretty_graph("Block Size", "Compression Ratio", "Compression ratio as function of Block size for different b in z-dir - C3_160313", 20)
plt.gca().set_facecolor("#fffcf5")
       
#%%PLOTTING SAMPLE SIZE VS ALL
ratios = []
sample_sizes = [10,30, 50, 80, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3500, 4000, 4500, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000]
full_encoder = Delta(DATA_PATH, 25, "all", direction="y")
full_encoder.encode_data(stats=False)
for i in sample_sizes:
    print(i)
    temp_encoder = Delta(DATA_PATH, 25, i, direction = "y")
    temp_encoder.encode_data(stats=False)
    ratio = temp_encoder.get_spacesaving_ratio()
    ratios.append(ratio)
#%% diff @100 = -0.2%, @1000 = 0.046%, @10000 = 0.027%
adj_rat = [i - full_encoder.get_spacesaving_ratio() for i in ratios ]
plt.plot(sample_sizes, adj_rat)
#plt.hlines(full_encoder.get_spacesaving_ratio(), 10, 15000, label = "All samples", color="red")
pretty_graph("Sample Size", "Difference in Compression Ratio from all", "Difference from compression ratio from using all samples in y-dir - C3_160313", 20)
plt.gca().set_facecolor("#fffcf5")
plt.legend(fontsize=18)