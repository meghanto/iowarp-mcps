
import json
from mcp_server.capabilities import data_query, hdf5_list, node_hardware

class UnknownToolError(Exception):
    """Raised when an unsupported tool_name is requested."""
    pass

def list_resources() -> dict:
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

def call_tool(tool_name: str, params: dict) -> dict:
    """
    MCP method: mcp/callTool
    Dispatches to the appropriate capability handler based on tool_name.
    Returns: {
      content: [ { text: JSON-stringified result } ],
      _meta: { metadata about the call },
      isError: bool
    }
    """
    result = {"content": [], "_meta": {}, "isError": False}
    try:
        if tool_name == "filter_csv":
            # CSV filtering: expects csv_path and threshold
            csv_path = params.get("csv_path", "data.csv")
            threshold = params.get("threshold", 50)
            rows = data_query.filter_values(csv_path, threshold)
            result["content"].append({"text": json.dumps(rows)})
            result["_meta"] = {
                "tool": "filter_csv",
                "file": csv_path,
                "threshold": threshold,
                "row_count": len(rows)
            }

        elif tool_name == "list_hdf5":
            # HDF5 listing: expects directory path
            directory = params.get("directory", "data/sim_run_123")
            files = hdf5_list.list_hdf5(directory)
            result["content"].append({"text": json.dumps(files)})
            result["_meta"] = {
                "tool": "list_hdf5",
                "directory": directory,
                "count": len(files)
            }

        elif tool_name == "node_hardware":
            # Node hardware info: no params needed
            info = node_hardware.report_cpu_cores()
            result["content"].append({"text": json.dumps(info)})
            result["_meta"] = {"tool": "node_hardware"}

        else:
            # Unknown tool: raise to be caught below
            raise UnknownToolError(f"Tool '{tool_name}' not available")

    except UnknownToolError:
        # Propagate so that server can return JSON-RPC error code -32601
        raise

    except Exception as e:
        # Any other exception is wrapped into a tool‐level error response
        result["content"] = [{"text": f"Error: {str(e)}"}]
        result["_meta"] = {"tool": tool_name, "error": type(e).__name__}
        result["isError"] = True

    return result
