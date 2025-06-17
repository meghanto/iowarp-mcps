#!/bin/bash
#SBATCH --job-name=memory_test
#SBATCH --time=00:03:00
#SBATCH --nodes=1
#SBATCH --ntasks=2
#SBATCH --mem=8GB
echo "Memory-intensive job starting..."
echo "Job ID: $SLURM_JOB_ID"
echo "Memory per CPU: $SLURM_MEM_PER_CPU"
echo "Simulating memory-intensive computation..."
sleep 10
