#!/usr/bin/env python3
"""
Complete Slurm MCP Server Demo with Job Submission and Response Testing
======================================================================
This script demonstrates:
1. Job submission with real job IDs
2. Job status checking
3. Job information retrieval
4. Queue monitoring
5. Complete MCP handler testing
"""

import sys
import os
import json
import time
import asyncio

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def print_header(title):
    """Print formatted header."""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")

def print_result(title, result):
    """Print formatted result."""
    print(f"\n📋 {title}:")
    print("-" * 40)
    if isinstance(result, dict):
        print(json.dumps(result, indent=2))
    else:
        print(result)
    print("-" * 40)

def test_job_submission():
    """Test job submission and get job ID."""
    print_header("Job Submission Demo")
    
    try:
        from mcp_handlers import submit_slurm_job_handler
        
        # Test job parameters
        job_params = {
            "script_content": "#!/bin/bash\n#SBATCH --job-name=mcp_test_job\n#SBATCH --time=00:05:00\n#SBATCH --nodes=1\n#SBATCH --ntasks=1\n\necho 'Hello from MCP Slurm Server!'\necho 'Current date:' $(date)\necho 'Running on node:' $(hostname)\nsleep 10\necho 'Job completed successfully!'",
            "job_name": "mcp_demo_job",
            "partition": "normal",
            "time_limit": "00:05:00",
            "nodes": 1,
            "ntasks": 1,
            "memory": "1GB"
        }
        
        print("🚀 Submitting job with parameters:")
        print(json.dumps(job_params, indent=2))
        
        # Submit job
        result = submit_slurm_job_handler(**job_params)
        print_result("Job Submission Result", result)
        
        # Extract job ID if successful
        if result.get("success") and "job_id" in result:
            job_id = result["job_id"]
            print(f"✅ Job submitted successfully with ID: {job_id}")
            return job_id
        else:
            print(f"⚠️  Job submission result: {result}")
            return None
            
    except Exception as e:
        print(f"❌ Error submitting job: {e}")
        return None

def test_job_info(job_id):
    """Test job information retrieval."""
    if not job_id:
        print("⚠️  No job ID available for info test")
        return
        
    print_header(f"Job Information for ID: {job_id}")
    
    try:
        from mcp_handlers import get_slurm_job_details_handler
        
        result = get_slurm_job_details_handler(job_id=str(job_id))
        print_result(f"Job {job_id} Details", result)
        
        return result
        
    except Exception as e:
        print(f"❌ Error getting job info: {e}")
        return None

def test_job_status(job_id):
    """Test job status checking."""
    if not job_id:
        print("⚠️  No job ID available for status test")
        return
        
    print_header(f"Job Status for ID: {job_id}")
    
    try:
        from mcp_handlers import list_slurm_jobs_handler
        
        # Get all jobs and find our job
        result = list_slurm_jobs_handler()
        print_result("All Jobs List", result)
        
        # Look for our specific job
        if result.get("success") and "jobs" in result:
            our_job = None
            for job in result["jobs"]:
                if str(job.get("job_id")) == str(job_id):
                    our_job = job
                    break
            
            if our_job:
                print_result(f"Our Job {job_id} Status", our_job)
            else:
                print(f"⚠️  Job {job_id} not found in job list")
        
        return result
        
    except Exception as e:
        print(f"❌ Error checking job status: {e}")
        return None

def test_queue_info():
    """Test queue information."""
    print_header("Queue Information")
    
    try:
        from mcp_handlers import get_queue_info_handler
        
        result = get_queue_info_handler()
        print_result("Queue Information", result)
        
        return result
        
    except Exception as e:
        print(f"❌ Error getting queue info: {e}")
        return None

def test_cluster_info():
    """Test cluster information."""
    print_header("Cluster Information")
    
    try:
        from mcp_handlers import get_slurm_info_handler
        
        result = get_slurm_info_handler()
        print_result("Cluster Information", result)
        
        return result
        
    except Exception as e:
        print(f"❌ Error getting cluster info: {e}")
        return None

def test_multiple_jobs():
    """Test submitting multiple jobs."""
    print_header("Multiple Job Submission Test")
    
    job_ids = []
    
    for i in range(3):
        try:
            from mcp_handlers import submit_slurm_job_handler
            
            job_params = {
                "script_content": f"#!/bin/bash\n#SBATCH --job-name=mcp_test_{i}\n#SBATCH --time=00:02:00\n#SBATCH --nodes=1\n#SBATCH --ntasks=1\n\necho 'Test job {i} running'\nsleep 5\necho 'Test job {i} completed'",
                "job_name": f"mcp_test_job_{i}",
                "time_limit": "00:02:00",
                "nodes": 1,
                "ntasks": 1
            }
            
            print(f"🚀 Submitting job {i+1}/3...")
            result = submit_slurm_job_handler(**job_params)
            
            if result.get("success") and "job_id" in result:
                job_id = result["job_id"]
                job_ids.append(job_id)
                print(f"✅ Job {i+1} submitted with ID: {job_id}")
            else:
                print(f"⚠️  Job {i+1} submission failed: {result}")
                
            time.sleep(1)  # Small delay between submissions
            
        except Exception as e:
            print(f"❌ Error submitting job {i+1}: {e}")
    
    print(f"\n📊 Summary: {len(job_ids)} jobs submitted successfully")
    print(f"Job IDs: {job_ids}")
    
    return job_ids

def run_comprehensive_demo():
    """Run the complete demonstration."""
    print_header("Complete Slurm MCP Server Demo")
    
    # Test 1: Cluster and Queue Information
    cluster_info = test_cluster_info()
    queue_info = test_queue_info()
    
    # Test 2: Single Job Submission
    job_id = test_job_submission()
    
    if job_id:
        # Test 3: Job Information and Status
        time.sleep(2)  # Give job time to be processed
        job_info = test_job_info(job_id)
        job_status = test_job_status(job_id)
    
    # Test 4: Multiple Job Submission
    multiple_job_ids = test_multiple_jobs()
    
    # Test 5: Final Status Check
    if multiple_job_ids:
        print_header("Final Status Check for All Jobs")
        for jid in multiple_job_ids:
            test_job_info(jid)
            time.sleep(1)
    
    # Summary
    print_header("Demo Summary")
    total_jobs = 1 + len(multiple_job_ids) if job_id else len(multiple_job_ids)
    print(f"✅ Demo completed successfully!")
    print(f"📊 Total jobs submitted: {total_jobs}")
    print(f"🆔 Job IDs: {[job_id] + multiple_job_ids if job_id else multiple_job_ids}")
    print(f"🔧 Cluster info retrieved: {'✅' if cluster_info else '❌'}")
    print(f"📊 Queue info retrieved: {'✅' if queue_info else '❌'}")

if __name__ == "__main__":
    try:
        run_comprehensive_demo()
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
