# MCP - Architecture Deep Dive

### Index :

- [How Model Context Protocol Works](https://www.notion.so/MCP-Architecture-Deep-Dive-1c4f4544c8d48094bf34da1b5bddae7a?pvs=21)
- [Specification](https://www.notion.so/MCP-Architecture-Deep-Dive-1c4f4544c8d48094bf34da1b5bddae7a?pvs=21)
- [**Base Protocol**](https://www.notion.so/MCP-Architecture-Deep-Dive-1c4f4544c8d48094bf34da1b5bddae7a?pvs=21)
- [**Features**](https://www.notion.so/MCP-Architecture-Deep-Dive-1c4f4544c8d48094bf34da1b5bddae7a?pvs=21)
- [Core Architecture](https://www.notion.so/MCP-Architecture-Deep-Dive-1c4f4544c8d48094bf34da1b5bddae7a?pvs=21)
- [**Connection lifecycle**](https://www.notion.so/MCP-Architecture-Deep-Dive-1c4f4544c8d48094bf34da1b5bddae7a?pvs=21)
- [**Error handling**](https://www.notion.so/MCP-Architecture-Deep-Dive-1c4f4544c8d48094bf34da1b5bddae7a?pvs=21)
- [Citation](https://www.notion.so/MCP-Architecture-Deep-Dive-1c4f4544c8d48094bf34da1b5bddae7a?pvs=21)

---

### How Model Context Protocol Works

MCP follows a client-server architecture similar to LSP:

- The *client* is typically an AI application or development environmentFor example, Claude Desktop, Zed, and Cursor.
- The *server* is a program that provides access to data and/or tools

Requests and responses are encoded according to the JSON-RPC 2.0 specification.

Like LSP, MCP has clients and servers negotiate a set of capabilities. 

- When a client connects to a server, it sends an [`initialize`](https://spec.modelcontextprotocol.io/specification/2024-11-05/basic/lifecycle/#initialization) message, with information about what **protocol version it supports.** The server responds in kind.
- From there, the client can ask the server about what features it has. MCP describes three different kinds of features that a server can provide:
    - **Prompts →** Templates that shape how language models respond.
    - **Resources →** Reference materials that ground models in reality
    - **Tools →** Functions that extend what models can do.
- To get a list of available tools on an MCP, the client would send a `tools/list` request to the server:
    
    ```json
    {
      "jsonrpc": "2.0",
      "id": 1,
      "method": "tools/list",
      "params": {}
    }
    ```
    
- the server’s response might look something like :
    
    ```json
    {
      "jsonrpc":"2.0",
      "id": 1,
      "result": {
        "tools": [
          {
              "name": "get_weather",
              "description": "Returns current weather conditions for the specified coordinates.",
              "inputSchema": {
                  "type": "object",
                  "properties": {
                      "latitude": { "type": "number" },
                      "longitude": { "type": "number" }
                  },
                  "required": ["latitude", "longitude"]
              }
          }
        ]
      }
    }
    ```
    
- The client can share this list of tools with the language model in a *system prompt or a user message.*
- When the model responds wanting to invoke the `get_weather` tool, the client asks the user to confirm tool use.
- If the human-in-the-loop says 🆗, the client sends a `tools/call` request:
    
    ```json
    {
      "jsonrpc": "2.0",
      "id": 2,
      "method": "tools/call",
      "params": {
        "name": "get_weather",
        "arguments": {
          "latitude": 45.5155,
          "longitude": -122.6789
        }
      }
    }
    ```
    
- In response, the server sends:
    
    ```json
    {
      "jsonrpc":"2.0",
      "id": 2,
      "content": [
        {
          "type": "text",
          "text": "{\"temperature\": 12, \"conditions\": \"cloudy\", \"humidity\": 85}"
          "annotations": {
            "audience": ["assistant"]
          }
        }
      ]
    }
    ```
    
- The client then passes that result to the AI assistant, the assistant generates a response with this information, and the client passes that along to the user.

### Specification

- MCP provides a standardized way to connect LLMs with the context they need
- This specification defines the authoritative protocol requirements, based on the TypeScript schema in [schema.ts](https://github.com/modelcontextprotocol/specification/blob/main/schema/2025-03-26/schema.ts).
- The protocol uses [JSON-RPC](https://www.jsonrpc.org/) 2.0 messages to establish communication between:
    - **Hosts**: LLM applications that initiate connections
    - **Clients**: Connectors within the host application
    - **Servers**: Services that provide context and capabilities

### **Base Protocol**

- [J](https://www.jsonrpc.org/)[SON-RPC](https://youtu.be/FmeyLUKHI4Q) message format
- [Stateful](https://www.redhat.com/en/topics/cloud-native-apps/stateful-vs-stateless#:~:text=Stateful%20applications%20and%20processes%20maintain,conversation%20with%20the%20same%20person) connections
- Server and client capability negotiation

### **Features**

Server features to client → 

- **Resources**: Context and data, for the user or the AI model to use
- **Prompts**: Templated messages and workflows for users
- **Tools**: Functions for the AI model to execute

Client features to server ->

- **Sampling**: Server-initiated agentic behaviors and recursive LLM interactions

## Core Architecture

Key classes include:

- **`Protocol`**
- **`Client`**
- **`Server`**

### Protocol Layer

- Handles message framing, request/response linking, and high-level communication patterns.
    
    ```tsx
    class Protocol<Request, Notification, Result> {
        // Handle incoming requests
        setRequestHandler<T>(schema: T, handler: (request: T, extra: RequestHandlerExtra) => Promise<Result>): void
    
        // Handle incoming notifications
        setNotificationHandler<T>(schema: T, handler: (notification: T) => Promise<void>): void
    
        // Send requests and await responses
        request<T>(request: Request, schema: T, options?: RequestOptions): Promise<T>
    
        // Send one-way notifications
        notification(notification: Notification): Promise<void>
    }
    ```
    

### **Transport layer**

- Handles the actual communication between clients and servers.
- MCP supports multiple transport mechanisms:
    1. **Stdio transport**
        - Uses standard input/output for communication
        - Ideal for local processes
    2. **HTTP with SSE transport**
        - Uses Server-Sent Events for server-to-client messages
        - HTTP POST for client-to-server messages
- **Message types**
    - MCP has these main types of messages:
        1. **Requests** expect a response from the other side:
            
            ```tsx
            interface Request {
              method: string;
              params?: { ... };
            }
            ```
            
        2. **Results** are successful responses to requests:
            
            ```tsx
            interface Result {
              [key: string]: unknown;
            }
            ```
            
        3. **Errors** indicate that a request failed:
            
            ```tsx
            interface Error {
              code: number;
              message: string;
              data?: unknown;
            }
            ```
            
        4. **Notifications** are one-way messages that don’t expect a response:
            
            ```tsx
            interface Notification {
              method: string;
              params?: { ... };
            }
            ```
            

## **Connection lifecycle**

### **1. Initialization**

![image.png](./assets/image%203.png)

1. Client sends **`initialize`** request with protocol version and capabilities ([example](https://www.notion.so/MCP-Architecture-Deep-Dive-1c4f4544c8d48094bf34da1b5bddae7a?pvs=21))
2. Server responds with its protocol version and capabilities ([example](https://www.notion.so/MCP-Architecture-Deep-Dive-1c4f4544c8d48094bf34da1b5bddae7a?pvs=21))
3. Client sends **`initialized`** notification as acknowledgment
4. Normal message exchange begins

### **2. Message exchange**

After initialization, the following patterns are supported:

- **Request-Response**: Client or server sends requests, the other responds
- **Notifications**: Either party sends one-way messages

### **3. Termination**

Either party can terminate the connection:

- Clean shutdown via **`close()`**
- Transport disconnection
- Error conditions

## **Error handling**

MCP defines these standard error codes:

```tsx
enum ErrorCode {
  // Standard JSON-RPC error codes
  ParseError = -32700,
  InvalidRequest = -32600,
  MethodNotFound = -32601,
  InvalidParams = -32602,
  InternalError = -32603
}
```

- Errors are propagated through:
    - Error responses to requests
    - Error events on transports
    - Protocol-level error handlers

## Citation

https://spec.modelcontextprotocol.io/specification/2025-03-26/

https://youtu.be/FmeyLUKHI4Q

https://www.redhat.com/en/topics/cloud-native-apps/stateful-vs-stateless#:~:text=Stateful%20applications%20and%20processes%20maintain,conversation%20with%20the%20same%20person

https://nshipster.com/model-context-protocol/

https://spec.modelcontextprotocol.io/specification/2024-11-05/basic/lifecycle/#initialization

https://modelcontextprotocol.io/docs/concepts/architecture#transport-layer