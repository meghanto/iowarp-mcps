#!/usr/bin/env python3
"""
Simple Slurm Job Submission Demo
Shows exactly how to submit real Slurm jobs using MCP capabilities
"""

import os
import sys
import tempfile
import json

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def demo_job_submission():
    """Demonstrate job submission step by step."""
    
    print("🎯 Slurm Job Submission via MCP Demo")
    print("=" * 50)
    
    # Import MCP handlers
    from mcp_handlers import submit_slurm_job_handler, check_job_status_handler
    from capabilities.slurm_handler import _check_slurm_available
    
    # Check Slurm availability
    is_real_slurm = _check_slurm_available()
    print(f"🔍 Slurm Available: {'YES (will try real, fallback to mock)' if is_real_slurm else 'NO (using mock)'}")
    
    # Create a simple job script
    script_content = """#!/bin/bash
echo "🚀 Job started at: $(date)"
echo "🖥️ Running on: $(hostname)"
echo "🔄 Doing some work..."
sleep 2
echo "✅ Job completed at: $(date)"
"""
    
    # Write script to temporary file
    fd, script_path = tempfile.mkstemp(suffix='.sh', prefix='demo_job_')
    with os.fdopen(fd, 'w') as f:
        f.write(script_content)
    os.chmod(script_path, 0o755)
    
    print(f"📝 Created job script: {script_path}")
    print(f"📄 Script content:\n{script_content}")
    
    # Submit the job
    print("🚀 Submitting job...")
    try:
        result = submit_slurm_job_handler(
            script_path=script_path,
            cores=1,
            memory="512MB",
            time_limit="00:02:00",
            job_name="demo_job"
        )
        
        print("✅ Job Submission Result:")
        print(json.dumps(result, indent=2))
        
        # If job was submitted successfully, check its status
        if "job_id" in result:
            job_id = result["job_id"]
            print(f"\n🔍 Checking status of job {job_id}...")
            
            status = check_job_status_handler(job_id)
            print("📊 Job Status:")
            print(json.dumps(status, indent=2))
            
        else:
            print("❌ No job ID returned - submission may have failed")
            
    except Exception as e:
        print(f"❌ Error during job submission: {e}")
    
    finally:
        # Cleanup
        try:
            os.unlink(script_path)
            print(f"\n🧹 Cleaned up script file")
        except:
            pass

if __name__ == "__main__":
    demo_job_submission()
