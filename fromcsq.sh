#!/bin/bash

echo input file : $1
base=$(basename "$1" .csq)
trimmed_dir=$(echo $2 | sed 's:/*$::')
echo output directory : $trimmed_dir
echo -

# split each frame into .fff
mkdir $trimmed_dir/frame_fff
perl -f ./scripts/split.pl -i $1 -o $trimmed_dir/frame_fff -b $base -p fff -x fff

# extract raw image from .fff
mkdir $trimmed_dir/raw
for filename in $trimmed_dir/frame_fff/*
do
    name=$(basename $filename .fff)
    raw="$name.raw"
    exiftool -b -RawThermalImage $filename > $trimmed_dir/raw/$raw
done

# convert .raw to .png
mkdir $trimmed_dir/png
for inputfile in $trimmed_dir/raw/*
do
    outputfile="$trimmed_dir/png/$(basename $inputfile .raw).png"
    ffmpeg -f image2 -vcodec jpegls -i $inputfile -f image2 -vcodec png $outputfile
done

# convert .png to .csv
mkdir $trimmed_dir/csv_raw
for inputfile in $trimmed_dir/png/*
do
    output_dir="$trimmed_dir/csv_raw/"
    python image2csv.py $inputfile $output_dir
done

# convert raw data to celsius
mkdir $trimmed_dir/csv_celsius
for inputfile in $trimmed_dir/csv_raw/*
do
    output_dir="$trimmed_dir/csv_celsius/"
    python raw2celsius.py $inputfile $output_dir
done

# convert celsius csv to color image
mkdir $trimmed_dir/color
for inputfile in $trimmed_dir/csv_celsius/*
do
    ./csv2colorimg.py $inputfile $trimmed_dir/color/
done

#remove tmp files
rm -r $trimmed_dir/frame_fff $trimmed_dir/raw $trimmed_dir/png $trimmed_dir/csv_raw
