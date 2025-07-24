---
title: Arxiv MCP
description: "ArXiv MCP is a comprehensive Model Context Protocol (MCP) server that enables Language Learning Models (LLMs) to search, analyze, and access research papers from the ArXiv preprint repository. This server provides advanced search capabilities, paper analysis tools, and citation management with se..."
---

import MCPDetail from '@site/src/components/MCPDetail';

<MCPDetail 
  name="Arxiv"
  icon="📄"
  category="Utilities"
  description="ArXiv MCP is a comprehensive Model Context Protocol (MCP) server that enables Language Learning Models (LLMs) to search, analyze, and access research papers from the ArXiv preprint repository. This server provides advanced search capabilities, paper analysis tools, and citation management with seamless integration with AI coding assistants."
  version="1.0.0"
  actions={["search_arxiv", "get_recent_papers", "search_papers_by_author", "search_by_title", "search_by_abstract", "search_by_subject", "search_date_range", "get_paper_details", "export_to_bibtex", "find_similar_papers", "download_paper_pdf", "get_pdf_url", "download_multiple_pdfs"]}
  platforms={["claude", "cursor", "vscode"]}
>

## Advanced Features


### Utility Functions
Essential utility functions for scientific computing:
- **Data Transformation**: Convert and process data efficiently
- **Automation**: Automate repetitive tasks
- **Integration**: Easy integration with other tools

### Performance Optimized
- **Fast Processing**: Optimized algorithms for speed
- **Memory Efficient**: Smart memory management
- **Scalable**: Handles large workloads efficiently


## Available Actions


#### `search_arxiv`
Search ArXiv for research papers by category or topic.

**Usage Example:**
```python
# Use search_arxiv function
result = search_arxiv()
print(result)
```


#### `get_recent_papers`
Get recent papers from a specific ArXiv category.

**Usage Example:**
```python
# Use get_recent_papers function
result = get_recent_papers()
print(result)
```


#### `search_papers_by_author`
Search ArXiv papers by author name.

**Usage Example:**
```python
# Use search_papers_by_author function
result = search_papers_by_author()
print(result)
```


#### `search_by_title`
Search ArXiv papers by title keywords.

**Usage Example:**
```python
# Use search_by_title function
result = search_by_title()
print(result)
```


#### `search_by_abstract`
Search ArXiv papers by abstract keywords.

**Usage Example:**
```python
# Use search_by_abstract function
result = search_by_abstract()
print(result)
```


#### Additional Actions
This MCP provides 8 additional actions. Refer to the MCP server documentation for complete details.


## Integration Examples


### Utility Operations
```python
# Use Arxiv utilities
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


</MCPDetail>
