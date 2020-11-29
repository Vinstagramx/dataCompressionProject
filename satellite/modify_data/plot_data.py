# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 16:57:14 2020

@author: Ronan
"""
import numpy as np
import matplotlib.pyplot as plt

def load_data(path):
    data = np.loadtxt(path).T
    fixed_x = [x for x in data[1]]; fixed_y = [y for y in data[2]]; fixed_z = [z for z in data[3]]
    fixed_array = np.array([fixed_x, fixed_y, fixed_z], dtype = np.float) #does this round down or nearest - if we can't reconstruct data look at this 
    return fixed_array

def pretty_graph(x_label, y_label, title, fontsize): #formatting graphs
    figure = plt.gcf()  # Sets figure size
    figure.set_size_inches(18, 10)
    plt.xlabel(x_label,fontsize=fontsize)
    plt.title(title,fontsize=fontsize)
    plt.ylabel(y_label,fontsize=fontsize) 
    plt.tick_params(labelsize=fontsize)
    plt.legend()
    plt.grid()

data = load_data("C1_160309_cavity.txt")
time = np.array([i for i in range(len(data[1]))])*0.14866719

#plt.plot(time[:1000], data[0][:1000])
#plt.plot(time[:1000], sin_wave)

high_res = np.linspace(time[1], time[3], 1000)
sin_wave = 5*np.sin(2*np.pi*27*high_res)
sin_wave2 = 5*np.sin(2*np.pi*10*high_res)

plt.plot(time[1], data[0][1], "x", color="red", ms = 15)
plt.plot(time[2], data[0][2], "x", color="red", ms = 15)
plt.plot(time[3], data[0][3], "x", color="red", ms = 15)
plt.plot(high_res, sin_wave, label = "freq = 27")
plt.plot(high_res, sin_wave2, label = "freq = 10")

pretty_graph("Time", "Magnetic field (nT)", "Plot of magnetic field of cavity data with sinusoidal interference", fontsize=24)
plt.legend(fontsize = 24)
