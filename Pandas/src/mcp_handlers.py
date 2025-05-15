# mcp_handlers files
from typing import Dict, Any, Tuple, List
import importlib
import logging
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)

# Import capability handlers
from src.capabilities.pandas_handler import PandasHandler

# Initialize handlers
handlers = {
    "pandas": PandasHandler(),
}

# Available resources
resources = {
    
    "pandas_data": {
        "type": "data",
        "description": "Pandas data analysis",
        "handler": "pandas"
    }
}

# Available tools
tools = {
    
    "pandas": {
        "type": "tool",
        "description": "Pandas data analysis",
        "handler": "pandas"
    },
}

async def handle_mcp_request(method: str, params: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Handle MCP requests based on the method and parameters.
    
    Args:
        method: The MCP method to execute
        params: Parameters for the method
        
    Returns:
        Tuple containing (result, metadata)
    """
    logger.info(f"Handling method: {method} with params: {params}")
    
    if method == "mcp/listResources":
        return await list_resources(params)
    elif method == "mcp/getResource":
        return await get_resource(params)
    elif method == "mcp/listTools":
        return await list_tools(params)
    elif method == "mcp/callTool":
        return await call_tool(params)
    else:
        return {}, {"status": "error", "message": f"Unknown method: {method}"}

async def list_resources(params: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """List available MCP resources."""
    resource_list = []
    
    for resource_id, resource_info in resources.items():
        resource_list.append({
            "id": resource_id,
            "type": resource_info["type"],
            "description": resource_info["description"]
        })
    
    return {"resources": resource_list}, {"status": "success"}

async def get_resource(params: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Get details about a specific resource."""
    resource_id = params.get("resource_id")
    
    if not resource_id:
        return {}, {"status": "error", "message": "Resource ID is required"}
    
    if resource_id not in resources:
        return {}, {"status": "error", "message": f"Resource not found: {resource_id}"}
    
    resource_info = resources[resource_id]
    handler_name = resource_info["handler"]
    
    if handler_name in handlers:
        handler = handlers[handler_name]
        resource_details = await handler.get_details()
        return {
            "resource_details": {
                "id": resource_id,
                "type": resource_info["type"],
                "description": resource_info["description"],
                "details": resource_details
            }
        }, {"status": "success"}
    else:
        return {}, {"status": "error", "message": f"Handler not found for resource: {resource_id}"}

async def list_tools(params: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """List available MCP tools."""
    tool_list = []
    
    for tool_id, tool_info in tools.items():
        tool_list.append({
            "id": tool_id,
            "type": tool_info["type"],
            "description": tool_info["description"]
        })
    
    return {"tools": tool_list}, {"status": "success"}

async def call_tool(params: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Execute a tool with the given parameters."""
    tool_id = params.get("tool_id")
    tool_params = params.get("tool_params", {})
    
    if not tool_id:
        return {}, {"status": "error", "message": "Tool ID is required"}
    
    if tool_id not in tools:
        return {}, {"status": "error", "message": f"Tool not found: {tool_id}"}
    
    tool_info = tools[tool_id]
    handler_name = tool_info["handler"]
    
    if handler_name in handlers:
        handler = handlers[handler_name]
        try:
            result = await handler.execute(tool_params)
            return {"tool_result": result}, {"status": "success"}
        except Exception as e:
            logger.error(f"Error executing tool {tool_id}: {str(e)}")
            return {}, {"status": "error", "message": f"Error executing tool: {str(e)}"}
    else:
        return {}, {"status": "error", "message": f"Handler not found for tool: {tool_id}"}
