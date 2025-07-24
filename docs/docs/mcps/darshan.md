---
title: Darshan MCP
description: "Darshan MCP is a comprehensive Model Context Protocol (MCP) server that enables Language Learning Models (LLMs) to analyze HPC application I/O performance through Darshan profiler trace files. This server provides advanced I/O analysis capabilities, performance bottleneck identification, and comp..."
---

import MCPDetail from '@site/src/components/MCPDetail';

<MCPDetail 
  name="Darshan"
  icon="⚡"
  category="Utilities"
  description="Darshan MCP is a comprehensive Model Context Protocol (MCP) server that enables Language Learning Models (LLMs) to analyze HPC application I/O performance through Darshan profiler trace files. This server provides advanced I/O analysis capabilities, performance bottleneck identification, and comprehensive reporting tools with seamless integration with AI coding assistants."
  version="0.1.0"
  actions={["load_darshan_log", "get_job_summary", "analyze_file_access_patterns", "get_io_performance_metrics", "analyze_posix_operations", "analyze_mpiio_operations", "identify_io_bottlenecks", "get_timeline_analysis", "compare_darshan_logs", "generate_io_summary_report", "load_darshan_log", "get_job_summary", "analyze_file_access_patterns", "get_io_performance_metrics", "analyze_posix_operations", "analyze_mpiio_operations", "identify_io_bottlenecks", "get_timeline_analysis", "compare_darshan_logs", "generate_io_summary_report"]}
  platforms={["claude", "cursor", "vscode"]}
  keywords={[]}
  license="MIT"
>

### 1. HPC Application Performance Analysis
```
Analyze the I/O performance of my application using the Darshan log at /data/app_trace.darshan. Identify bottlenecks and provide optimization recommendations.
```

**Tools called:**
- `load_darshan_log` - Parse the Darshan trace file
- `get_job_summary` - Extract job-level statistics
- `identify_io_bottlenecks` - Find performance issues
- `get_io_performance_metrics` - Calculate detailed metrics

This prompt will:
- Use `load_darshan_log` to parse the trace file and extract metadata
- Generate job summary using `get_job_summary` for runtime and I/O statistics
- Identify performance bottlenecks using `identify_io_bottlenecks`
- Provide comprehensive performance analysis with optimization recommendations

### 2. I/O Pattern Optimization Study
```
Compare the I/O patterns between /data/before_opt.darshan and /data/after_opt.darshan to validate our optimization efforts and measure performance improvements.
```

**Tools called:**
- `analyze_file_access_patterns` - Analyze access patterns for both files
- `compare_darshan_logs` - Compare performance metrics
- `get_io_performance_metrics` - Extract detailed performance data

This prompt will:
- Analyze access patterns using `analyze_file_access_patterns` for both traces
- Compare performance metrics using `compare_darshan_logs`
- Extract detailed metrics using `get_io_performance_metrics`
- Provide comprehensive optimization validation and improvement quantification

### 3. MPI-IO Collective Performance Analysis
```
Examine the MPI-IO operations in /data/parallel_app.darshan, focusing on collective vs independent I/O patterns and their impact on overall performance.
```

**Tools called:**
- `analyze_mpiio_operations` - Analyze MPI-IO patterns
- `get_timeline_analysis` - Understand temporal patterns
- `generate_io_summary_report` - Create comprehensive report

This prompt will:
- Analyze MPI-I/O operations using `analyze_mpiio_operations`
- Generate temporal analysis using `get_timeline_analysis`
- Create detailed report using `generate_io_summary_report`
- Provide insights into collective I/O efficiency and optimization opportunities

### 4. POSIX System Call Analysis
```
Investigate the POSIX I/O operations in /data/serial_app.darshan to understand file access patterns and identify potential optimizations for system call efficiency.
```

**Tools called:**
- `analyze_posix_operations` - Examine POSIX system calls
- `analyze_file_access_patterns` - Study file access behavior
- `identify_io_bottlenecks` - Find system-level bottlenecks

This prompt will:
- Analyze POSIX operations using `analyze_posix_operations`
- Study file access patterns using `analyze_file_access_patterns`
- Identify bottlenecks using `identify_io_bottlenecks`
- Provide system call optimization recommendations

### 5. Comprehensive I/O Performance Report
```
Generate a complete I/O performance analysis report for /data/production_app.darshan including all metrics, visualizations, and recommendations for our production environment.
```

**Tools called:**
- `load_darshan_log` - Load and validate trace file
- `generate_io_summary_report` - Create comprehensive analysis
- `get_timeline_analysis` - Add temporal performance data

This prompt will:
- Load and validate trace using `load_darshan_log`
- Generate complete report using `generate_io_summary_report`
- Add timeline analysis using `get_timeline_analysis`
- Provide production-ready performance assessment with actionable insights

</MCPDetail>
