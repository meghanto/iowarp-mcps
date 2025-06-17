#!/usr/bin/env python3
"""
Real Slurm MCP Server Demo
Demonstrates all the advanced Slurm MCP capabilities
"""
import sys
import os
import asyncio
import tempfile
import json

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


def create_demo_script(script_name: str, script_content: str) -> str:
    """Create a demo script file."""
    script_path = f"/tmp/{script_name}"
    with open(script_path, 'w') as f:
        f.write(script_content)
    os.chmod(script_path, 0o755)
    return script_path


async def demo_basic_job_submission():
    """Demonstrate basic job submission."""
    print("🚀 Demo: Basic Job Submission")
    print("-" * 40)
    
    # Create a simple test script
    script_content = """#!/bin/bash
#SBATCH --job-name=basic_demo
echo "Basic demo job started on $(hostname)"
echo "Current time: $(date)"
echo "Working directory: $(pwd)"
echo "Job ID: $SLURM_JOB_ID"
sleep 5
echo "Basic demo job completed successfully"
"""
    
    script_path = create_demo_script("basic_demo.sh", script_content)
    
    try:
        # Submit the job
        result = await submit_slurm_job_tool(
            script_path=script_path,
            cores=2,
            memory="1GB",
            time_limit="00:10:00",
            job_name="basic_demo_job"
        )
        
        print(f"📋 Job submission result:")
        print(json.dumps(result, indent=2))
        
        return result.get("job_id") if result else None
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


async def demo_enhanced_job_submission():
    """Demonstrate enhanced job submission with all parameters."""
    print("\n🚀 Demo: Enhanced Job Submission")
    print("-" * 40)
    
    # Create a more complex test script
    script_content = """#!/bin/bash
echo "Enhanced demo job started"
echo "========================================="
echo "SLURM Environment Variables:"
echo "  Job ID: $SLURM_JOB_ID"
echo "  Job Name: $SLURM_JOB_NAME"
echo "  CPUs per task: $SLURM_CPUS_PER_TASK"
echo "  Memory per node: $SLURM_MEM_PER_NODE MB"
echo "  Partition: $SLURM_JOB_PARTITION"
echo "  Submit directory: $SLURM_SUBMIT_DIR"
echo "========================================="
echo "System Information:"
echo "  Hostname: $(hostname)"
echo "  OS: $(uname -a)"
echo "  CPU count: $(nproc)"
echo "  Memory: $(free -h | grep Mem)"
echo "========================================="
echo "Running computational task..."
for i in {1..10}; do
    echo "  Processing step $i/10"
    sleep 2
done
echo "Enhanced demo job completed successfully"
"""
    
    script_path = create_demo_script("enhanced_demo.sh", script_content)
    
    try:
        # Submit the job with all parameters
        result = await submit_slurm_job_tool(
            script_path=script_path,
            cores=4,
            memory="4GB",
            time_limit="00:15:00",
            job_name="enhanced_demo_job",
            partition="compute"  # This may not exist, but demonstrates parameter passing
        )
        
        print(f"📋 Enhanced job submission result:")
        print(json.dumps(result, indent=2))
        
        return result.get("job_id") if result else None
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


async def demo_array_job_submission():
    """Demonstrate array job submission."""
    print("\n🚀 Demo: Array Job Submission")
    print("-" * 40)
    
    # Create an array job script
    script_content = """#!/bin/bash
echo "Array job task $SLURM_ARRAY_TASK_ID started"
echo "Array Job ID: $SLURM_ARRAY_JOB_ID"
echo "Task ID: $SLURM_ARRAY_TASK_ID"
echo "Total tasks: $SLURM_ARRAY_TASK_COUNT"
echo "Processing task-specific data..."

# Simulate different processing times for each task
sleep_time=$((SLURM_ARRAY_TASK_ID * 3))
echo "Task $SLURM_ARRAY_TASK_ID will sleep for $sleep_time seconds"
sleep $sleep_time

echo "Task $SLURM_ARRAY_TASK_ID completed successfully"
"""
    
    script_path = create_demo_script("array_demo.sh", script_content)
    
    try:
        # Submit the array job
        result = await submit_array_job_tool(
            script_path=script_path,
            array_range="1-5",
            cores=1,
            memory="1GB",
            time_limit="00:10:00",
            job_name="array_demo_job"
        )
        
        print(f"📋 Array job submission result:")
        print(json.dumps(result, indent=2))
        
        return result.get("array_job_id") if result else None
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


async def demo_job_monitoring(job_id: str):
    """Demonstrate job monitoring capabilities."""
    print(f"\n📊 Demo: Job Monitoring for Job {job_id}")
    print("-" * 40)
    
    try:
        # Check job status
        status = await check_job_status_tool(job_id)
        print(f"📈 Job Status:")
        print(json.dumps(status, indent=2))
        
        # Get detailed job information
        details = await get_job_details_tool(job_id)
        print(f"\n🔍 Job Details:")
        print(json.dumps(details, indent=2))
        
        # Get job output (if available)
        stdout = await get_job_output_tool(job_id, "stdout")
        print(f"\n📄 Job Output (stdout):")
        print(json.dumps(stdout, indent=2))
        
        stderr = await get_job_output_tool(job_id, "stderr")
        print(f"\n📄 Job Output (stderr):")
        print(json.dumps(stderr, indent=2))
        
    except Exception as e:
        print(f"❌ Error: {e}")


