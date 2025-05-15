from src.capabilities.hdf5_handler import handle_hdf5
from src.capabilities.slurm_handler import handle_slurm
from src.capabilities.arxiv_handler import handle_arxiv
from src.capabilities.compression_handler import handle_compression
from src.capabilities.plot_handler import handle_plot


async def handle_mcp_request(body):
    method = body.get("method")
    params = body.get("params", {})
    req_id = body.get("id")

    if method == "mcp/listResources":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": [
                {
                    "name": "hdf5",
                    "type": "data",
                    "description": "HDF5 file search using glob"
                },
                {
                    "name": "slurm",
                    "type": "tool",
                    "description": "Slurm-like job submission simulator"
                },
                {
                    "name": "arxiv",
                    "type": "data",
                    "description": "Fetch scientific papers using Arxiv API"
                },
                {
                    "name": "compression",
                    "type": "tool",
                    "description": "Simulated gzip compression"
                },
                {
                    "name": "plot",
                    "type": "tool",
                    "description": "Simulated plotting using Matplotlib and CSV"
                }
            ]
        }
    elif method == "mcp/listTools":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": [
                {
                    "name": "slurm",
                    "description": "Slurm-like job submission simulator"
                },
                {
                    "name": "compression",
                    "description": "Simulated gzip compression"
                },
                {
                    "name": "plot",
                    "description": "Simulated plotting using Matplotlib and CSV"
                }
            ]
        }
    elif method == "mcp/callTool":
        tool = params.get("tool")
        if tool == "hdf5":
            return await handle_hdf5(params, req_id)
        elif tool == "slurm":
            return await handle_slurm(params, req_id)
        elif tool == "arxiv":
            return await handle_arxiv(params, req_id)
        elif tool == "compression":
            return await handle_compression(params, req_id)
        elif tool == "plot":
            return await handle_plot(params, req_id)
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Unknown tool"}}

    elif method == "mcp/listDataSources":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": [
                {
                    "name": "hdf5",
                    "description": "HDF5 file search using glob"
                },
                {
                    "name": "arxiv",
                    "description": "Fetch scientific papers using Arxiv API"
                }
            ]
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}


