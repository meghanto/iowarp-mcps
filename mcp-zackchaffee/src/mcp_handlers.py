from typing import Dict, Any, List
import logging
from .capabilities.hdf5_handler import HDF5Handler
from .capabilities.slurm_handler import SlurmHandler
from .capabilities.node_hardware import NodeHardwareHandler
from .capabilities.compression import CompressionHandler

logger = logging.getLogger(__name__)

# Initialize capability handlers
hdf5_handler = HDF5Handler()
slurm_handler = SlurmHandler()
node_hardware_handler = NodeHardwareHandler()
compression_handler = CompressionHandler()


async def handle_list_resources(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle mcp/listResources requests.

    Returns a list of available MCP resources.
    """
    # Simulate listing available HDF5 files as resources
    resources = await hdf5_handler.list_available_resources()

    return {
            "resources": resources
            }


async def handle_list_tools(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle mcp/listTools requests.

    Returns a list of available MCP tools.
    """
    tools = [
            # HDF5 tools
            {
                "id": "hdf5.read_dataset",
                "name": "Read HDF5 Dataset",
                "description": "Read data from an HDF5 dataset",
                "parameters": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the HDF5 file"
                        },
                    "dataset_path": {
                        "type": "string",
                        "description": "Path to the dataset within the file"
                        }
                    },
                "returns": {
                    "data": {
                        "type": "array",
                        "description": "The dataset content"
                        },
                    "metadata": {
                        "type": "object",
                        "description": "Dataset metadata"
                        }
                    }
                },
            {
                "id": "hdf5.list_contents",
                "name": "List HDF5 Contents",
                "description": "List groups and datasets in an HDF5 file",
                "parameters": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the HDF5 file"
                        },
                    "group_path": {
                        "type": "string",
                        "description": "Path to the group within the file (optional)",
                        "optional": True
                        }
                    },
                "returns": {
                    "groups": {
                        "type": "array",
                        "description": "List of groups"
                        },
                    "datasets": {
                        "type": "array",
                        "description": "List of datasets"
                        }
                    }
                },
        # Slurm tools
        {
                "id": "slurm.submit_job",
                "name": "Submit Slurm Job",
                "description": "Submit a job to the Slurm scheduler",
                "parameters": {
                    "script_path": {
                        "type": "string",
                        "description": "Path to the job script"
                        },
                    "job_name": {
                        "type": "string",
                        "description": "Name for the job (optional)",
                        "optional": True
                        },
                    "partition": {
                        "type": "string",
                        "description": "Slurm partition to use (optional)",
                        "optional": True
                        }
                    },
                "returns": {
                    "job_id": {
                        "type": "string",
                        "description": "The assigned job ID"
                        },
                    "status": {
                        "type": "string",
                        "description": "Submission status"
                        }
                    }
                },
        {
                "id": "slurm.get_job_status",
                "name": "Get Slurm Job Status",
                "description": "Check the status of a Slurm job",
                "parameters": {
                    "job_id": {
                        "type": "string",
                        "description": "The Slurm job ID"
                        }
                    },
                "returns": {
                    "status": {
                        "type": "string",
                        "description": "Current job status"
                        },
                    "details": {
                        "type": "object",
                        "description": "Additional job details"
                        }
                    }
                },
        # Node Hardware tools
        {
                "id": "node.get_cpu_info",
                "name": "Get CPU Information",
                "description": "Get information about the CPU on the current node",
                "parameters": {},
                "returns": {
                    "cpu_count": {
                        "type": "integer",
                        "description": "Number of CPU cores"
                        },
                    "system": {
                        "type": "string",
                        "description": "Operating system name"
                        },
                    "processor": {
                        "type": "string",
                        "description": "Processor information"
                        }
                    }
                },
        {
                "id": "node.get_memory_info",
                "name": "Get Memory Information",
                "description": "Get information about memory on the current node",
                "parameters": {},
                "returns": {
                    "total_memory_gb": {
                        "type": "number",
                        "description": "Total memory in GB"
                        },
                    "available_memory_gb": {
                        "type": "number",
                        "description": "Available memory in GB"
                        },
                    "used_memory_gb": {
                        "type": "number",
                        "description": "Used memory in GB"
                        }
                    }
                },
        {
                "id": "node.get_system_info",
                "name": "Get System Information",
                "description": "Get comprehensive system information about the current node",
                "parameters": {},
                "returns": {
                    "node_name": {
                        "type": "string",
                        "description": "Node hostname"
                        },
                    "system": {
                        "type": "string",
                        "description": "Operating system"
                        },
                    "cpu": {
                        "type": "object",
                        "description": "CPU information"
                        },
                    "memory": {
                        "type": "object",
                        "description": "Memory information"
                        },
                    "disk": {
                        "type": "object",
                        "description": "Disk information"
                        }
                    }
                },
        # Compression tools
        {
                "id": "compression.compress_data",
                "name": "Compress Data",
                "description": "Compress a string using the specified algorithm",
                "parameters": {
                    "data": {
                        "type": "string",
                        "description": "The string data to compress"
                        },
                    "algorithm": {
                        "type": "string",
                        "description": "Compression algorithm to use (gzip or zlib)",
                        "optional": True
                        }
                    },
                "returns": {
                    "algorithm": {
                        "type": "string",
                        "description": "Compression algorithm used"
                        },
                    "original_size_bytes": {
                        "type": "integer",
                        "description": "Original data size in bytes"
                        },
                    "compressed_size_bytes": {
                        "type": "integer",
                        "description": "Compressed data size in bytes"
                        },
                    "compression_ratio": {
                        "type": "number",
                        "description": "Compression ratio (original / compressed)"
                        },
                    "compressed_data_b64": {
                        "type": "string",
                        "description": "Base64 encoded compressed data (truncated)"
                        }
                    }
                },
        {
                "id": "compression.compress_file",
                "name": "Compress File",
                "description": "Compress a file using the specified algorithm",
                "parameters": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to compress"
                        },
                    "output_path": {
                        "type": "string",
                        "description": "Path for the compressed output file (optional)",
                        "optional": True
                        },
                    "algorithm": {
                        "type": "string",
                        "description": "Compression algorithm to use (gzip or zlib)",
                        "optional": True
                        }
                    },
                "returns": {
                    "algorithm": {
                        "type": "string",
                        "description": "Compression algorithm used"
                        },
                    "original_file": {
                        "type": "string",
                        "description": "Path to the original file"
                        },
                    "compressed_file": {
                        "type": "string",
                        "description": "Path to the compressed file"
                        },
                    "compression_ratio": {
                        "type": "number",
                        "description": "Compression ratio (original / compressed)"
                        }
                    }
                },
        {
                "id": "compression.decompress_data",
                "name": "Decompress Data",
                "description": "Decompress a base64-encoded compressed string",
                "parameters": {
                    "compressed_data_b64": {
                        "type": "string",
                        "description": "Base64-encoded compressed data"
                        },
                    "algorithm": {
                        "type": "string",
                        "description": "Compression algorithm used (gzip or zlib)",
                        "optional": True
                        }
                    },
                "returns": {
                    "algorithm": {
                        "type": "string",
                        "description": "Compression algorithm used"
                        },
                    "compressed_size_bytes": {
                        "type": "integer",
                        "description": "Compressed data size in bytes"
                        },
                    "decompressed_size_bytes": {
                        "type": "integer",
                        "description": "Decompressed data size in bytes"
                        },
                    "decompressed_data": {
                        "type": "string",
                        "description": "Decompressed data (truncated)"
                        }
                    }
                }
    ]

    return {
            "tools": tools
            }


