#!/usr/bin/env python3
"""
Complete MCP Server Job Submission Demo
======================================
This script demonstrates:
1. Submitting jobs through MCP server (sbatch equivalent)
2. Getting job IDs and tracking them
3. Retrieving job information and status
4. Monitoring job progress
5. Getting job output and details
"""

import sys
import os
import json
import time
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def print_header(title):
    """Print formatted header."""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")

def print_job_result(title, result):
    """Print formatted job result."""
    print(f"\n📋 {title}:")
    print("-" * 50)
    if isinstance(result, dict):
        print(json.dumps(result, indent=2))
    else:
        print(result)
    print("-" * 50)

def create_test_job_script():
    """Create a test job script for submission."""
    script_content = """#!/bin/bash
#SBATCH --job-name=mcp_demo_job
#SBATCH --time=00:05:00
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --mem=2GB
#SBATCH --partition=compute

echo "=== MCP Server Job Submission Demo ==="
echo "Job ID: $SLURM_JOB_ID"
echo "Job Name: $SLURM_JOB_NAME"
echo "Node: $(hostname)"
echo "Date: $(date)"
echo "User: $(whoami)"
echo "Working Directory: $(pwd)"
echo "Number of CPUs: $SLURM_CPUS_ON_NODE"
echo "Memory per CPU: $SLURM_MEM_PER_CPU"
echo ""

echo "Starting computational work..."
for i in {1..10}; do
    echo "Processing step $i/10..."
    sleep 2
    echo "  - Completed step $i"
done

echo ""
echo "Job completed successfully!"
echo "End time: $(date)"
echo "Total execution time: $SECONDS seconds"
"""
    
    with open('mcp_demo_job.sh', 'w') as f:
        f.write(script_content)
    
    os.chmod('mcp_demo_job.sh', 0o755)
    print("✅ Created test job script: mcp_demo_job.sh")
    return 'mcp_demo_job.sh'

