#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Import libraries:
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.mcp_handlers import mcp_router

# Create the FastAPI app:
app = FastAPI(tittle="ScientificMCPServer")

# Add the routers from the mcp_handlers.py module
app.include_router(mcp_router, prefix="/mcp")

# Mount the /images path that will use it store the genereated plot path to share it with the client
app.mount("/images", StaticFiles(directory="images"), name="images")
