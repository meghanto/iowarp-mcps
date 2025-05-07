import pytest
import asyncio
import random
from src.capabilities.hdf5_handler import HDF5Handler
from src.capabilities.slurm_handler import SlurmHandler
from src.capabilities.node_hardware import NodeHardwareHandler
from src.capabilities.compression import CompressionHandler


@pytest.mark.asyncio
async def test_node_hardware_get_cpu_info():
    """Test getting CPU information."""
    handler = NodeHardwareHandler()
    result = await handler.get_cpu_info()

    assert "cpu_count" in result
    assert isinstance(result["cpu_count"], int)
    assert "system" in result
    assert "processor" in result
    assert "architecture" in result


@pytest.mark.asyncio
async def test_node_hardware_get_memory_info():
    """Test getting memory information."""
    handler = NodeHardwareHandler()
    result = await handler.get_memory_info()

    assert "total_memory_gb" in result
    assert "available_memory_gb" in result
    assert "used_memory_gb" in result
    assert "percent_used" in result


@pytest.mark.asyncio
async def test_node_hardware_get_system_info():
    """Test getting system information."""
    handler = NodeHardwareHandler()
    result = await handler.get_system_info()

    assert "node_name" in result
    assert "system" in result
    assert "cpu" in result
    assert "memory" in result
    assert "disk" in result


@pytest.mark.asyncio
async def test_compression_compress_data():
    """Test compressing string data."""
    handler = CompressionHandler()
    test_data = "This is some test data to compress. " * 10

    # Test with gzip
    result = await handler.compress_data(test_data, "gzip")
    assert "algorithm" in result
    assert result["algorithm"] == "gzip"
    assert "original_size_bytes" in result
    assert "compressed_size_bytes" in result
    assert "compression_ratio" in result
    assert "compressed_data_b64" in result
    assert result["original_size_bytes"] > result["compressed_size_bytes"]

    # Test with zlib
    result = await handler.compress_data(test_data, "zlib")
    assert result["algorithm"] == "zlib"
    assert result["original_size_bytes"] > result["compressed_size_bytes"]

    # Test with empty data
    with pytest.raises(ValueError):
        await handler.compress_data("", "gzip")

    # Test with invalid algorithm
    with pytest.raises(ValueError):
        await handler.compress_data(test_data, "invalid_algo")


@pytest.mark.asyncio
async def test_compression_compress_file():
    """Test compressing a file."""
    handler = CompressionHandler()

    # Test with valid file path
    result = await handler.compress_file("/path/to/file.txt")
    assert "algorithm" in result
    assert "original_file" in result
    assert "compressed_file" in result
    assert "compression_ratio" in result

    # Test with output path specified
    result = await handler.compress_file("/path/to/file.txt", "/path/to/output.gz")
    assert result["compressed_file"] == "/path/to/output.gz"

    # Test with invalid file path
    with pytest.raises(FileNotFoundError):
        await handler.compress_file("/nonexistent/file.txt")

    # Test with empty file path
    with pytest.raises(ValueError):
        await handler.compress_file("")


@pytest.mark.asyncio
async def test_compression_decompress_data():
    """Test decompressing data."""
    handler = CompressionHandler()

    # First compress some data to get valid compressed data
    test_data = "This is some test data to decompress. " * 10
    compress_result = await handler.compress_data(test_data, "gzip")

    # Now test decompression
    decompress_result = await handler.decompress_data(
            compress_result["full_compressed_data_b64"],
            "gzip"
            )

    assert "algorithm" in decompress_result
    assert "compressed_size_bytes" in decompress_result
    assert "decompressed_size_bytes" in decompress_result
    assert "decompressed_data" in decompress_result
    assert "full_decompressed_data" in decompress_result
    assert decompress_result["full_decompressed_data"] == test_data

    # Test with empty data
    with pytest.raises(ValueError):
        await handler.decompress_data("", "gzip")

    # Test with invalid algorithm
    with pytest.raises(ValueError):
        await handler.decompress_data(compress_result["full_compressed_data_b64"],
                                      "invalid_algo")
