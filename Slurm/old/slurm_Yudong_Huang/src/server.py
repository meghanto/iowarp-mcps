# src/server.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.mcp_handlers import handle_mcp_request

app = FastAPI()

@app.post("/mcp")
async def mcp_entrypoint(request: Request):
    """
    accept MCP JSON-RPC 2.0 request。
    """
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={
                "jsonrpc": "2.0",
                "error": {"code": -32700, "message": "Parse error: Invalid JSON"},
                "id": None
            }
        )

    response = handle_mcp_request(data)
    return JSONResponse(content=response)
