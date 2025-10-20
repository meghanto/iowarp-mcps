---
title: Chronolog MCP
description: "Part of [IoWarp MCPs](https://iowarp.github.io/iowarp-mcps/) - Gnosis Research Center"
---

import MCPDetail from '@site/src/components/MCPDetail';

<MCPDetail 
  name="Chronolog"
  icon="⏰"
  category="Utilities"
  description="Part of [IoWarp MCPs](https://iowarp.github.io/iowarp-mcps/) - Gnosis Research Center"
  version="1.0.0"
  actions={["start_chronolog", "record_interaction", "stop_chronolog", "retrieve_interaction"]}
  platforms={["claude", "cursor", "vscode"]}
  keywords={[]}
  license="MIT"
  tools={[{"name": "start_chronolog", "description": "Connects to ChronoLog, creates a chronicle, and acquires a story handle for logging interactions.", "function_name": "start_chronolog"}, {"name": "record_interaction", "description": "Logs user messages and LLM responses to the active story with structured event formatting.", "function_name": "record_interaction"}, {"name": "stop_chronolog", "description": "Releases the story handle and cleanly disconnects from ChronoLog system.", "function_name": "stop_chronolog"}, {"name": "retrieve_interaction", "description": "Extracts logged records from specified chronicle and story, generates timestamped output files with filtering options.", "function_name": "retrieve_interaction"}]}
>

### 1. Session Logging and Analysis
```
Start logging our conversation, then after we discuss machine learning concepts, retrieve the interaction history for analysis.
```

**Tools called:**
- `start_chronolog` - Initialize logging session
- `record_interaction` - Log conversation events  
- `retrieve_interaction` - Generate interaction history

This prompt will:
- Use `start_chronolog` to create a new chronicle and story
- Automatically log interactions using `record_interaction`
- Extract conversation history using `retrieve_interaction`
- Provide structured session analysis

### 2. Multi-Session Context Sharing
```
Connect to the research chronicle and retrieve yesterday's discussion about neural networks to continue our conversation.
```

**Tools called:**
- `start_chronolog` - Connect to existing chronicle
- `retrieve_interaction` - Fetch historical interactions

This prompt will:
- Connect to existing research chronicle using `start_chronolog`
- Retrieve previous session data using `retrieve_interaction`
- Enable context continuation across sessions
- Support multi-client collaborative workflows

### 3. Structured Event Documentation
```
Begin recording our software design discussion, ensuring all architectural decisions and code examples are captured for future reference.
```

**Tools called:**
- `start_chronolog` - Begin structured logging
- `record_interaction` - Capture design decisions
- `stop_chronolog` - Complete session

This prompt will:
- Initialize structured event logging using `start_chronolog`
- Capture all conversation elements using `record_interaction`
- Maintain detailed architectural documentation
- Provide clean session termination using `stop_chronolog`

</MCPDetail>

