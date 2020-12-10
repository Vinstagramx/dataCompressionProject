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
    #plt.title(title,fontsize=fontsize)
    plt.ylabel(y_label,fontsize=fontsize) 
    plt.tick_params(labelsize=fontsize)
    #plt.legend()
    plt.grid()
    
    
def expo_decay(b):
    cavity_data=[]
    times = np.array([i*0.14866719 for i in range(1017)])
    cavity_data = b*np.exp(-1*times) #turns out this is independent of sign of b
    cavity_data = [round(i,2) for i in cavity_data]
    return (times, cavity_data)

data = load_data("C1_160309.FS.UNCAL.FULLRES")
time = np.array([i for i in range(len(data[1]))])*0.14866719


plt.plot(time, data[0], lw=3)
#%%
plt.vlines(580000*0.14866719, ymin=-300, ymax=300, linestyle="--", lw=3, color="red")
plt.text(601000*0.14866719, 110, "Earth's dipole", fontsize =24, color="red")

plt.text(39000, 110, "Magnetosheath", fontsize =24, color="#fc8200")

plt.text(200, 110, "Solar Wind", fontsize =24, color="#fcbd00")
plt.vlines(27300, ymin=-300, ymax=300, linestyle="--", lw=3, color="#fcbd00")
#plt.plot(time[:1000], sin_wave)

#high_res = np.linspace(time[1], time[3], 1000)
#sin_wave = 5*np.sin(2*np.pi*27*time)
#sin_wave2 = 5*np.sin(2*np.pi*28*time)

#plt.plot(time, data[0][1], "x", color="red", ms = 15)
#plt.plot(time, data[0][2], "x", color="red", ms = 15)
#plt.plot(time, data[0], "x", color="red", ms = 15)
#plt.plot(time[:1000], (sin_wave)[:1000], label = "freq = 27")
#plt.plot(time[:1000], (sin_wave2)[:1000], label = "freq = 28")

pretty_graph("Time", "Magnetic field (nT)", "Plot of magnetic field vs time with cutoff drawn at end of magnetosheath", fontsize=24)
plt.legend(fontsize = 24)
plt.gca().set_facecolor("#fffcf5")

dir_data = data[0][:580000]
cavity_data = expo_decay(dir_data[-1])
print(cavity_data)

ax  = plt.gca()
#x percent across, y percent up, x,y percent size
axins = ax.inset_axes([0.5, 0.06, 0.31, 0.31]) 
#plot the lines on the inset graph

axins.plot(time, data[0], label="Cluster data", lw=3)
axins.plot(cavity_data[0]+580000*0.14866719, cavity_data[1], lw=3, label="Simulated cavity")

#set the limits of the inset graph
x1, x2, y1, y2 = 580000*0.14866719, 580100*0.14866719, -40, 5
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.tick_params(labelsize=20)
axins.set_facecolor("#fffcf5")
#call function to plot inset on current graph 
ax.indicate_inset_zoom(axins)
axins.legend(fontsize=20)


