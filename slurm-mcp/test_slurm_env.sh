#!/bin/bash
#SBATCH --job-name=env_test
#SBATCH --output=env_test_%j.out
#SBATCH --error=env_test_%j.err
#SBATCH --time=00:01:00
#SBATCH --ntasks=1
#SBATCH --partition=debug

echo "=== SLURM ENVIRONMENT TEST JOB ==="
echo "Job ID: $SLURM_JOB_ID"
echo "Job Name: $SLURM_JOB_NAME"
echo "Node: $(hostname)"
echo "User: $(whoami)"
echo "Date: $(date)"
echo "Working Directory: $(pwd)"
echo "Slurm Variables:"
echo "  SLURM_CPUS_ON_NODE: $SLURM_CPUS_ON_NODE"
echo "  SLURM_JOB_NODELIST: $SLURM_JOB_NODELIST"
echo "  SLURM_NTASKS: $SLURM_NTASKS"
echo "  SLURM_PROCID: $SLURM_PROCID"
echo ""
echo "System Information:"
echo "  CPU cores: $(nproc)"
echo "  Memory: $(free -h | grep Mem:)"
echo "  Load average: $(uptime)"
echo ""
echo "Environment test completed successfully!"
