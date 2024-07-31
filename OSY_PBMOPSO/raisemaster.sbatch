#!/bin/bash
#
#SBATCH --account=OD-231268
#
#SBATCH --job-name=bm4_samopso-2
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=3:00:00
#SBATCH --mem-per-cpu=4000

cd master
./pestpp-mou mou_bm4.pst /H :4021
