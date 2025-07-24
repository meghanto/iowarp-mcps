---
title: Parallel-Sort MCP
description: "Parallel Sort MCP is a comprehensive Model Context Protocol (MCP) server that enables Language Learning Models (LLMs) to perform high-performance log file processing and analysis operations. This server provides advanced log sorting, filtering, analysis tools, and scalable data processing capabil..."
---

import MCPDetail from '@site/src/components/MCPDetail';

<MCPDetail 
  name="Parallel-Sort"
  icon="🔄"
  category="Data Processing"
  description="Parallel Sort MCP is a comprehensive Model Context Protocol (MCP) server that enables Language Learning Models (LLMs) to perform high-performance log file processing and analysis operations. This server provides advanced log sorting, filtering, analysis tools, and scalable data processing capabilities with seamless integration with AI coding assistants. Key Features: - Log File Sorting: Timestamp-based sorting with parallel processing for large log files - Advanced Filtering: Multi-condition filtering by time range, log level, keywords, and custom patterns - Pattern Detection: Anomaly detection, error clustering, and trend analysis - Statistical Analysis: Comprehensive log statistics, temporal patterns, and quality metrics - Multiple Export Formats: Support for JSON, CSV, and text output with metadata - Scalable Processing: Handle large log files with memory-efficient chunked processing - MCP Integration: Full Model Context Protocol compliance for seamless LLM integration"
  version="1.0.0"
  actions={["sort_log_by_timestamp", "parallel_sort_large_file", "analyze_log_statistics", "detect_log_patterns", "filter_logs", "filter_by_time_range", "filter_by_log_level", "filter_by_keyword", "apply_filter_preset", "export_to_json", "export_to_csv", "export_to_text", "generate_summary_report"]}
  platforms={["claude", "cursor", "vscode"]}
  keywords={["parallel-sorting", "log-processing", "log-analysis", "high-performance", "timestamp-sorting", "pattern-detection", "log-filtering", "data-export"]}
  license="MIT"
>

## Installation

### Requirements
 
- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)
 
<details>
<summary><b>Install in Cursor</b></summary>
 
Go to: `Settings` -> `Cursor Settings` -> `MCP` -> `Add new global MCP server`
 
