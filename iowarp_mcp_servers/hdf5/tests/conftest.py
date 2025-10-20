"""
Pytest configuration and shared fixtures for HDF5 MCP tests.

Provides test fixtures for:
- Sample HDF5 files
- Mock FastMCP contexts
- Test data generation
- Resource cleanup
"""

import pytest
import tempfile
import h5py
import numpy as np
from pathlib import Path
from unittest.mock import Mock, AsyncMock


@pytest.fixture
def temp_dir():
    """Temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_hdf5_file(temp_dir):
    """Create a sample HDF5 file with realistic scientific data structure."""
    filepath = temp_dir / "test_data.h5"

    with h5py.File(filepath, 'w') as f:
        # Root level metadata
        f.attrs['experiment'] = 'Sample Experiment'
        f.attrs['version'] = '1.0.0'
        f.attrs['timestamp'] = '2025-01-15T10:30:00Z'

        # Create group structure
        grp_results = f.create_group('results')
        grp_metadata = f.create_group('metadata')

        # Add datasets with various types and shapes
        grp_results.create_dataset('temperature', data=np.random.rand(100, 50))
        grp_results.create_dataset('pressure', data=np.random.rand(100, 50))
        grp_results.create_dataset('velocity', data=np.random.rand(100, 50, 3))

        # Add metadata datasets
        grp_metadata.create_dataset('timestamps', data=np.arange(100))
        grp_metadata.create_dataset('sensor_ids', data=np.arange(50))

        # Add attributes to datasets
        grp_results['temperature'].attrs['unit'] = 'Kelvin'
        grp_results['temperature'].attrs['min_value'] = 273.15
        grp_results['temperature'].attrs['max_value'] = 373.15

        grp_results['pressure'].attrs['unit'] = 'Pascal'

        # Create chunked dataset for testing
        grp_results.create_dataset(
            'large_data',
            data=np.random.rand(1000, 1000),
            chunks=(100, 100),
            compression='gzip'
        )

    yield filepath


@pytest.fixture
def empty_hdf5_file(temp_dir):
    """Create an empty HDF5 file."""
    filepath = temp_dir / "empty.h5"
    with h5py.File(filepath, 'w') as f:
        f.attrs['empty'] = True
    yield filepath


@pytest.fixture
def large_hdf5_file(temp_dir):
    """Create a large HDF5 file for streaming tests."""
    filepath = temp_dir / "large_data.h5"

    with h5py.File(filepath, 'w') as f:
        # Create large dataset (10,000 x 10,000 = 100M floats = ~800MB)
        f.create_dataset(
            'simulation_data',
            data=np.random.rand(10000, 10000),
            chunks=(1000, 1000),
            compression='gzip'
        )
        f['simulation_data'].attrs['size_gb'] = 0.8

    yield filepath


@pytest.fixture
def mock_context():
    """Mock FastMCP Context for testing."""
    context = Mock()
    context.request_context = AsyncMock()
    context.request_context.return_value.__aenter__ = AsyncMock()
    context.request_context.return_value.__aexit__ = AsyncMock()
    context.report_progress = AsyncMock()
    context.sample_llm = AsyncMock(return_value="AI generated insight")
    context.request_user_input = AsyncMock(return_value="user input")
    return context


@pytest.fixture
def sample_datasets():
    """Provide sample dataset paths and expected metadata."""
    return {
        'temperature': {
            'path': '/results/temperature',
            'shape': (100, 50),
            'dtype': 'float64',
            'attrs': {'unit': 'Kelvin'}
        },
        'pressure': {
            'path': '/results/pressure',
            'shape': (100, 50),
            'dtype': 'float64',
            'attrs': {'unit': 'Pascal'}
        },
        'velocity': {
            'path': '/results/velocity',
            'shape': (100, 50, 3),
            'dtype': 'float64',
            'attrs': {}
        }
    }


@pytest.fixture(autouse=True)
def reset_global_state():
    """Reset global state between tests."""
    from hdf5_mcp import server

    yield

    # Cleanup after each test
    if server.current_file is not None:
        try:
            server.current_file.close()
        except:
            pass
        server.current_file = None


@pytest.fixture
def test_config():
    """Provide test configuration."""
    return {
        'cache_size': 100,
        'num_workers': 2,
        'show_performance': True,
        'data_dir': None
    }
