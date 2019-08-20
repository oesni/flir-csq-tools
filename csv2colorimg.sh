#!/bin/bash

input_dir=$(echo $1 | sed 's:/*$::')
output_dir=$(echo $2 | sed 's:/*$::')

echo input directory : $1
echo output directory : $output_dir
echo 

for filename in $input_dir/*.csv
do
    ./csv2colorimg.py $filename $output_dir/
done
