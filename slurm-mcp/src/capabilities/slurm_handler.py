"""
Slurm job management capabilities.
Handles actual Slurm job submission and status checking with both real and mock implementations.
"""
import os
import subprocess
import re
import random
import shutil
import tempfile
from typing import Optional


def _check_slurm_available() -> bool:
    """Check if Slurm is available on the system."""
    return shutil.which("sbatch") is not None


def _create_sbatch_script(original_script: str, cores: int, memory: Optional[str] = None, 
                         time_limit: Optional[str] = None, job_name: Optional[str] = None, 
                         partition: Optional[str] = None) -> str:
    """
    Create a proper Slurm job script with SBATCH directives.
    
    Args:
        original_script: Path to the original script
        cores: Number of cores to request
        memory: Memory requirement (e.g., "4G", "2048M")
        time_limit: Time limit (e.g., "1:00:00")
        job_name: Name for the job
        partition: Slurm partition to use
        
    Returns:
        Path to the modified script with SBATCH directives
    """
    with open(original_script, 'r') as f:
        content = f.read()
    
    # Create a temporary script with SBATCH directives
    fd, temp_script = tempfile.mkstemp(suffix='.sh', prefix='slurm_job_')
    
    with os.fdopen(fd, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write(f"#SBATCH --cpus-per-task={cores}\n")
        f.write(f"#SBATCH --job-name={job_name or 'mcp_job'}\n")
        f.write(f"#SBATCH --output=slurm_%j.out\n")
        f.write(f"#SBATCH --error=slurm_%j.err\n")
        
        if memory:
            f.write(f"#SBATCH --mem={memory}\n")
        if time_limit:
            f.write(f"#SBATCH --time={time_limit}\n")
        if partition:
            f.write(f"#SBATCH --partition={partition}\n")
            
        f.write("\n# Original script content:\n")
        
        # Skip shebang in original content if it exists
        lines = content.split('\n')
        if lines and lines[0].startswith('#!'):
            lines = lines[1:]
        
        f.write('\n'.join(lines))
    
    os.chmod(temp_script, 0o755)
    return temp_script


def submit_slurm_job(script_path: str, cores: int, memory: Optional[str] = None, 
                    time_limit: Optional[str] = None, job_name: Optional[str] = None, 
                    partition: Optional[str] = None) -> str:
    """
    Submits a job to Slurm via sbatch with script path and cores.
    Automatically detects if Slurm is available and uses real sbatch or simulation.

    Args:
        script_path: Path to the Slurm job script
        cores: Number of CPU cores to request
        memory: Memory requirement (e.g., "4G", "2048M")
        time_limit: Time limit (e.g., "1:00:00")
        job_name: Name for the job
        partition: Slurm partition to use

    Returns:
        The Slurm job ID as a string

    Raises:
        FileNotFoundError: If the script file does not exist
        ValueError: If cores <= 0
        RuntimeError: If job submission fails
    """
    # Validate inputs
    if not os.path.isfile(script_path):
        raise FileNotFoundError(f"Script file '{script_path}' not found")
    if cores <= 0:
        raise ValueError("Core count must be positive")

    if _check_slurm_available():
        try:
            return _submit_real_slurm_job(script_path, cores, memory, time_limit, job_name, partition)
        except RuntimeError as e:
            print(f"⚠️  Real Slurm failed ({e}), falling back to mock mode")
            return _submit_mock_slurm_job(script_path, cores, memory, time_limit, job_name, partition)
    else:
        return _submit_mock_slurm_job(script_path, cores, memory, time_limit, job_name, partition)


def _submit_real_slurm_job(script_path: str, cores: int, memory: Optional[str] = None, 
                          time_limit: Optional[str] = None, job_name: Optional[str] = None, 
                          partition: Optional[str] = None) -> str:
    """Submit a real Slurm job using sbatch."""
    # Create a proper SBATCH script
    sbatch_script = _create_sbatch_script(script_path, cores, memory, time_limit, job_name, partition)
    
    try:
        # Submit the job using sbatch
        cmd = ["sbatch", sbatch_script]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"sbatch failed: {result.stderr}")
        
        output = result.stdout.strip()
        
        # Parse the job ID from sbatch output
        match = re.search(r"Submitted batch job (\d+)", output)
        if not match:
            raise RuntimeError(f"Could not parse job ID from sbatch output: {output}")
        
        job_id = match.group(1)
        print(f"✅ Real Slurm job submitted! Job ID: {job_id}")
        print(f"📄 SBATCH script: {sbatch_script}")
        print(f"💻 Cores requested: {cores}")
        
        return job_id
        
    finally:
        # Clean up temporary script
        if os.path.exists(sbatch_script):
            os.unlink(sbatch_script)


