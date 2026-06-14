# Python & Agentic AI Course

A comprehensive course covering Python fundamentals and modern Agentic AI development.

---

## Course Overview

This course takes you from Python basics to building production-ready AI agents using the latest frameworks and tools in the Agentic AI ecosystem.

---

## Module 1: Python Fundamentals

- Variables, data types, and operators
- Control flow: conditionals and loops
- Functions, scope, and closures
- Object-Oriented Programming (classes, inheritance, polymorphism)
- Modules, packages, and virtual environments
- File handling and exception management
- List comprehensions, generators, and decorators
- Working with popular libraries: `requests`, `json`, `os`, `pathlib`

---

## Module 2: FastAPI

- Introduction to REST APIs and HTTP methods
- Setting up a FastAPI project
- Path parameters, query parameters, and request bodies
- Pydantic models for data validation
- Dependency injection
- Async endpoints with `async/await`
- Authentication and middleware
- API documentation with Swagger UI and ReDoc
- Deploying FastAPI applications

---

## Module 3: LangChain

- Introduction to LangChain and its ecosystem
- LLM wrappers and prompt templates
- Chains: sequential and custom chains
- Memory management for conversational AI
- Document loaders, text splitters, and vector stores
- Retrieval-Augmented Generation (RAG)
- LangChain agents and tools
- LangSmith for tracing and monitoring

---

## Module 4: LangGraph

- Introduction to agentic workflows and graphs
- Nodes, edges, and state management
- Building stateful multi-step agents
- Conditional edges and branching logic
- Human-in-the-loop workflows
- Checkpointing and persistence
- Multi-agent architectures with LangGraph
- Streaming agent outputs

---

## Module 5: Model Context Protocol (MCP)

- What is MCP and why it matters
- MCP architecture: hosts, clients, and servers
- Building MCP servers with Python
- Exposing tools, resources, and prompts via MCP
- Connecting MCP servers to Claude and other LLMs
- MCP with LangChain and LangGraph integration
- Real-world MCP use cases and patterns

---

## Module 6: Agentic AI Concepts

- What are AI agents?
- ReAct (Reasoning + Acting) pattern
- Tool use and function calling
- Planning and task decomposition
- Multi-agent collaboration and orchestration
- Agent memory: short-term, long-term, and episodic
- Evaluation and observability for AI agents
- Safety and guardrails in agentic systems

---

## Prerequisites

- Basic programming knowledge helpful but not required
- Python 3.10+ installed
- Familiarity with terminal/command line

---

## Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.10+ |
| API Framework | FastAPI, Uvicorn, Pydantic |
| AI Orchestration | LangChain, LangGraph |
| Agent Protocol | Model Context Protocol (MCP) |
| LLMs | Claude (Anthropic), OpenAI GPT |
| Vector Stores | FAISS, Chroma |
| Monitoring | LangSmith |

---

## Getting Started

```bash
# Clone the repository
git clone https://github.com/TechGeekConnectTech/Python-Agentic-AI-Course.git
cd Python-Agentic-AI-Course

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License.
