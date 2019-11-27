#!/bin/bash
echo "Usage: ./convert.sh modelxxx.tflite"
name=`echo $1 | cut -d '.' -f 1`
tflite_out=$name.tflite
kmodel_out=$name.kmodel

#nncase
ncc_exe=./ncc/ncc

echo ">> Converting TFlite to Kmodel"
$ncc_exe compile $tflite_out ./$kmodel_out -i tflite -o kmodel -t k210 --dataset dataset-all

echo ">> OK. Not if all goes well, copy $kmodel_out to scr folder"
