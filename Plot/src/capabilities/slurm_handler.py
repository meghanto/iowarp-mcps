import uuid


async def handle_slurm(params, req_id):
    job_script = params.get("script", "job.sh")
    cores = params.get("cores", 1)
    job_id = str(uuid.uuid4())

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "result": {
            "message": f"Job '{job_script}' submitted with {cores} cores.",
            "job_id": job_id,
            "context": {"type": "slurm", "cores": cores}
        }
    }
