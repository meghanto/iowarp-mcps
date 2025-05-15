from flask import Flask, jsonify, request
from src.mcp_handlers import json_validate, list_resources, call_tool, jsonrpc_error

app = Flask(__name__)

# server endpoint for handling MCP commands
@app.route('/mcp/listResources', methods=['POST'])
def handle_list_resources():
  data = request.get_json()

  # json validation check
  invalid_JSON = json_validate(data)
  if invalid_JSON: 
    return invalid_JSON
  
  # parse the fields from the
  request_id = data.get("id")
  method = data["method"]

  # handles listResources method
  if method == "listResources":
    return list_resources(request_id)

  else: # if the method isn't found, return an -32601 non-existent method error message
    return jsonify(jsonrpc_error(request_id, -32601, "Method not found"))
  
# server endpoint for handling MCP commands
@app.route('/mcp/callTool', methods=['POST'])
def handle_call_tool():
  data = request.get_json()

  # json validation check
  invalid_JSON = json_validate(data)
  if invalid_JSON: 
    return invalid_JSON
  
  # parse the fields from the
  request_id = data.get("id")
  method = data["method"]
  params = data.get("params", {})

  # handles callTool method
  if method == "callTool":
    return call_tool(request_id, params)

  else: # if the method isn't found, return an -32601 non-existent method error message
    return jsonify(jsonrpc_error(request_id, -32601, "Method not found"))
  


if __name__ == '__main__':
  app.run(debug=True, port=3000)