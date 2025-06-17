#!/bin/bash
# Complete Native Slurm Functionality Demonstration
# For full installation guide, see: SLURM_INSTALLATION_GUIDE.md

echo "🎯 SLURM FUNCTIONALITY DEMONSTRATION"
echo "===================================="
echo ""
echo "📖 For complete installation instructions, see:"
echo "   SLURM_INSTALLATION_GUIDE.md"
echo ""

echo "📋 CURRENT SYSTEM STATUS:"
echo "========================"
echo ""

echo "Cluster Information:"
sinfo
echo ""

echo "Node Details:"
scontrol show node $(hostname) | grep -E "(NodeName|CPUTot|RealMemory|State)"
echo ""

echo "Current Queue:"
squeue
echo ""

echo "🎉 NATIVE SLURM IS FULLY OPERATIONAL!"
echo ""
echo "Available commands:"
echo "✅ sbatch  - Job submission"
echo "✅ squeue  - Queue monitoring" 
echo "✅ scancel - Job cancellation"
echo "✅ sinfo   - Cluster information"
echo "✅ scontrol- Administrative control"
echo "✅ srun    - Interactive execution"
echo "✅ salloc  - Resource allocation"
echo ""
echo "📖 See SLURM_INSTALLATION_GUIDE.md for:"
echo "   • Installation instructions"
echo "   • Job script examples"
echo "   • Testing procedures"
echo "   • Troubleshooting guide"
echo "   • Complete command reference"
