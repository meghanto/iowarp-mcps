#!/usr/bin/env python3
"""
Practical Demo: How to Submit Real Slurm Jobs using MCP Capabilities
====================================================================

This script demonstrates step-by-step how to submit jobs to Slurm using 
the MCP (Model Context Protocol) server capabilities.

It shows both REAL Slurm integration and MOCK fallback functionality.
"""

import os
import sys
import tempfile
import time
import json

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import MCP handlers (these are the main interfaces)
from mcp_handlers import (
    submit_slurm_job_handler,
    check_job_status_handler,
    list_slurm_jobs_handler,
    get_slurm_info_handler,
    cancel_slurm_job_handler,
    get_job_details_handler,
    get_job_output_handler
)

# Import core capabilities 
from capabilities.slurm_handler import _check_slurm_available

def print_header(title):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")

def print_step(step_num, description):
    """Print a formatted step."""
    print(f"\n📋 Step {step_num}: {description}")
    print("-" * 50)

def print_result(data, title="Result"):
    """Print formatted JSON result."""
    print(f"\n✅ {title}:")
    print(json.dumps(data, indent=2))

def create_sample_job_script():
    """Create a sample job script for demonstration."""
    script_content = """#!/bin/bash
#
# Sample Slurm Job Script
# This script demonstrates basic job execution
#

echo "🚀 Job started at: $(date)"
echo "🖥️ Running on node: $(hostname)"
echo "👤 User: $(whoami)"
echo "📁 Working directory: $(pwd)"

# Simulate some work
echo "🔄 Processing data..."
for i in {1..5}; do
    echo "  Processing item $i/5"
    sleep 1
done

echo "✅ Job completed at: $(date)"
echo "📊 Job statistics:"
echo "  - Duration: ~5 seconds"
echo "  - Items processed: 5"
echo "  - Status: SUCCESS"
"""

    # Create temporary script file
    fd, script_path = tempfile.mkstemp(suffix='.sh', prefix='mcp_demo_job_')
    with os.fdopen(fd, 'w') as f:
        f.write(script_content)
    
    # Make script executable
    os.chmod(script_path, 0o755)
    return script_path

def demonstrate_slurm_job_submission():
    """Complete demonstration of Slurm job submission via MCP."""
    
    print_header("Slurm Job Submission via MCP Capabilities")
    
    # Check Slurm availability
    is_real_slurm = _check_slurm_available()
    print(f"\n🔍 Slurm Detection:")
    print(f"   Real Slurm Available: {'✅ YES' if is_real_slurm else '❌ NO'}")
    if is_real_slurm:
        print(f"   Mode: REAL Slurm Integration")
        print(f"   Note: Will fall back to MOCK if cluster not configured")
    else:
        print(f"   Mode: MOCK Simulation")
        print(f"   Note: Install Slurm for real job submission")
    
    # Step 1: Get cluster information
    print_step(1, "Get Cluster Information")
    cluster_info = get_slurm_info_handler()
    print_result(cluster_info, "Cluster Information")
    
    # Step 2: Check current job queue
    print_step(2, "Check Current Job Queue")
    current_jobs = list_slurm_jobs_handler()
    print_result(current_jobs, "Current Jobs")
    
    # Step 3: Create and submit a job
    print_step(3, "Create and Submit Job")
    script_path = create_sample_job_script()
    print(f"📝 Created job script: {script_path}")
    
    # Show script content
    print(f"\n📄 Job Script Content:")
    with open(script_path, 'r') as f:
        print("```bash")
        print(f.read())
        print("```")
    
    # Submit the job using MCP handler
    print(f"\n🚀 Submitting job via MCP...")
    job_result = submit_slurm_job_handler(
        script_path=script_path,
        cores=2,
        memory="1GB",
        time_limit="00:05:00",
        job_name="mcp_demo_job",
        partition=None  # Use default partition
    )
    print_result(job_result, "Job Submission Result")
    
    # Extract job ID for monitoring
    if "job_id" in job_result:
        job_id = job_result["job_id"]
        
        # Step 4: Monitor job status
        print_step(4, f"Monitor Job Status (ID: {job_id})")
        
        # Check status multiple times
        for check_num in range(1, 4):
            print(f"\n🔍 Status Check #{check_num}:")
            status = check_job_status_handler(job_id)
            print_result(status, f"Status Check #{check_num}")
            
            if check_num < 3:
                print("⏳ Waiting 3 seconds before next check...")
                time.sleep(3)
        
        # Step 5: Get detailed job information
        print_step(5, "Get Detailed Job Information")
        job_details = get_job_details_handler(job_id)
        print_result(job_details, "Job Details")
        
        # Step 6: Try to get job output
        print_step(6, "Retrieve Job Output")
        for output_type in ["stdout", "stderr"]:
            print(f"\n📋 Getting {output_type}:")
            output = get_job_output_handler(job_id, output_type)
            print_result(output, f"Job {output_type.upper()}")
        
        # Step 7: Demonstrate job cancellation (optional)
        print_step(7, "Job Management - Cancel Job")
        print("🛑 Attempting to cancel job (for demonstration)...")
        cancel_result = cancel_slurm_job_handler(job_id)
        print_result(cancel_result, "Cancellation Result")
        
        # Final status check
        print(f"\n🔍 Final Status Check:")
        final_status = check_job_status_handler(job_id)
        print_result(final_status, "Final Status")
    
    else:
        print("❌ Job submission failed - no job ID returned")
    
    # Step 8: List all jobs after submission
    print_step(8, "Final Job Queue Status")
    final_jobs = list_slurm_jobs_handler()
    print_result(final_jobs, "Final Job List")
    
    # Cleanup
    print(f"\n🧹 Cleaning up temporary script: {script_path}")
    try:
        os.unlink(script_path)
        print("✅ Cleanup completed")
    except:
        print("⚠️ Could not remove temporary script")

