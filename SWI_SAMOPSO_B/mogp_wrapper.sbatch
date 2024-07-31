#!/bin/bash
#
#SBATCH --account=SC-000383
#
#SBATCH --job-name=irun7b6.2.3f_gp4a1.6.2
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=64
#SBATCH --time=1:00:00
#SBATCH --mem-per-cpu=4000

module load python
module load R/4.3.1

python mogp.py
