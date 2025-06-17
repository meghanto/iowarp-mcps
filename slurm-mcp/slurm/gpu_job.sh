#!/bin/bash
#SBATCH --job-name=gpu_job
#SBATCH --output=gpu-%j.out
#SBATCH --error=gpu-%j.err
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32GB
#SBATCH --partition=gpu
#SBATCH --gres=gpu:2

# Example GPU job script
# This demonstrates a GPU-accelerated job

echo "=== GPU Job Information ==="
echo "Job ID: $SLURM_JOB_ID"
echo "Job Name: $SLURM_JOB_NAME"
echo "Node: $SLURMD_NODENAME"
echo "GPU devices: $CUDA_VISIBLE_DEVICES"
echo "Number of GPUs: $SLURM_GPUS"
echo ""

echo "=== System Information ==="
echo "Available GPUs:"
nvidia-smi 2>/dev/null || echo "nvidia-smi not available (no GPUs or drivers)"
echo ""
echo "CPU information:"
lscpu | grep "Model name" || echo "CPU info not available"
echo "Memory information:"
free -h
echo ""

echo "=== Loading GPU Modules ==="
module load cuda/11.8 || echo "CUDA module not available"
module load cudnn/8.6.0 || echo "cuDNN module not available"
module load python/3.9 || echo "Python module not available"
echo ""

echo "=== GPU Work Simulation ==="
echo "Starting GPU-accelerated computation..."

# Simulate GPU work
echo "Initializing GPU devices..."
sleep 2

for gpu in {0..1}; do
    echo "GPU $gpu: Loading data..."
    sleep 3
    echo "GPU $gpu: Starting computation..."
    
    for iter in {1..8}; do
        echo "  GPU $gpu: Iteration $iter/8"
        sleep 5  # Simulate GPU computation
    done
    
    echo "GPU $gpu: Computation completed"
done

echo ""
echo "=== Results ==="
echo "GPU job completed successfully"
echo "Total GPU time: $SECONDS seconds"
echo "Final GPU status:"
nvidia-smi 2>/dev/null || echo "GPU status not available"
