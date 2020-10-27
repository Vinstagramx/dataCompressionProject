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
    def __init__(self, PATH, block_size=10, samples="all", direction ="x", bits = 14):
        self._block_size = block_size
        self._new_data =[]
        self._data = self.load_data(PATH)
        self._direction = direction
        directions = ["x", "y", "z"]
        self._current_data = self._data[directions.index(direction)]  #filter to x,y,z only
        self._lengths_distribution = []
        self._lengths_stats = []
        self._original_bit_length = 0
        self._encoded_bit_length = 0
        self._range = (2**bits) / 7.8125e-3
        self._keep_original = True #flag to keep the original data if length of encoded block is longer
        self.filter_data()
        self._block_regions = self.gen_samples(samples)
       
    def load_data(self, path):
        data = np.loadtxt(path).T
        fixed_x = data[1]/7.8125e-3; fixed_y = data[2]/7.8125e-3; fixed_z = data[3]/7.8125e-3
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
        return block
    
    def get_mean(self):
        mean = np.mean(self._current_data)
        return mean

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
        orig_len = 14*len(orig_block); encoded_len = max_bit_length*len(encoded_block) + codeword
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
            if stats:
                lengths = self.get_block_bit_lengths(encoded_block)
                self.block_stats(lengths)   
            if ratio:
                codeword_length = sum(self.get_block_bit_lengths(encoded_data[0]))
                self.update_bit_diff(codeword_length, block, encoded_block) #change this when golomb breaks!!

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

class GolombRice(Encoder):
    """
    Inherited class of Encoder with Golomb-Rice encoding implementation overriding
    encode(), init() and update_bit_diff_diff() to account for differences
    between golomb and generic method. Main difference between Golomb-Rice encoding and Golomb
    is that the parameter b is the nearest exponent of 2 to the maximum value of the block.
    """
    def __init__(self, PATH, block_size=10, samples="all", direction ="x", bits=14):
        """
        Overwritten to allow you to set mode for b - whether mean/min/max of 
        block is used to divide.
        """
        self._block_size = block_size
        self._new_data =[]
        self._data = self.load_data(PATH)
        self._direction = direction
        directions = ["x", "y", "z"]
        self._current_data = self._data[directions.index(direction)]  #filter to x,y,z only
        self._lengths_distribution = []
        self._lengths_stats = []
        self._original_bit_length = 0
        self._encoded_bit_length = 0
        self._range = (2**bits) / 7.8125e-3
        self._keep_original = True
        self.filter_data()
        self._block_regions = self.gen_samples(samples)
    
    def golomb(self, n, b):
        q = n//b if n != 0 else 0
        r = n - q*b if n!= 0 else 0
        quot = ["1" for i in range(0,q)] + ["0"]
        return ("".join(quot), r)
    
    def power_two(self, param):
        power = 1
        while(power < param):
            power*=2
        # print(f'closest exponent = {power}')
        return power

    def encode(self, block):
        maxval = max(block)
        b = self.power_two(maxval)
        golombs = [self.golomb(i, b) for i in block]
        data = np.concatenate(([self.binary(i[1]) for i in golombs], [i[0] for i in golombs] ), axis=None)
        return [[b], data]

    def update_bit_diff(self, codeword, orig_block, encoded_block):
        """
        Fixed for Golomb - uses fact golomb encoded block is split [remainders, unaries] so can
        just half at the middle and take max of both halves and multiply both by the length of the
        half-block.
        """
        orig_len = 14*len(orig_block)
        block_length = len(encoded_block); halfway_point = int(block_length/2)
        self._original_bit_length += orig_len
        max_bit_length_remainders = max(self.get_block_bit_lengths(encoded_block[:halfway_point]))
        max_bit_length_unaries = max(self.get_block_bit_lengths(encoded_block[halfway_point:]))
        encoded_len = max_bit_length_remainders*halfway_point + max_bit_length_unaries * halfway_point + codeword
        if self._keep_original == True:
            if orig_len < encoded_len:
                self._encoded_bit_length += orig_len
            else:
                self._encoded_bit_length += encoded_len
        else:
            self._encoded_bit_length += encoded_len
        return 0

class Golomb(Encoder):
    """
    Inherited class of Encoder with Golomb encoding implementation overriding
    encode(), init() and update_bit_diff_diff() to account for differences
    between golomb and generic method.
    """
    def __init__(self, PATH, block_size=10, samples="all", direction ="x", bits=14, mode = "max"):
        """
        Overwritten to allow you to set mode for b - whether mean/min/max of 
        block is used to divide.
        """
        self._block_size = block_size
        self._new_data =[]
        self._data = self.load_data(PATH)
        self._direction = direction
        directions = ["x", "y", "z"]
        self._current_data = self._data[directions.index(direction)]  #filter to x,y,z only
        self._lengths_distribution = []
        self._lengths_stats = []
        self._original_bit_length = 0
        self._encoded_bit_length = 0
        self._mode = mode
        self._range = (2**bits) / 7.8125e-3
        self._keep_original = True
        self.filter_data()
        self._block_regions = self.gen_samples(samples)
    
    def golomb(self, n, b):
        q = n//b if n != 0 else 0
        r = n - q*b if n!= 0 else 0
        quot = ["1" for i in range(0,q)] + ["0"]
        return ("".join(quot), r)
    
    def encode(self, block):
        if self._mode == "mean":
            b = int(np.mean(block))
        elif self._mode == "max":
            b = max(block)
        elif self._mode == "min":
            b = min(block)
        elif isinstance(self._mode, int): #can set b parameter to percentage of max
            b = int(round((self._mode/100) * max(block)))

        golombs = [self.golomb(i, b) for i in block]
        data = np.concatenate(([self.binary(i[1]) for i in golombs], [i[0] for i in golombs] ), axis=None)
        return [[b], data]

    def update_bit_diff(self, codeword, orig_block, encoded_block):
        """
        Fixed for Golomb - uses fact golomb encoded block is split [remainders, unaries] so can
        just half at the middle and take max of both halves and multiply both by the length of the
        half-block.
        """
        orig_len = 14*len(orig_block)
        block_length = len(encoded_block); halfway_point = int(block_length/2)
        self._original_bit_length += orig_len
        max_bit_length_remainders = max(self.get_block_bit_lengths(encoded_block[:halfway_point]))
        max_bit_length_unaries = max(self.get_block_bit_lengths(encoded_block[halfway_point:]))
        encoded_len = max_bit_length_remainders*halfway_point + max_bit_length_unaries * halfway_point + codeword
        if self._keep_original == True:
            if orig_len < encoded_len:
                self._encoded_bit_length += orig_len
            else:
                self._encoded_bit_length += encoded_len
        else:
            self._encoded_bit_length += encoded_len
        return 0

class DeltaGolomb(Golomb):
    def encode(self, block):
        ref_point = block[0]; compressed = []
        for i in range(1,len(block)):
            compressed.append(block[i]-block[i-1])
        b = int(np.mean(compressed))
        golombs = [self.golomb(i, b) for i in compressed]
        data = np.concatenate(([self.binary(i[1]) for i in golombs], [i[0] for i in golombs] ), axis=None)
        return [[ref_point, b], data]
        
        

            