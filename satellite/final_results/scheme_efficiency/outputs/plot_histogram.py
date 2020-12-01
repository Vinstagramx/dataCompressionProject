# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 16:04:17 2020

@author: Ronan
"""
import numpy as np
import matplotlib.pyplot as plt

def load_files():
    names = []; cavity_indices = []
    with open("comp_rat_file_list.txt") as f:
        data = f.readlines()#.split(" ")
        for i in data:
            n =  i
            names.append(n.strip("\n")+".txt")
    return names

def pretty_graph(x_label, y_label, title, fontsize): #formatting graphs
    figure = plt.gcf()  # Sets figure size
    figure.set_size_inches(18, 10)
    plt.xlabel(x_label,fontsize=fontsize)
    plt.title(title,fontsize=fontsize)
    plt.ylabel(y_label,fontsize=fontsize) 
    plt.tick_params(labelsize=fontsize)
    plt.legend()
    #plt.grid()

def main():
    files_to_load = load_files()
    compression_ratios = []
    for file in files_to_load:
        ratios = np.loadtxt(file)
        avg = np.mean(ratios)
        compression_ratios.append(avg)
    labels = ['$\Delta$', '$\Delta$ squared', '$\Delta$ G max', '$\Delta$ G mean', \
              '$\Delta$ G min', "G max", 'G mean', 'G min',\
                  'Step $\Delta$']
    plt.bar(labels, compression_ratios)
    pretty_graph("Encoder Type", "Average Compression ratio (%)", "Average Compression ratios of all directions and files for different encoding types", 20)
    #plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    
main()