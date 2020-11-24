#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 16:55:16 2020

@author: ronan
"""
import sys
import matplotlib.pyplot as plt

def pretty_graph(x_label, y_label, title, fontsize): #formatting graphs
    figure = plt.gcf()  # Sets figure size
    figure.set_size_inches(18, 10)
    plt.xlabel(x_label,fontsize=fontsize)
    plt.title(title,fontsize=fontsize)
    plt.ylabel(y_label,fontsize=fontsize) 
    plt.tick_params(labelsize=fontsize)
    plt.legend()
    plt.grid()

#data seems to go 2,4,0,6,1,3,5=7,5

#if __name__ == "__main__":
def main(file):
    with open(file) as f: #pass in file name as argument, as always argv[0] is program name
        lines = [float(line.rstrip()) for line in f] #strip newline, convert to float
    labels = "xyz"
    markers = ["^", ".", "s"]
    x = []; y = []; z = [];
    data = [x,y,z]
    for i in range(0, len(lines)):
        data[i%3].append(lines[i])
    wave_no = [i for i in range(0, len(data[0]))]
    for i in range(3):
        plt.plot(wave_no, data[i], label=labels[i], marker=markers[i], \
                 ms=20,ls="-",  lw=4)
    pretty_graph("Number of waves", "Compression ratio (%)", \
                 "Compression ratio of Delta encoding as a function of interference", 24)
    plt.legend(fontsize=20)
    plt.gca().set_facecolor("#fffcf5")
    plt.savefig("compression_vs_waves")

main("temp_compression_data.txt")
