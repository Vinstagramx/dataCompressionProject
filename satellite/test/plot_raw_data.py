import numpy as np 
import matplotlib.pyplot as plt 
import os 

os.chdir(os.path.dirname(os.path.abspath(__file__)))
cwd = os.getcwd()
parent_dir = os.path.dirname(cwd)
cwd = os.path.dirname(cwd)
filename = 'C1_160313'
path = os.path.join(cwd, 'data', f'{filename}.FS.UNCAL.FULLRES')
#c1_160309

data = np.loadtxt(path).T

time = np.arange(0, len(data[0]), 1) * 0.14866719
fixed_x = data[1]; fixed_y = data[2]; fixed_z = data[3]
b_data = np.array([fixed_x, fixed_y, fixed_z], dtype = np.int32) 

def plot_settings():
    plt.clf()  # Clears any previous figures
    figure = plt.gcf()  # Sets figure size
    figure.set_size_inches(18, 10)
    plt.rc('axes', labelsize = 22, titlesize = 24) 
    plt.rc('xtick', labelsize = 18)   
    plt.rc('ytick', labelsize = 18)    
    plt.rc('legend', fontsize = 20)
    plt.grid()    

plot_settings()
plt.title(f"{filename} - Magnetic Field as a function of Time")
plt.xlabel("Time (s)")
plt.ylabel("Magnetic Field (nT)")
plt.plot(time, b_data[0], label = 'x')
#plt.plot(time, b_data[1], label = 'y')
#plt.plot(time, b_data[2], label = 'z')
plt.legend()


