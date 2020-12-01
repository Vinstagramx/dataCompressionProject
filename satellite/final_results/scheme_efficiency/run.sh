for i in 6 7 8 9
do 
    ./mtf "Delta" "7000" "mean" "delta_iters_$i.txt" "interference_file_list.txt" "16" "False" "$i"
done