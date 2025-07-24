#!/usr/bin/env python3
"""
Script to automatically generate Docusaurus markdown files for MCP documentation website.
Reads from pyproject.toml, README.md, and server.py files to extract metadata and capabilities.
"""

import os
import sys
import ast
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

try:
    import tomllib  # Python 3.11+
except ImportError:
    try:
        import tomli as tomllib  # Fallback for older Python
    except ImportError:
        print("Error: tomllib/tomli not available. Please install tomli: pip install tomli")
        sys.exit(1)


class MCPDataExtractor:
    """Extract MCP data from project files."""
    
    def __init__(self):
        self.category_mapping = {
            "data": "Data Processing",
            "analysis": "Analysis & Visualization", 
            "visualization": "Analysis & Visualization",
            "plot": "Analysis & Visualization",
            "system": "System Management",
            "slurm": "System Management",
            "hpc": "System Management",
            "hardware": "System Management",
            "management": "System Management",
            "utility": "Utilities",
            "utilities": "Utilities"
        }
        
        self.icon_mapping = {
            "adios": "📊",
            "arxiv": "📄", 
            "hdf5": "🗂️",
            "pandas": "🐼",
            "parquet": "📋",
            "plot": "📈",
            "darshan": "⚡",
            "slurm": "🖥️",
            "lmod": "📦",
            "node_hardware": "💻",
            "compression": "🗜️",
            "parallel_sort": "🔄",
            "jarvis": "🤖",
            "chronolog": "⏰"
        }

    def extract_mcp_data(self, mcps_dir: Path) -> Dict:
        """Extract data for all MCPs in the directory."""
        mcps_data = {}
        
        for mcp_dir in mcps_dir.iterdir():
            if mcp_dir.is_dir() and not mcp_dir.name.startswith('.'):
                print(f"Processing MCP: {mcp_dir.name}")
                try:
                    mcp_data = self._extract_single_mcp_data(mcp_dir)
                    if mcp_data:
                        mcps_data[mcp_data['slug']] = mcp_data
                except Exception as e:
                    print(f"Error processing {mcp_dir.name}: {e}")
        
        return mcps_data
    
    def _extract_single_mcp_data(self, mcp_dir: Path) -> Optional[Dict]:
        """Extract data for a single MCP."""
        # Read pyproject.toml
        pyproject_file = mcp_dir / "pyproject.toml"
        if not pyproject_file.exists():
            print(f"Warning: No pyproject.toml found in {mcp_dir.name}")
            return None
        
        try:
            with open(pyproject_file, 'rb') as f:
                pyproject_data = tomllib.load(f)
        except Exception as e:
            print(f"Error reading pyproject.toml in {mcp_dir.name}: {e}")
            return None
        
        # Extract basic info from pyproject.toml
        project_info = pyproject_data.get('project', {})
        name = project_info.get('name', mcp_dir.name).replace('-mcp', '').replace('_', ' ').title()
        description = project_info.get('description', f'{name} MCP server')
        version = project_info.get('version', '1.0.0')
        
        # Determine slug and category
        slug = mcp_dir.name.lower().replace('_', '_').replace('-', '_')
        category = self._determine_category(name, description, mcp_dir.name)
        icon = self.icon_mapping.get(slug, "🔧")
        
        # Read README.md for enhanced description
        readme_file = mcp_dir / "README.md"
        enhanced_description = description
        capabilities = []
        
        if readme_file.exists():
            try:
                with open(readme_file, 'r', encoding='utf-8') as f:
                    readme_content = f.read()
                
                # Extract better description from README
                enhanced_description = self._extract_description_from_readme(readme_content) or description
                
                # Extract capabilities from README
                capabilities = self._extract_capabilities_from_readme(readme_content)
                
            except Exception as e:
                print(f"Error reading README.md in {mcp_dir.name}: {e}")
        
        # Extract tools from server.py
        tools = self._extract_tools_from_server(mcp_dir)
        
        # If no capabilities in README, use tools as actions
        if not capabilities and tools:
            capabilities = [tool['name'] for tool in tools]
        
        return {
            'name': name,
            'slug': slug,
            'category': category,
            'description': enhanced_description,
            'icon': icon,
            'version': version,
            'actions': capabilities,
            'tools': tools,
            'platforms': ["claude", "cursor", "vscode"],
            'updated': datetime.now().strftime("%Y-%m-%d"),
            'path': str(mcp_dir)
        }
    
    def _determine_category(self, name: str, description: str, dir_name: str) -> str:
        """Determine MCP category based on name and description."""
        text = f"{name} {description} {dir_name}".lower()
        
        # Check for specific category keywords
        for keyword, category in self.category_mapping.items():
            if keyword in text:
                return category
        
        # Default category
        return "Utilities"
    
    def _extract_description_from_readme(self, readme_content: str) -> Optional[str]:
        """Extract a better description from README content."""
        lines = readme_content.split('\n')
        
        # Look for description after the title
        in_description = False
        description_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Skip title and badges
            if line.startswith('#') or line.startswith('[!['):
                continue
            
            # Start collecting description after badges/title
            if not in_description and line and not line.startswith('#'):
                in_description = True
            
            if in_description:
                if line.startswith('##') or line.startswith('# '):  # Stop at next section
                    break
                if line:
                    description_lines.append(line)
                elif description_lines:  # Stop at first empty line after content
                    break
        
        if description_lines:
            description = ' '.join(description_lines)
            # Clean up common patterns
            description = re.sub(r'\*\*([^*]+)\*\*', r'\1', description)  # Remove bold
            description = re.sub(r'`([^`]+)`', r'\1', description)  # Remove code quotes
            description = re.sub(r'\s+', ' ', description)  # Normalize whitespace
            return description.strip()
        
        return None
    
    def _extract_capabilities_from_readme(self, readme_content: str) -> List[str]:
        """Extract capabilities/actions from README."""
        capabilities = []
        
        # Look for capabilities section
        in_capabilities = False
        for line in readme_content.split('\n'):
            line = line.strip()
            
            if '## Capabilities' in line or '### Capabilities' in line:
                in_capabilities = True
                continue
            elif in_capabilities and line.startswith('##') and 'Capabilities' not in line:
                break
            
            if in_capabilities:
                # Look for function names in backticks
                func_matches = re.findall(r'`([a-zA-Z_][a-zA-Z0-9_]*)`', line)
                for func in func_matches:
                    if func not in capabilities and not func.startswith('_'):
                        capabilities.append(func)
        
        return capabilities
    
    def _extract_tools_from_server(self, mcp_dir: Path) -> List[Dict]:
        """Extract tool information from server.py files."""
        server_files = list(mcp_dir.glob("src/**/server.py"))
        
        tools = []
        for server_file in server_files:
            try:
                with open(server_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        tool_info = self._extract_tool_from_function(node)
                        if tool_info:
                            tools.append(tool_info)
            
            except Exception as e:
                print(f"Error parsing {server_file}: {e}")
        
        return tools
    
    def _extract_tool_from_function(self, node) -> Optional[Dict]:
        """Extract tool information from a function node."""
        # Check for @mcp.tool decorator
        for decorator in node.decorator_list:
            if self._is_mcp_tool_decorator(decorator):
                name = self._extract_decorator_name(decorator) or node.name
                description = self._extract_decorator_description(decorator)
                
                # Get enhanced description from docstring
                docstring = ast.get_docstring(node)
                if docstring and not description:
                    description = docstring.split('\n')[0].strip()
                
                return {
                    'name': name,
                    'description': description or f"Tool: {name}",
                    'function_name': node.name
                }
        
        return None
    
    def _is_mcp_tool_decorator(self, decorator) -> bool:
        """Check if decorator is @mcp.tool."""
        if isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Attribute):
                return (decorator.func.attr == 'tool' and 
                       isinstance(decorator.func.value, ast.Name) and 
                       decorator.func.value.id == 'mcp')
        elif isinstance(decorator, ast.Attribute):
            return (decorator.attr == 'tool' and 
                   isinstance(decorator.value, ast.Name) and 
                   decorator.value.id == 'mcp')
        return False
    
    def _extract_decorator_name(self, decorator) -> Optional[str]:
        """Extract name from decorator arguments."""
        if isinstance(decorator, ast.Call):
            for keyword in decorator.keywords:
                if keyword.arg == 'name' and isinstance(keyword.value, ast.Constant):
                    return keyword.value.value
        return None
    
    def _extract_decorator_description(self, decorator) -> Optional[str]:
        """Extract description from decorator arguments."""
        if isinstance(decorator, ast.Call):
            for keyword in decorator.keywords:
                if keyword.arg == 'description' and isinstance(keyword.value, ast.Constant):
                    return keyword.value.value
        return None


