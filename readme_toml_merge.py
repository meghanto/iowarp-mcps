#!/usr/bin/env python3
"""
MCP Documentation Generator for Docusaurus
Extracts information from MCP folders and creates Docusaurus-compatible markdown files with frontmatter.
"""

import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Use built-in tomllib for Python 3.11+
import tomllib

class MCPDocusaurusGenerator:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.mcps_dir = self.base_dir / "mcps"
        self.docs_dir = self.base_dir / "docs" / "mcps"  # Docusaurus docs folder
        
    def get_last_commit_date(self, mcp_path: str) -> str:
        """Get the last commit date for a specific MCP directory."""
        try:
            cmd = ["git", "log", "-1", "--format=%ad", "--date=format:%Y-%m-%d", "--", mcp_path]
            result = subprocess.run(cmd, cwd=self.base_dir, capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            else:
                # Fallback to today's date if git command fails
                return datetime.now().strftime("%Y-%m-%d")
        except Exception:
            return datetime.now().strftime("%Y-%m-%d")
    
    def extract_capabilities_count(self, readme_path: Path) -> int:
        """Count the number of capabilities (### `function_name`) in README.md."""
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for capabilities section with pattern ### `function_name`
            capability_pattern = r'^### `[^`]+`$'
            matches = re.findall(capability_pattern, content, re.MULTILINE)
            return len(matches)
        except Exception as e:
            print(f"Error counting capabilities in {readme_path}: {e}")
            return 0
    
    def extract_installation_info(self, readme_path: Path) -> str:
        """Extract installation information from README.md."""
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for installation section with emoji or plain text
            installation_section = re.search(
                r'## (?:🛠️ )?Installation.*?(?=^## [^#]|\Z)', 
                content, 
                re.DOTALL | re.IGNORECASE | re.MULTILINE
            )
            
            if installation_section:
                # Return the entire installation section as markdown
                return installation_section.group(0).strip()
            
            # Fallback to generic installation section
            return """## Installation

```bash
uv pip install iowarp-mcps
```"""
            
        except Exception as e:
            print(f"Error extracting installation from {readme_path}: {e}")
            return """## Installation

```bash
uv pip install iowarp-mcps
```"""
    
    def extract_available_actions(self, readme_path: Path) -> List[Dict[str, str]]:
        """Extract available actions from the capabilities section of README.md."""
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            actions = []
            
            # Find all capability sections - updated pattern to handle the actual structure
            capability_pattern = r'### `([^`]+)`\s*\n\*\*Description\*\*:\s*([^\n]+)(?:\n\n\*\*Parameters\*\*:\s*\n(.*?)\n\n\*\*Returns\*\*)?'
            matches = re.finditer(capability_pattern, content, re.MULTILINE | re.DOTALL)
            
            for match in matches:
                action_name = match.group(1)
                description = match.group(2).strip()
                params_section = match.group(3) if match.group(3) else ""
                
                # Extract parameters
                param_list = []
                if params_section:
                    # Look for parameter lines starting with "-"
                    param_matches = re.findall(r'-\s+`([^`]+)`\s*\([^)]+\):\s*([^\n]+)', params_section)
                    param_list = [f"{p[0]}: {p[1].strip()}" for p in param_matches]
                
                actions.append({
                    'name': action_name,
                    'description': description,
                    'parameters': ', '.join(param_list) if param_list else 'No parameters'
                })
            
            return actions
            
        except Exception as e:
            print(f"Error extracting actions from {readme_path}: {e}")
            return []
    
    def extract_examples(self, readme_path: Path) -> str:
        """Extract examples from README.md and format as markdown."""
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for examples section - using exact match with space after ##
            examples_section = re.search(
                r'^## Examples.*?(?=^## |\Z)', 
                content, 
                re.MULTILINE | re.DOTALL
            )
            
            if examples_section:
                examples_text = examples_section.group(0)
                
                # Extract multiple examples with their descriptions and tools
                examples_md = ""
                
                # Find all example subsections
                example_pattern = r'### (\d+)\.\s*([^\n]+)\n```\s*\n(.*?)\n```\s*\n\n\*\*Tools called:\*\*\s*\n((?:- `[^`]+`[^\n]*\n)*)'
                matches = re.finditer(example_pattern, examples_text, re.DOTALL)
                
                example_count = 0
                for match in matches:
                    example_num = match.group(1)
                    example_title = match.group(2).strip()
                    example_text = match.group(3).strip()
                    tools_section = match.group(4).strip()
                    
                    # Parse tools called
                    tools = []
                    tool_matches = re.findall(r'- `([^`]+)`\s*-\s*([^\n]+)', tools_section)
                    for tool_name, tool_desc in tool_matches:
                        tools.append(f"- **{tool_name}**: {tool_desc.strip()}")
                    
                    # Build example markdown
                    if example_count > 0:
                        examples_md += "\n"
                    
                    examples_md += f"### {example_title}\n\n"
                    examples_md += f"```\n{example_text}\n```\n\n"
                    
                    if tools:
                        examples_md += "**Tools used:**\n"
                        examples_md += "\n".join(tools) + "\n"
                    
                    example_count += 1
                
                if examples_md:
                    return examples_md
                
                # Fallback: try to extract just the first example without tools
                first_example = re.search(
                    r'### 1\..*?\n```\s*\n(.*?)\n```', 
                    examples_text, 
                    re.DOTALL
                )
                
                if first_example:
                    example_text = first_example.group(1).strip()
                    return f"### Example Usage\n\n```\n{example_text}\n```\n"
                
                # If still no examples, create a generic one based on capabilities
                return "### Example Usage\n\n```\n// Use the available MCP functions to interact with the service\n// See Available Actions section for specific function details\n```\n"
            
            # Fallback to generic example
            return "### Example Usage\n\n```\n// Use the MCP capabilities to interact with the service\n// Check the Available Actions section for specific functions\n```\n"
            
        except Exception as e:
            print(f"Error extracting examples from {readme_path}: {e}")
            return "### Examples\n\n```\n// Examples not available\n```\n"
    
    def extract_pyproject_info(self, pyproject_path: Path) -> Dict[str, str]:
        """Extract information from pyproject.toml."""
        try:
            with open(pyproject_path, 'rb') as f:
                data = tomllib.load(f)
            
            project = data.get('project', {})
            
            # Extract all keywords and format them for category display
            keywords = project.get('keywords', [])
            
            # Filter out common MCP keywords and format the rest
            filtered_keywords = [kw for kw in keywords if kw.lower() not in ['mcp', 'llm-integration']]
            
            if filtered_keywords:
                # Format keywords individually with line breaks for better display
                formatted_keywords = []
                for kw in filtered_keywords:
                    formatted_kw = kw.replace('-', ' ').title()
                    formatted_keywords.append(formatted_kw)
                # Join with bullet points or line breaks
                category = ' • '.join(formatted_keywords)
            else:
                category = "Other"
            
            # Extract language from dependencies or requires-python
            language = "Python"  # Default since all projects use Python
            if 'requires-python' in project:
                language = "Python"
            
            return {
                'version': project.get('version', '1.0.0'),
                'description': project.get('description', ''),
                'category': category,
                'language': language,
                'keywords': filtered_keywords
            }
            
        except Exception as e:
            print(f"Error extracting pyproject info from {pyproject_path}: {e}")
            return {
                'version': '1.0.0',
                'description': '',
                'category': 'Other',
                'language': 'Python',
                'keywords': []
            }
    
    def create_docusaurus_markdown_file(self, mcp_info: Dict):
        """Create a Docusaurus-compatible markdown file with frontmatter."""
        try:
            # Create filename: mcp-<name>.md in the docs folder
            filename = f"mcp-{mcp_info['name'].lower()}.md"
            file_path = self.docs_dir / filename
            
            # Ensure docs directory exists
            self.docs_dir.mkdir(parents=True, exist_ok=True)
            
            # Format the available actions as markdown
            actions_md = ""
            for action in mcp_info["available_actions"]:
                actions_md += f"### `{action['name']}`\n\n"
                actions_md += f"**Description**: {action['description']}\n\n"
                actions_md += f"**Parameters**: {action['parameters']}\n\n"
            
            # Create Docusaurus frontmatter
            frontmatter = f"""---
id: mcp-{mcp_info['name'].lower()}
title: {mcp_info['name']} MCP
sidebar_label: {mcp_info['name']}
description: {mcp_info['description']}
keywords: {mcp_info['keywords']}
tags: {mcp_info['keywords']}
last_update:
  date: {mcp_info['updated']}
  author: IOWarp Team
---

"""
            
            # Create the markdown content
            markdown_content = f"""{frontmatter}# {mcp_info['name']} MCP

## Overview
{mcp_info['description']}

## Information
- **Version**: {mcp_info['version']}
- **Language**: {mcp_info['language']}
- **Category**: {mcp_info['category']}
- **Actions**: {mcp_info['actions_count']}
- **Last Updated**: {mcp_info['updated']}

{mcp_info['installation']}

## Available Actions

{actions_md}

## Examples

{mcp_info['examples']}
"""
            
            # Write the markdown file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"Created docs/mcps/{filename}")
            
        except Exception as e:
            print(f"Error creating Docusaurus markdown file for {mcp_info['name']}: {e}")
    
    
    def process_mcp(self, mcp_name: str) -> Optional[Dict]:
        """Process a single MCP and extract all information."""
        mcp_dir = self.mcps_dir / mcp_name
        readme_path = mcp_dir / "README.md"
        pyproject_path = mcp_dir / "pyproject.toml"
        
        if not readme_path.exists() or not pyproject_path.exists():
            print(f"Skipping {mcp_name}: Missing README.md or pyproject.toml")
            return None
        
        print(f"Processing {mcp_name}...")
        
        # Extract information
        pyproject_info = self.extract_pyproject_info(pyproject_path)
        capabilities_count = self.extract_capabilities_count(readme_path)
        installation = self.extract_installation_info(readme_path)
        available_actions = self.extract_available_actions(readme_path)
        examples = self.extract_examples(readme_path)
        updated_date = self.get_last_commit_date(str(mcp_dir))
        
        return {
            'name': mcp_name,
            'version': pyproject_info['version'],
            'description': pyproject_info['description'],
            'category': pyproject_info['category'],
            'language': pyproject_info['language'],
            'keywords': pyproject_info['keywords'],
            'actions_count': capabilities_count,
            'installation': installation,
            'available_actions': available_actions,
            'examples': examples,
            'updated': updated_date
        }
    
    def create_sidebar_config(self, mcp_infos: List[Dict]):
        """Create sidebars.js configuration for Docusaurus."""
        try:
            sidebar_items = []
            
            # Group MCPs by category
            categories = {}
            for mcp_info in mcp_infos:
                category = mcp_info['category']
                if category not in categories:
                    categories[category] = []
                categories[category].append({
                    'type': 'doc',
                    'id': f"mcp-{mcp_info['name'].lower()}",
                    'label': mcp_info['name']
                })
            
            # Create sidebar structure
            for category, items in categories.items():
                if len(items) == 1:
                    sidebar_items.extend(items)
                else:
                    sidebar_items.append({
                        'type': 'category',
                        'label': category,
                        'items': items
                    })
            
            # Create sidebars.js content
            sidebars_content = f"""module.exports = {{
  mcpSidebar: [
    {{
      type: 'doc',
      id: 'intro',
      label: 'Introduction',
    }},
    {{
      type: 'category',
      label: 'MCPs',
      items: {str(sidebar_items).replace("'", '"')},
    }},
  ],
}};
"""
            
            # Write sidebars.js
            sidebars_path = self.base_dir / "docs" / "sidebars.js"
            with open(sidebars_path, 'w', encoding='utf-8') as f:
                f.write(sidebars_content)
            
            print("Created docs/sidebars.js")
            
        except Exception as e:
            print(f"Error creating sidebars.js: {e}")
    
    def run(self):
        """Main function to process all MCPs and create Docusaurus-compatible markdown files."""
        print("Starting MCP Docusaurus documentation generation...")
        
        # Get list of MCP directories
        mcp_dirs = [d.name for d in self.mcps_dir.iterdir() if d.is_dir()]
        
        mcp_infos = []
        for mcp_name in mcp_dirs:
            mcp_info = self.process_mcp(mcp_name)
            if mcp_info:
                self.create_docusaurus_markdown_file(mcp_info)
                mcp_infos.append(mcp_info)
        
        # Create sidebar configuration
        self.create_sidebar_config(mcp_infos)
        
        print("MCP Docusaurus documentation generation completed!")

def main():
    """Entry point for the script."""
    # Use current working directory or script directory as base
    base_dir = os.getcwd()
    generator = MCPDocusaurusGenerator(base_dir)
    generator.run()

if __name__ == "__main__":
    main()