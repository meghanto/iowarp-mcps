#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
import click

# Determine if we're running from development or installed package
MODULE_DIR = Path(__file__).parent
DEV_SERVERS_PATH = MODULE_DIR.parent.parent  # ../../ from module (points to repo root)
INSTALLED_SERVERS_PATH = MODULE_DIR / "servers"  # within installed package

# Map server names to their entry point commands (from existing pyproject.toml)
SERVER_COMMAND_MAP = {
    "adios": "adios-mcp",
    "arxiv": "arxiv-mcp",
    "chronolog": "chronolog-mcp",
    "compression": "compression-mcp",
    "darshan": "darshan-mcp",
    "hdf5": "hdf5-mcp",
    "jarvis": "jarvis-mcp",
    "lmod": "lmod-mcp",
    "node-hardware": "node-hardware-mcp",
    "pandas": "pandas-mcp",
    "parallel-sort": "parallel-sort-mcp",
    "parquet": "parquet-mcp",
    "plot": "plot-mcp",
    "slurm": "slurm-mcp"
}

# Map server names to actual directory names (for case sensitivity)
DIR_NAME_MAP = {
    "adios": "Adios",
    "arxiv": "Arxiv",
    "chronolog": "Chronolog",
    "compression": "Compression",
    "darshan": "Darshan",
    "hdf5": "HDF5",
    "jarvis": "Jarvis",
    "lmod": "lmod",
    "node-hardware": "Node_Hardware",
    "pandas": "Pandas",
    "parallel-sort": "Parallel_Sort",
    "parquet": "parquet",
    "plot": "Plot",
    "slurm": "Slurm"
}

def get_servers_path():
    """Get the path to servers directory (dev or installed)"""
    if DEV_SERVERS_PATH.exists():
        # In development, servers are at repo root
        return DEV_SERVERS_PATH
    return INSTALLED_SERVERS_PATH

def list_available_servers():
    """List all available servers"""
    return sorted(SERVER_COMMAND_MAP.keys())

@click.command()
@click.argument('server', required=False)
@click.option('-b', '--branch', help='Git branch to use (for development)')
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def main(server, branch, args):
    """Launch IOWarp MCP servers with isolated dependencies using uvx"""
    
    if not server:
        click.echo("Available servers:")
        for s in list_available_servers():
            click.echo(f"  - {s}")
        click.echo("\nUsage: uvx iowarp-mcps <server-name>")
        click.echo("   or: iowarp-mcps <server-name> (if installed)")
        return
    
    # Normalize server name to lowercase
    server_lower = server.lower()
    
    if server_lower not in SERVER_COMMAND_MAP:
        click.echo(f"Error: Unknown server '{server}'")
        click.echo(f"Available servers: {', '.join(list_available_servers())}")
        sys.exit(1)
    
    # Get the entry point command
    entry_command = SERVER_COMMAND_MAP[server_lower]
    
    # Build uvx command
    if branch:
        # Run from git branch
        actual_dir = DIR_NAME_MAP[server_lower]
        cmd = [
            "uvx",
            "--from",
            f"git+https://github.com/iowarp/iowarp-mcps.git@{branch}#subdirectory={actual_dir}",
            entry_command
        ]
    else:
        # Run from local path in development mode
        servers_path = get_servers_path()
        actual_dir = DIR_NAME_MAP[server_lower]
        server_path = servers_path / actual_dir
        
        if server_path.exists():
            # Development mode - run from local path
            cmd = [
                "uvx",
                "--from",
                str(server_path),
                entry_command
            ]
        else:
            # Not in development, try to run the command directly (if installed)
            cmd = [entry_command]
    
    # Add any additional arguments
    cmd.extend(args)
    
    # Execute the command
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
    except FileNotFoundError:
        if cmd[0] == "uvx":
            click.echo("Error: uvx not found. Please install uv: https://github.com/astral-sh/uv")
        else:
            click.echo(f"Error: {entry_command} not found. Please install the server package.")
        sys.exit(1)

if __name__ == "__main__":
    main()