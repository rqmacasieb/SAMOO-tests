#!/bin/bash
#
#SBATCH --account=OD-231268
#
#SBATCH --job-name=bm3_orun
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:10:00
#SBATCH --mem-per-cpu=4000

cd master
./pestpp-mou mou_bm3.pst /H :4017
