# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 18:24:44 2020

@author: Ronan
"""

import numpy as np
import matplotlib.pyplot as plt
from read_data import vary_buffer_size, get_fixed_data

def pretty_graph(x_label, y_label, title, fontsize): #formatting graphs
    plt.xlabel(x_label,fontsize=fontsize)
    plt.title(title,fontsize=fontsize)
    plt.ylabel(y_label,fontsize=fontsize) 
    plt.tick_params(labelsize=fontsize)

fixed_data = get_fixed_data()
title = ["x", "y", "z"]
fig = plt.gcf()
fig.set_size_inches(18,12)
for index, i in enumerate(fixed_data):
    delta_data = vary_buffer_size("delta", i, (1,100))
    plt.plot(delta_data[0], delta_data[1], marker = "x", ms =10, ls = "-", lw = 3)
    pretty_graph("Buffer size", "Compression ratio (%)", "Delta compression ratio in "+ title[index] +" direction", 20)
    #plt.gca().set_aspect("auto")
    plt.savefig("plots\\comprat_blocksize_delta_"+title[index]+".png", dpi= "figure")
    plt.clf()
    golomb_data = vary_buffer_size("golomb", i, (1,100))
    plt.plot(golomb_data[0], golomb_data[1], marker = "x", ms =10, ls = "-", lw = 3)
    pretty_graph("Buffer size", "Compression ratio (%)", "Golomb compression ratio in "+ title[index] +" direction", 20)
    plt.savefig("plots\\comprat_blocksize_golomb_"+title[index]+".png")
    plt.clf()
    