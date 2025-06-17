#!/bin/bash
#SBATCH --job-name=mcp_demo_job
#SBATCH --time=00:05:00
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --mem=2GB
#SBATCH --partition=compute

echo "=== MCP Server Job Submission Demo ==="
echo "Job ID: $SLURM_JOB_ID"
echo "Job Name: $SLURM_JOB_NAME"
echo "Node: $(hostname)"
echo "Date: $(date)"
echo "User: $(whoami)"
echo "Working Directory: $(pwd)"
echo "Number of CPUs: $SLURM_CPUS_ON_NODE"
echo "Memory per CPU: $SLURM_MEM_PER_CPU"
echo ""

echo "Starting computational work..."
for i in {1..10}; do
    echo "Processing step $i/10..."
    sleep 2
    echo "  - Completed step $i"
done

echo ""
echo "Job completed successfully!"
echo "End time: $(date)"
echo "Total execution time: $SECONDS seconds"
