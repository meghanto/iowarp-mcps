---
title: Adios MCP
description: "ADIOS MCP is a comprehensive Model Context Protocol (MCP) server that enables Language Learning Models (LLMs) to access and analyze scientific simulation and real-time data through the ADIOS2 framework. This server provides read-only access to BP5 datasets with intelligent data handling and seaml..."
---

import MCPDetail from '@site/src/components/MCPDetail';

<MCPDetail 
  name="Adios"
  icon="📊"
  category="Data Processing"
  description="ADIOS MCP is a comprehensive Model Context Protocol (MCP) server that enables Language Learning Models (LLMs) to access and analyze scientific simulation and real-time data through the ADIOS2 framework. This server provides read-only access to BP5 datasets with intelligent data handling and seamless integration with AI coding assistants."
  version="1.0.0"
  actions={["list_bp5", "inspect_variables", "inspect_variables_at_step", "inspect_attributes", "read_variable_at_step"]}
  platforms={["claude", "cursor", "vscode"]}
>

## Advanced Features


### High-Performance Data Processing
This MCP provides optimized data processing capabilities:
- **Fast I/O Operations**: Efficient reading and writing of data
- **Format Support**: Multiple data format compatibility
- **Memory Optimization**: Smart memory usage for large datasets

### Integration Ready
- **Pipeline Compatible**: Works seamlessly in data processing pipelines
- **Cross-format**: Convert between different data formats
- **Scalable**: Handles datasets of various sizes


## Available Actions


#### `list_bp5`
Lists all BP5 files in a given directory, the bp5 files are actually directories so both file and directory words are correct. The 'directory' parameter must be an absolute path.

**Usage Example:**
```python
# Use list_bp5 function
result = list_bp5()
print(result)
```


#### `inspect_variables`
Inspects variables in a BP5 file. If variable_name is provided, returns data for that specific variable. Otherwise, shows type, shape, and steps for all variables. The 'filename' parameter must be ...

**Usage Example:**
```python
# Use inspect_variables function
result = inspect_variables()
print(result)
```


#### `inspect_variables_at_step`
Inspects a specific variable at a given step in a BP5 file. Shows variable type, shape, min, max. All parameters are required. The 'filename' must be an absolute path.

**Usage Example:**
```python
# Use inspect_variables_at_step function
result = inspect_variables_at_step()
print(result)
```


#### `inspect_attributes`
Reads global or variable-specific attributes from a BP5 file. The 'filename' parameter must be an absolute path. The 'variable_name' is optional.

**Usage Example:**
```python
# Use inspect_attributes function
result = inspect_attributes()
print(result)
```


#### `read_variable_at_step`
Reads a named variable at a specific step from a BP5 file. All parameters are required. The 'filename' must be an absolute path.

**Usage Example:**
```python
# Use read_variable_at_step function
result = read_variable_at_step()
print(result)
```


## Integration Examples


### Data Processing Workflow
```python
# Load and process data with Adios MCP
data = load_data("input_file")
processed = process_data(data)

# Integrate with other MCPs
visualization = create_plot(processed, "chart_type")
save_results(processed, "output_file")
```

### Batch Processing
```python
# Process multiple files
files = list_files("data_directory")
for file in files:
    data = load_data(file)
    result = process_data(data)
    save_processed(result, f"processed_{file}")
```


</MCPDetail>
