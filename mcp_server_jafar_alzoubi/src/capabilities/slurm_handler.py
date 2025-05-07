import uuid
import subprocess
import os
from typing import Dict, Any
from ..models import JSONRPCResponse

# Handle job submission requests
async def handle_request(params: Dict[str, Any]):
    required_params = ["script", "cores"]
    
    # Check if required parameters are provided
    if not all(p in params for p in required_params):
        return JSONRPCResponse(
            error={"code": -32602, "message": f"Required parameters: {', '.join(required_params)}"}
        ).dict()
    
    try:
        script_path = params["script"]
        cores = params["cores"]
        memory = params.get("memory", "4GB")  # Default memory to 4GB if not provided
        job_name = params.get("jobName", "mcp_job")  # Default job name to 'mcp_job' if not provided
        
        # Validate the script file path
        if not os.path.exists(script_path):
            raise ValueError(f"Script file not found: {script_path}")
        
        # Validate the cores input
        if not isinstance(cores, int) or cores < 1:
            raise ValueError("Cores must be a positive integer")
        
        # Simulate job submission
        job_id = str(uuid.uuid4())  # Generate a unique job ID
        mock_command = [
            "sbatch",
            f"--job-name={job_name}",
            f"--ntasks={cores}",
            f"--mem={memory}",
            script_path
        ]
        
        # In a real implementation, the subprocess would submit the job
        # For example, use subprocess.run to submit the job:
        # result = subprocess.run(mock_command, capture_output=True, text=True)
        
        # For simulation, we'll mock the response
        return {
            "jobId": job_id,
            "status": "PENDING",  # Job is in a pending state
            "command": " ".join(mock_command),  # The simulated sbatch command
            "submissionTime": "2023-01-01T12:00:00Z",  # Simulated submission time
            "metadata": {
                "estimatedStart": "2023-01-01T12:05:00Z",  # Estimated job start time
                "queue": "normal",  # Job queue
                "allocatedNodes": []  # No nodes allocated yet
            }
        }

    except Exception as e:
        # Handle any exceptions and return a JSON-RPC error response
        return JSONRPCResponse(
            error={"code": -32000, "message": str(e)}
        ).dict()
