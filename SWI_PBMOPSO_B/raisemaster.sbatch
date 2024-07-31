#!/bin/bash
#
#SBATCH --account=OD-231268
#
#SBATCH --job-name=run7b6.2.1full
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=03-00:00:00
#SBATCH --mem-per-cpu=4000

cd master
./pestpp-mou mou_henry.pst /H :4019
