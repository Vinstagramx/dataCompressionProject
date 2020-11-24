#!/bin/bash

#Run python script to generate simulated interference data, then get compression ratios w/ mtf then plot the data with another script

python sim_interference.py C1_160308.FS.FULLRES.txt
./mtf "Delta" "7000" "None" "temp_compression_data.txt" "temp_file_list.txt" 16
python modified_comp_rat.py temp_compression_data.txt
