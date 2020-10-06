# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 17:55:18 2020

@author: Ronan
"""
import numpy as np
import random 

class Encoder(object):
    def __init__(self, PATH, block_size=10, samples="all", direction ="x"):
        self._block_size = block_size
        self._new_data =[]
        self._data = self.load_data(PATH)
        directions = ["x", "y", "z"]
        self._current_data = self._data[directions.index(direction)]  #filter to x,y,z only
        self._block_regions = self.gen_samples(samples)
       
    def load_data(self, path):
        data = np.loadtxt(path).T
        fixed_x = data[1] * 10000; fixed_y = data[2] * 10000; fixed_z = data[3] * 10000
        fixed_array = np.array([fixed_x, fixed_y, fixed_z], dtype = np.int32)
        return fixed_array
    
    def gen_samples(self, samples, seed=1):
        """
        Get list of starts of blocks from block_siz and data length, then choose samples randomly with a given seed.
        Returns list of indices that are starts of blocks.
        """
        random.seed(a=seed)
        block_regions = [i*self._block_size for i in range(0, len(self._current_data)//self._block_size)]
        if samples == "all": #get every index that represents start of a block
            chosen_indices = block_regions
        else:
            chosen_indices = random.sample(block_regions, samples)
        return chosen_indices

    def binary(self, decimal):
        if decimal >= 0:
            sign_bit = 0
        else:
            sign_bit = 1
        bin_string = str(sign_bit) + bin(abs(decimal)).replace("0b", "") 
        return bin_string
    
    def encode(self, block): #generic method to be overwritten by golomb and delta and others
        return block
    
    def get_block_bit_lengths(self, block):
        """
        Returns list of the bit length of binary/unary whatever is in the block.
        """
        block_bit_lengths = [len(self.binary(i)) for i in block] if type(block[0]) != np.str_ else [len(i) for i in block]
        return block_bit_lengths
    
    def truncate(self, data_block, lengths_block):
        """
        Takes a block of data and a block of lengths of bits in the data block,
        makes every int the same length as the longest int in the block. Keeps
        the data and has a 1 at the end if it's a negative.
        """
        biggest_int = max(lengths_block); trunc_block = []
        for data in data_block:
            length = len(self.binary(data))
            if length < biggest_int:
                if data[-1] == "1":
                    trunc_block.append("1"+"0"*(biggest_int-(length+1)) + data)
                else:
                    trunc_block.append("0"*(biggest_int-length) + data)
            else:
                trunc_block.append(data)
        return trunc_block
                
    def encode_data(self):
        """
        High level function meant to represent a generic encoding process so 
        stuff like stats and plots can be easily created. Will require that 
        specific encoding schemes have consistent outputs though. Ideally a block
        based scheme will allow us to do things like strings for binary so long 
        as we don't try to save the whole list of blocks of strings.
        """
        block_regions = self._block_regions
        for block_start in block_regions:
            block = self._current_data[block_start:(block_start+self._block_size)]
            encoded_block = self.encode(block)[1] #encode(block)[0] is the codeword, [1] the data encoded by codeword
            print(encoded_block)
            lengths = self.get_block_bit_lengths(encoded_block)
            #do some stats on encoded block in here
            #trunc_block = self.truncate(encoded_block, lengths)
            biggest_int = max(lengths)
            print(biggest_int)
            #compressed.append(encoded_block)
        return self._new_data
    
class Delta(Encoder):
    """
    Inherited class of Encoder with delta encoding implementation overriding
    encode().
    """      
    def encode(self, block):
        ref_point = block[0]
        compressed = [(i- ref_point) for i in block[1:]]
        return (ref_point, compressed)

class Golomb(Encoder):
    """
    Inherited class of Encoder with Golomb encoding implementation overriding
    encode().
    """      
    def golomb(self, n, b):
        q = n//b
        r = n - q*b
        quot = ["1" for i in range(0,q)] + ["0"]
        return ("".join(quot), r)
    
    def encode(self, block):
        b = int(np.mean(block))
        golombs = [self.golomb(i, b) for i in block]
        data = np.concatenate(([self.binary(i[1]) for i in golombs], [i[0] for i in golombs] ), axis=None)
        print(type(data))
        return (b, data)
    
#%%
DATA_PATH = "C:\\Users\\Ronan\\Documents\\uni_work\\physics\\third year\\project\\data\\test_data\\C1_160308.txt"

d = Delta(DATA_PATH, 10, 100)

#%%
d.encode_data()
            