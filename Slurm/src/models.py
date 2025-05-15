from typing import Optional, Dict, Any, Union
from pydantic import BaseModel, Field

# JSON-RPC 2.0 compliant response object
class JSONRPCResponse(BaseModel):
    jsonrpc: str = "2.0"
    result: Optional[Any] = None
    error: Optional[Dict[str, Union[int, str]]] = None
    id: Optional[Union[int, str, None]] = None

    class Config:
        # This will ensure that the class is serialized to JSON correctly
        orm_mode = True

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        base = super().dict(*args, **kwargs)
        # Remove keys with None values to keep the response clean
        return {k: v for k, v in base.items() if v is not None}


# Describes an available data resource (like a dataset)
class MCPResource(BaseModel):
    id: str
    name: str
    type: str  # e.g., 'dataset', 'image', etc.
    description: str
    accessProtocol: str  # e.g., 'hdf5', 'http', 's3'
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


# Describes an executable tool (like a processor)
class MCPTool(BaseModel):
    id: str
    name: str
    description: str
    parameters: Dict[str, Dict[str, Any]]  # Parameter schema
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
