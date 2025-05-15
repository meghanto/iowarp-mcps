#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import libraries for API testing
import pytest
from fastapi.testclient import TestClient
from src.server import app  # import your FastAPI app

# Create a TestClient instance for testing:
client = TestClient(app)

# Test mcp/listResources endpoint:
# Test the server successfully list the available resources when client requested
def test_list_resources_success():
    # Simulate a correct listResources request
    payload = {
        "jsonrpc": "2.0",
        "method": "listResources",
        "id": 1
    }
    response = client.post("/mcp/listResources", json=payload)
    assert response.status_code == 200 #Make sure the server responded successfully (HTTP 200=OK)
    data = response.json()
    assert data["id"] == 1 
    assert "result" in data # to make sure the server responded with the list of available resources
    
    
# Test the server when client send a wrong json rpc version    
def test_list_resources_invalid_jsonrpc():
    # Simulate a wrong JSONRPC version
    payload = {
        "jsonrpc": "1.0",  # should be 2.0
        "method": "listResources",
        "id": 1
    }
    response = client.post("/mcp/listResources", json=payload)
    assert response.status_code == 422  #To make sure the server reject the request with a Unprocessable Entity as the json rpc version is invalid
    data = response.json()
    assert "detail" in data
    
    
# Test mcp//callTool endpoint:
# Test the mcp correctly call the the client requested tool: pandas
def test_call_tool_success_filter_csv():    
    payload = {
        "jsonrpc": "2.0",
        "method": "Pandas",
        "params": {
           "file_path":"https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv",
           "column":'age', "threshold":50}, 
        "id":2}

    response = client.post("/mcp/callTool", json=payload)
    assert response.status_code == 200 #Make sure the server responded successfully (HTTP 200=OK)
    assert "result" in response.json()
    
    
# Test the mcp rejected client bad request when requested to call unkown method
def test_call_tool_unknown_method():
    response = client.post("/mcp/callTool", json={
        "jsonrpc": "2.0",
        "method": "unknown method",
        "id": 3}
        )
    assert response.status_code == 400 # To make sure the server return a bad request error

