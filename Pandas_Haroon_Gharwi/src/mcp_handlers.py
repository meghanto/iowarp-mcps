#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Import libraries:
from fastapi import FastAPI, Request, APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Literal, Optional
from src.capabilities.pandas_handler import filter_csv_data
from src.capabilities.matplotlib_handler import plot_csv_columns


# Define the JsonRPCR strecture to check the client request is in jsonrpc 2.0 format correctly:
class JsonRPCRequest(BaseModel):
    jsonrpc: Literal["2.0"]
    method: str
    params: Dict[str, Any] = {}
    id: int
    
# Create a FastAPI APIRouter instance   
mcp_router = APIRouter()

# Define all the available tools and their descriptions that will used for listed resources request:
tools = {
    "Pandas": {
        "description": "Data analysis",
        },
    "Matplotlib": {
        "description": "Visualization",
        }
    }

# Endpoint to list the available resources:
@mcp_router.post("/listResources")
async def handle_resources(request: JsonRPCRequest):
    method = request.method
    request_id = request.id
    params = request.params

    if method == "listResources":
        return {
            "jsonrpc": "2.0",
            "result": tools,
            "id": request_id
            }
    else:
        raise HTTPException( status_code=400,
                            detail="Method Is Not Found"
                            )
        
        
# Endpoint for calling a specific tool based on the client requested method   
@mcp_router.post("/callTool")
async def handle_tools_call(request: JsonRPCRequest):
    method = request.method
    request_id = request.id
    params = request.params
    # Tool 1: pandas for data analysis
    if method == "Pandas":
       file_path = params.get("file_path")
       column = params.get("column")
       threshold = params.get("threshold", 0)
       request_id = request.id
       result = filter_csv_data(file_path, column, threshold)  # I have one tool in Pandas: handle filtering data based on column using Pandas
       return {"jsonrpc": "2.0", "result": result, "id": request_id}
   
   # Tool 2: Matplotlib for data visualization
    elif method == "Matplotlib":
        file_path = params.get("file_path")
        x_column = params.get("x_column")
        y_column = params.get("y_column")
        request_id = request.id
        result = plot_csv_columns(file_path, x_column, y_column)  # I have define one tool in matplotlib: handle plotting data using scatter Matplotlib
        return {"jsonrpc": "2.0", "result": result, "id": request_id}
    
    else:
        raise HTTPException( status_code=400,
                            detail="Method Is Not Found"
                            )