def show_mcp_api_usage():
    """Show how to use the MCP API programmatically."""
    
    print_header("MCP API Usage Examples")
    
    print("""
📚 How to Use MCP Handlers Programmatically:

1. Import the MCP handlers:
   ```python
   from mcp_handlers import (
       submit_slurm_job_handler,
       check_job_status_handler,
       list_slurm_jobs_handler,
       get_slurm_info_handler
   )
   ```

2. Submit a job:
   ```python
   result = submit_slurm_job_handler(
       script_path="/path/to/script.sh",
       cores=4,
       memory="8GB",
       time_limit="01:00:00",
       job_name="my_job",
       partition="compute"
   )
   job_id = result["job_id"]
   ```

3. Check job status:
   ```python
   status = check_job_status_handler(job_id)
   print(f"Job status: {status['status']}")
   ```

4. List all jobs:
   ```python
   jobs = list_slurm_jobs_handler()
   print(f"Total jobs: {jobs['count']}")
   ```

5. Get cluster info:
   ```python
   cluster = get_slurm_info_handler()
   print(f"Cluster: {cluster['cluster_name']}")
   ```

🔧 Real vs Mock Behavior:
- If Slurm is properly configured: Uses real sbatch, squeue, etc.
- If Slurm is not available/configured: Uses realistic mock simulation
- API remains identical regardless of mode
- Automatic fallback ensures your code always works
""")

def main():
    """Main demonstration function."""
    print("🎯 Slurm MCP Job Submission Demonstration")
    print("=" * 60)
    print("This demo shows how to submit and manage Slurm jobs using MCP capabilities.")
    print("It works with both REAL Slurm clusters and MOCK simulation.")
    
    try:
        # Show API usage
        show_mcp_api_usage()
        
        # Run the demonstration
        demonstrate_slurm_job_submission()
        
        print_header("Demonstration Complete! 🎉")
        print("""
✅ What you just saw:
   • Cluster information retrieval
   • Job queue monitoring
   • Job script creation and submission
   • Real-time job status monitoring
   • Detailed job information retrieval
   • Job output access
   • Job cancellation capabilities

🚀 Next Steps:
   • Modify the job script for your use case
   • Integrate MCP handlers into your applications
   • Use the MCP server with AI agents
   • Deploy on real Slurm clusters for production
        """)
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        print("This might indicate a configuration issue.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
