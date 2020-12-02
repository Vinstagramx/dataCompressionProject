#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 11:43:59 2020

@author: ronan
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

def pretty_graph(x_label, y_label, title, fontsize): #formatting graphs
    figure = plt.gcf()  # Sets figure size
    figure.set_size_inches(18, 10)
    plt.xlabel(x_label,fontsize=fontsize)
    plt.title(title,fontsize=fontsize)
    plt.ylabel(y_label,fontsize=fontsize) 
    plt.tick_params(labelsize=fontsize)
    #plt.legend()
    #plt.grid()



delta_data = np.loadtxt("delta_comp_rats").reshape((28, 3))
d4_data = np.loadtxt("d4_random_output_all.txt").reshape((28, 3))
magnitudes = np.loadtxt("magnitudes.txt")
#pearson = scipy.stats.pearsonr(magnitudes, comp_rat_data[:, 2])
#print(pearson)
directions = "xyz"
d_colours = ["#00476e", "#0072b0", "#009aed"]
dd_colours = ["#5c0119", "#b0002e", "#fa0041"]

for i in range(3):
    plt.plot(magnitudes, delta_data[:,i],".", label = "Delta "+directions[i], color = d_colours[i])
    plt.plot(magnitudes, d4_data[:,i],".", label = "$\Delta-4$  "+directions[i], color = dd_colours[i])

plt.gca().set_facecolor("#fffcf5")
plt.legend(fontsize = 18)
pretty_graph("Magnitude of interference (nT)", "Compression ratio", "Compression ratio vs random interference for Delta and $\Delta$-4 encoding", 24)