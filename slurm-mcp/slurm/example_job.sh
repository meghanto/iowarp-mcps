#!/bin/bash
#SBATCH --job-name=example_job
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=1
#SBATCH --mem=8GB
#SBATCH --partition=compute

# Example Slurm job script
# This is what you would submit with: sbatch example_job.sh

echo "=== Job Information ==="
echo "Job ID: $SLURM_JOB_ID"
echo "Job Name: $SLURM_JOB_NAME"
echo "Node: $SLURMD_NODENAME"
echo "Number of nodes: $SLURM_JOB_NUM_NODES"
echo "Number of tasks: $SLURM_NTASKS"
echo "CPUs per task: $SLURM_CPUS_PER_TASK"
echo "Memory per node: $SLURM_MEM_PER_NODE"
echo "Partition: $SLURM_JOB_PARTITION"
echo "Account: $SLURM_JOB_ACCOUNT"
echo "User: $SLURM_JOB_USER"
echo ""

echo "=== Environment Information ==="
echo "Working directory: $(pwd)"
echo "Date and time: $(date)"
echo "Available modules:"
module avail 2>&1 | head -10 || echo "No modules system available"
echo ""

echo "=== Running the actual work ==="
echo "Starting computational work..."

# Simulate some computational work
for i in {1..10}; do
    echo "Processing step $i/10..."
    sleep 6  # Simulate work
    echo "  -> Step $i completed"
done

echo ""
echo "=== Job Completion ==="
echo "Job completed successfully at $(date)"
echo "Total execution time: $SECONDS seconds"
echo "Job finished on node: $SLURMD_NODENAME"
