#!/usr/bin/env python3
"""
Simple Real Slurm Job Submission Demo through MCP
"""
import sys
import os
import asyncio
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from server import (
    submit_slurm_job_tool,
    check_job_status_tool,
    get_slurm_info_tool,
    list_slurm_jobs_tool
)

def create_test_script():
    """Create a simple test script."""
    script_content = """#!/bin/bash
#SBATCH --job-name=mcp_test
#SBATCH --output=mcp_test_%j.out
#SBATCH --error=mcp_test_%j.err
#SBATCH --time=00:01:00

echo "MCP Slurm Test Job"
echo "Started at: $(date)"
echo "Running on: $(hostname)"
echo "Job ID: $SLURM_JOB_ID"
sleep 30
echo "Completed at: $(date)"
"""
    
    script_path = "/tmp/mcp_test.sh"
    with open(script_path, 'w') as f:
        f.write(script_content)
    os.chmod(script_path, 0o755)
    return script_path

async def main():
    print("🎯 Simple MCP Slurm Job Demo")
    print("=" * 40)
    
    # Check cluster info
    print("\n1. Checking cluster info...")
    cluster_info = await get_slurm_info_tool()
    print(f"Cluster info: {json.dumps(cluster_info, indent=2)}")
    
    # Create and submit job
    print("\n2. Creating job script...")
    script_path = create_test_script()
    print(f"Created script: {script_path}")
    
    print("\n3. Submitting job...")
    result = await submit_slurm_job_tool(
        script_path=script_path,
        cores=1,
        memory="1GB",
        time_limit="00:01:00",
        job_name="mcp_test"
    )
    print(f"Submit result: {json.dumps(result, indent=2)}")
    
    if "job_id" in result:
        job_id = result["job_id"]
        print(f"\n4. Job submitted with ID: {job_id}")
        
        # Check status
        print("\n5. Checking job status...")
        status = await check_job_status_tool(job_id)
        print(f"Status: {json.dumps(status, indent=2)}")
    
    # List jobs
    print("\n6. Listing current jobs...")
    jobs = await list_slurm_jobs_tool()
    print(f"Jobs: {json.dumps(jobs, indent=2)}")
    
    print("\n✅ Demo completed!")

if __name__ == "__main__":
    asyncio.run(main())