def submit_job_via_mcp(script_path, job_name, cores, memory, time_limit, partition):
    """Submit a job through MCP server."""
    print_header(f"Job Submission via MCP Server")
    
    try:
        from mcp_handlers import submit_slurm_job_handler
        
        print(f"🚀 Submitting job: {job_name}")
        print(f"   📄 Script: {script_path}")
        print(f"   💻 Cores: {cores}")
        print(f"   🧠 Memory: {memory}")
        print(f"   ⏰ Time: {time_limit}")
        print(f"   🔧 Partition: {partition}")
        
        # Submit job through MCP handler
        result = submit_slurm_job_handler(
            script_path=script_path,
            cores=cores,
            memory=memory,
            time_limit=time_limit,
            job_name=job_name,
            partition=partition
        )
        
        print_job_result("Job Submission Result", result)
        
        if result.get("job_id"):
            job_id = result["job_id"]
            print(f"\n✅ SUCCESS: Job submitted with ID: {job_id}")
            return job_id, result
        else:
            print(f"\n⚠️  Job submission issues: {result}")
            return None, result
            
    except Exception as e:
        print(f"\n❌ Error submitting job: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def get_job_information(job_id):
    """Get detailed job information."""
    print_header(f"Job Information for ID: {job_id}")
    
    try:
        from mcp_handlers import get_job_details_handler
        
        print(f"🔍 Retrieving details for job: {job_id}")
        
        result = get_job_details_handler(job_id=str(job_id))
        print_job_result(f"Job {job_id} Details", result)
        
        return result
        
    except Exception as e:
        print(f"❌ Error getting job info: {e}")
        return None

def list_all_jobs():
    """List all jobs in the queue."""
    print_header("All Jobs in Queue")
    
    try:
        from mcp_handlers import list_slurm_jobs_handler
        
        print("📋 Retrieving all jobs...")
        
        result = list_slurm_jobs_handler()
        print_job_result("All Jobs", result)
        
        return result
        
    except Exception as e:
        print(f"❌ Error listing jobs: {e}")
        return None

def get_job_output(job_id):
    """Get job output if available."""
    print_header(f"Job Output for ID: {job_id}")
    
    try:
        from mcp_handlers import get_job_output_handler
        
        print(f"📄 Retrieving output for job: {job_id}")
        
        result = get_job_output_handler(job_id=str(job_id))
        print_job_result(f"Job {job_id} Output", result)
        
        return result
        
    except Exception as e:
        print(f"❌ Error getting job output: {e}")
        return None

def get_cluster_info():
    """Get cluster information."""
    print_header("Cluster Information")
    
    try:
        from mcp_handlers import get_slurm_info_handler
        
        print("🏭 Retrieving cluster information...")
        
        result = get_slurm_info_handler()
        print_job_result("Cluster Info", result)
        
        return result
        
    except Exception as e:
        print(f"❌ Error getting cluster info: {e}")
        return None

def submit_multiple_jobs():
    """Submit multiple jobs for demonstration."""
    print_header("Multiple Job Submission Demo")
    
    job_configs = [
        {
            'name': 'small_job',
            'cores': 1,
            'memory': '1GB',
            'time': '00:02:00',
            'partition': 'compute'
        },
        {
            'name': 'medium_job',
            'cores': 4,
            'memory': '4GB',
            'time': '00:05:00',
            'partition': 'compute'
        },
        {
            'name': 'large_job',
            'cores': 8,
            'memory': '8GB',
            'time': '00:10:00',
            'partition': 'compute'
        }
    ]
    
    submitted_jobs = []
    
    for i, config in enumerate(job_configs, 1):
        print(f"\n🚀 Submitting job {i}/3: {config['name']}")
        
        job_id, result = submit_job_via_mcp(
            script_path='mcp_demo_job.sh',
            job_name=config['name'],
            cores=config['cores'],
            memory=config['memory'],
            time_limit=config['time'],
            partition=config['partition']
        )
        
        if job_id:
            submitted_jobs.append({
                'job_id': job_id,
                'name': config['name'],
                'config': config,
                'result': result
            })
            print(f"✅ Job {config['name']} submitted with ID: {job_id}")
        else:
            print(f"❌ Failed to submit job {config['name']}")
        
        time.sleep(1)  # Small delay between submissions
    
    return submitted_jobs

def run_complete_demo():
    """Run the complete MCP server job submission demo."""
    print_header("Complete MCP Server Job Submission Demo")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Get cluster information
    cluster_info = get_cluster_info()
    
    # Step 2: Create test job script
    script_path = create_test_job_script()
    
    # Step 3: Submit single job
    print_header("Single Job Submission")
    job_id, job_result = submit_job_via_mcp(
        script_path=script_path,
        job_name='mcp_single_demo',
        cores=2,
        memory='2GB',
        time_limit='00:03:00',
        partition='compute'
    )
    
    # Step 4: Get job information
    if job_id:
        job_info = get_job_information(job_id)
        
        # Step 5: Get job output (if available)
        job_output = get_job_output(job_id)
    
    # Step 6: Submit multiple jobs
    multiple_jobs = submit_multiple_jobs()
    
    # Step 7: List all jobs
    all_jobs = list_all_jobs()
    
    # Step 8: Get information for all submitted jobs
    if multiple_jobs:
        print_header("Information for All Submitted Jobs")
        for job in multiple_jobs:
            print(f"\n📊 Getting info for {job['name']} (ID: {job['job_id']})")
            get_job_information(job['job_id'])
            time.sleep(0.5)
    
    # Summary
    print_header("Demo Summary")
    total_jobs = 1 + len(multiple_jobs) if job_id else len(multiple_jobs)
    all_job_ids = [job_id] if job_id else []
    all_job_ids.extend([job['job_id'] for job in multiple_jobs])
    
    print(f"✅ Demo completed successfully!")
    print(f"📊 Total jobs submitted: {total_jobs}")
    print(f"🆔 Job IDs: {all_job_ids}")
    print(f"🏭 Cluster info retrieved: {'✅' if cluster_info else '❌'}")
    print(f"📋 All jobs listed: {'✅' if all_jobs else '❌'}")
    print(f"⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return {
        'total_jobs': total_jobs,
        'job_ids': all_job_ids,
        'cluster_info': cluster_info,
        'single_job_result': job_result,
        'multiple_jobs': multiple_jobs,
        'all_jobs': all_jobs
    }

if __name__ == "__main__":
    try:
        demo_results = run_complete_demo()
        print(f"\n🎉 All job submissions completed successfully!")
        print(f"📊 Total job IDs generated: {len(demo_results['job_ids'])}")
        print(f"🆔 Job IDs: {demo_results['job_ids']}")
        
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
