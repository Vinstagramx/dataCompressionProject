# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 16:39:32 2020

@author: Ronan
"""

import matplotlib.pyplot as plt
from encoder import Delta, Golomb

DATA_PATH = "C:\\Users\\Ronan\\Documents\\uni_work\\physics\\third year\\project\\data\\test_data\\C1_160308.txt"

d = Delta(DATA_PATH, 9, 100)

#%%
d.encode_data()