class DocusaurusGenerator:
    """Generate Docusaurus markdown files from MCP data."""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.mcps_output_dir = output_dir / "docs" / "mcps"
        self.data_output_dir = output_dir / "src" / "data"
    
    def generate_all_docs(self, mcps_data: Dict):
        """Generate all documentation files."""
        # Ensure output directories exist
        self.mcps_output_dir.mkdir(parents=True, exist_ok=True)
        self.data_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate individual MCP markdown files
        for slug, mcp_data in mcps_data.items():
            self._generate_mcp_markdown(mcp_data)
        
        # Generate mcpData.js file
        self._generate_mcp_data_js(mcps_data)
        
        print(f"Generated {len(mcps_data)} MCP documentation files")
    
    def _generate_mcp_markdown(self, mcp_data: Dict):
        """Generate markdown file for a single MCP."""
        # Escape YAML special characters in description
        description = mcp_data['description'].replace('"', '\\"').replace('\n', ' ')
        # Truncate very long descriptions for YAML front matter
        if len(description) > 300:
            description = description[:297] + "..."
        
        # Escape quotes in the full description for JSX
        jsx_description = mcp_data['description'].replace('"', '&quot;').replace('\n', ' ')
        
        # Format actions and platforms as proper JSX arrays  
        actions_jsx = json.dumps(mcp_data['actions'])
        platforms_jsx = json.dumps(mcp_data['platforms'])
        
        content = f"""---
title: {mcp_data['name']} MCP
description: "{description}"
---

import MCPDetail from '@site/src/components/MCPDetail';

<MCPDetail 
  name="{mcp_data['name']}"
  icon="{mcp_data['icon']}"
  category="{mcp_data['category']}"
  description="{jsx_description}"
  version="{mcp_data['version']}"
  actions={{{actions_jsx}}}
  platforms={{{platforms_jsx}}}
>

## Advanced Features

{self._generate_features_section(mcp_data)}

## Available Actions

{self._generate_actions_section(mcp_data)}

## Integration Examples

{self._generate_examples_section(mcp_data)}

</MCPDetail>
"""
        
        output_file = self.mcps_output_dir / f"{mcp_data['slug']}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Generated {output_file}")
    
    def _generate_features_section(self, mcp_data: Dict) -> str:
        """Generate features section based on MCP category."""
        category_features = {
            "Data Processing": """
### High-Performance Data Processing
This MCP provides optimized data processing capabilities:
- **Fast I/O Operations**: Efficient reading and writing of data
- **Format Support**: Multiple data format compatibility
- **Memory Optimization**: Smart memory usage for large datasets

### Integration Ready
- **Pipeline Compatible**: Works seamlessly in data processing pipelines
- **Cross-format**: Convert between different data formats
- **Scalable**: Handles datasets of various sizes
""",
            "Analysis & Visualization": """
### Advanced Analytics
Comprehensive analysis and visualization capabilities:
- **Statistical Analysis**: Built-in statistical functions
- **Visualization**: Create charts, plots, and visual representations
- **Interactive**: Generate interactive visualizations

### Customizable Output
- **Multiple Formats**: Support for various output formats
- **Styling Options**: Customizable appearance and themes
- **Export Ready**: Easy export for reports and presentations
""",
            "System Management": """
### System Monitoring
Comprehensive system management and monitoring:
- **Real-time Monitoring**: Live system status updates
- **Resource Tracking**: CPU, memory, and disk usage monitoring
- **Performance Analytics**: Detailed performance metrics

### Remote Capabilities
- **SSH Support**: Connect to remote systems securely
- **Distributed Monitoring**: Monitor multiple nodes
- **Health Checks**: Automated system health assessments
""",
            "Utilities": """
### Utility Functions
Essential utility functions for scientific computing:
- **Data Transformation**: Convert and process data efficiently
- **Automation**: Automate repetitive tasks
- **Integration**: Easy integration with other tools

### Performance Optimized
- **Fast Processing**: Optimized algorithms for speed
- **Memory Efficient**: Smart memory management
- **Scalable**: Handles large workloads efficiently
"""
        }
        
        return category_features.get(mcp_data['category'], """
### Core Functionality
This MCP provides essential functionality for scientific computing workflows:
- **Reliable**: Tested and validated implementations
- **Documented**: Comprehensive documentation and examples
- **Extensible**: Easy to extend and customize
""")
    
    def _generate_actions_section(self, mcp_data: Dict) -> str:
        """Generate actions section from tools data."""
        if not mcp_data['tools']:
            actions_list = '\n'.join([f"- **`{action}`**: {action.replace('_', ' ').title()} functionality" 
                                    for action in mcp_data['actions']])
            return f"""
The following actions are available:

{actions_list}

Refer to the MCP server documentation for detailed parameter information and usage examples.
"""
        
        actions_content = []
        for tool in mcp_data['tools'][:5]:  # Limit to first 5 tools to avoid MDX parsing issues
            # Truncate very long descriptions
            description = tool['description']
            if len(description) > 200:
                description = description[:197] + "..."
            
            actions_content.append(f"""
#### `{tool['name']}`
{description}

**Usage Example:**
```python
# Use {tool['name']} function
result = {tool['name']}()
print(result)
```
""")
        
        if len(mcp_data['tools']) > 5:
            actions_content.append(f"""
#### Additional Actions
This MCP provides {len(mcp_data['tools']) - 5} additional actions. Refer to the MCP server documentation for complete details.
""")
        
        return '\n'.join(actions_content)
    
    def _generate_examples_section(self, mcp_data: Dict) -> str:
        """Generate integration examples section."""
        examples = {
            "Data Processing": f"""
### Data Processing Workflow
```python
# Load and process data with {mcp_data['name']} MCP
data = load_data("input_file")
processed = process_data(data)

# Integrate with other MCPs
visualization = create_plot(processed, "chart_type")
save_results(processed, "output_file")
```

### Batch Processing
```python
# Process multiple files
files = list_files("data_directory")
for file in files:
    data = load_data(file)
    result = process_data(data)
    save_processed(result, f"processed_{{file}}")
```
""",
            "Analysis & Visualization": f"""
### Data Analysis Pipeline
```python
# Analyze data with {mcp_data['name']} MCP
data = load_csv("experiment_data.csv")
analysis = analyze_data(data)

# Create visualizations
plot = create_visualization(analysis, "plot_type")
save_plot(plot, "analysis_results.png")
```

### Interactive Analysis
```python
# Interactive data exploration
summary = get_data_summary(data)
correlations = calculate_correlations(data)
create_dashboard(summary, correlations)
```
""",
            "System Management": f"""
### System Monitoring
```python
# Monitor system with {mcp_data['name']} MCP
status = get_system_status()
performance = get_performance_metrics()

# Set up alerts
if status.cpu_usage > 80:
    send_alert("High CPU usage detected")

# Resource optimization
optimize_resources(performance)
```

### Remote Management
```python
# Manage remote systems
remote_status = get_remote_status("server1.example.com")
deploy_configuration(remote_status, "config.yaml")
monitor_deployment_status()
```
""",
            "Utilities": f"""
### Utility Operations
```python
# Use {mcp_data['name']} utilities
result = perform_operation("input_data")
optimized = optimize_result(result)

# Chain operations
processed = process_data(input_data)
final_result = finalize_processing(processed)
```

### Automation Workflow
```python
# Automate repetitive tasks
for item in input_list:
    processed = process_item(item)
    validate_result(processed)
    store_result(processed)
```
"""
        }
        
        return examples.get(mcp_data['category'], f"""
### Basic Usage
```python
# Use {mcp_data['name']} MCP
result = perform_action("input")
print(result)
```

### Integration Example
```python
# Integrate with other MCPs
data = load_data("input")
processed = process_with_{mcp_data['slug']}(data)
save_output(processed)
```
""")
    
    def _generate_mcp_data_js(self, mcps_data: Dict):
        """Generate the mcpData.js file for the frontend."""
        # Count categories
        category_counts = {}
        for mcp_data in mcps_data.values():
            category = mcp_data['category']
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Generate JavaScript object
        js_mcps = {}
        for slug, mcp_data in mcps_data.items():
            js_mcps[slug] = {
                'name': mcp_data['name'],
                'category': mcp_data['category'],
                'description': mcp_data['description'],
                'icon': mcp_data['icon'],
                'actions': mcp_data['actions'],
                'stats': {
                    'version': mcp_data['version'],
                    'updated': mcp_data['updated']
                },
                'platforms': mcp_data['platforms'],
                'slug': mcp_data['slug']
            }
        
        # Generate categories object
        categories = {
            "All": {
                "count": len(mcps_data),
                "color": "#6b7280",
                "icon": "🔍"
            }
        }
        
        category_colors = {
            "Data Processing": "#3b82f6",
            "Analysis & Visualization": "#10b981", 
            "System Management": "#f59e0b",
            "Utilities": "#ef4444"
        }
        
        category_icons = {
            "Data Processing": "📊",
            "Analysis & Visualization": "📈",
            "System Management": "🖥️", 
            "Utilities": "🔧"
        }
        
        for category, count in category_counts.items():
            categories[category] = {
                "count": count,
                "color": category_colors.get(category, "#6b7280"),
                "icon": category_icons.get(category, "🔧")
            }
        
        # Popular MCPs (those with most actions)
        popular_mcps = sorted(mcps_data.keys(), 
                            key=lambda k: len(mcps_data[k]['actions']), 
                            reverse=True)[:6]
        
        content = f"""// MCP data structure for tile-based showcase
export const mcpData = {json.dumps(js_mcps, indent=2)};

// Categories with counts and colors
export const categories = {json.dumps(categories, indent=2)};

// Popular MCPs for featured section
export const popularMcps = {json.dumps(popular_mcps, indent=2)};
"""
        
        output_file = self.data_output_dir / "mcpData.js"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Generated {output_file}")


def main():
    """Main entry point."""
    if len(sys.argv) != 3:
        print("Usage: python generate_docs.py <mcps_directory> <docs_output_directory>")
        sys.exit(1)
    
    mcps_dir = Path(sys.argv[1])
    docs_output_dir = Path(sys.argv[2])
    
    if not mcps_dir.exists():
        print(f"Error: MCPs directory {mcps_dir} does not exist")
        sys.exit(1)
    
    try:
        # Extract MCP data
        extractor = MCPDataExtractor()
        mcps_data = extractor.extract_mcp_data(mcps_dir)
        
        if not mcps_data:
            print("Error: No MCPs found or processed")
            sys.exit(1)
        
        # Generate documentation
        generator = DocusaurusGenerator(docs_output_dir)
        generator.generate_all_docs(mcps_data)
        
        print(f"Successfully generated documentation for {len(mcps_data)} MCPs!")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()