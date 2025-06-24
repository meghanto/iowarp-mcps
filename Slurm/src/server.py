from fastapi import FastAPI
from .mcp_handlers import router as mcp_router

# Create FastAPI instance with metadata
app = FastAPI(
    title="Scientific MCP Server",
    description="Implementation of Model Context Protocol for scientific computing",
    version="0.1.0",
    docs_url="/mcp/docs",  # Custom documentation URL
    redoc_url="/mcp/redoc"  # Custom redoc URL
)

# Include the MCP routes from mcp_handlers
app.include_router(mcp_router, prefix="/mcp")

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
