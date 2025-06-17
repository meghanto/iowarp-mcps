#!/bin/bash
#SBATCH --job-name=mcp_test
#SBATCH --time=00:02:00
#SBATCH --nodes=1
#SBATCH --ntasks=1

echo "Hello from MCP Slurm Server!"
echo "Current date: $(date)"
echo "Running on node: $(hostname)"
sleep 10
echo "Job completed successfully!"
