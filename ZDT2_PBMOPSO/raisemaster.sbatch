#!/bin/bash
#
#SBATCH --account=OD-224554
#
#SBATCH --job-name=bm3_samopso-2
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=3:00:00
#SBATCH --mem-per-cpu=4000

cd master
./pestpp-mou mou_bm3.pst /H :4020
