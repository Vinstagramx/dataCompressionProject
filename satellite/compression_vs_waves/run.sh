#!/bin/bash

#Run python script to generate simulated interference data, then get compression ratios w/ mtf then plot the data with another script

python new_sim_interference.py C1_160308.FS.FULLRES.txt
./mtf "Golomb" "7000" "mean" "temp_compression_data.txt" "temp_file_list.txt" "16"
python modified_comp_rat.py temp_compression_data.txt
