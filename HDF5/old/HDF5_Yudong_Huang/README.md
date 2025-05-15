# CS550MCP
Project assignment for CS550, 2025

Author: Yudong Huang. ID:A20581530


Execution Instructions：

1.Extract the downloaded archive. You will see the following directory structure:

CS550MCP/

├── pyproject.toml

├── src/

│   └── ...

└── tests/

└── ...

2.Next, make sure your Python version is ≥ 3.10. Then, install uv using the following command:

pip install uv

3.In the directory containing pyproject.toml, run:

uv venv

uv sync

This will install the required packages: fastapi, uvicorn, and pytest.

4.Activate the uv virtual environment and start the FastAPI server with the following command:

uvicorn src.server:app --reload

By default, the server listens on: http://127.0.0.1:8000/mcp

If the server runs successfully, you should see output similar to the figure shown below.

For more detailed test record and code description, please refer to the pdf file in the project.
