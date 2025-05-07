import os
import platform
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class NodeHardwareHandler:
    """
    Handles operations related to node hardware information as part of MCP capability.
    """

    async def get_cpu_info(self) -> Dict[str, Any]:
        """
        Get information about the CPU on the current node.

        Returns:
            Dictionary with CPU information
        """
        try:
            # Get CPU count
            cpu_count = os.cpu_count()

            # Get platform information
            system = platform.system()
            processor = platform.processor()
            architecture = platform.architecture()[0]
            machine = platform.machine()

            # Create a structured response
            return {
                    "cpu_count": cpu_count,
                    "system": system,
                    "processor": processor,
                    "architecture": architecture,
                    "machine": machine
                    }
        except Exception as e:
            logger.error(f"Error getting CPU info: {str(e)}")
            raise

    async def get_memory_info(self) -> Dict[str, Any]:
        """
        Get information about memory on the current node.

        Returns:
            Dictionary with memory information
        """
        try:
            # Simulate memory information
            return {
                    "total_memory_gb": 32,
                    "available_memory_gb": 24.5,
                    "used_memory_gb": 7.5,
                    "percent_used": 23.4,
                    "simulated": True
                    }
        except Exception as e:
            logger.error(f"Error getting memory info: {str(e)}")
            raise

    async def get_disk_info(self) -> Dict[str, Any]:
        """
        Get information about disk space on the current node.

        This is a simulation that returns realistic but mock values.

        Returns:
            Dictionary with disk information
        """
        try:
            # Simulate disk information
            return {
                    "mount_points": [
                        {
                            "path": "/",
                            "total_gb": 500,
                            "used_gb": 325,
                            "available_gb": 175,
                            "percent_used": 65.0
                            },
                        {
                            "path": "/data",
                            "total_gb": 2000,
                            "used_gb": 1200,
                            "available_gb": 800,
                            "percent_used": 60.0
                            }
                        ],
                    "simulated": True
                    }
        except Exception as e:
            logger.error(f"Error getting disk info: {str(e)}")
            raise

    async def get_system_info(self) -> Dict[str, Any]:
        """
        Get comprehensive system information about the current node.

        Returns:
            Dictionary with system information
        """
        try:
            # Get CPU, memory, and disk information
            cpu_info = await self.get_cpu_info()
            memory_info = await self.get_memory_info()
            disk_info = await self.get_disk_info()

            # Get additional system information
            node_name = platform.node()
            system = platform.system()
            release = platform.release()
            version = platform.version()

            return {
                    "node_name": node_name,
                    "system": system,
                    "release": release,
                    "version": version,
                    "cpu": cpu_info,
                    "memory": memory_info,
                    "disk": disk_info
                    }
        except Exception as e:
            logger.error(f"Error getting system info: {str(e)}")
            raise
