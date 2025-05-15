Devin Liu 20483790
Implemented HDF5 and Slurm

## How to Run Server:
To start the server->
in root dir, run:
`python -m src.server`

## How to Run Test:
To run test->
in root dir, run:
`pytest`

## listResources
Example call to listResources:
POST to http://localhost:3000/mcp/listResources, submit with body:
```
{
    "jsonrpc": "2.0", 
    "method": "listResources", 
    "id": "5",
    "params": {}
}
```

## callTool
### HDF5
User specifies path directory under params -> arguments -> path. See example below. User can test with path "./mock_hdf5/a" or "./mock_hdf5/b"

Assumptions: user input a path and desired file extension (ie hdf5, no period).
Example hdf5_file request:
POST to http://localhost:3000/mcp/callTool, submit with body:
```
{
    "jsonrpc": "2.0", 
    "method": "callTool", 
    "id": "5",
    "params": {
        "tool": "hdf5_files",
        "arguments": {
            "path": "./mock_hdf5/a",
            "file_extension": "hdf5"
        }
    }
}
```
This will return a list of files that ends in .hdf5 and ignore ones that doesn't

### Slurm
Example slurm_job_submission request:
POST to http://localhost:3000/mcp/callTool, submit with body:
```
{
    "jsonrpc": "2.0", 
    "method": "callTool", 
    "id": "5",
    "params": {
        "tool": "slurm_job_submission",
        "arguments": {
            "script_path": "run_analysis.sh",
            "cores": 5
        }
    }
}

This is run a subprocess that echoes the command, and return the content of that echo to the user as a response, along with a randomly generated job id.
```