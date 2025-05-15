import pytest
from src.capabilities.slurm_handler import handle_request

@pytest.fixture
def create_mock_script(tmp_path):
    script_path = tmp_path / "test_script.sh"
    script_path.write_text("#!/bin/bash\necho 'Hello World'")
    return str(script_path)

@pytest.mark.asyncio
async def test_slurm_submission(create_mock_script):
    response = await handle_request({
        "script": create_mock_script,
        "cores": 4,
        "memory": "8GB"
    })
    assert "jobId" in response["result"]
    assert response["result"]["status"] == "PENDING"

@pytest.mark.asyncio
async def test_slurm_missing_parameters():
    response = await handle_request({})
    assert response["error"]["code"] == -32602
