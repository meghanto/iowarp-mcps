#!/usr/bin/env python3
"""
Step-by-step demonstration of Slurm MCP capabilities.
Shows both real and mock Slurm job execution with clear output.
"""
import sys
import os
import time
import tempfile

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from capabilities.slurm_handler import (
    submit_slurm_job, 
    get_job_status, 
    list_slurm_jobs,
    get_slurm_info,
    _check_slurm_available
)

def create_sample_job_script():
    """Create a sample job script for demonstration."""
    script_content = """#!/bin/bash
echo "=== Job Information ==="
echo "Job started at: $(date)"
echo "Running on node: $(hostname)"
echo "Current directory: $(pwd)"
echo "Job ID: $SLURM_JOB_ID"
echo "======================="

echo "Performing sample computation..."
# Simulate some work
for i in {1..5}; do
    echo "Processing step $i/5..."
    sleep 2
done

echo "=== Job Complete ==="
echo "Job finished at: $(date)"
echo "===================="
"""
    
    # Create temporary script file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
        f.write(script_content)
        script_path = f.name
    
    # Make script executable
    os.chmod(script_path, 0o755)
    return script_path

def demonstrate_job_submission():
    """Demonstrate job submission with both real and mock Slurm."""
    print("🚀 Slurm MCP Capabilities Demonstration")
    print("=" * 60)
    
    # Check Slurm availability
    is_real_slurm = _check_slurm_available()
    print(f"📋 Slurm Detection:")
    print(f"   - Commands available: {is_real_slurm}")
    
    if is_real_slurm:
        print("   - Will attempt real Slurm, fallback to mock if cluster unavailable")
    else:
        print("   - Using mock implementation")
    print()
    
    # Get cluster information
    print("🖥️  Cluster Information:")
    cluster_info = get_slurm_info()
    print(f"   - Real Slurm: {cluster_info.get('real_slurm', 'Unknown')}")
    print(f"   - Cluster: {cluster_info.get('cluster_name', 'Unknown')}")
    if 'partitions' in cluster_info:
        print(f"   - Partitions: {len(cluster_info['partitions'])} available")
    if 'error' in cluster_info:
        print(f"   - Note: {cluster_info['error'][:50]}...")
    print()
    
    # Create job script
    print("📝 Creating Sample Job Script...")
    script_path = create_sample_job_script()
    print(f"   - Script created: {script_path}")
    print()
    
    # Submit basic job
    print("🎯 Submitting Basic Job...")
    try:
        job_id = submit_slurm_job(
            script_path=script_path,
            cores=2,
            memory="1GB",
            time_limit="00:05:00",
            job_name="demo_basic_job"
        )
        print(f"   ✅ Job submitted successfully!")
        print(f"   - Job ID: {job_id}")
        print()
        
        # Check job status
        print("📊 Checking Job Status...")
        status = get_job_status(job_id)
        print(f"   - Status: {status.get('status', 'Unknown')}")
        print(f"   - Reason: {status.get('reason', 'N/A')}")
        print(f"   - Real Slurm: {status.get('real_slurm', 'Unknown')}")
        print()
        
        # Submit enhanced job
        print("⚡ Submitting Enhanced Job...")
        enhanced_job_id = submit_slurm_job(
            script_path=script_path,
            cores=4,
            memory="2GB",
            time_limit="00:10:00",
            job_name="demo_enhanced_job",
            partition="compute"
        )
        print(f"   ✅ Enhanced job submitted!")
        print(f"   - Job ID: {enhanced_job_id}")
        print()
        
        # List all jobs
        print("📋 Listing All Jobs...")
        jobs = list_slurm_jobs()
        print(f"   - Total jobs found: {jobs.get('count', len(jobs.get('jobs', [])))}")
        print(f"   - Real Slurm: {jobs.get('real_slurm', 'Unknown')}")
        
        if 'jobs' in jobs and jobs['jobs']:
            print("   - Recent jobs:")
            for job in jobs['jobs'][:3]:  # Show first 3 jobs
                print(f"     * {job.get('job_id', 'N/A')} - {job.get('state', 'Unknown')} - {job.get('name', 'N/A')}")
        
        if 'error' in jobs:
            print(f"   - Note: Using fallback data due to: {jobs['error'][:50]}...")
        print()
        
        # Monitor job for a few iterations
        print("🔍 Monitoring Job Progress...")
        for i in range(3):
            status = get_job_status(job_id)
            print(f"   Check {i+1}: {status.get('status', 'Unknown')} - {status.get('reason', 'N/A')}")
            time.sleep(2)
        print()
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        print()
    
    finally:
        # Cleanup
        if os.path.exists(script_path):
            os.unlink(script_path)
            print("🧹 Cleaned up temporary script")

def demonstrate_mcp_integration():
    """Demonstrate MCP server integration."""
    print("\n🔌 MCP Server Integration")
    print("=" * 60)
    
    print("📡 Available MCP Tools:")
    mcp_tools = [
        "submit_slurm_job_tool",
        "check_job_status_tool", 
        "cancel_slurm_job_tool",
        "list_slurm_jobs_tool",
        "get_slurm_info_tool",
        "get_job_details_tool",
        "get_job_output_tool",
        "get_queue_info_tool",
        "submit_array_job_tool",
        "get_node_info_tool"
    ]
    
    for i, tool in enumerate(mcp_tools, 1):
        print(f"   {i:2d}. {tool}")
    
    print(f"\n📋 Server Startup Commands:")
    print("   # Stdio mode (default):")
    print("   python src/server.py")
    print()
    print("   # HTTP/SSE mode:")
    print("   MCP_TRANSPORT=sse MCP_HOST=localhost MCP_PORT=8000 python src/server.py")
    print()

def main():
    """Main demonstration function."""
    try:
        demonstrate_job_submission()
        demonstrate_mcp_integration()
        
        print("🎉 Demonstration Complete!")
        print("=" * 60)
        print("💡 Key Points:")
        print("   - System automatically detects Slurm availability")
        print("   - Falls back to mock mode when real Slurm unavailable")
        print("   - All MCP tools work in both real and mock modes")
        print("   - Complete job lifecycle supported")
        print("   - Ready for production use!")
        print()
        print("🚀 Next Steps:")
        print("   - Run full demo: python demo_real_slurm.py")
        print("   - Run tests: python -m pytest tests/ -v")
        print("   - Start MCP server: python src/server.py")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("💡 This is expected if dependencies are missing")

if __name__ == "__main__":
    main()
