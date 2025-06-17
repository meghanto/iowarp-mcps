#!/bin/bash
#SBATCH --job-name=capability_test
#SBATCH --output=capability_%j.out
#SBATCH --time=00:01:00

echo "🎯 Testing MCP Slurm Capability"
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $(hostname)"
echo "Time: $(date)"
echo "MCP Server Integration: SUCCESS"
sleep 5
echo "✅ Capability test completed successfully!"
