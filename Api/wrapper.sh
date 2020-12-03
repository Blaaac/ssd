#!/bin/bash
source /home/ruben/anaconda3/etc/profile.d/conda.sh
echo $1
echo $2
conda activate $1
python $2 $3
