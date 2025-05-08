import random
import glob
import subprocess
import os
from flask import jsonify

# we will handle hdf5 and slurm from the assignment
RESOURCES = [
  {
    "name": "hdf5_files", 
    "description": "List all HDF5 Files"
  },
  {
    "name": "slurm_job_submission", 
    "description": "Mock slurm job submission"
  }
]

# template for success message with results
def jsonrpc_result(request_id, result):
  return {
    "jsonrpc": "2.0",
    "result": result,
    "id": request_id
  }

# template for error messages with error code and error message
def jsonrpc_error(request_id, code, message):
  return {
    "jsonrpc": "2.0",
    "error": {
      "code": code,
      "message": message,
    },
    "id": request_id
  }

# check if the json is json rpc 2.0 compliant
def json_validate(data):
  if not data or "jsonrpc" not in data or "method" not in data:
    return jsonify(jsonrpc_error(data.get("id"), -32600, "Invalid Request")) # code for invalid JSON according to jsonrpc.org/specification
  return None

# return a list of handled resources
def list_resources(request_id):
  result = {
    "resources": RESOURCES
  }
  
  return jsonify(jsonrpc_result(request_id, result))

# hdf5
def handle_hdf5(arguments):
  # parse args
  path = arguments.get("path")
  file_extension = arguments.get("file_extension")

  # look for all files ending with file_extension in dir path given
  search_pattern = os.path.join(path, f"*.{file_extension}")
  files = glob.glob(search_pattern)

  file_names = [os.path.basename(file) for file in files]
  
  results = {
    "file_results": file_names
  }
  return results

# slurm
def handle_slurm(arguments):
  # parse args
  script_path = arguments.get("script_path", "fake_script.sh") # default to fake_script if no script was specified.
  cores = arguments.get("cores", 1) # default to 1 if cores wasn't provided
  if cores > 8: # mock max core to 8 to simulate edge case handling
    cores = 8
  
  echo_message = f"echo 'Submitted {script_path} using {cores} cores'"

  try:
    # execute the command and store message
    command_result = subprocess.check_output(echo_message, shell=True, text=True).strip();
  
    fake_job_id = f"fake-job-{random.randint(10000, 99999)}"

    results = {
      "job_id": fake_job_id,
      "submission_output": command_result
    }

    return results
  
  except Exception as e:
    return {
      "error": "Failed to run job"
    }

# handles which tool to call
def call_tool(request_id, params):
  tool = params.get("tool")
  arguments = params.get("arguments", {})

  if tool == "hdf5_files":
    results = handle_hdf5(arguments)
    return jsonify(jsonrpc_result(request_id, results))

  elif tool == "slurm_job_submission":
    results = handle_slurm(arguments)
    return jsonify(jsonrpc_result(request_id, results))

  else:
    return jsonify(jsonrpc_error(request_id, -32601, "Tool not found"))

