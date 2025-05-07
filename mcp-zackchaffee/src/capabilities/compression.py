import gzip
import zlib
import base64
import os
import logging
import random
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class CompressionHandler:
    """
    Handles compression operations as part of MCP capability.
    """

    async def compress_data(self, data: str, algorithm: str = "gzip") -> Dict[str, Any]:
        """
        Compress a string using the specified algorithm.

        Args:
            data: The string data to compress
            algorithm: Compression algorithm to use (gzip or zlib)

        Returns:
            Dictionary with compressed data information
        """
        if not data:
            raise ValueError("Data cannot be empty")

        # Convert string to bytes
        data_bytes = data.encode('utf-8')
        original_size = len(data_bytes)

        try:
            # Compress using the specified algorithm
            if algorithm.lower() == "gzip":
                compressed_bytes = gzip.compress(data_bytes)
            elif algorithm.lower() == "zlib":
                compressed_bytes = zlib.compress(data_bytes)
            else:
                raise ValueError(f"Unsupported compression algorithm: {algorithm}")

            # Calculate compression ratio
            compressed_size = len(compressed_bytes)
            compression_ratio = original_size / compressed_size if compressed_size > 0 else 0

            # Base64 encode for JSON compatibility
            compressed_b64 = base64.b64encode(compressed_bytes).decode('utf-8')

            return {
                    "algorithm": algorithm,
                    "original_size_bytes": original_size,
                    "compressed_size_bytes": compressed_size,
                    "compression_ratio": round(compression_ratio, 2),
                    "compressed_data_b64": compressed_b64[:100] + "..." if len(compressed_b64) > 100 else compressed_b64,
                    "full_compressed_data_b64": compressed_b64
                    }
        except Exception as e:
            logger.error(f"Error compressing data: {str(e)}")
            raise

    async def compress_file(self, file_path: str, output_path: Optional[str] = None, 
                            algorithm: str = "gzip") -> Dict[str, Any]:
        """
        Compress a file using the specified algorithm.

        Args:
            file_path: Path to the file to compress
            output_path: Path for the compressed output file (optional)
            algorithm: Compression algorithm to use (gzip or zlib)

        Returns:
            Dictionary with compressed file information
        """
        if not file_path:
            raise ValueError("File path cannot be empty")

        # Determine output path if not provided
        if output_path is None:
            if algorithm.lower() == "gzip":
                output_path = f"{file_path}.gz"
            elif algorithm.lower() == "zlib":
                output_path = f"{file_path}.zz"
            else:
                raise ValueError(f"Unsupported compression algorithm: {algorithm}")

        # Simulate file existence check
        if not self._simulate_file_exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            # Simulate file sizes and compression ratio
            original_size = random.randint(1000000, 10000000)  # 1-10 MB
            compression_ratio = 3.5 if algorithm.lower() == "gzip" else 4.2  # Typical ratios
            compressed_size = int(original_size / compression_ratio)

            return {
                    "algorithm": algorithm,
                    "original_file": file_path,
                    "compressed_file": output_path,
                    "original_size_bytes": original_size,
                    "compressed_size_bytes": compressed_size,
                    "compression_ratio": round(compression_ratio, 2),
                    "simulated": True
                    }
        except Exception as e:
            logger.error(f"Error compressing file: {str(e)}")
            raise

    async def decompress_data(self, compressed_data_b64: str, algorithm: str = "gzip") -> Dict[str, Any]:
        """
        Decompress a base64-encoded compressed string.

        Args:
            compressed_data_b64: Base64-encoded compressed data
            algorithm: Compression algorithm used (gzip or zlib)

        Returns:
            Dictionary with decompressed data information
        """
        if not compressed_data_b64:
            raise ValueError("Compressed data cannot be empty")

        try:
            # Decode base64 to bytes
            compressed_bytes = base64.b64decode(compressed_data_b64)

            # Decompress using the specified algorithm
            if algorithm.lower() == "gzip":
                decompressed_bytes = gzip.decompress(compressed_bytes)
            elif algorithm.lower() == "zlib":
                decompressed_bytes = zlib.decompress(compressed_bytes)
            else:
                raise ValueError(f"Unsupported compression algorithm: {algorithm}")

            # Convert bytes back to string
            decompressed_data = decompressed_bytes.decode('utf-8')

            return {
                    "algorithm": algorithm,
                    "compressed_size_bytes": len(compressed_bytes),
                    "decompressed_size_bytes": len(decompressed_bytes),
                    "decompressed_data": decompressed_data[:100] + "..." if len(decompressed_data) > 100 else decompressed_data,
                    "full_decompressed_data": decompressed_data
                    }
        except Exception as e:
            logger.error(f"Error decompressing data: {str(e)}")
            raise

    def _simulate_file_exists(self, file_path: str) -> bool:
        """
        Simulate checking if a file exists.

        Args:
            file_path: Path to the file

        Returns:
            True if the file exists (simulated), False otherwise
        """
        if "nonexistent" in file_path or not file_path:
            return False
        return True
