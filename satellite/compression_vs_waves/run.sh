#!/bin/bash

#Run python script to generate simulated interference data, then get compression ratios w/ mtf then plot the data with another script

python new_sim_interference.py C1_160309_cavity.txt
./mtf "Delta" "7000" "mean" "temp_compression_data.txt" "temp_file_list.txt" "16" "False" "1" "1"
python modified_comp_rat.py temp_compression_data.txt
