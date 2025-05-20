## Explanation of `server.py`

The `server.py` script is a Python-based server implementation designed to handle file system operations securely. It uses the `FastMCP` library to create tools for reading, writing, and searching files while ensuring strict security measures. Below is an in-depth breakdown of the code, its functions, and how they work.

---

### **1. Initialization**

```python
from mcp.server.fastmcp import FastMCP
from pathlib import Path
import os
import base64
from typing import List

mcp = FastMCP(name="FileSystem")
ALLOWED_DIRS = [Path.cwd()]
```

- **FastMCP Initialization**: The script initializes an MCP (Modular Command Processor) server named `FileSystem`. This acts as the backbone for defining tools (`read_file`, `write_file`, and `search_file`) that interact with the file system.
- **Allowed Directories**: The `ALLOWED_DIRS` list restricts file operations to the current working directory (`Path.cwd()`) for security purposes. Any operation outside this directory is disallowed.

---

### **2. Helper Functions**

#### **a. `normalize_path(file_path: str) ->  Path`**

```python
def normalize_path(file_path: str) ->  Path:
    expanded = Path(os.path.expanduser(file_path))
    resolved = expanded.resolve(strict=False)
    for i in range(1, len(resolved.parts) + 1):
        partial = Path(*resolved.parts[:i])
        if partial.is_symlink():
            real_partial = partial.resolve(strict=True)
            if not is_path_allowed(real_partial):
                raise PermissionError(f"Symlink target restricted: {real_partial}")
    return resolved
```

- **Purpose**: This function normalizes and resolves a given file path while performing security checks.
- **Steps**:
    - Expands user home directories (e.g., `~` to `/home/user`).
    - Resolves symlinks (`strict=False` allows non-existent paths).
    - Validates each component of the path recursively to ensure no symlink points outside allowed directories.
- **Security**: Raises a `PermissionError` if a symlink points to a restricted location.


#### **b. `is_path_allowed(resolved_path: Path) ->  bool`**

```python
def is_path_allowed(resolved_path: Path) ->  bool:
    return any(resolved_path.is_relative_to(allowed_dir) for allowed_dir in ALLOWED_DIRS)
```

- **Purpose**: Checks if a resolved path is within the allowed directories.
- **Logic**: Uses the `is_relative_to` method to verify if the path belongs to any directory in `ALLOWED_DIRS`.


#### **c. `validate_file_operation(path: Path) ->  None`**

```python
def validate_file_operation(path: Path) ->  None:
    parent = path.parent.resolve()
    if not parent.exists():
        raise FileNotFoundError(f"Parent directory does not exist: {parent}")
    if not is_path_allowed(parent):
        raise PermissionError(f"Parent directory not allowed: {parent}")
```

- **Purpose**: Ensures that file operations are performed only in valid directories.
- **Checks**:
    - Verifies that the parent directory of the target path exists.
    - Ensures the parent directory is within allowed paths.

---

### **3. Tools**

#### **a. `read_file(file_path: str)`**

```python
@mcp.tool(name="read_file", description="Reads the content of a file")
async def read_file(file_path: str) ->  list:
    try:
        normalized = normalize_path(file_path)
        if not is_path_allowed(normalized):
            raise PermissionError("Access denied")
        with open(normalized, "rb") as f:
            content = f.read()
        try:
            text_content = content.decode('utf-8')
            return [{"type": "text", "text": text_content}]
        except UnicodeDecodeError:
            return [{"type": "text", "text": base64.b64encode(content).decode('ascii')}]
    except Exception as e:
        return [{"type": "text", "text": f"Error: {str(e)}"}]
```

- **Purpose**: Reads the content of a file securely.
- **Process**:

1. Normalizes and validates the file path.
2. Opens the file in binary mode (`rb`) and reads its content.
3. Tries to decode the content as UTF-8 for text files.
4. If decoding fails, encodes the binary content in Base64 (useful for non-text files).
- **Output**: Returns a list containing a dictionary with either text or Base64-encoded data.


#### **b. `write_file(file_path: str, content: str)`**

```python
@mcp.tool(name="write_file", description="Writes content to a file")
async def write_file(file_path: str, content: str) ->  list:
    try:
        normalized = normalize_path(file_path)
        validate_file_operation(normalized)
        if not is_path_allowed(normalized.parent):
            raise PermissionError("Parent directory not whitelisted")
        with open(normalized, "a") as f:
            f.write(content)
        return [{"type": "text", "text": "Updated file content successfully"}]
    except Exception as e:
        return [{"type": "text", "text": f"Error: {str(e)}"}]
```

- **Purpose**: Appends content to a file after validation.
- **Process**:

1. Normalizes and validates the file path.
2. Ensures that the parent directory exists and is allowed.
3. Opens the file in append mode (`a`) and writes the provided content.
- **Output**: Returns success or error messages.


#### **c. `search_file(file_extension: str, search_dir: str)`**

```python
@mcp.tool(name="search_file", description="Search for files with a specific extension")
async def search_file(file_extension: str, search_dir: str = str(Path.cwd())) ->   list:
    try:
        resolved_search_dir = normalize_path(search_dir).resolve(strict=True)
        if not is_path_allowed(resolved_search_dir):
            return [{"type": "text", "text": "Error: Search directory not in allowed paths"}]
        results = [
            str(resolved)
            for resolved in resolved_search_dir.rglob(f"*{file_extension}")
            if is_path_allowed(resolved)
        ]
        if not results:
            return [{"type": "text", "text": f"No files found with {file_extension}"}]
        return [{"type": "text", "text": "\n".join(results)}]
    except Exception as e:
        return [{"type": "text", "text": f"Error: {str(e)}"}]
```

- **Purpose**: Searches for files with a specific extension within allowed directories.
- **Process**:

1. Resolves and validates the search directory.
2. Uses recursive globbing (`rglob`) to find matching files while ensuring they are within allowed paths.
- **Output**: Returns a list of matching file paths or an error message.

---

### **4. Entry Point**

```python
if __name__ == "__main__":
    mcp.run(transport='stdio')
```

- The script runs the MCP server using standard I/O (`stdio`) transport when executed directly.

---

### Summary of Features

| Tool Name | Description | Key Features |
| :-- | :-- | :-- |
| read_file | Reads file content securely | Handles both text (UTF-8) and binary (Base64) files |
| write_file | Writes/appends content to a file | Validates paths and ensures safe write operations |
| search_file | Searches for files by extension | Recursively searches within allowed directories |

Operations are restricted to pre-defined safe areas (`ALLOWED_DIRS`).

