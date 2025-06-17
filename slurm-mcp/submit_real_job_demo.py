#!/usr/bin/env python3
"""
Real Slurm Job Submission Demo through MCP
Demonstrates submitting actual jobs to Slurm using MCP capabilities
"""
import sys
import os
import asyncio
import tempfile
import json
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from server import (
    submit_slurm_job_tool,
    check_job_status_tool,
    cancel_slurm_job_tool,
    list_slurm_jobs_tool,
    get_slurm_info_tool,
    get_job_details_tool,
    get_job_output_tool,
    get_queue_info_tool,
    submit_array_job_tool,
    get_node_info_tool
)


def create_job_script(script_name: str, script_content: str) -> str:
    """Create a job script file."""
    script_path = f"/tmp/{script_name}"
    with open(script_path, 'w') as f:
        f.write(script_content)
    os.chmod(script_path, 0o755)
    print(f"📄 Created job script: {script_path}")
    return script_path


def print_json_result(title: str, result: dict):
    """Pretty print JSON results."""
    print(f"\n{title}")
    print("=" * len(title))
    print(json.dumps(result, indent=2, default=str))


async def main():
    """Main demonstration function."""
    print("🎯 Real Slurm Job Submission Demo via MCP")
    print("=" * 60)
    print("This demo will submit actual jobs to Slurm using MCP capabilities")
    print("=" * 60)

    # 1. First, check cluster information
    print("\n📊 Step 1: Checking Slurm cluster information...")
    cluster_info = await get_slurm_info_tool()
    print_json_result("🏢 Cluster Information", cluster_info)

    # 2. Check node information
    print("\n📊 Step 2: Checking node information...")
    node_info = await get_node_info_tool()
    print_json_result("🖥️ Node Information", node_info)

    # 3. Check current queue status
    print("\n📊 Step 3: Checking current queue status...")
    queue_info = await get_queue_info_tool()
    print_json_result("🏃 Queue Information", queue_info)

    # 4. Create and submit a simple job
    print("\n🚀 Step 4: Creating and submitting a simple job...")
    
    simple_job_script = """#!/bin/bash
#SBATCH --job-name=mcp_demo_simple
#SBATCH --output=mcp_demo_simple_%j.out
#SBATCH --error=mcp_demo_simple_%j.err
#SBATCH --time=00:02:00
#SBATCH --cpus-per-task=1

echo "========================================="
echo "MCP Slurm Demo Job - Simple"
echo "========================================="
echo "Job started at: $(date)"
echo "Running on node: $(hostname)"
echo "Job ID: $SLURM_JOB_ID"
echo "Working directory: $(pwd)"
echo "User: $(whoami)"
echo "Environment: $SLURM_CLUSTER_NAME"
echo ""
echo "Performing simple computation..."
for i in {1..10}; do
    echo "Step $i: $(date)"
    sleep 1
done
echo ""
echo "Simple computation completed!"
echo "Job finished at: $(date)"
echo "========================================="
"""
    
    script_path = create_job_script("mcp_demo_simple.sh", simple_job_script)
    
    # Submit the job through MCP
    print("\n📨 Submitting job through MCP...")
    submit_result = await submit_slurm_job_tool(
        script_path=script_path,
        cores=1,
        memory="1GB",
        time_limit="00:02:00",
        job_name="mcp_demo_simple"
    )
    print_json_result("📋 Job Submission Result", submit_result)
    
    if "job_id" in submit_result:
        job_id = submit_result["job_id"]
        print(f"\n✅ Job submitted successfully with ID: {job_id}")
        
        # 5. Monitor the job status
        print("\n⏳ Step 5: Monitoring job status...")
        for i in range(5):
            print(f"\nCheck #{i+1}:")
            status_result = await check_job_status_tool(job_id)
            print_json_result(f"📈 Job Status Check #{i+1}", status_result)
            
            if status_result.get("status") in ["COMPLETED", "FAILED", "CANCELLED"]:
                print(f"🏁 Job finished with status: {status_result.get('status')}")
                break
            
            print("⏱️ Waiting 10 seconds before next check...")
            time.sleep(10)
        
        # 6. Get detailed job information
        print("\n🔍 Step 6: Getting detailed job information...")
        details_result = await get_job_details_tool(job_id)
        print_json_result("🔍 Job Details", details_result)
        
        # 7. Get job output
        print("\n📄 Step 7: Getting job output...")
        stdout_result = await get_job_output_tool(job_id, "stdout")
        print_json_result("📄 Job Output (stdout)", stdout_result)
        
        stderr_result = await get_job_output_tool(job_id, "stderr")
        print_json_result("📄 Job Output (stderr)", stderr_result)
        
    else:
        print("❌ Job submission failed!")
        if submit_result.get("error"):
            print(f"Error: {submit_result['error']}")

    # 8. Create and submit a computational job
    print("\n🧮 Step 8: Creating and submitting a computational job...")
    
    compute_job_script = """#!/bin/bash
#SBATCH --job-name=mcp_demo_compute
#SBATCH --output=mcp_demo_compute_%j.out
#SBATCH --error=mcp_demo_compute_%j.err
#SBATCH --time=00:03:00
#SBATCH --cpus-per-task=2

echo "========================================="
echo "MCP Slurm Demo Job - Computational"
echo "========================================="
echo "Job started at: $(date)"
echo "Running on node: $(hostname)"
echo "Job ID: $SLURM_JOB_ID"
echo "Cores allocated: $SLURM_CPUS_PER_TASK"
echo ""

# Simple computational task
echo "Performing matrix multiplication..."
python3 -c "
import numpy as np
import time

print('Starting computational work...')
# Create two random matrices
size = 500
A = np.random.rand(size, size)
B = np.random.rand(size, size)

start_time = time.time()
C = np.dot(A, B)
end_time = time.time()

print(f'Matrix multiplication ({size}x{size}) completed in {end_time - start_time:.2f} seconds')
print(f'Result matrix sum: {np.sum(C):.2f}')
print('Computational work completed successfully!')
"

echo ""
echo "Job finished at: $(date)"
echo "========================================="
"""
    
    compute_script_path = create_job_script("mcp_demo_compute.sh", compute_job_script)
    
    # Submit the computational job
    print("\n📨 Submitting computational job through MCP...")
    compute_submit_result = await submit_slurm_job_tool(
        script_path=compute_script_path,
        cores=2,
        memory="2GB",
        time_limit="00:03:00",
        job_name="mcp_demo_compute"
    )
    print_json_result("📋 Computational Job Submission Result", compute_submit_result)
    
    if "job_id" in compute_submit_result:
        compute_job_id = compute_submit_result["job_id"]
        print(f"\n✅ Computational job submitted successfully with ID: {compute_job_id}")
        
        # Monitor this job briefly
        print("\n⏳ Monitoring computational job...")
        compute_status = await check_job_status_tool(compute_job_id)
        print_json_result("📈 Computational Job Status", compute_status)

    # 9. List all current jobs
    print("\n📋 Step 9: Listing all current jobs...")
    all_jobs = await list_slurm_jobs_tool()
    print_json_result("📋 All Current Jobs", all_jobs)

    # 10. Check final queue status
    print("\n📊 Step 10: Final queue status check...")
    final_queue_info = await get_queue_info_tool()
    print_json_result("🏃 Final Queue Information", final_queue_info)

    print("\n" + "=" * 60)
    print("🏁 MCP Slurm Job Submission Demo Completed!")
    print("=" * 60)
    print("\n💡 Key Demonstrations:")
    print("   ✅ Real job submission through MCP tools")
    print("   ✅ Job status monitoring via MCP")
    print("   ✅ Job details retrieval through MCP")
    print("   ✅ Job output access via MCP")
    print("   ✅ Queue and cluster monitoring through MCP")
    print("   ✅ Multiple job types (simple and computational)")
    
    print("\n📁 Check the following for job outputs:")
    print("   - /tmp/mcp_demo_simple_<jobid>.out")
    print("   - /tmp/mcp_demo_simple_<jobid>.err")
    print("   - /tmp/mcp_demo_compute_<jobid>.out")
    print("   - /tmp/mcp_demo_compute_<jobid>.err")


if __name__ == "__main__":
    # Check if numpy is available for the computational demo
    try:
        import numpy
        print("✅ NumPy available for computational demo")
    except ImportError:
        print("⚠️ NumPy not available - computational demo will use basic shell commands")
    
    # Run the demo
    asyncio.run(main())
