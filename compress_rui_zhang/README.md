Author: Rui Zhang A20304066

The MCP capabilities I have implemented are HDF5 and Compression Library.

The environment can be set up by using the following commands:
uv run server.py(Go to src directory first)
uv venv

How to run MCP server:
1 Place the project under e disk.
2 Start a command prompt like Anaconda Prompt.
3 Go to directory e:\compress_rui_zhang\src.
4 Enter "fastapi dev server.py" to start the server.

How to run the tests:
1 Start another command prompt.(Don't close the command prompt that is just started or stop the server)
2 Go to directory e:\compress_rui_zhang\tests.
3 Enter "pytest".

Assumption:  
1 The tests will pass only if you place the project under e disk. Otherwise, you need to modify the corresponding in the test code.
2 I assume that you test this project under Window environment.

Note: 
1 If you want to send the json request manually, use the following commands(You need to keep the server running to do this test):
curl -X POST  -H "Content-Type: application/json" -d "{\"jsonrpc\": \"2.0\", \"method\":\"HDF5\",\"params\": [\"e:\\mcpassign\\src\",\".py\"],\"Id\": 2}" http://127.0.0.1:8000/mcp/callTool
curl -X POST  -H "Content-Type: application/json" -d "{\"jsonrpc\": \"2.0\", \"method\":\"compress\",\"params\": [\"demo.txt\",\"cdemo.gz\"],\"Id\": 2}" http://127.0.0.1:8000/mcp/callTool
Just replace the "{...}" after -d with the json data you want to send.(You need a \ before every " or \) Only in this way can you see the json result returned from the server.
2 You will see the compressed file in the corresponding directory(mentioned in the test code) or the directory specified by you.
3 "demo1.txt" and "demo.txt" are files for compression.