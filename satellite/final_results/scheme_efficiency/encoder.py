# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 17:55:18 2020

@author: Ronan
"""
import numpy as np
from math import log, ceil, floor
from scipy import stats
import random 
import matplotlib.pyplot as plt

class Encoder(object):
    def __init__(self, PATH, block_size=10, samples="all", direction ="x", bits = 14):
        self._block_size = block_size
        self._new_data =[]
        self._scale_factor = 31.25e-3
        self._data = self.load_data(PATH)
        self._direction = direction
        directions = ["x", "y", "z"]
        self._current_data = self._data[directions.index(direction)]  #filter to x,y,z only
        self._lengths_distribution = []
        self._lengths_stats = []
        self._original_bit_length = 0
        self._encoded_bit_length = 0
        self._range = (2**bits) / self._scale_factor
        self._keep_original = True #flag to keep the original data if length of encoded block is longer
        self.filter_data()
        self._block_regions = self.gen_samples(samples)
        self._bits = bits
       
    def load_data(self, path):
        data = np.loadtxt(path).T
        fixed_x = data[1]/self._scale_factor; fixed_y = data[2]/self._scale_factor; fixed_z = data[3]/self._scale_factor
        fixed_array = np.array([fixed_x, fixed_y, fixed_z], dtype = np.int32) #does this round down or nearest - if we can't reconstruct data look at this 
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

    def filter_data(self):
        self._current_data = [value for value in self._current_data if abs(value) < self._range]
        
    def binary(self, decimal):
        if decimal >= 0:
            sign_bit = 0
        else:
            sign_bit = 1
        bin_string = str(sign_bit) + bin(abs(decimal)).replace("0b", "") 
        return bin_string
    
    def encode(self, block): #generic method to be overwritten by golomb and delta and others
        return [[block[0]], block[1:]]
    
    def get_mean(self):
        mean = np.mean(self._current_data)
        return mean

    def get_block_bit_lengths(self, block):
        """
        Returns list of the bit length of binary/unary whatever is in the block.
        """
        block_bit_lengths = [len(self.binary(i)) for i in block] #if type(block[0]) != np.str_ else [len(i) for i in block
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
        plt.figure("Block Stats Plots")
        fig, axs = plt.subplots(2,2)
        stats_data = np.asarray(self._lengths_stats).T
        data = [self._lengths_distribution] + [list(i) for i in stats_data]
        #print(data)
        ax_tag_color = [(axs[0,0], "", "blue"), (axs[1,0], "Max ", "green"), (axs[0,1], "Min ", "orange"), (axs[1,1],"Mean ", "red")]
        for index, i in enumerate(ax_tag_color):
            #print(index)
            i[0].hist(data[index], color=i[2])
            i[0].set_title(i[1]+"Bit Lengths in Block")
        
    def get_spacesaving_ratio(self):
        ratio = (1-self._encoded_bit_length/self._original_bit_length)*100
        print(f'{self._direction}-space-saving ratio = {ratio}')
        return ratio
        
    def update_bit_diff(self, codeword, orig_block, encoded_block):
        """
        Adjusted slightly. Updates the class variables that track the running totals
        of bit lengths in unencoded and encoded blocks. Now just multiplies the 
        length of block by the maximum bit length in the block (because this 
        is how it will be on sub satellite.) Added a check to see if encoded
        block is bigger than original block and if so just uses the original
        block, as reference
        """
        max_bit_length = max(self.get_block_bit_lengths(encoded_block))
        orig_len = self._bits*len(orig_block); encoded_len = max_bit_length*len(encoded_block) + codeword
        self._original_bit_length += orig_len
        if self._keep_original == True:
            if orig_len < encoded_len: #equivalent to the non-encoded flag as per paper
                self._encoded_bit_length += orig_len
            else:
                self._encoded_bit_length += encoded_len
        else: 
            self._encoded_bit_length += encoded_len
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
            print(block)
            print(encoded_block)
            if stats:
                lengths = self.get_block_bit_lengths(encoded_block)
                print(lengths)
                self.block_stats(lengths)   
            if ratio:
                codeword_length = sum(self.get_block_bit_lengths(encoded_data[0]))
                self.update_bit_diff(codeword_length, block, encoded_block) #change this when golomb breaks!!
                print(self._original_bit_length, self._encoded_bit_length, codeword_length)
        if stats:
            print("Doing stats")
            self.plot_block_stats()
        return self._new_data
    
class Delta(Encoder):
    """
    Inherited class of Encoder with delta encoding implementation overriding
    encode().
    """      
    def encode(self, block):
        ref_point = block[0]; compressed = []
        #compressed.append(ref_point)
        for i in range(1,len(block)):
            compressed.append(block[i]-block[i-1])
        #compressed = [(i- ref_point) for i in block[1:]]
        return [[ref_point], compressed]

class DeltaSq(Encoder):
    """
    Inherited class of Encoder with delta squared encoding implementation overriding
    encode().
    """      
    def encode(self, block):
        
        ref_point = block[0]; compressed, compressed2 = [], []
        for i in range(1,len(block)):
            compressed.append(block[i]-block[i-1])
        delta_ref = compressed[0]
        for i in range(1,len(block)):
            compressed2.append(compressed[i]-compressed[i-1])
        return [[ref_point, delta_ref], compressed2]

class DeltaIter(Encoder):
        
    def encode(self, block):
        codewords = []
        encoded_vec = block
        for i in range(3):
            temp = []
            codewords.append(encoded_vec[0])
            for j in range(1, len(encoded_vec)):
                temp.append(encoded_vec[j]-encoded_vec[j-1])
            #print("econded vec is: ", temp)
            encoded_vec = temp
        #print("block is ", block)
        #print("codewords are: ", codewords)
        #print("encoded vec is: ", encoded_vec)
        return [codewords, encoded_vec]
            
            
            