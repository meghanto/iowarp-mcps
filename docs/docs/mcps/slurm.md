---
title: Slurm MCP
description: "Slurm MCP is a Model Context Protocol server that enables LLMs to manage HPC workloads on Slurm-managed clusters with comprehensive job submission, monitoring, and resource management capabilities, featuring intelligent job scheduling, cluster monitoring, array job support, and interactive node a..."
---

import MCPDetail from '@site/src/components/MCPDetail';

<MCPDetail 
  name="Slurm"
  icon="🖥️"
  category="System Management"
  description="Slurm MCP is a Model Context Protocol server that enables LLMs to manage HPC workloads on Slurm-managed clusters with comprehensive job submission, monitoring, and resource management capabilities, featuring intelligent job scheduling, cluster monitoring, array job support, and interactive node allocation for seamless high-performance computing workflows."
  version="1.0.0"
  actions={["submit_slurm_job", "check_job_status", "cancel_slurm_job", "list_slurm_jobs", "get_slurm_info", "get_job_details", "get_job_output", "get_queue_info", "submit_array_job", "get_node_info", "allocate_slurm_nodes", "deallocate_slurm_nodes", "get_allocation_status"]}
  platforms={["claude", "cursor", "vscode"]}
  keywords={["MCP", "Slurm", "HPC", "job-management", "cluster-monitoring", "workload-management", "scientific-computing", "high-performance-computing"]}
  license="MIT"
>

### 1. Job Submission and Monitoring
```
I need to submit a Python simulation script to Slurm with 16 cores and 32GB memory, then monitor its progress until completion.
```

**Tools called:**
- `submit_slurm_job` - Submit job with resource specification
- `check_job_status` - Monitor job progress and performance

This prompt will:
- Use `submit_slurm_job` to submit the Python script with specified resources
- Use `check_job_status` to continuously monitor job execution and performance
- Provide comprehensive job lifecycle management with intelligent optimization

### 2. Array Job Management
```
Submit an array job for parameter sweep analysis with 100 tasks, each requiring 4 cores and 8GB memory, then check the overall progress.
```

**Tools called:**
- `submit_array_job` - Submit parallel array job
- `list_slurm_jobs` - Monitor array job progress
- `get_job_details` - Get detailed array job information

This prompt will:
- Use `submit_array_job` to create a high-throughput parameter sweep with intelligent task distribution
- Use `list_slurm_jobs` to monitor overall array job progress and efficiency
- Use `get_job_details` to analyze individual task performance and optimization opportunities

### 3. Interactive Session Management
```
Allocate 2 compute nodes with 8 cores each for an interactive analysis session, then deallocate when finished.
```

**Tools called:**
- `allocate_slurm_nodes` - Allocate interactive nodes
- `get_node_info` - Check node status and resources
- `get_allocation_status` - Monitor allocation efficiency
- `deallocate_slurm_nodes` - Clean up allocated resources

This prompt will:
- Use `allocate_slurm_nodes` to request interactive compute resources with optimization
- Use `get_node_info` to verify node availability and resource status
- Use `get_allocation_status` to monitor allocation usage and efficiency
- Use `deallocate_slurm_nodes` to clean up resources when analysis is complete

### 4. Job Management and Cleanup
```
I have a long-running job that needs to be cancelled, and I want to retrieve the output from a completed job before cleaning up.
```

**Tools called:**
- `cancel_slurm_job` - Cancel running job with cleanup
- `get_job_output` - Retrieve completed job outputs
- `get_job_details` - Get final job performance metrics

This prompt will:
- Use `cancel_slurm_job` to safely terminate the running job with intelligent cleanup
- Use `get_job_output` to retrieve both stdout and stderr from completed jobs
- Use `get_job_details` to analyze final performance metrics and resource utilization

### 5. Comprehensive Cluster Analysis
```
Analyze the current cluster queue status, identify bottlenecks, and suggest optimal resource allocation for my pending jobs.
```

**Tools called:**
- `get_slurm_info` - Get cluster status and capacity
- `get_queue_info` - Analyze queue performance and bottlenecks
- `list_slurm_jobs` - Review pending job queue and priorities

This prompt will:
- Use `get_slurm_info` to assess overall cluster capacity and resource availability
- Use `get_queue_info` to analyze partition-specific queue performance and bottlenecks
- Use `list_slurm_jobs` to review pending jobs and identify optimization opportunities

### 6. HPC Workflow Optimization
```
I need to optimize my computational workflow by analyzing my recent job performance, understanding cluster utilization patterns, and planning future submissions with better resource allocation.
```

**Tools called:**
- `list_slurm_jobs` - Review recent job history and performance patterns
- `get_job_details` - Analyze specific job performance metrics
- `get_slurm_info` - Understand cluster capacity and optimization opportunities
- `get_queue_info` - Analyze queue performance for optimal timing

This prompt will:
- Use `list_slurm_jobs` to examine historical job performance and identify trends
- Use `get_job_details` to deep-dive into resource utilization and efficiency metrics
- Use `get_slurm_info` to understand cluster constraints and optimization opportunities
- Use `get_queue_info` to plan optimal submission timing and partition selection

</MCPDetail>