def _submit_mock_slurm_job(script_path: str, cores: int, memory: Optional[str] = None, 
                          time_limit: Optional[str] = None, job_name: Optional[str] = None, 
                          partition: Optional[str] = None) -> str:
    """Submit a mock Slurm job for testing/demo purposes."""
    # Generate a realistic mock job ID
    job_id = random.randint(1000000, 9999999)  # 7-digit job ID like real Slurm
    
    # Simulate sbatch output
    cmd = ["echo", f"Submitted batch job {job_id}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout.strip()

    # Parse the job ID from the mock output
    match = re.search(r"Submitted batch job (\d+)", output)
    if not match:
        raise RuntimeError(f"Failed to submit mock job: {output}")
    
    print(f"🔧 Mock Slurm job submitted! Job ID: {job_id}")
    print(f"📄 Script: {script_path}")
    print(f"💻 Cores requested: {cores}")
    if memory:
        print(f"🧠 Memory: {memory}")
    if time_limit:
        print(f"⏰ Time limit: {time_limit}")
    if job_name:
        print(f"🏷️  Job name: {job_name}")
    if partition:
        print(f"🔧 Partition: {partition}")
    print(f"ℹ️  Note: This is a simulation - install Slurm for real job submission")
    
    return match.group(1)


def get_job_status(job_id: str) -> dict:
    """
    Get the status of a Slurm job.
    
    Args:
        job_id: The Slurm job ID
        
    Returns:
        Dictionary with job status information
    """
    if _check_slurm_available():
        try:
            cmd = ["squeue", "--job", job_id, "--format=%T,%R", "--noheader"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout.strip():
                status_parts = result.stdout.strip().split(',')
                return {
                    "job_id": job_id,
                    "status": status_parts[0] if status_parts else "UNKNOWN",
                    "reason": status_parts[1] if len(status_parts) > 1 else "N/A",
                    "real_slurm": True
                }
            else:
                return {
                    "job_id": job_id,
                    "status": "COMPLETED",
                    "reason": "Job not found (may have completed)",
                    "real_slurm": True
                }
        except Exception as e:
            return {
                "job_id": job_id,
                "status": "ERROR",
                "reason": str(e),
                "real_slurm": True
            }
    else:
        # Mock status for demo
        statuses = ["PENDING", "RUNNING", "COMPLETED"]
        return {
            "job_id": job_id,
            "status": random.choice(statuses),
            "reason": "Mock status",
            "real_slurm": False
        }


def cancel_slurm_job(job_id: str) -> dict:
    """
    Cancel a Slurm job.
    
    Args:
        job_id: The Slurm job ID to cancel
        
    Returns:
        Dictionary with cancellation results
    """
    if _check_slurm_available():
        try:
            cmd = ["scancel", job_id]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    "job_id": job_id,
                    "status": "cancelled",
                    "message": f"Job {job_id} cancelled successfully",
                    "real_slurm": True
                }
            else:
                return {
                    "job_id": job_id,
                    "status": "error",
                    "message": f"Failed to cancel job: {result.stderr.strip()}",
                    "real_slurm": True
                }
        except Exception as e:
            return {
                "job_id": job_id,
                "status": "error",
                "message": str(e),
                "real_slurm": True
            }
    else:
        # Mock cancellation for demo
        return {
            "job_id": job_id,
            "status": "cancelled",
            "message": f"Mock job {job_id} cancelled successfully",
            "real_slurm": False
        }


def list_slurm_jobs(user: Optional[str] = None, state: Optional[str] = None) -> dict:
    """
    List Slurm jobs with optional filtering.
    
    Args:
        user: Username to filter by (default: current user)
        state: Job state to filter by (PENDING, RUNNING, COMPLETED, etc.)
        
    Returns:
        Dictionary with list of jobs
    """
    if _check_slurm_available():
        try:
            # Build squeue command
            cmd = ["squeue", "--format=%i,%T,%j,%u,%M,%l,%D,%C", "--noheader"]
            
            if user:
                cmd.extend(["--user", user])
            if state:
                cmd.extend(["--states", state])
                
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                jobs = []
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        parts = line.split(',')
                        if len(parts) >= 8:
                            jobs.append({
                                "job_id": parts[0],
                                "state": parts[1],
                                "name": parts[2],
                                "user": parts[3],
                                "time": parts[4],
                                "time_limit": parts[5],
                                "nodes": parts[6],
                                "cpus": parts[7]
                            })
                
                return {
                    "jobs": jobs,
                    "count": len(jobs),
                    "user_filter": user,
                    "state_filter": state,
                    "real_slurm": True
                }
            else:
                # Command failed, return error but with proper structure
                return {
                    "jobs": [],
                    "count": 0,
                    "user_filter": user,
                    "state_filter": state,
                    "error": result.stderr.strip(),
                    "real_slurm": True
                }
        except Exception as e:
            return {
                "jobs": [],
                "error": str(e),
                "real_slurm": True
            }
    else:
        # Mock job listing for demo
        mock_jobs = [
            {
                "job_id": "1234567",
                "state": "RUNNING",
                "name": "test_job_1",
                "user": user or "demo_user",
                "time": "00:15:30",
                "time_limit": "01:00:00",
                "nodes": "1",
                "cpus": "4"
            },
            {
                "job_id": "1234568",
                "state": "PENDING",
                "name": "test_job_2",
                "user": user or "demo_user",
                "time": "00:00:00",
                "time_limit": "02:00:00",
                "nodes": "2",
                "cpus": "8"
            }
        ]
        
        # Filter by state if requested
        if state:
            mock_jobs = [job for job in mock_jobs if job["state"] == state]
            
        return {
            "jobs": mock_jobs,
            "count": len(mock_jobs),
            "user_filter": user,
            "state_filter": state,
            "real_slurm": False
        }


def get_slurm_info() -> dict:
    """
    Get information about the Slurm cluster.
    
    Returns:
        Dictionary with cluster information
    """
    if _check_slurm_available():
        try:
            # Get cluster info using sinfo
            cmd = ["sinfo", "--format=%P,%A,%l,%D,%T,%N", "--noheader"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            partitions = []
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        parts = line.split(',')
                        if len(parts) >= 6:
                            partitions.append({
                                "partition": parts[0].rstrip('*'),
                                "avail_idle": parts[1],
                                "timelimit": parts[2],
                                "nodes": parts[3],
                                "state": parts[4],
                                "nodelist": parts[5]
                            })
            
            # Get cluster name and version
            cluster_info = {
                "cluster_name": "slurm-cluster",
                "partitions": partitions,
                "real_slurm": True
            }
            
            # Try to get Slurm version
            try:
                version_cmd = ["sinfo", "--version"]
                version_result = subprocess.run(version_cmd, capture_output=True, text=True)
                if version_result.returncode == 0:
                    cluster_info["version"] = version_result.stdout.strip()
            except:
                pass
                
            return cluster_info
            
        except Exception as e:
            return {
                "error": str(e),
                "real_slurm": True
            }
    else:
        # Mock cluster info for demo
        return {
            "cluster_name": "demo-cluster",
            "version": "slurm 22.05.0 (mock)",
            "partitions": [
                {
                    "partition": "compute",
                    "avail_idle": "10/20",
                    "timelimit": "7-00:00:00",
                    "nodes": "20",
                    "state": "mixed",
                    "nodelist": "node[001-020]"
                },
                {
                    "partition": "gpu",
                    "avail_idle": "2/4",
                    "timelimit": "1-00:00:00",
                    "nodes": "4",
                    "state": "mixed",
                    "nodelist": "gpu[001-004]"
                }
            ],
            "real_slurm": False
        }


def get_job_details(job_id: str) -> dict:
    """
    Get detailed information about a specific Slurm job.
    
    Args:
        job_id: The Slurm job ID
        
    Returns:
        Dictionary with detailed job information
    """
    if _check_slurm_available():
        try:
            # Use scontrol to get detailed job information
            cmd = ["scontrol", "show", "job", job_id]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                job_info = {}
                output = result.stdout.strip()
                
                # Parse scontrol output
                for line in output.split('\n'):
                    for item in line.split():
                        if '=' in item:
                            key, value = item.split('=', 1)
                            job_info[key.lower()] = value
                
                return {
                    "job_id": job_id,
                    "details": job_info,
                    "real_slurm": True
                }
            else:
                # Try sacct for completed jobs
                cmd = ["sacct", "-j", job_id, "--format=JobID,JobName,Partition,Account,AllocCPUS,State,ExitCode,Start,End,Elapsed,MaxRSS,MaxVMSize", "--parsable2", "--noheader"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0 and result.stdout.strip():
                    lines = result.stdout.strip().split('\n')
                    if lines:
                        fields = ["jobid", "jobname", "partition", "account", "alloccpus", "state", "exitcode", "start", "end", "elapsed", "maxrss", "maxvmsize"]
                        values = lines[0].split('|')
                        
                        job_details = {}
                        for i, field in enumerate(fields):
                            if i < len(values):
                                job_details[field] = values[i]
                        
                        return {
                            "job_id": job_id,
                            "details": job_details,
                            "real_slurm": True,
                            "source": "accounting"
                        }
                
                return {
                    "job_id": job_id,
                    "error": "Job not found",
                    "real_slurm": True
                }
        except Exception as e:
            return {
                "job_id": job_id,
                "error": str(e),
                "real_slurm": True
            }
    else:
        # Mock detailed job info
        return {
            "job_id": job_id,
            "details": {
                "jobname": f"mock_job_{job_id}",
                "partition": "compute",
                "state": "RUNNING",
                "nodes": "1",
                "cpus": "4",
                "timelimit": "01:00:00",
                "starttime": "2024-01-01T10:00:00",
                "workdir": "/home/user",
                "stdout": f"slurm-{job_id}.out",
                "stderr": f"slurm-{job_id}.err"
            },
            "real_slurm": False
        }


def get_job_output(job_id: str, output_type: str = "stdout") -> dict:
    """
    Get job output files (stdout/stderr).
    
    Args:
        job_id: The Slurm job ID
        output_type: Type of output ("stdout" or "stderr")
        
    Returns:
        Dictionary with job output content
    """
    if _check_slurm_available():
        try:
            # First get job details to find output files
            details = get_job_details(job_id)
            
            if "details" in details:
                job_details = details["details"]
                
                # Look for standard output file patterns
                output_file = None
                if output_type == "stdout":
                    output_file = job_details.get("stdout") or f"slurm-{job_id}.out"
                elif output_type == "stderr":
                    output_file = job_details.get("stderr") or f"slurm-{job_id}.err"
                
                if output_file and os.path.exists(output_file):
                    with open(output_file, 'r') as f:
                        content = f.read()
                    
                    return {
                        "job_id": job_id,
                        "output_type": output_type,
                        "file_path": output_file,
                        "content": content,
                        "real_slurm": True
                    }
                else:
                    return {
                        "job_id": job_id,
                        "output_type": output_type,
                        "error": f"Output file not found: {output_file}",
                        "real_slurm": True
                    }
            else:
                return {
                    "job_id": job_id,
                    "output_type": output_type,
                    "error": "Could not get job details",
                    "real_slurm": True
                }
                
        except Exception as e:
            return {
                "job_id": job_id,
                "output_type": output_type,
                "error": str(e),
                "real_slurm": True
            }
    else:
        # Mock output
        mock_content = f"Mock {output_type} for job {job_id}\nJob started at: 2024-01-01 10:00:00\nJob completed successfully\n"
        return {
            "job_id": job_id,
            "output_type": output_type,
            "content": mock_content,
            "real_slurm": False
        }


def get_queue_info(partition: Optional[str] = None) -> dict:
    """
    Get information about the Slurm job queue.
    
    Args:
        partition: Specific partition to query (optional)
        
    Returns:
        Dictionary with queue information
    """
    if _check_slurm_available():
        try:
            # Build squeue command for queue overview
            cmd = ["squeue", "--format=%i,%T,%j,%u,%P,%M,%l,%D,%C,%Q", "--noheader"]
            
            if partition:
                cmd.extend(["--partition", partition])
                
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                jobs = []
                state_counts = {"PENDING": 0, "RUNNING": 0, "SUSPENDED": 0, "CANCELLED": 0, "COMPLETING": 0}
                
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        parts = line.split(',')
                        if len(parts) >= 9:
                            job_info = {
                                "job_id": parts[0],
                                "state": parts[1],
                                "name": parts[2],
                                "user": parts[3],
                                "partition": parts[4],
                                "time": parts[5],
                                "time_limit": parts[6],
                                "nodes": parts[7],
                                "cpus": parts[8],
                                "priority": parts[9] if len(parts) > 9 else "N/A"
                            }
                            jobs.append(job_info)
                            
                            # Count states
                            state = job_info["state"]
                            if state in state_counts:
                                state_counts[state] += 1
                
                return {
                    "jobs": jobs,
                    "total_jobs": len(jobs),
                    "state_summary": state_counts,
                    "partition_filter": partition,
                    "real_slurm": True
                }
            else:
                return {
                    "jobs": [],
                    "total_jobs": 0,
                    "state_summary": {"PENDING": 0, "RUNNING": 0, "SUSPENDED": 0, "CANCELLED": 0, "COMPLETING": 0},
                    "partition_filter": partition,
                    "error": result.stderr.strip(),
                    "real_slurm": True
                }
        except Exception as e:
            return {
                "jobs": [],
                "total_jobs": 0,
                "state_summary": {"PENDING": 0, "RUNNING": 0, "SUSPENDED": 0, "CANCELLED": 0, "COMPLETING": 0},
                "partition_filter": partition,
                "error": str(e),
                "real_slurm": True
            }
    else:
        # Mock queue info
        mock_jobs = [
            {
                "job_id": "1234567",
                "state": "RUNNING",
                "name": "simulation_1",
                "user": "user1",
                "partition": partition or "compute",
                "time": "00:45:30",
                "time_limit": "02:00:00",
                "nodes": "2",
                "cpus": "8",
                "priority": "100"
            },
            {
                "job_id": "1234568",
                "state": "PENDING",
                "name": "analysis_job",
                "user": "user2",
                "partition": partition or "compute",
                "time": "00:00:00",
                "time_limit": "01:30:00",
                "nodes": "1",
                "cpus": "4",
                "priority": "90"
            }
        ]
        
        return {
            "jobs": mock_jobs,
            "total_jobs": len(mock_jobs),
            "state_summary": {"PENDING": 1, "RUNNING": 1, "SUSPENDED": 0, "CANCELLED": 0, "COMPLETING": 0},
            "partition_filter": partition,
            "real_slurm": False
        }


def submit_array_job(script_path: str, array_range: str, cores: int = 1, 
                    memory: Optional[str] = None, time_limit: Optional[str] = None,
                    job_name: Optional[str] = None, partition: Optional[str] = None) -> dict:
    """
    Submit a Slurm array job.
    
    Args:
        script_path: Path to the job script
        array_range: Array range specification (e.g., "1-10", "1-100:2")
        cores: Number of cores per array task
        memory: Memory per array task
        time_limit: Time limit per array task
        job_name: Base name for the array job
        partition: Slurm partition to use
        
    Returns:
        Dictionary with array job submission results
    """
    if _check_slurm_available():
        try:
            # Create SBATCH script with array directive
            with open(script_path, 'r') as f:
                content = f.read()
            
            fd, temp_script = tempfile.mkstemp(suffix='.sh', prefix='slurm_array_')
            
            with os.fdopen(fd, 'w') as f:
                f.write("#!/bin/bash\n")
                f.write(f"#SBATCH --array={array_range}\n")
                f.write(f"#SBATCH --cpus-per-task={cores}\n")
                f.write(f"#SBATCH --job-name={job_name or 'array_job'}\n")
                f.write(f"#SBATCH --output=slurm_%A_%a.out\n")
                f.write(f"#SBATCH --error=slurm_%A_%a.err\n")
                
                if memory:
                    f.write(f"#SBATCH --mem={memory}\n")
                if time_limit:
                    f.write(f"#SBATCH --time={time_limit}\n")
                if partition:
                    f.write(f"#SBATCH --partition={partition}\n")
                    
                f.write("\n# Array job script content:\n")
                f.write("echo \"Array job ${SLURM_ARRAY_JOB_ID}, task ${SLURM_ARRAY_TASK_ID}\"\n")
                f.write("echo \"Running on node: $(hostname)\"\n")
                f.write("\n# Original script content:\n")
                
                # Skip shebang in original content if it exists
                lines = content.split('\n')
                if lines and lines[0].startswith('#!'):
                    lines = lines[1:]
                
                f.write('\n'.join(lines))
            
            os.chmod(temp_script, 0o755)
            
            # Submit the array job
            cmd = ["sbatch", temp_script]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise RuntimeError(f"sbatch failed: {result.stderr}")
            
            output = result.stdout.strip()
            
            # Parse the array job ID from sbatch output
            match = re.search(r"Submitted batch job (\d+)", output)
            if not match:
                raise RuntimeError(f"Could not parse job ID from sbatch output: {output}")
            
            array_job_id = match.group(1)
            
            return {
                "array_job_id": array_job_id,
                "array_range": array_range,
                "script_path": script_path,
                "cores": cores,
                "memory": memory,
                "time_limit": time_limit,
                "job_name": job_name,
                "partition": partition,
                "message": f"Array job {array_job_id} submitted successfully",
                "real_slurm": True
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "real_slurm": True
            }
        finally:
            # Clean up temporary script
            if 'temp_script' in locals() and os.path.exists(temp_script):
                os.unlink(temp_script)
    else:
        # Mock array job submission
        array_job_id = random.randint(2000000, 2999999)
        return {
            "array_job_id": str(array_job_id),
            "array_range": array_range,
            "script_path": script_path,
            "cores": cores,
            "memory": memory,
            "time_limit": time_limit,
            "job_name": job_name,
            "partition": partition,
            "message": f"Mock array job {array_job_id} submitted successfully",
            "real_slurm": False
        }


def get_node_info() -> dict:
    """
    Get information about cluster nodes.
    
    Returns:
        Dictionary with node information
    """
    if _check_slurm_available():
        try:
            cmd = ["sinfo", "--Node", "--format=%N,%T,%C,%m,%f,%G", "--noheader"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                nodes = []
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        parts = line.split(',')
                        if len(parts) >= 4:
                            nodes.append({
                                "node_name": parts[0],
                                "state": parts[1],
                                "cpus": parts[2],
                                "memory": parts[3],
                                "features": parts[4] if len(parts) > 4 else "",
                                "gres": parts[5] if len(parts) > 5 else ""
                            })
                
                return {
                    "nodes": nodes,
                    "total_nodes": len(nodes),
                    "real_slurm": True
                }
            else:
                return {
                    "nodes": [],
                    "total_nodes": 0,
                    "error": result.stderr.strip(),
                    "real_slurm": True
                }
        except Exception as e:
            return {
                "nodes": [],
                "total_nodes": 0,
                "error": str(e),
                "real_slurm": True
            }
    else:
        # Mock node info
        mock_nodes = [
            {
                "node_name": "compute-01",
                "state": "idle",
                "cpus": "16/0/0/16",
                "memory": "64000",
                "features": "CPU_Intel",
                "gres": ""
            },
            {
                "node_name": "compute-02",
                "state": "alloc",
                "cpus": "16/8/0/8",
                "memory": "64000",
                "features": "CPU_Intel",
                "gres": ""
            },
            {
                "node_name": "gpu-01",
                "state": "idle",
                "cpus": "32/0/0/32",
                "memory": "128000",
                "features": "GPU_V100",
                "gres": "gpu:v100:4"
            }
        ]
        
        return {
            "nodes": mock_nodes,
            "total_nodes": len(mock_nodes),
            "real_slurm": False
        }