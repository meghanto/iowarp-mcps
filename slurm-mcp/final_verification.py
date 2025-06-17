#!/usr/bin/env python3
"""
Final Verification Script - Slurm MCP Server
===========================================
This script verifies that all components are working correctly.
"""

import sys
import os
import json
import subprocess

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def check_server_running():
    """Check if server is running."""
    try:
        with open('server.pid', 'r') as f:
            pid = f.read().strip()
        
        # Check if process exists
        subprocess.run(['kill', '-0', pid], check=True, capture_output=True)
        print(f"✅ Server is running (PID: {pid})")
        return True
    except:
        print("❌ Server is not running")
        return False

def test_job_submission():
    """Test job submission functionality."""
    try:
        from mcp_handlers import submit_slurm_job_handler
        
        result = submit_slurm_job_handler(
            script_path='test_job.sh',
            cores=1,
            memory='1G',
            time_limit='00:01:00',
            job_name='final_verification_job',
            partition='normal'
        )
        
        if 'job_id' in result:
            print(f"✅ Job submission successful - ID: {result['job_id']}")
            return result['job_id']
        else:
            print("❌ Job submission failed")
            return None
    except Exception as e:
        print(f"❌ Job submission error: {e}")
        return None

def test_job_info(job_id):
    """Test job information retrieval."""
    try:
        from mcp_handlers import get_job_details_handler
        
        result = get_job_details_handler(job_id=str(job_id))
        print(f"✅ Job details retrieved for ID: {job_id}")
        return True
    except Exception as e:
        print(f"❌ Job details error: {e}")
        return False

def test_cluster_info():
    """Test cluster information."""
    try:
        from mcp_handlers import get_slurm_info_handler
        
        result = get_slurm_info_handler()
        print("✅ Cluster information retrieved")
        return True
    except Exception as e:
        print(f"❌ Cluster info error: {e}")
        return False

def main():
    print("🎯 Final Verification of Slurm MCP Server")
    print("="*50)
    
    results = {}
    
    # Test 1: Server running
    print("\n1. Checking server status...")
    results['server_running'] = check_server_running()
    
    # Test 2: Cluster info
    print("\n2. Testing cluster information...")
    results['cluster_info'] = test_cluster_info()
    
    # Test 3: Job submission
    print("\n3. Testing job submission...")
    job_id = test_job_submission()
    results['job_submission'] = job_id is not None
    
    # Test 4: Job information
    if job_id:
        print("\n4. Testing job information...")
        results['job_info'] = test_job_info(job_id)
    else:
        results['job_info'] = False
    
    # Summary
    print("\n" + "="*50)
    print("📊 VERIFICATION SUMMARY")
    print("="*50)
    
    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test.replace('_', ' ').title()}: {status}")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print(f"\nTests Passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED - SYSTEM FULLY OPERATIONAL!")
        return 0
    else:
        print(f"\n⚠️  {total_tests - passed_tests} tests failed")
        return 1

if __name__ == "__main__":
    exit(main())
