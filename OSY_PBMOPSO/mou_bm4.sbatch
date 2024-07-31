#!/bin/bash
#
#SBATCH --account=OD-231268
#
#SBATCH --job-name=bm4_samopso-2
#SBATCH --array=0-25
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH --time=3:00:00
#SBATCH --mem-per-cpu=2000

function runpack()
{
     (( n = SLURM_ARRAY_TASK_ID * SLURM_NTASKS_PER_NODE + SLURM_PROCID))
     ./runworker $n > runlog$n.out 2>&1
}

export -f runpack

srun bash -c runpack

