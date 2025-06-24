from fastapi import FastAPI, Request
from src.mcp_handlers import handle_mcp_request

app = FastAPI()

@app.post("/mcp")
async def mcp_endpoint(request: Request):
    body = await request.json()
    return await handle_mcp_request(body)

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
