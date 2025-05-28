import json
from typing import Dict, List, Any, Optional
from capabilities import data_query, hdf5_list, node_hardware

class UnknownToolError(Exception):
    """Raised when an unsupported tool_name is requested."""
    pass

def list_resources() -> Dict[str, Any]:
    """
    MCP method: mcp/listResources
    Returns a list of available MCP resources and a count.
    """
    return {
        "resources": [
            {"uri": "resource://data.csv", "description": "CSV data file"},
            {"uri": "resource://data/sim_run_123", "description": "Directory of HDF5 files"},
            {"uri": "resource://node_hardware", "description": "CPU core information"}
        ],
        "_meta": {"count": 3}
    }

async def filter_values(csv_path: str = "data.csv", threshold: int = 50) -> Dict[str, Any]:
    """
    Filter CSV data based on a threshold value.
    
    Args:
        csv_path: Path to the CSV file
        threshold: Threshold value for filtering
        
    Returns:
        Dict containing filtered rows and metadata
    """
    try:
        rows = data_query.filter_values(csv_path, threshold)
        return {
            "content": [{"text": json.dumps(rows)}],
            "_meta": {
                "tool": "filter_csv",
                "file": csv_path,
                "threshold": threshold,
                "row_count": len(rows)
            },
            "isError": False
        }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "filter_csv", "error": type(e).__name__},
            "isError": True
        }

async def list_hdf5_files(directory: str = "data/sim_run_123") -> Dict[str, Any]:
    """
    List HDF5 files in a directory.
    
    Args:
        directory: Path to the directory containing HDF5 files
        
    Returns:
        Dict containing list of files and metadata
    """
    try:
        files = hdf5_list.list_hdf5(directory)
        return {
            "content": [{"text": json.dumps(files)}],
            "_meta": {
                "tool": "list_hdf5",
                "directory": directory,
                "count": len(files)
            },
            "isError": False
        }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "list_hdf5", "error": type(e).__name__},
            "isError": True
        }

async def get_hardware_info() -> Dict[str, Any]:
    """
    Get information about CPU cores and hardware.
    
    Returns:
        Dict containing hardware information and metadata
    """
    try:
        info = node_hardware.report_cpu_cores()
        return {
            "content": [{"text": json.dumps(info)}],
            "_meta": {"tool": "node_hardware"},
            "isError": False
        }
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "node_hardware", "error": type(e).__name__},
            "isError": True
        }

def call_tool(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP method: mcp/callTool
    Dispatches to the appropriate capability handler based on tool_name.
    
    Args:
        tool_name: Name of the tool to call
        params: Parameters for the tool
        
    Returns:
        Dict containing tool response and metadata
    """
    tool_map = {
        "filter_csv": lambda: filter_values(
            params.get("csv_path", "data.csv"),
            params.get("threshold", 50)
        ),
        "list_hdf5": lambda: list_hdf5_files(
            params.get("directory", "data/sim_run_123")
        ),
        "node_hardware": lambda: get_hardware_info()
    }
    
    if tool_name not in tool_map:
        return {
            "content": [{"text": json.dumps({"error": f"Tool '{tool_name}' not available"})}],
            "_meta": {"tool": tool_name, "error": "UnknownToolError"},
            "isError": True
        }
        
    return tool_map[tool_name]()
