import pytest
from src.capabilities.hdf5_handler import handle_request
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

@pytest.mark.asyncio
async def test_hdf5_list():
    response = await handle_request({
        "action": "list",
        "path": "simulations",
        "pattern": "*.h5"
    })
    assert "files" in response["result"]
    assert isinstance(response["result"]["files"], list)

@pytest.mark.asyncio
async def test_hdf5_read():
    response = await handle_request({
        "action": "read",
        "filePath": "test_data.h5",
        "dataset": "temperature"
    })
    assert "dataset" in response["result"]
    assert response["result"]["dataset"] == "temperature"

@pytest.mark.asyncio
async def test_hdf5_invalid_action():
    response = await handle_request({"action": "invalid"})
    assert response["error"]["code"] == -32602