Pasting the following configuration into your Cursor `~/.cursor/mcp.json` file is the recommended approach. You may also install in a specific project by creating `.cursor/mcp.json` in your project folder. See [Cursor MCP docs](https://docs.cursor.com/context/model-context-protocol) for more info.
 
```json
{
  "mcpServers": {
    "parallel-sort-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "parallel-sort"]
    }
  }
}
```
 
</details>
 
<details>
<summary><b>Install in VS Code</b></summary>
 
Add this to your VS Code MCP config file. See [VS Code MCP docs](https://code.visualstudio.com/docs/copilot/chat/mcp-servers) for more info.
 
```json
"mcp": {
  "servers": {
    "parallel-sort-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["iowarp-mcps", "parallel-sort"]
    }
  }
}
```
 
</details>
 
<details>
<summary><b>Install in Claude Code</b></summary>
 
Run this command. See [Claude Code MCP docs](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials#set-up-model-context-protocol-mcp) for more info.
 
```sh
claude mcp add parallel-sort-mcp -- uvx iowarp-mcps parallel-sort
```
 
</details>
 
<details>
<summary><b>Install in Claude Desktop</b></summary>
 
Add this to your Claude Desktop `claude_desktop_config.json` file. See [Claude Desktop MCP docs](https://modelcontextprotocol.io/quickstart/user) for more info.
 
```json
{
  "mcpServers": {
    "parallel-sort-mcp": {
      "command": "uvx",
      "args": ["iowarp-mcps", "parallel-sort"]
    }
  }
}
```
 
</details>
 
<details>
<summary><b>Manual Setup</b></summary>
 
**Linux/macOS:**
```bash
CLONE_DIR=$(pwd)
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$CLONE_DIR/iowarp-mcps/mcps/Parallel_Sort run parallel-sort-mcp --help
```
 
**Windows CMD:**
```cmd
set CLONE_DIR=%cd%
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=%CLONE_DIR%\iowarp-mcps\mcps\Parallel_Sort run parallel-sort-mcp --help
```
 
**Windows PowerShell:**
```powershell
$env:CLONE_DIR=$PWD
git clone https://github.com/iowarp/iowarp-mcps.git
uv --directory=$env:CLONE_DIR\iowarp-mcps\mcps\Parallel_Sort run parallel-sort-mcp --help
```
 
</details>

## Available Tools


### `sort_log_by_timestamp`

Sort log file lines by timestamps in YYYY-MM-DD HH:MM:SS format. Handles edge cases like empty files and invalid timestamps.

**Usage Example:**
```python
# Use sort_log_by_timestamp function
result = sort_log_by_timestamp()
print(result)
```


### `parallel_sort_large_file`

Sort large log files using parallel processing with chunked approach for improved performance.

**Usage Example:**
```python
# Use parallel_sort_large_file function
result = parallel_sort_large_file()
print(result)
```


### `analyze_log_statistics`

Generate comprehensive statistics and analysis for log files including temporal patterns, log levels, and quality metrics.

**Usage Example:**
```python
# Use analyze_log_statistics function
result = analyze_log_statistics()
print(result)
```


### `detect_log_patterns`

Detect patterns in log files including anomalies, error clusters, trending issues, and repeated patterns.

**Usage Example:**
```python
# Use detect_log_patterns function
result = detect_log_patterns()
print(result)
```


### `filter_logs`

Filter log entries based on multiple conditions with support for complex logical operations.

**Usage Example:**
```python
# Use filter_logs function
result = filter_logs()
print(result)
```


### `filter_by_time_range`

Filter log entries by time range using start and end timestamps.

**Usage Example:**
```python
# Use filter_by_time_range function
result = filter_by_time_range()
print(result)
```


### `filter_by_log_level`

Filter log entries by log level (ERROR, WARN, INFO, DEBUG, etc.).

**Usage Example:**
```python
# Use filter_by_log_level function
result = filter_by_log_level()
print(result)
```


### `filter_by_keyword`

Filter log entries by keywords in the message content with support for multiple keywords and logical operations.

**Usage Example:**
```python
# Use filter_by_keyword function
result = filter_by_keyword()
print(result)
```


### `apply_filter_preset`

Apply predefined filter presets like 'errors_only', 'warnings_and_errors', 'connection_issues', etc.

**Usage Example:**
```python
# Use apply_filter_preset function
result = apply_filter_preset()
print(result)
```


### `export_to_json`

Export log processing results to JSON format with optional metadata.

**Usage Example:**
```python
# Use export_to_json function
result = export_to_json()
print(result)
```


### `export_to_csv`

Export log entries to CSV format with structured columns for timestamp, level, and message.

**Usage Example:**
```python
# Use export_to_csv function
result = export_to_csv()
print(result)
```


### `export_to_text`

Export log entries to plain text format with optional processing summary.

**Usage Example:**
```python
# Use export_to_text function
result = export_to_text()
print(result)
```


### `generate_summary_report`

Generate a comprehensive summary report of log processing results with statistics and analysis.

**Usage Example:**
```python
# Use generate_summary_report function
result = generate_summary_report()
print(result)
```


## Examples

### 1. Large Log File Sorting and Analysis
```
I have a large application log file at /var/logs/app.log with millions of entries. Sort this log chronologically and analyze the error patterns.
```

**Tools called:**
- `parallel_sort_large_file` - Sort the large log file using parallel processing
- `analyze_log_statistics` - Analyze log statistics and patterns
- `detect_log_patterns` - Detect error patterns and anomalies

This prompt will:
- Use `parallel_sort_large_file` to efficiently sort the large log file with optimal chunk processing
- Analyze log statistics using `analyze_log_statistics` for comprehensive metrics
- Detect patterns using `detect_log_patterns` to identify issues and trends
- Generate sorted output with detailed analysis reports

### 2. Error Log Filtering and Export
```
Filter all ERROR and WARN level entries from /var/logs/system.log from the last 24 hours and export to CSV for analysis.
```

**Tools called:**
- `filter_by_time_range` - Filter logs by time range
- `filter_by_log_level` - Filter by ERROR and WARN levels
- `export_to_csv` - Export filtered results to CSV

This prompt will:
- Filter logs by time range using `filter_by_time_range` for the last 24 hours
- Apply log level filtering using `filter_by_log_level` for ERROR and WARN entries
- Export results using `export_to_csv` with structured columns
- Provide filtered dataset ready for analysis

### 3. Connection Issue Pattern Detection
```
Analyze /var/logs/network.log for connection timeout patterns and generate a comprehensive report with trend analysis.
```

**Tools called:**
- `filter_by_keyword` - Filter for connection-related entries
- `detect_log_patterns` - Detect timeout patterns and trends
- `generate_summary_report` - Create comprehensive analysis report

This prompt will:
- Filter connection-related entries using `filter_by_keyword` with timeout keywords
- Analyze patterns using `detect_log_patterns` for anomaly detection
- Generate comprehensive report using `generate_summary_report`
- Provide trend analysis and proactive issue identification

### 4. Multi-Condition Log Analysis
```
Find all database connection errors in /var/logs/db.log that occurred during business hours (9 AM - 5 PM) and contain "timeout" or "refused".
```

**Tools called:**
- `filter_by_time_range` - Filter for business hours
- `filter_by_keyword` - Filter for timeout and connection refused
- `filter_logs` - Apply complex multi-condition filtering
- `analyze_log_statistics` - Analyze filtered results

This prompt will:
- Apply time-based filtering using `filter_by_time_range` for business hours
- Filter by keywords using `filter_by_keyword` for timeout and refused conditions
- Combine filters using `filter_logs` with logical operators
- Analyze results using `analyze_log_statistics` for comprehensive insights

### 5. Log Quality Assessment and Cleanup
```
Analyze the quality of /var/logs/application.log, identify malformed entries, and generate a clean sorted version with quality metrics.
```

**Tools called:**
- `analyze_log_statistics` - Assess log quality and identify issues
- `sort_log_by_timestamp` - Sort logs chronologically
- `generate_summary_report` - Create quality assessment report

This prompt will:
- Assess log quality using `analyze_log_statistics` with quality metrics
- Sort logs using `sort_log_by_timestamp` for chronological order
- Generate quality report using `generate_summary_report`
- Provide clean dataset with quality improvement recommendations

### 6. Historical Log Trend Analysis
```
Analyze error trends in /var/logs/historic.log over the past month, detect anomalies, and export findings to JSON for dashboard integration.
```

**Tools called:**
- `filter_by_time_range` - Filter for past month
- `detect_log_patterns` - Detect trends and anomalies
- `analyze_log_statistics` - Generate temporal analysis
- `export_to_json` - Export results for dashboard

This prompt will:
- Filter historical data using `filter_by_time_range` for the past month
- Detect trends using `detect_log_patterns` with anomaly detection
- Analyze temporal patterns using `analyze_log_statistics`
- Export findings using `export_to_json` for dashboard integration

</MCPDetail>
