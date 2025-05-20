# ADIOS MCP Server

A read-only Model Context Protocol (MCP) server for ADIOS datasets, enabling LLMS to query scientific simulation and real-time data.

## Key Features

- **Read-Only ADIOS Access**  
  Uses the ADIOS2 Python API to list files, inspect variables, and retrieve data slices or full arrays without modifying the source.

- **Standardized MCP Interface**  
  Exposes data-access tools (e.g. `list_datasets`, `list_variables`, `read_variable`, `get_stats`) via the MCP JSON-RPC protocol.

- **Local LLM Integration**  
  Connects to on-device language models through MCP, allowing natural-language queries and inference without internet or cloud dependencies.

- **Cross-Platform**  
  Pure Python implementation runs on Linux, macOS, and Windows. Package installable via `pip` or Spack.

## Architecture

 ![](https://github.com/sohamvsonar/AdiosMCP/blob/main/assets/architecture.png)


## Example Use-Cases

Pre-simulation exploration (“What’s the pressure range in runA.bp?”)

Real-time sensor alerts (“Notify me when wind_speed > 20 m/s”)

Post-processing summaries (“Average temperature over steps 0–100 in simulation.hdf5”)

Interactive teaching and notebook integration