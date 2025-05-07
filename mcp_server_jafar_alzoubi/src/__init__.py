# __init__.py

from .server import app  # Importing the app instance from server
from .mcp_handlers import *  # Importing all functions or classes from mcp_handlers

# Set __all__ to only expose 'app' when using `from module import *`
__all__ = ['app']
