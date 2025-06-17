#!/usr/bin/env python3
"""
Quick demo showing real vs mock Slurm job execution output.
"""
import sys
import os
import tempfile

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from capabilities.slurm_handler import submit_slurm_job, get_job_status, _check_slurm_available
    
    print("🎯 Slurm MCP Quick Demo")
    print("=" * 40)
    
    # Check what mode we're in
    has_slurm = _check_slurm_available()
    print(f"Slurm commands available: {has_slurm}")
    
    # Create a simple test script
    with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
        f.write("#!/bin/bash\necho 'Hello from Slurm job!'\nsleep 5\necho 'Job complete!'\n")
        script_path = f.name
    os.chmod(script_path, 0o755)
    
    try:
        # Submit a job
        print("\n📤 Submitting job...")
        job_id = submit_slurm_job(script_path, cores=1, job_name="quick_demo")
        print(f"Job ID: {job_id}")
        
        # Check status
        print("\n📊 Checking status...")
        status = get_job_status(job_id)
        print(f"Status: {status}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        os.unlink(script_path)
        
    print("\n✅ Demo complete!")

except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're in the slurm-mcp directory")
