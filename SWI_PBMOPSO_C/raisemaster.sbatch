#!/bin/bash
#
#SBATCH --account=OD-224554
#
#SBATCH --job-name=run7f
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=07-00:00:00
#SBATCH --mem-per-cpu=4000

cd master
./pestpp-mou mou_henry.pst /H :4018
