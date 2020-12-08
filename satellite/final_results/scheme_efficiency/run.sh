for i in 1 2 3 4 5 6 7 8 9 10
do 
    ./mtf "Delta" "7000" "mean" "delta_iters_$i.txt" "interference_file_list.txt" "16" "True" "$i" "delta_tols_$i.txt"
done