#!/usr/bin/env python3
"""
Plot MCP Server with comprehensive data visualization capabilities.
Provides plotting functionality for CSV, Excel, and other data formats using pandas and matplotlib.
"""
import os
import sys
import json
import argparse
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add current directory to path for relative imports
sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables
load_dotenv()

import mcp_handlers

# Initialize MCP server
mcp = FastMCP("PlotMCP")

@mcp.tool(
    name="create_line_plot",
    description="Create a line plot from CSV or Excel data file."
)
async def create_line_plot_tool(
    file_path: str,
    x_column: str,
    y_column: str,
    title: str = "Line Plot",
    output_path: str = "line_plot.png"
) -> dict:
    """
    Create a line plot from data file.
    
    Args:
        file_path: Path to CSV or Excel file
        x_column: Column name for x-axis
        y_column: Column name for y-axis
        title: Plot title
        output_path: Output image file path
        
    Returns:
        Dictionary with plot information
    """
    logger.info(f"Creating line plot from {file_path}")
    return mcp_handlers.create_line_plot_handler(file_path, x_column, y_column, title, output_path)

@mcp.tool(
    name="create_bar_plot",
    description="Create a bar plot from CSV or Excel data file."
)
async def create_bar_plot_tool(
    file_path: str,
    x_column: str,
    y_column: str,
    title: str = "Bar Plot",
    output_path: str = "bar_plot.png"
) -> dict:
    """
    Create a bar plot from data file.
    
    Args:
        file_path: Path to CSV or Excel file
        x_column: Column name for x-axis
        y_column: Column name for y-axis
        title: Plot title
        output_path: Output image file path
        
    Returns:
        Dictionary with plot information
    """
    logger.info(f"Creating bar plot from {file_path}")
    return mcp_handlers.create_bar_plot_handler(file_path, x_column, y_column, title, output_path)

@mcp.tool(
    name="create_scatter_plot",
    description="Create a scatter plot from CSV or Excel data file."
)
async def create_scatter_plot_tool(
    file_path: str,
    x_column: str,
    y_column: str,
    title: str = "Scatter Plot",
    output_path: str = "scatter_plot.png"
) -> dict:
    """
    Create a scatter plot from data file.
    
    Args:
        file_path: Path to CSV or Excel file
        x_column: Column name for x-axis
        y_column: Column name for y-axis
        title: Plot title
        output_path: Output image file path
        
    Returns:
        Dictionary with plot information
    """
    logger.info(f"Creating scatter plot from {file_path}")
    return mcp_handlers.create_scatter_plot_handler(file_path, x_column, y_column, title, output_path)

@mcp.tool(
    name="create_histogram",
    description="Create a histogram from CSV or Excel data file."
)
async def create_histogram_tool(
    file_path: str,
    column: str,
    bins: int = 30,
    title: str = "Histogram",
    output_path: str = "histogram.png"
) -> dict:
    """
    Create a histogram from data file.
    
    Args:
        file_path: Path to CSV or Excel file
        column: Column name for histogram
        bins: Number of bins for histogram
        title: Plot title
        output_path: Output image file path
        
    Returns:
        Dictionary with plot information
    """
    logger.info(f"Creating histogram from {file_path}")
    return mcp_handlers.create_histogram_handler(file_path, column, bins, title, output_path)

@mcp.tool(
    name="create_heatmap",
    description="Create a heatmap from CSV or Excel data file."
)
async def create_heatmap_tool(
    file_path: str,
    title: str = "Heatmap",
    output_path: str = "heatmap.png"
) -> dict:
    """
    Create a heatmap from data file.
    
    Args:
        file_path: Path to CSV or Excel file
        title: Plot title
        output_path: Output image file path
        
    Returns:
        Dictionary with plot information
    """
    logger.info(f"Creating heatmap from {file_path}")
    return mcp_handlers.create_heatmap_handler(file_path, title, output_path)

@mcp.tool(
    name="get_data_info",
    description="Get information about data file including columns, shape, and data types."
)
async def get_data_info_tool(file_path: str) -> dict:
    """
    Get information about data file.
    
    Args:
        file_path: Path to CSV or Excel file
        
    Returns:
        Dictionary with data information
    """
    logger.info(f"Getting data info for {file_path}")
    return mcp_handlers.get_data_info_handler(file_path)

def main():
    """
    Main entry point for the Plot MCP server.
    Supports both stdio and SSE transports based on environment variables.
    """
    parser = argparse.ArgumentParser(
        description="Plot MCP Server - Data visualization server with comprehensive plotting capabilities"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version="Plot MCP Server v1.0.0"
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport type to use (default: stdio)"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host for SSE transport (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for SSE transport (default: 8000)"
    )
    
    args = parser.parse_args()
    
    try:
        logger.info("Starting Plot MCP Server")
        
        # Use command-line args or environment variables
        transport = args.transport or os.getenv("MCP_TRANSPORT", "stdio").lower()
        
        if transport == "sse":
            # SSE transport for web-based clients
            host = args.host or os.getenv("MCP_SSE_HOST", "0.0.0.0")
            port = args.port or int(os.getenv("MCP_SSE_PORT", "8000"))
            logger.info(f"Starting SSE transport on {host}:{port}")
            print(json.dumps({"message": f"Starting SSE on {host}:{port}"}), file=sys.stderr)
            mcp.run(transport="sse", host=host, port=port)
        else:
            # Default stdio transport
            logger.info("Starting stdio transport")
            print(json.dumps({"message": "Starting stdio transport"}), file=sys.stderr)
            mcp.run(transport="stdio")

    except Exception as e:
        logger.error(f"Server error: {e}")
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
