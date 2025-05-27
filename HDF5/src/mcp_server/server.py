import os
import sys
import json
from fastmcp import FastMCP
from dotenv import load_dotenv

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables from .env file
load_dotenv()

# Import HDF5 capabilities
from capabilities import data_query, hdf5_list, node_hardware
import mcp_handlers

# Initialize FastMCP server instance
mcp = FastMCP("HDF5Server")

# ─── HDF5 TOOLS ─────────────────────────────────────────────────────────────

@mcp.tool(
    name="filter_csv",
    description="Filter CSV data based on a threshold value."
)
async def filter_csv_tool(csv_path: str = "data.csv", threshold: int = 50) -> dict:
    """Filter CSV data based on a threshold value."""
    try:
        return await mcp_handlers.filter_values(csv_path, threshold)
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "filter_csv", "error": type(e).__name__},
            "isError": True
        }

@mcp.tool(
    name="list_hdf5",
    description="List HDF5 files in a directory."
)
async def list_hdf5_tool(directory: str = "data/sim_run_123") -> dict:
    """List all HDF5 files in the specified directory."""
    try:
        return await mcp_handlers.list_hdf5_files(directory)
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "list_hdf5", "error": type(e).__name__},
            "isError": True
        }

@mcp.tool(
    name="node_hardware",
    description="Get information about CPU cores."
)
async def node_hardware_tool() -> dict:
    """Get detailed information about CPU cores and hardware."""
    try:
        return await mcp_handlers.get_hardware_info()
    except Exception as e:
        return {
            "content": [{"text": json.dumps({"error": str(e)})}],
            "_meta": {"tool": "node_hardware", "error": type(e).__name__},
            "isError": True
        }

def main():
    """
    Main entry point to start the FastMCP server using the specified transport.
    Chooses between stdio and SSE based on MCP_TRANSPORT environment variable.
    """
    try:
        transport = os.getenv("MCP_TRANSPORT", "stdio").lower()
        if transport == "sse":
            host = os.getenv("MCP_SSE_HOST", "0.0.0.0")
            port = int(os.getenv("MCP_SSE_PORT", "8000"))
            print(json.dumps({"message": f"Starting SSE on {host}:{port}"}), file=sys.stderr)
            mcp.run(transport="sse", host=host, port=port)
        else:
            print(json.dumps({"message": "Starting stdio transport"}), file=sys.stderr)
            mcp.run(transport="stdio")
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
