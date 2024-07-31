#!/bin/bash
#
#SBATCH --account=OD-231268
#
#SBATCH --job-name=bm4_irun19d2.7.1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=64
#SBATCH --time=1:30:00
#SBATCH --mem-per-cpu=4000

module load python
module load R/4.3.1

python mogp.py
