#!/bin/bash
#SBATCH --job-name=quick_test
#SBATCH --time=00:01:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
echo "Quick job running on $(hostname)"
echo "Job ID: $SLURM_JOB_ID"
sleep 5
