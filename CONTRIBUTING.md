# Contributing to IoWarp MCPs

Thank you for your interest in contributing to IoWarp MCPs! This guide will help you get started with development, testing, and submitting contributions.

## Table of Contents

- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Running Tests](#running-tests)
- [Code Quality Standards](#code-quality-standards)
- [Submitting Pull Requests](#submitting-pull-requests)
- [Adding a New MCP Server](#adding-a-new-mcp-server)
- [Issue Reporting](#issue-reporting)
- [Community & Support](#community--support)

## Development Setup

### Prerequisites

- **Python 3.10+** (required)
- **[UV package manager](https://docs.astral.sh/uv/)** (recommended for dependency management)
- **Git** for version control

### Clone and Setup

```bash
# Clone the repository
git clone https://github.com/iowarp/iowarp-mcps.git
cd iowarp-mcps

# Install all dependencies (development mode)
uv sync --all-extras --dev
```

### For a Specific MCP Server

```bash
# Navigate to the server directory
cd iowarp_mcp_servers/hdf5

# Install dependencies
uv sync --all-extras --dev
```

## Project Structure

IoWarp MCPs uses a **monorepo architecture** with a unified launcher:

```
iowarp-mcps/
├── src/iowarp_mcps/           # Unified launcher CLI
├── iowarp_mcp_servers/         # 15 independent MCP servers
│   ├── hdf5/                  # Each server has:
│   │   ├── src/               # - Source code
│   │   ├── tests/             # - Test suite
│   │   ├── pyproject.toml     # - Dependencies & entry points
│   │   └── README.md          # - Documentation
│   └── ...
├── .github/workflows/          # CI/CD automation
└── pyproject.toml             # Root configuration
```

**Key Principles:**
- Each MCP server is **independently developed and tested**
- Servers are **launched through a single unified command**: `iowarp-mcps <server-name>`
- **Dependency isolation** via individual `pyproject.toml` files
- **Auto-discovery** pattern for new servers

## Running Tests

### Test a Single Server

```bash
cd iowarp_mcp_servers/hdf5

# Run all tests
uv run pytest -v

# Run specific test file
uv run pytest tests/test_server.py -v

# Run specific test
uv run pytest tests/test_server.py::test_function_name -v

# Run with coverage
uv run pytest --cov=src/ --cov-report=html --cov-report=term
```

### Test All Servers

```bash
# From root directory
for server in iowarp_mcp_servers/*/; do
    echo "Testing $server"
    cd "$server" && uv run pytest -v && cd - || exit 1
done
```

## Code Quality Standards

We enforce strict code quality standards through automated CI checks. **All checks must pass** before merging.

### Ruff (Linting + Formatting)

```bash
cd iowarp_mcp_servers/hdf5

# Check linting
uv run ruff check .

# Auto-fix linting issues
uv run ruff check --fix .

# Check formatting
uv run ruff format . --check

# Auto-format code
uv run ruff format .
```

### MyPy (Type Checking)

```bash
cd iowarp_mcp_servers/hdf5

# Run type checking
uv run mypy src/ --ignore-missing-imports
```

### pip-audit (Security)

```bash
cd iowarp_mcp_servers/hdf5

# Scan for vulnerabilities
uv run pip-audit
```

### Run All Quality Checks (Mimic CI)

```bash
cd iowarp_mcp_servers/hdf5

uv run ruff check .
uv run ruff format . --check
uv run mypy src/ --ignore-missing-imports
uv run pytest -v --cov=src/
uv run pip-audit
```

## Submitting Pull Requests

### Before Submitting

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Ensure all tests pass**:
   ```bash
   cd iowarp_mcp_servers/your-server
   uv run pytest -v
   ```

3. **Run quality checks**:
   ```bash
   uv run ruff check .
   uv run ruff format .
   uv run mypy src/
   ```

4. **Update documentation** if needed (README.md, docstrings)

### PR Guidelines

- **Target branch**: `main` (for releases)
- **Clear description**: Explain what changes you made and why
- **Reference issues**: Link related issues (e.g., "Fixes #123")
- **Small, focused changes**: One feature/fix per PR
- **Tests required**: Add tests for new features
- **Documentation**: Update READMEs and docstrings

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All tests pass locally
- [ ] Added tests for new features
- [ ] Updated documentation

## Checklist
- [ ] Code follows project style (Ruff)
- [ ] Type hints added (MyPy compliant)
- [ ] No security vulnerabilities (pip-audit)
- [ ] Documentation updated
```

## Adding a New MCP Server

Follow these steps to add a new MCP server to the monorepo:

### 1. Create Directory Structure

```bash
# Use kebab-case for directory name
mkdir -p iowarp_mcp_servers/my-server/src/my_server_mcp
mkdir -p iowarp_mcp_servers/my-server/tests
```

### 2. Create `pyproject.toml`

```toml
[project]
name = "my-server-mcp"
version = "1.0.0"
description = "Your server description"
readme = "README.md"
requires-python = ">=3.10"
license = "MIT"
authors = [
    {name = "IoWarp Team - Gnosis Research Center", email = "grc@illinoistech.edu"}
]

dependencies = [
    "fastmcp>=0.2.0",
    # Add your dependencies
]

[project.scripts]
my-server-mcp = "my_server_mcp.server:main"

[dependency-groups]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
    "pip-audit>=2.0.0"
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### 3. Implement Server (`src/my_server_mcp/server.py`)

```python
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool(description="What this tool does")
def my_tool(param1: str, param2: int) -> str:
    """Detailed docstring"""
    return f"Result: {param1} {param2}"

async def main():
    """Entry point for the server"""
    await mcp.run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### 4. Create Tests (`tests/test_server.py`)

```python
import pytest
from my_server_mcp.server import mcp

def test_my_tool():
    result = my_tool("test", 42)
    assert "test" in result
    assert "42" in result
```

### 5. Create README.md

Use the standard template from existing servers (see `iowarp_mcp_servers/hdf5/README.md` as reference).

### 6. Test Your Server

```bash
cd iowarp_mcp_servers/my-server
uv sync --all-extras --dev
uv run pytest -v
uv run ruff check .
uv run mypy src/
```

### 7. Verify Auto-Discovery

```bash
# From root directory
uvx iowarp-mcps

# Your server should appear in the list
uvx iowarp-mcps my-server
```

## Issue Reporting

### Bug Reports

When reporting bugs, include:

- **Clear title**: Concise description of the issue
- **Steps to reproduce**: Exact commands/code to trigger the bug
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**:
  - Python version (`python --version`)
  - UV version (`uv --version`)
  - OS and version
  - MCP server name and version

### Feature Requests

When requesting features, include:

- **Use case**: Why is this feature needed?
- **Proposed solution**: How should it work?
- **Alternatives considered**: Other approaches you've thought about
- **Additional context**: Any relevant examples or documentation

### Template

```markdown
## Description
Clear description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. ...

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Python version: 3.10.x
- UV version: 0.x.x
- OS: Ubuntu 22.04
- MCP server: hdf5-mcp v2.0.0
```

## Community & Support

### Get Help

- **Zulip Chat**: [IoWarp-mcp Community](https://grc.zulipchat.com/#narrow/channel/518574-iowarp-mcps)
- **GitHub Discussions**: [Ask questions](https://github.com/iowarp/iowarp-mcps/discussions)
- **GitHub Issues**: [Report bugs](https://github.com/iowarp/iowarp-mcps/issues)

### Contributing Guidelines

- **Be respectful**: Follow our code of conduct
- **Be clear**: Provide context and details
- **Be patient**: Maintainers are volunteers
- **Be collaborative**: Help review others' PRs

### Recognition

Contributors are recognized in:
- **GitHub Contributors**: Automatically listed
- **Release Notes**: Mentioned in CHANGELOG
- **Community**: Featured in project discussions

---

## Quick Reference

### Common Commands

```bash
# Setup
uv sync --all-extras --dev

# Test
uv run pytest -v

# Format
uv run ruff format .

# Lint
uv run ruff check --fix .

# Type check
uv run mypy src/

# Security scan
uv run pip-audit

# Run server
uv run <server-name>-mcp
```

### Branch Strategy

- **main**: Stable releases (target for PRs)
- **dev**: Development integration
- **feature/***: Feature branches

### Code Style

- **Formatting**: Ruff (automatic)
- **Imports**: Sorted by Ruff
- **Line length**: 100 characters (Ruff default)
- **Type hints**: Required for all public functions
- **Docstrings**: Required for all public functions

---

**Thank you for contributing to IoWarp MCPs!**

Your contributions help advance AI integration in scientific computing. 

For more information, visit:
- **Website**: [https://iowarp.github.io/iowarp-mcps/](https://iowarp.github.io/iowarp-mcps/)
- **Repository**: [https://github.com/iowarp/iowarp-mcps](https://github.com/iowarp/iowarp-mcps)
- **Gnosis Research Center**: [https://grc.iit.edu/](https://grc.iit.edu/)
