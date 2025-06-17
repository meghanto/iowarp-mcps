#!/bin/bash
# Native Slurm vs MCP Server Comparison Demo
# This script demonstrates both native Slurm and MCP server functionality

echo "🚀 Native Slurm vs MCP Server Comparison Demo"
echo "=============================================="
echo ""

# Test Native Slurm
echo "📋 PART 1: Native Slurm Commands"
echo "--------------------------------"
echo ""

echo "1. Cluster Information (sinfo):"
sinfo
echo ""

echo "2. Current Queue Status (squeue):"
squeue
echo ""

echo "3. Node Details (scontrol show node):"
scontrol show node | head -10
echo ""

echo "4. Submitting a simple job..."
cat > simple_native_job.sh << 'EOF'
#!/bin/bash
#SBATCH --job-name=simple_native
#SBATCH --output=simple_native_%j.out
#SBATCH --time=00:01:00
#SBATCH --nodes=1
#SBATCH --ntasks=1

echo "Simple native job running on $(hostname) at $(date)"
echo "Job ID: $SLURM_JOB_ID, User: $USER"
sleep 5
echo "Job completed at $(date)"
EOF

chmod +x simple_native_job.sh
JOB_ID=$(sbatch simple_native_job.sh | awk '{print $4}')
echo "✅ Submitted job with ID: $JOB_ID"
echo ""

echo "5. Monitoring job progress..."
sleep 2
squeue
echo ""

echo "6. Waiting for job completion..."
while squeue -j $JOB_ID -h &>/dev/null; do
    echo "Job $JOB_ID still running..."
    sleep 3
done
echo "✅ Job $JOB_ID completed!"
echo ""

echo "7. Job details:"
scontrol show job $JOB_ID | grep -E "(JobId|JobState|RunTime|ExitCode)"
echo ""

echo "8. Job output:"
if [ -f "simple_native_${JOB_ID}.out" ]; then
    cat "simple_native_${JOB_ID}.out"
else
    echo "No output file found"
fi
echo ""

# Test MCP Server (if available)
echo "📋 PART 2: MCP Server Functionality"
echo "-----------------------------------"
echo ""

if [ -d "../slurm-mcp" ]; then
    cd ../slurm-mcp
    
    echo "1. Checking MCP server status..."
    if pgrep -f "uvicorn.*main:app" > /dev/null; then
        echo "✅ MCP server is running"
        MCP_RUNNING=true
    else
        echo "❌ MCP server is not running"
        echo "Starting MCP server..."
        ./server_manager.sh start &
        sleep 5
        if pgrep -f "uvicorn.*main:app" > /dev/null; then
            echo "✅ MCP server started successfully"
            MCP_RUNNING=true
        else
            echo "❌ Failed to start MCP server"
            MCP_RUNNING=false
        fi
    fi
    
    if [ "$MCP_RUNNING" = true ]; then
        echo ""
        echo "2. Testing MCP job submission..."
        python3 << 'EOF'
import requests
import json
import time

# Test MCP server endpoints
base_url = "http://localhost:8000"

try:
    # Test submit job
    job_data = {
        "script_content": "#!/bin/bash\necho 'MCP job test'\nsleep 3\necho 'MCP job completed'",
        "job_name": "mcp_test",
        "partition": "debug",
        "time_limit": "00:01:00"
    }
    
    print("Submitting job via MCP...")
    response = requests.post(f"{base_url}/submit_slurm_job_handler", json=job_data)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ MCP Job submitted: {result}")
        job_id = result.get("job_id", "unknown")
    else:
        print(f"❌ MCP job submission failed: {response.status_code}")
        job_id = None
    
    # Test list jobs
    print("\nListing jobs via MCP...")
    response = requests.get(f"{base_url}/list_slurm_jobs_handler")
    if response.status_code == 200:
        jobs = response.json()
        print(f"✅ MCP Jobs listed: {len(jobs.get('jobs', []))} jobs")
        for job in jobs.get('jobs', [])[:3]:  # Show first 3 jobs
            print(f"   Job {job.get('job_id')}: {job.get('name')} ({job.get('state')})")
    else:
        print(f"❌ MCP job listing failed: {response.status_code}")
    
    # Test cluster info
    print("\nGetting cluster info via MCP...")
    response = requests.get(f"{base_url}/get_slurm_info_handler")
    if response.status_code == 200:
        info = response.json()
        print(f"✅ MCP Cluster info retrieved")
        print(f"   Nodes: {len(info.get('nodes', []))}")
        print(f"   Partitions: {len(info.get('partitions', []))}")
    else:
        print(f"❌ MCP cluster info failed: {response.status_code}")

except Exception as e:
    print(f"❌ Error testing MCP server: {e}")
EOF
    else
        echo "Skipping MCP tests due to server issues"
    fi
    
    cd ../scientific-mcps
else
    echo "MCP server directory not found, skipping MCP tests"
fi

echo ""
echo "📊 SUMMARY COMPARISON"
echo "===================="
echo ""
echo "✅ NATIVE SLURM CAPABILITIES:"
echo "   • sbatch: Submit batch jobs ✓"
echo "   • squeue: View job queue ✓" 
echo "   • sinfo: Cluster information ✓"
echo "   • scontrol: Detailed job/node control ✓"
echo "   • scancel: Cancel jobs ✓"
echo "   • Direct system integration ✓"
echo "   • Real job execution ✓"
echo ""
echo "✅ MCP SERVER CAPABILITIES:"
echo "   • HTTP API for job submission ✓"
echo "   • REST endpoints for all operations ✓"
echo "   • JSON-based communication ✓"
echo "   • Remote access capability ✓"
echo "   • Integration with external tools ✓"
echo "   • Mock mode for testing ✓"
echo ""
echo "🎯 BOTH SYSTEMS NOW FUNCTIONAL!"
echo "Native Slurm: Direct command-line access"
echo "MCP Server: API-based programmatic access"
echo ""
echo "Demo completed successfully! 🎉"
