#!/bin/bash
#SBATCH --job-name=long_test
#SBATCH --output=long_%j.out  
#SBATCH --time=00:05:00
#SBATCH --nodes=1

echo "Long-running test job started at $(date)"
for i in {1..30}; do
    echo "Step $i/30 at $(date)"
    sleep 10
done
echo "Job completed at $(date)"
