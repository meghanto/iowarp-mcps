# test_capabilities file
import pytest
from src.capabilities.pandas_handler import PandasHandler



@pytest.mark.asyncio
async def test_pandas_handler_filter_data():
    """Test Pandas handler filter_data operation."""
    handler = PandasHandler()
    result = await handler.filter_data({
        "file_path": "test.csv", 
        "column": "value", 
        "operator": ">", 
        "value": 50
    })
    
    assert "file_path" in result
    assert "filter_condition" in result
    assert "filtered_data" in result
    assert isinstance(result["filtered_data"], list)
    assert "row_count" in result
    assert result["row_count"] == len(result["filtered_data"])

