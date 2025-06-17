#!/bin/bash
#SBATCH --job-name=cancel_test
#SBATCH --output=cancel_%j.out
#SBATCH --time=00:05:00

echo "🎯 Testing Job Cancellation Capability"
echo "Job ID: $SLURM_JOB_ID"
echo "This job will run for 2 minutes to test cancellation"
for i in {1..120}; do
    echo "Step $i/120 - $(date)"
    sleep 1
done
echo "Job completed (should not reach here if canceled)"
