from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import uvicorn
import logging
import json
from .mcp_handlers import (
        handle_list_resources,
        handle_list_tools,
        handle_get_resource,
        handle_call_tool
        )

# Configure logging
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
logger = logging.getLogger(__name__)

app = FastAPI(title="Scientific MCP Server",
              description="MCP server for scientific computing resources")


@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """
    Handle MCP JSON_RPC 2.0 requests
    """

    try:
        # Parse the JSON-RPC request
        body = await request.json()

        # Validate JSON-RPC structure
        if "jsonrpc" not in body or body["jsonrpc"] != "2.0":
            return JSONResponse(
                    status_code=400,
                    content={"error": {"code": -32600, "message":
                                       "Invalid Request: Not a valid JSON-RPC 2.0 request"}}
                    )

        if "method" not in body:
            return JSONResponse(
                    status_code=400,
                    content={"error": {"code": -32600, "message":
                                       "Invalid Request: Method not specified"}}
                    )

        if "id" not in body:
            return JSONResponse(
                    status_code=400,
                    content={"error": {"code": -32600, "message":
                                       "Invalid Request: ID not specified"}}
                    )

        # Extract method, params, and id
        method = body["method"]
        params = body.get("params", {})
        request_id = body["id"]

        # Route to appropriate handler based on method
        result = None
        if method == "mcp/listResources":
            result = await handle_list_resources(params)
        elif method == "mcp/listTools":
            result = await handle_list_tools(params)
        elif method == "mcp/getResource":
            result = await handle_get_resource(params)
        elif method == "mcp/callTool":
            result = await handle_call_tool(params)
        else:
            return JSONResponse(
                    content={
                        "jsonrpc": "2.0",
                        "error": {"code": -32601, "message": f"Method '{method}' not found"},
                        "id": request_id
                        }
                    )

        # Return successful response
        return JSONResponse(
                content={
                    "jsonrpc": "2.0",
                    "result": result,
                    "id": request_id
                    }
                )

    except json.JSONDecodeError:
        return JSONResponse(
                status_code=400,
                content={"error": {"code": -32700, "message":
                                   "Parse error: Invalid JSON"}}
                )
    except Exception as e:
        logger.error(f"Error handling MCP request: {str(e)}")
        return JSONResponse(
                status_code=500,
                content={
                    "jsonrpc": "2.0",
                    "error": {"code": -32603, "message":
                              f"Internal error: {str(e)}"},
                    "id": None
                    }
                )


@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("src.server:app", host="0.0.0.0", port=8000, reload=True)
