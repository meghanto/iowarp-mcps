# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 22:55:29 2025

@author: lenovo
"""

#This segment of code will make you avoid import error when running the server with a command line 
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
#rootPath = os.path.split(curPath)[0]
sys.path.append(curPath)


from fastapi import FastAPI
from pydantic import BaseModel
import mcp_handler as mh

#Json-rpc 2.0 request structure
class Request(BaseModel):
    jsonrpc:str
    method: str 
    params: list[str]
    Id: int | None = None #Id is used here because id is a preserved word in Python
    
app = FastAPI()

#Handle post request to list all the implemented capabilities and return the json object
@app.post("/mcp/listResource")
async def listRes(req:Request):
    if req.method == "list":
        return {"jsonrpc" : req.jsonrpc,
                "result" : mh.listResource(),
                "id" : req.Id}
    else:
        return {"jsonrpc" : req.jsonrpc,
                "result" : "Error:Your request method should be (list).",
                "id" : req.Id}
     

#Handle post request to execute the implemented tools and return the json object.
@app.post("/mcp/callTool")
async def execution(req:Request):
    if req.method == "HDF5":
        return {"jsonrpc" : req.jsonrpc,
                "result" : mh.callHDF5(req.params),
                "id" : req.Id}
    
    elif req.method == "compress":
        return {"jsonrpc" : req.jsonrpc,
                "result" : mh.callCompress(req.params),
                "id" : req.Id}
    
    else:
        return {"jsonrpc" : req.jsonrpc,
                "result" : "Error:Your request method should be either (HDF5) or (compress)",
                "id" : req.Id}
    
    