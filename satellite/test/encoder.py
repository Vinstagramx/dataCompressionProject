# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 17:55:18 2020

@author: Ronan
"""
import numpy as np
from scipy import stats
import random 
import matplotlib.pyplot as plt

class Encoder(object):
    def __init__(self, PATH, block_size=10, samples="all", direction ="x"):
        self._block_size = block_size
        self._new_data =[]
        self._data = self.load_data(PATH)
        directions = ["x", "y", "z"]
        self._current_data = self._data[directions.index(direction)]  #filter to x,y,z only
        self._block_regions = self.gen_samples(samples)
        self._lengths_distribution = []
        self._lengths_stats = []
        self._original_bit_length = 0
        self._encoded_bit_length = 0
       
    def load_data(self, path):
        data = np.loadtxt(path).T
        fixed_x = data[1] * 10000; fixed_y = data[2] * 10000; fixed_z = data[3] * 10000
        fixed_array = np.array([fixed_x, fixed_y, fixed_z], dtype = np.int32)
        return fixed_array
    
    def gen_samples(self, samples, seed=2):
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
                
    def block_stats(self, lengths_block):
        """
        Look at a bunch of properties of list of bit lengths: max, min, mean, mode
        and adds the lengths to dist list for plotting later.
        """
        maximum = np.max(lengths_block); minimum = np.min(lengths_block)
        mean = np.mean(lengths_block); mode = stats.mode(lengths_block)
        self._lengths_distribution = self._lengths_distribution + lengths_block
        self._lengths_stats.append([maximum, minimum, mean, mode])
        return 0
    
    def plot_block_stats(self):
        fig, axs = plt.subplots(2,2)
        stats_data = np.asarray(self._lengths_stats).T
        data = [self._lengths_distribution] + [list(i) for i in stats_data]
        print(data)
        ax_tag_color = [(axs[0,0], "", "blue"), (axs[1,0], "Max ", "green"), (axs[0,1], "Min ", "orange"), (axs[1,1],"Mean ", "red")]
        for index, i in enumerate(ax_tag_color):
            print(index)
            i[0].hist(data[index], color=i[2])
            i[0].set_title(i[1]+"Bit Lengths in Block")
        
    def get_compression_ratio(self):
        ratio = (1-self._encoded_bit_length/self._original_bit_length)*100
        print(ratio)
        return ratio
        
    def update_bit_diff(self, codeword, orig_block, encoded_block):
        self._original_bit_length += sum(self.get_block_bit_lengths(orig_block))
        self._encoded_bit_length += sum(self.get_block_bit_lengths(encoded_block)) + codeword
        return 0
    
    def encode_data(self, ratio=True, stats=True):
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
            encoded_data = self.encode(block)
            encoded_block = encoded_data[1] #encode(block)[0] is the codeword, [1] the data encoded by codeword
            if stats:
                lengths = self.get_block_bit_lengths(encoded_block)
                self.block_stats(lengths)   
            if ratio:
                codeword_length = self.get_block_bit_lengths([encoded_data[0]])[0]
                self.update_bit_diff(codeword_length, block, encoded_block) #change this when golomb breaks!!
        if ratio:
            self.get_compression_ratio()
        if stats:
            self.plot_block_stats()
        return self._new_data
    
class Delta(Encoder):
    """
    Inherited class of Encoder with delta encoding implementation overriding
    encode().
    """      
    def encode(self, block):
        ref_point = block[0]
        compressed = [(i- ref_point) for i in block[1:]]
        return [ref_point, compressed]

class DeltaSq(Encoder):
    """
    Inherited class of Encoder with delta squared encoding implementation overriding
    encode().
    """      
    def encode(self, block):
        ref_point = block[0]
        compressed = [(i- ref_point) for i in block[1:]]
        delta_ref = compressed[0]
        compressed2 = [(i- delta_ref) for i in compressed[1:]]
        return [[ref_point, delta_ref], compressed2]

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
        return [b, data]
    

            