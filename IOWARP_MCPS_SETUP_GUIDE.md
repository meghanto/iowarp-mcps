# IOWarp MCPs: Auto-Discovery Architecture

This repository uses an auto-discovery system that eliminates the need for manual server mapping. New MCP servers are automatically detected from the `mcps/` folder.

## Auto-Discovery Architecture

### Key Features
- **Zero Configuration**: New MCPs are automatically discovered from `mcps/` folder
- **No Manual Mapping**: No need to update hardcoded lists when adding servers
- **Consistent Interface**: `uvx iowarp-mcps <server-name>` works for all servers
- **Automatic Entry Points**: Extracts entry points from each server's `pyproject.toml`

### How It Works
1. **Scans `mcps/` folder** for directories containing `pyproject.toml`
2. **Extracts entry points** automatically (e.g., `server-mcp = "module:main"`)
3. **Creates server names** by removing `-mcp` suffix from entry points
4. **Maps to directories** using actual folder names

## Step-by-Step Transformation

### Step 1: Create the Launcher Package

Create `src/iowarp_mcps/__init__.py`:

```python
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

# Map directory names to their entry point commands
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

# Map directory names to actual directory names (for case sensitivity)
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
    """Launch scientific MCP servers with isolated dependencies using uvx"""
    
    if not server:
        click.echo("Available servers:")
        for s in list_available_servers():
            click.echo(f"  - {s}")
        click.echo("\nUsage: uvx iowarp-mcps <server-name>")
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
        # Run from local path
        servers_path = get_servers_path()
        actual_dir = DIR_NAME_MAP[server_lower]
        server_path = servers_path / actual_dir
        
        if not server_path.exists():
            click.echo(f"Error: Server directory not found: {server_path}")
            sys.exit(1)
        
        cmd = [
            "uvx",
            "--from",
            str(server_path),
            entry_command
        ]
    
    # Add any additional arguments
    cmd.extend(args)
    
    # Execute the command
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
    except FileNotFoundError:
        click.echo("Error: uvx not found. Please install uv: https://github.com/astral-sh/uv")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Step 2: Update Root pyproject.toml

Replace your current `pyproject.toml` with:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "iowarp-mcps"
version = "0.2.0"
description = "Open Source MCP Servers for Scientific Computing"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [
    {name = "IOWarp Team", email = "team@iowarp.com"}
]
dependencies = [
    "click>=8.1.0",
]

[project.urls]
Homepage = "https://github.com/iowarp/iowarp-mcps"
Repository = "https://github.com/iowarp/iowarp-mcps"
Issues = "https://github.com/iowarp/iowarp-mcps/issues"

[project.scripts]
iowarp-mcps = "iowarp_mcps:main"

[tool.hatch.build]
packages = ["src/iowarp_mcps"]

[tool.hatch.build.targets.wheel]
packages = ["src/iowarp_mcps"]

# Include all server directories in the wheel
[tool.hatch.build.targets.wheel.force-include]
"Adios" = "iowarp_mcps/servers/Adios"
"Arxiv" = "iowarp_mcps/servers/Arxiv"
"Chronolog" = "iowarp_mcps/servers/Chronolog"
"Compression" = "iowarp_mcps/servers/Compression"
"Darshan" = "iowarp_mcps/servers/Darshan"
"HDF5" = "iowarp_mcps/servers/HDF5"
"Jarvis" = "iowarp_mcps/servers/Jarvis"
"lmod" = "iowarp_mcps/servers/lmod"
"Node_Hardware" = "iowarp_mcps/servers/Node_Hardware"
"Pandas" = "iowarp_mcps/servers/Pandas"
"Parallel_Sort" = "iowarp_mcps/servers/Parallel_Sort"
"parquet" = "iowarp_mcps/servers/parquet"
"Plot" = "iowarp_mcps/servers/Plot"
"Slurm" = "iowarp_mcps/servers/Slurm"

[tool.hatch.build.targets.sdist]
include = [
    "/src",
    "/Adios",
    "/Arxiv",
    "/Chronolog",
    "/Compression",
    "/Darshan",
    "/HDF5",
    "/Jarvis",
    "/lmod",
    "/Node_Hardware",
    "/Pandas",
    "/Parallel_Sort",
    "/parquet",
    "/Plot",
    "/Slurm",
    "/README.md",
    "/pyproject.toml"
]
```

### Step 3: Standardize Server Configurations

For each server, ensure the pyproject.toml follows this pattern:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "server-name-mcp"
version = "0.1.0"
description = "MCP server for [functionality]"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "mcp[cli]>=1.0.0",
    "fastmcp",
    # server-specific dependencies
]

[project.scripts]
mcp-server-name = "module_name:main"

[tool.hatch.build]
packages = ["src"]
```

### Step 4: Fix Server Entry Points

Some servers have inconsistent module paths. Standardize them:

1. **Adios**: Change `"server:main"` to `"implementation.server:main"` or create proper init
2. **Compression, Parallel_Sort, parquet**: Change `"server:main"` to `"src.server:main"`
3. **Jarvis, Node_Hardware, etc**: Already use `"src.server:main"`

### Step 5: Create Directory Structure

```bash
# Create the launcher directory
mkdir -p src/iowarp_mcps

# Create __init__.py with the launcher code
# (Copy the code from Step 1)

# Initialize with uv
uv init --package iowarp-mcps

# Add dependencies
uv add click
```

### Step 6: Update manifest.json Files

For each server that has a manifest.json, update the command to use the launcher:

```json
{
  "server": {
    "type": "python",
    "entry_point": "",
    "mcp_config": {
      "command": "uvx",
      "args": ["iowarp-mcps", "server-name"],
      "env": {}
    }
  }
}
```

### Step 7: Set Up PyPI Publishing

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:

permissions:
  contents: read
  id-token: write

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/p/iowarp-mcps
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install uv
      uses: astral-sh/setup-uv@v3
    
    - name: Build package
      run: uv build
    
    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
```

## Usage After Setup

### For Users (after PyPI publication):
```bash
# Install and run any server
uvx iowarp-mcps adios
uvx iowarp-mcps hdf5
uvx iowarp-mcps slurm --help

# List available servers
uvx iowarp-mcps
```

### For Development:
```bash
# Install locally
uv sync

# Run directly
python -m iowarp_mcps adios

# Or install and run
uv pip install -e .
iowarp-mcps hdf5
```

## Benefits

1. **Clean Command**: `uvx iowarp-mcps <server>` instead of remembering individual commands
2. **Isolated Dependencies**: Each server runs with its own dependencies via uvx
3. **Easy Discovery**: Users can list available servers
4. **Backward Compatible**: Individual server commands still work
5. **PyPI Distribution**: Single package installation for all servers
6. **Development Friendly**: Works both in development and production

## Migration Checklist

- [ ] Create src/iowarp_mcps/__init__.py with launcher
- [ ] Update root pyproject.toml to use hatchling
- [ ] Standardize all server pyproject.toml files
- [ ] Fix inconsistent entry points
- [ ] Update manifest.json files
- [ ] Test each server with new launcher
- [ ] Set up GitHub Actions for PyPI publishing
- [ ] Configure PyPI trusted publishing
- [ ] Document the new usage in README

This architecture provides the same elegant experience as mcp.science while maintaining your existing server structure!