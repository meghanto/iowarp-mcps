from typing import Dict, Any, Optional
import logging
import random
import time

logger = logging.getLogger(__name__)

class SlurmHandler:
    """
    Handles interactions with Slurm workload manager as part of MCP capability.
    """

    def __init__(self):
        """Initialize the Slurm handler with a job database for simulation."""
        # Simulated job database for tracking jobs
        self.jobs = {}

    async def submit_job(self, script_path: str, job_name: Optional[str] = None, 
                         partition: Optional[str] = None) -> Dict[str, Any]:
        """
        Simulate submitting a job to Slurm.

        Args:
            script_path: Path to the job script
            job_name: Name for the job (optional)
            partition: Slurm partition to use (optional)

        Returns:
            Dictionary with job submission results
        """
        # Validate script path
        if not script_path:
            raise ValueError("Script path cannot be empty")

        # Generate a random job ID for simulation
        job_id = str(random.randint(10000, 99999))

        # Create a simulated job record
        job_record = {
                "job_id": job_id,
                "script_path": script_path,
                "job_name": job_name or f"job_{job_id}",
                "partition": partition or "compute",
                "status": "PENDING",
                "submit_time": time.time(),
                "start_time": None,
                "end_time": None,
                "node_list": None,
                "simulated": True
                }

        # Store in simulated job database
        self.jobs[job_id] = job_record
        if random.random() < 0.3:  # 30% chance the job is already running
            self.jobs[job_id]["status"] = "RUNNING"
            self.jobs[job_id]["start_time"] = time.time()
            self.jobs[job_id]["node_list"] = f"node-{random.randint(1, 100)}"

        return {
                "job_id": job_id,
                "status": "submitted",
                "command_output": f"Submitted batch job {job_id}",
                "simulated": True
                }

    async def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """
        Simulate getting the status of a Slurm job.

        Args:
            job_id: The Slurm job ID

        Returns:
            Dictionary with job status information
        """
        if not job_id:
            raise ValueError("Job ID cannot be empty")

        # Check if job exists in our simulated database
        if job_id not in self.jobs:
            # Simulate getting info for unknown jobs
            return {
                    "job_id": job_id,
                    "state": "UNKNOWN",
                    "message": "Job not found",
                    "simulated": True
                    }

        job = self.jobs[job_id]

        if job["status"] == "PENDING" and random.random() < 0.5:
            # 50% chance a pending job is now running
            job["status"] = "RUNNING"
            job["start_time"] = time.time()
            job["node_list"] = f"node-{random.randint(1, 100)}"
        elif job["status"] == "RUNNING" and random.random() < 0.2:
            # 20% chance a running job is now completed
            job["status"] = "COMPLETED"
            job["end_time"] = time.time()

        # Calculate elapsed time
        elapsed = None
        if job["start_time"]:
            end_time = job["end_time"] or time.time()
            elapsed_seconds = end_time - job["start_time"]
            # Format as HH:MM:SS
            elapsed = time.strftime("%H:%M:%S", time.gmtime(elapsed_seconds))

        return {
                "job_id": job_id,
                "state": job["status"],
                "job_name": job["job_name"],
                "partition": job["partition"],
                "elapsed": elapsed,
                "node_list": job["node_list"],
                "simulated": True
                }
