#!/bin/bash
#SBATCH --job-name=compute_test
#SBATCH --time=00:05:00
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --mem=4GB
echo "Compute job starting..."
echo "Job ID: $SLURM_JOB_ID"
echo "CPUs: $SLURM_CPUS_ON_NODE"
for i in {1..5}; do
    echo "Processing step $i"
    sleep 2
done