async def handle_get_resource(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle mcp/getResource requests.

    Returns details about a specific resource.
    """
    resource_id = params.get("id")
    if not resource_id:
        raise ValueError("Resource ID not provided")

    # For this assignment, we'll simulate resource retrieval for HDF5 files
    if resource_id.startswith("hdf5:"):
        file_path = resource_id.replace("hdf5:", "", 1)
        resource_details = await hdf5_handler.get_resource_details(file_path)
        return {
                "resource": resource_details
                }
    else:
        raise ValueError(f"Unsupported resource type: {resource_id}")


async def handle_call_tool(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle mcp/callTool requests.

    Executes a tool with the provided parameters.
    """
    tool_id = params.get("id")
    tool_params = params.get("parameters", {})

    if not tool_id:
        raise ValueError("Tool ID not provided")

    # Route to appropriate handler based on tool ID
    if tool_id == "hdf5.read_dataset":
        result = await hdf5_handler.read_dataset(
                tool_params.get("file_path", ""),
                tool_params.get("dataset_path", "")
                )
        return {
                "result": result
                }
    elif tool_id == "hdf5.list_contents":
        result = await hdf5_handler.list_contents(
                tool_params.get("file_path", ""),
                tool_params.get("group_path", "/")
                )
        return {
                "result": result
                }
    elif tool_id == "slurm.submit_job":
        result = await slurm_handler.submit_job(
                tool_params.get("script_path", ""),
                tool_params.get("job_name"),
                tool_params.get("partition")
                )
        return {
                "result": result
                }
    elif tool_id == "slurm.get_job_status":
        result = await slurm_handler.get_job_status(
                tool_params.get("job_id", "")
                )
        return {
                "result": result
                }
    # Node Hardware Tools
    elif tool_id == "node.get_cpu_info":
        result = await node_hardware_handler.get_cpu_info()
        return {
                "result": result
                }
    elif tool_id == "node.get_memory_info":
        result = await node_hardware_handler.get_memory_info()
        return {
                "result": result
                }
    elif tool_id == "node.get_system_info":
        result = await node_hardware_handler.get_system_info()
        return {
                "result": result
                }
        # Compression Tools
    elif tool_id == "compression.compress_data":
        result = await compression_handler.compress_data(
                tool_params.get("data", ""),
                tool_params.get("algorithm", "gzip")
                )
        return {
                "result": result
                }
    elif tool_id == "compression.compress_file":
        result = await compression_handler.compress_file(
                tool_params.get("file_path", ""),
                tool_params.get("output_path"),
                tool_params.get("algorithm", "gzip")
                )
        return {
                "result": result
                }
    elif tool_id == "compression.decompress_data":
        result = await compression_handler.decompress_data(
                tool_params.get("compressed_data_b64", ""),
                tool_params.get("algorithm", "gzip")
                )
        return {
                "result": result
                }
    else:
        raise ValueError(f"Unsupported tool: {tool_id}")
