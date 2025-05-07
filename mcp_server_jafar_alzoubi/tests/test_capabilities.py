import pytest
from pathlib import Path
from src.capabilities import hdf5_handler, slurm_handler
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
@pytest.fixture
def mock_hdf5_dir(tmp_path):
    hdf5_dir = tmp_path / "hdf5"
    hdf5_dir.mkdir()
    (hdf5_dir / "data1.hdf5").touch()
    (hdf5_dir / "data2.hdf5").touch()
    return hdf5_dir

def test_hdf5_handler_success(mock_hdf5_dir):
    hdf5_handler.MOCK_DATA_ROOT = mock_hdf5_dir.parent
    result = hdf5_handler.handle({"path_pattern": "hdf5/*"})
    assert result["status"] == "success"
    assert len(result["data"]["files"]) == 2

def test_hdf5_handler_invalid_path():
    result = hdf5_handler.handle({"path_pattern": "/invalid/path/*"})
    assert result["status"] == "error"
    assert "Invalid base directory" in result["message"]

def test_slurm_handler_success():
    params = {"script_path": "/jobs/run.sh", "cores": 8}
    result = slurm_handler.handle(params)
    assert result["status"] == "success"
    assert len(result["data"]["job_id"]) == 13
    assert slurm_handler.jobs_db.get(result["data"]["job_id"]) is not None

def test_slurm_handler_missing_script():
    result = slurm_handler.handle({"cores": 4})
    assert result["status"] == "error"
    assert "script_path" in result["message"]