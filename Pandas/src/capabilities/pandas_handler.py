# pandas_handler file 
import logging
from typing import Dict, Any, List
import pandas as pd
import os 

logger = logging.getLogger(__name__)

class PandasHandler:
    """Handler for Pandas operations."""
    
    async def get_details(self) -> Dict[str, Any]:
        """Get details about the Pandas handler."""
        return {
            "supported_operations": ["load_csv", "filter_data", "aggregate_data"],
            "file_extensions": [".csv", ".xlsx", ".json"]
        }
    
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Pandas operations."""
        operation = params.get("operation")
        
        if operation == "load_csv":
            return await self.load_csv(params)
        elif operation == "filter_data":
            return await self.filter_data(params)
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
    async def load_csv(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Load a CSV file."""
        file_path = params.get("file_path", "data.csv")
        print(f"Loading CSV file: {file_path}")
        # Mock response - in a real implementation, use pandas
        try:
            # Get the directory of the current script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Create absolute path to the CSV file
            absolute_file_path = os.path.join(current_dir, file_path)
            df = pd.read_csv(absolute_file_path)
        except FileNotFoundError:
            print(f"File {file_path} not found. Using mock data.\n\n\n\n\n")
            # If the file doesn't exist, use the mock data
            df = pd.DataFrame([
                {"id": 1, "value": 45, "category": "A"},
                {"id": 2, "value": 62, "category": "B"},
                {"id": 3, "value": 38, "category": "A"},
                {"id": 4, "value": 71, "category": "C"},
                {"id": 5, "value": 55, "category": "B"}
            ])
        mock_data = df.to_dict(orient='records')
        
        
        return {
            "file_path": file_path,
            "data": mock_data,
            "row_count": len(mock_data),
            "columns": ["id", "value", "category"]
        }
    
    async def filter_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Filter data based on conditions."""
        file_path = params.get("file_path", "data.csv")
        column = params.get("column", "value")
        operator = params.get("operator", ">")
        value = int(params.get("value", 50))
        
        # Mock response - in a real implementation, use pandas
        try:
            # Get the directory of the current script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Create absolute path to the CSV file
            absolute_file_path = os.path.join(current_dir, file_path)
            df = pd.read_csv(absolute_file_path)
        except FileNotFoundError:
            print(f"File {file_path} not found. Using mock data.\n")
            # If the file doesn't exist, use the mock data
            df = pd.DataFrame([
                {"id": 1, "value": 45, "category": "A"},
                {"id": 2, "value": 62, "category": "B"},
                {"id": 3, "value": 38, "category": "A"},
                {"id": 4, "value": 71, "category": "C"},
                {"id": 5, "value": 55, "category": "B"}
            ])
        
        # Apply the filter
        if operator == ">":
            filtered_df = df[df[column] > value]
        elif operator == "<":
            filtered_df = df[df[column] < value]
        elif operator == "==":
            filtered_df = df[df[column] == value]
        elif operator == ">=":
            filtered_df = df[df[column] >= value]
        elif operator == "<=":
            filtered_df = df[df[column] <= value]
        else:
            raise ValueError(f"Unsupported operator: {operator}")
        
        # Convert the filtered DataFrame to a list of dictionaries
        mock_data = filtered_df.to_dict(orient='records')

        print(f"\n\nFiltered data: {mock_data}")
        
        return {
            "file_path": file_path,
            "filter_condition": f"{column} {operator} {value}",
            "filtered_data": mock_data,
            "row_count": len(mock_data)
        }

