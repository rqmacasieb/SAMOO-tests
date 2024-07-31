#!/bin/bash
#
#SBATCH --account=OD-224554
#
#SBATCH --job-name=run7f
#SBATCH --array=0-49
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH --time=7-00:00:00
#SBATCH --mem-per-cpu=4000

function runpack()
{
     (( n = SLURM_ARRAY_TASK_ID * SLURM_NTASKS_PER_NODE + SLURM_PROCID))
     ./runworker $n > runlog$n.out 2>&1
}

export -f runpack

srun bash -c runpack

