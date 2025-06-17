#!/bin/bash
#SBATCH --job-name=native_test
#SBATCH --output=native_test_%j.out
#SBATCH --error=native_test_%j.err
#SBATCH --time=00:02:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --partition=debug

echo "=== Native Slurm Test Job ==="
echo "Job ID: $SLURM_JOB_ID"
echo "Job Name: $SLURM_JOB_NAME"
echo "Node: $SLURMD_NODENAME"
echo "User: $USER"
echo "Date: $(date)"
echo ""
echo "System Information:"
echo "Hostname: $(hostname)"
echo "CPUs: $(nproc)"
echo "Memory: $(free -h | grep Mem)"
echo ""
echo "Slurm Environment:"
echo "SLURM_JOB_ID: $SLURM_JOB_ID"
echo "SLURM_JOB_NAME: $SLURM_JOB_NAME"
echo "SLURM_NTASKS: $SLURM_NTASKS"
echo "SLURM_CPUS_ON_NODE: $SLURM_CPUS_ON_NODE"
echo "SLURM_PARTITION: $SLURM_JOB_PARTITION"
echo ""
echo "Running native Slurm computation..."
for i in {1..5}; do
    echo "Step $i/5: $(date)"
    sleep 2
done
echo ""
echo "🎉 Native Slurm test job completed successfully!"
echo "This job was submitted using 'sbatch' command"
