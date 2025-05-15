
import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from mcp_server import mcp_handlers
from mcp_server.mcp_handlers import UnknownToolError

# Create FastAPI app
app = FastAPI()

@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """
    Main MCP JSON-RPC 2.0 endpoint.
    Expects payload with { jsonrpc, method, params, id }.
    Supports:
      - mcp/listResources
      - mcp/callTool
    Returns standard JSON-RPC responses.
    """
    try:
        payload = await request.json()
    except Exception:
        # Invalid JSON
        return JSONResponse(
            content={"jsonrpc": "2.0", "id": None,
                     "error": {"code": -32700, "message": "Parse error"}})

    # Validate JSON-RPC version
    if payload.get("jsonrpc") != "2.0":
        return JSONResponse(
            content={"jsonrpc": "2.0", "id": payload.get("id"),
                     "error": {"code": -32600, "message": "Invalid Request"}})

    req_id = payload.get("id")
    method = payload.get("method")
    params = payload.get("params", {})

    # Handle listResources
    if method == "mcp/listResources":
        result = mcp_handlers.list_resources()
        return JSONResponse({"jsonrpc": "2.0", "id": req_id, "result": result})

    # Handle callTool
    if method == "mcp/callTool":
        tool = params.get("tool")
        if not tool:
            # Missing required 'tool' param
            return JSONResponse(
                content={"jsonrpc": "2.0", "id": req_id,
                         "error": {"code": -32602, "message": "Missing 'tool' in params"}})
        try:
            result = mcp_handlers.call_tool(tool, params)
        except UnknownToolError as e:
            # Method not found for this tool
            return JSONResponse(
                content={"jsonrpc": "2.0", "id": req_id,
                         "error": {"code": -32601, "message": str(e)}})
        return JSONResponse({"jsonrpc": "2.0", "id": req_id, "result": result})

    # Method not implemented
    return JSONResponse(
        content={"jsonrpc": "2.0", "id": req_id,
                 "error": {"code": -32601, "message": f"Method '{method}' not found"}})

# When run as a script, start Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mcp_server.server:app", host="0.0.0.0", port=8000, log_level="info")
