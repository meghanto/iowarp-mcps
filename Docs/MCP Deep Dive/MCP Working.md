# MCP Working

### Index :

- [Features](https://www.notion.so/MCP-Working-1c5f4544c8d480df8c3df6c7defd2166?pvs=21)
- [Architecture](https://www.notion.so/MCP-Working-1c5f4544c8d480df8c3df6c7defd2166?pvs=21)
- [Citation](https://www.notion.so/MCP-Working-1c5f4544c8d480df8c3df6c7defd2166?pvs=21)

---

## Features

- MCP Client and MCP Server implementations supporting:
    - Protocol [**version compatibility negotiation**](https://spec.modelcontextprotocol.io/specification/2024-11-05/basic/lifecycle/#initialization)
    - [**Tool**](https://spec.modelcontextprotocol.io/specification/2024-11-05/server/tools/) discovery, execution, list change notifications
    - [**Resource**](https://spec.modelcontextprotocol.io/specification/2024-11-05/server/resources/) management with URI templates
    - [**Roots**](https://spec.modelcontextprotocol.io/specification/2024-11-05/client/roots/) list management and notifications
    - [**Prompt**](https://spec.modelcontextprotocol.io/specification/2024-11-05/server/prompts/) handling and management
    - [**Sampling**](https://spec.modelcontextprotocol.io/specification/2024-11-05/client/sampling/) support for AI model interactions
- Multiple transport implementations:
    - Default transports:
        - **Stdio**-based transport for process-based communication
        - **Java HttpClient**-based SSE client transport for HTTP SSE Client-side streaming
        - **Servlet**-based SSE server transport for HTTP SSE Server streaming
    - Spring-based transports:
        - WebFlux SSE client and server transports for reactive HTTP streaming
        - WebMVC SSE transport for servlet-based HTTP streaming
- Supports Synchronous and Asynchronous programming paradigms

## **Architecture**

The SDK follows a layered architecture with clear separation of concerns:

![image.png](./assets/image%204.png)

- **Client/Server Layer (McpClient/McpServer)**:
    - Both use **McpSession for sync/async operations.**
    - McpClient handling client-side protocol operations.
    - McpServer managing server-side protocol operations.
- **Session Layer (McpSession)**:
    - Manages communication patterns and state using **DefaultMcpSession implementation.**
- **Transport Layer (McpTransport)**:
    - Handles JSON-RPC message serialization/deserialization via:
        - StdioTransport (stdin/stdout) in the core module
        - HTTP SSE transports in dedicated transport modules (Java HttpClient, Spring WebFlux, Spring WebMVC)

The MCP Client is a key component in the Model Context Protocol (MCP) architecture, responsible for establishing and managing connections with MCP servers. It implements the client-side of the protocol.

![image.png](./assets/image%205.png)

The MCP Server is a foundational component in the Model Context Protocol (MCP) architecture that provides tools, resources, and capabilities to clients. It implements the server-side of the protocol.

![image.png](./assets/image%206.png)

Key Interactions:

- **Client/Server Initialization**:
    - Transport setup,
    - protocol compatibility check,
    - capability negotiation,
    - and implementation details exchange.
- **Message Flow**:
    - JSON-RPC message handling with validation,
    - type-safe response processing,
    - and error handling.
- **Resource Management**:
    - Resource discovery,
    - URI template-based access,
    - subscription system,
    - and content retrieval.

## Citation

https://spec.modelcontextprotocol.io/specification/2024-11-05/basic/lifecycle/#initialization

https://spec.modelcontextprotocol.io/specification/2024-11-05/server/tools/

https://spec.modelcontextprotocol.io/specification/2024-11-05/server/resources/

https://spec.modelcontextprotocol.io/specification/2024-11-05/client/roots/

https://spec.modelcontextprotocol.io/specification/2024-11-05/server/prompts/

https://spec.modelcontextprotocol.io/specification/2024-11-05/client/sampling/