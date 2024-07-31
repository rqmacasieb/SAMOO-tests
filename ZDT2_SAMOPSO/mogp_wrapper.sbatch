#!/bin/bash
#
#SBATCH --account=OD-231268
#
#SBATCH --job-name=bm3_irun28c2.7.1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=64
#SBATCH --time=0:20:00
#SBATCH --mem-per-cpu=4000

module load python
module load R/4.3.1

python mogp.py
