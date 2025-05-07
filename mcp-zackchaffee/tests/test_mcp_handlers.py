import pytest
import asyncio
from src.mcp_handlers import (
        handle_list_resources,
        handle_list_tools,
        handle_get_resource,
        handle_call_tool
        )


@pytest.mark.asyncio
async def test_handle_list_resources():
    """Test that list_resources returns a list of resources."""
    result = await handle_list_resources({})
    assert "resources" in result
    assert isinstance(result["resources"], list)
    assert len(result["resources"]) > 0

    # Check structure of a resource
    resource = result["resources"][0]
    assert "id" in resource
    assert "name" in resource
    assert "type" in resource
    assert resource["type"] == "hdf5"


@pytest.mark.asyncio
async def test_handle_list_tools():
    """Test that list_tools returns a list of tools."""
    result = await handle_list_tools({})
    assert "tools" in result
    assert isinstance(result["tools"], list)
    assert len(result["tools"]) > 0

    # Check for both HDF5 and Slurm tools
    tool_ids = [tool["id"] for tool in result["tools"]]
    assert any(id.startswith("hdf5.") for id in tool_ids)
    assert any(id.startswith("slurm.") for id in tool_ids)

    # Check structure of a tool
    tool = result["tools"][0]
    assert "id" in tool
    assert "name" in tool
    assert "description" in tool
    assert "parameters" in tool
    assert "returns" in tool


@pytest.mark.asyncio
async def test_handle_get_resource():
    """Test that get_resource returns details for a specific resource."""
    # Test with a valid resource ID
    result = await handle_get_resource({"id": "hdf5:/data/samples/sample1.h5"})
    assert "resource" in result
    assert result["resource"]["id"] == "hdf5:/data/samples/sample1.h5"
    assert "structure" in result["resource"]["metadata"]

    # Test with missing resource ID
    with pytest.raises(ValueError):
        await handle_get_resource({})

    # Test with unsupported resource type
    with pytest.raises(ValueError):
        await handle_get_resource({"id": "unsupported:resource"})


@pytest.mark.asyncio
async def test_handle_call_tool_hdf5_read():
    """Test calling the HDF5 read_dataset tool."""
    result = await handle_call_tool({
        "id": "hdf5.read_dataset",
        "parameters": {
            "file_path": "/data/samples/sample1.h5",
            "dataset_path": "group1/temperature"
            }
        })

    assert "result" in result
    assert "data" in result["result"]
    assert "shape" in result["result"]
    assert "dtype" in result["result"]
    assert "attributes" in result["result"]


@pytest.mark.asyncio
async def test_handle_call_tool_slurm_submit():
    """Test calling the Slurm submit_job tool."""
    result = await handle_call_tool({
        "id": "slurm.submit_job",
        "parameters": {
            "script_path": "/path/to/job.sh",
            "job_name": "test_job"
            }
        })

    assert "result" in result
    assert "job_id" in result["result"]
    assert "status" in result["result"]
    assert result["result"]["status"] == "submitted"


@pytest.mark.asyncio
async def test_handle_call_tool_slurm_status():
    """Test calling the Slurm get_job_status tool."""
    # First submit a job to get a job ID
    submit_result = await handle_call_tool({
        "id": "slurm.submit_job",
        "parameters": {
            "script_path": "/path/to/job.sh"
            }
        })

    job_id = submit_result["result"]["job_id"]

    # Now get status for that job
    result = await handle_call_tool({
        "id": "slurm.get_job_status",
        "parameters": {
            "job_id": job_id
            }
        })

    assert "result" in result
    assert "job_id" in result["result"]
    assert "state" in result["result"]
    assert result["result"]["job_id"] == job_id


@pytest.mark.asyncio
async def test_handle_call_tool_invalid():
    """Test calling an invalid tool."""
    with pytest.raises(ValueError):
        await handle_call_tool({
            "id": "invalid.tool",
            "parameters": {}
            })

    with pytest.raises(ValueError):
        await handle_call_tool({})
