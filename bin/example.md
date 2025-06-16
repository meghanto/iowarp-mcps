# `wrp_chat_factory` - Usage Examples

This document provides specific examples for running the `wrp_chat_factory` with each supported LLM provider.

---

### 1. Gemini

Google's Gemini models are a good choice for complex queries that involve multi-step tool use.

**Command:**
```bash
python bin/wrp_chat_factory.py --provider gemini --servers=Jarvis
```

**Interaction Example:**
```
Query: create a pipeline named "gemini-test" and then append the ior package to it

[Calling tool create_pipeline with args {'pipeline_id': 'gemini-test'}]
[Called create_pipeline: {'status': 'success', 'pipeline_id': 'gemini-test'}]
[Calling tool append_pkg with args {'pkg_id': 'ior'}]
[Called append_pkg: {'status': 'success', 'pkg_id': 'ior'}]
```

---

### 2. Ollama

Ollama is ideal for local, offline development and testing. Ensure the Ollama service is running before starting the client.

**Command:**
```bash
# Uses 'llama2' by default
python bin/wrp_chat_factory.py --provider ollama --servers=Jarvis

# Specify a different model (e.g., Llama 3)
python bin/wrp_chat_factory.py --provider ollama --servers=Jarvis -- --model=llama3
```

**Interaction Example:**
```
Query: list all pipelines

[Calling tool jm_list_pipelines with args {}]
[Called jm_list_pipelines: {'pipelines': ['gemini-test']}]
```

---

### 3. OpenAI

OpenAI's models, like GPT-4, are powerful and reliable for a wide range of tasks.

**Command:**
```bash
# Uses 'gpt-4-turbo' by default
python bin/wrp_chat_factory.py --provider openai --servers=Jarvis
```

**Interaction Example:**
```
Query: show me the configuration of the ior package in the "gemini-test" pipeline

[Calling tool get_pkg_config with args {'pipeline_id': 'gemini-test', 'pkg_id': 'ior'}]
[Called get_pkg_config: {'config': {'path': '...', 'version': '...'}, 'status': 'success'}]
```

---

### 4. Claude

Anthropic's Claude models are known for their conversational abilities and careful outputs.

**Command:**
```bash
# Uses 'claude-3-haiku-20240307' by default
python bin/wrp_chat_factory.py --provider claude --servers=Jarvis
```

**Interaction Example:**
```
Query: destroy the "gemini-test" pipeline

[Calling tool destroy_pipeline with args {'pipeline_id': 'gemini-test'}]
[Called destroy_pipeline: {'status': 'success', 'msg': 'Pipeline gemini-test destroyed.'}]
``` 