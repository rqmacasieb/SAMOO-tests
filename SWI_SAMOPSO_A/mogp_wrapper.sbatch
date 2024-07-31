#!/bin/bash
#
#SBATCH --account=OD-231268
#
#SBATCH --job-name=irun7c6.2.1f_gp4a1.6.2
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=64
#SBATCH --time=1:00:00
#SBATCH --mem-per-cpu=4000

module load python
module load R/4.3.1

python mogp.py
