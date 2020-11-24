#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 16:55:16 2020

@author: ronan
"""
import sys
import numpy as np
import matplotlib.pyplot as plt

def pretty_graph(x_label, y_label, title, fontsize): #formatting graphs
    plt.xlabel(x_label,fontsize=fontsize)
    plt.title(title,fontsize=fontsize)
    plt.ylabel(y_label,fontsize=fontsize) 
    plt.tick_params(labelsize=fontsize)
    plt.legend()

if __name__ == "__main__":
    with open(sys.argv[1]) as f: #pass in file name as argument, as always argv[0] is program name
        lines = [float(line.rstrip()) for line in f] #strip newline, convert to float
    labels = "xyz"
    markers = ["^", ".", "s"]
    x = []; y = []; z = [];
    data = [x,y,z]
    for i in range(0, len(lines)):
        data[i%3].append(lines[i])
    wave_no = [i for i in range(1, len(data[0])+1)]
    for i in range(3):
        plt.plot(wave_no, data[i], label=labels[i], marker=markers[i], \
                 ms=20,ls="-",  lw=4)
    pretty_graph("Number of waves", "Compression ratio (%)", \
                 "Compression ratio of Delta encoding as a function of interference", 24)
    plt.legend(fontsize=20)
    plt.gca().set_facecolor("#fffcf5")
