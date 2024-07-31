#!/bin/bash
#
#SBATCH --account=SC-000383
#
#SBATCH --job-name=orun7b6.2.3f_gp4a1.6.2
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=8:00:00
#SBATCH --mem-per-cpu=4000

cd master
./pestpp-mou mou_henry.pst /H :4020
