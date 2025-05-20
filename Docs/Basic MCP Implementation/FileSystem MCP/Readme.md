
# FileSystem MCP Integration Guide

## Project Navigation &amp; Setup

This project enables secure file system operations through an MCP (Modular Command Processor) server/client architecture. Follow this sequential guide for proper setup:


! IMPORTANT: Complete server setup before client configuration !



---
## Table of Contents
1. [Prerequisites](#-prerequisites)
2. [Server Setup](#%EF%B8%8F-server-setup)
3. [Client Setup](#-client-setup)
4. [System Verification](#-system-verification)
5. [Usage Examples](#-usage-examples)

---

## 📋 Prerequisites
- Python 3.9+
- UV package manager (`uv install`)
- [Gemini API Key](https://ai.google.dev/)
- Claude Desktop App (Optional for GUI)

---

## 🖥️ Server Setup

### 1. Initialize Project
```
uv init filesystem-mcp
cd filesystem-mcp
```

### 2. Install Dependencies
```

uv add "mcp[cli]"
```

### 3. Create Server File
Create `server.py` with [this code](./Server/server.py) containing:
- Path normalization logic
- Security constraints (`ALLOWED_DIRS`)
- Three core tools:
  - `read_file` (Text/Base64 support)
  - `write_file` (Append mode only)
  - `search_file` (Recursive glob)

### 4. Security Configuration
```
# Restrict operations to current directory by default

ALLOWED_DIRS = [Path.cwd()]
```

### 5. Run Server
```

uv run mcp dev server.py
```
- Access MCP Inspector at `http://localhost:8000` to test tools

---

## 📱 Client Setup

### 1. Environment Configuration
Create `.env` file:
```
GEMINI_API_KEY="your_actual_key_here"
```

### 2. Create Client File
Save as `client.py` with [provided code](./Client/client.py) featuring:
- Gemini 2.0 Flash integration
- Tool schema autodetection
- Interactive chat interface

### 3. Runtime Execution
```
uv run client.py server.py
```

---

## ✔️ System Verification

### Expected Successful Output
```

Connected to server with tools: ['read_file', 'write_file', 'search_file']
MCP Client Started!
Type your queries or 'quit' to exit.

Query: [Your input here]

```

### Test Queries
```

1. "Find all .txt files in current directory"
2. "Read contents of test_file.txt"
3. "Add 'Hello World' to output.log"
```

---

## 🚀 Usage Examples

### Basic File Search
```

Query: "List PDFs in documents folder"
-> Calls search_file("*.pdf", "documents")
-> Returns: "/documents/report.pdf\n/documents/guide.pdf"

```

### File Content Handling
```

Query: "Show me server.py contents"
-> Calls read_file("server.py")
-> Returns UTF-8 decoded text or Base64 for binaries

```

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Permission Errors | Verify `ALLOWED_DIRS` in server.py |
| Missing Tools | Ensure server.py contains all three @mcp.tool decorators |
| API Key Failures | Confirm .env file matches Gemini console credentials |
| Symlink Issues | Server blocks symlinks pointing outside allowed directories |

---

## Security Notes
- All file operations are contained within `ALLOWED_DIRS`
- Client-server communication uses stdio transport isolation
- Binary files are Base64-encoded to prevent data corruption