async def demo_cluster_information():
    """Demonstrate cluster information retrieval."""
    print("\n🖥️ Demo: Cluster Information")
    print("-" * 40)
    
    try:
        # Get cluster information
        cluster_info = await get_slurm_info_tool()
        print(f"🏢 Cluster Information:")
        print(json.dumps(cluster_info, indent=2))
        
        # Get node information
        node_info = await get_node_info_tool()
        print(f"\n🖥️ Node Information:")
        print(json.dumps(node_info, indent=2))
        
        # Get queue information
        queue_info = await get_queue_info_tool()
        print(f"\n🏃 Queue Information:")
        print(json.dumps(queue_info, indent=2))
        
        # Get queue information for specific partition (if it exists)
        queue_info_compute = await get_queue_info_tool("compute")
        print(f"\n🏃 Queue Information (compute partition):")
        print(json.dumps(queue_info_compute, indent=2))
        
    except Exception as e:
        print(f"❌ Error: {e}")


async def demo_job_management():
    """Demonstrate job management capabilities."""
    print("\n🔧 Demo: Job Management")
    print("-" * 40)
    
    try:
        # List all jobs
        all_jobs = await list_slurm_jobs_tool()
        print(f"📋 All Jobs:")
        print(json.dumps(all_jobs, indent=2))
        
        # List jobs by user
        user_jobs = await list_slurm_jobs_tool(user="testuser")
        print(f"\n📋 Jobs for user 'testuser':")
        print(json.dumps(user_jobs, indent=2))
        
        # List running jobs
        running_jobs = await list_slurm_jobs_tool(state="RUNNING")
        print(f"\n📋 Running Jobs:")
        print(json.dumps(running_jobs, indent=2))
        
        # List pending jobs
        pending_jobs = await list_slurm_jobs_tool(state="PENDING")
        print(f"\n📋 Pending Jobs:")
        print(json.dumps(pending_jobs, indent=2))
        
    except Exception as e:
        print(f"❌ Error: {e}")


async def demo_job_cancellation(job_id: str):
    """Demonstrate job cancellation."""
    print(f"\n❌ Demo: Job Cancellation for Job {job_id}")
    print("-" * 40)
    
    try:
        # Cancel the job
        result = await cancel_slurm_job_tool(job_id)
        print(f"🛑 Job cancellation result:")
        print(json.dumps(result, indent=2))
        
        # Check status after cancellation
        status = await check_job_status_tool(job_id)
        print(f"\n📈 Job Status after cancellation:")
        print(json.dumps(status, indent=2))
        
    except Exception as e:
        print(f"❌ Error: {e}")


async def main():
    """Run comprehensive Slurm MCP demo."""
    print("🎭 Comprehensive Slurm MCP Server Demo")
    print("=" * 60)
    print("This demo showcases all advanced Slurm MCP capabilities")
    print("=" * 60)
    
    # Demonstrate cluster information first
    await demo_cluster_information()
    
    # Demonstrate job management
    await demo_job_management()
    
    # Submit different types of jobs
    basic_job_id = await demo_basic_job_submission()
    enhanced_job_id = await demo_enhanced_job_submission()
    array_job_id = await demo_array_job_submission()
    
    # Wait a bit for jobs to start
    print("\n⏳ Waiting 10 seconds for jobs to initialize...")
    await asyncio.sleep(10)
    
    # Monitor jobs if they were submitted successfully
    if basic_job_id:
        await demo_job_monitoring(basic_job_id)
    
    if enhanced_job_id and enhanced_job_id != basic_job_id:
        await demo_job_monitoring(enhanced_job_id)
    
    if array_job_id:
        await demo_job_monitoring(array_job_id)
    
    # Demonstrate job management again to see current state
    await demo_job_management()
    
    # Cancel jobs
    if basic_job_id:
        await demo_job_cancellation(basic_job_id)
    
    if enhanced_job_id and enhanced_job_id != basic_job_id:
        await demo_job_cancellation(enhanced_job_id)
    
    if array_job_id:
        await demo_job_cancellation(array_job_id)
    
    print("\n" + "=" * 60)
    print("🏁 Slurm MCP Demo completed!")
    print("=" * 60)
    
    # Cleanup
    for script in ["basic_demo.sh", "enhanced_demo.sh", "array_demo.sh"]:
        script_path = f"/tmp/{script}"
        if os.path.exists(script_path):
            os.unlink(script_path)
    
    print("\n💡 Key Features Demonstrated:")
    print("   ✅ Basic job submission with parameters")
    print("   ✅ Enhanced job submission with all options")
    print("   ✅ Array job submission")
    print("   ✅ Job status monitoring")
    print("   ✅ Detailed job information")
    print("   ✅ Job output retrieval")
    print("   ✅ Cluster information")
    print("   ✅ Node information")
    print("   ✅ Queue monitoring")
    print("   ✅ Job listing and filtering")
    print("   ✅ Job cancellation")
    
    print("\n🔧 Real vs Mock Slurm:")
    print("   - If Slurm is installed: Uses real sbatch, squeue, scancel commands")
    print("   - If Slurm is not available: Uses mock implementation for testing")
    
    print("\n🚀 Next Steps:")
    print("   1. Install Slurm to test real integration")
    print("   2. Modify scripts in /tmp/ for your specific use case")
    print("   3. Use the MCP server in your applications")
    print("   4. Check slurm-*.out files for job output")


if __name__ == "__main__":
    asyncio.run(main())
