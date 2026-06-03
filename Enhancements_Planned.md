# Synora Studio: Planned Enhancements & Future Roadmap

This document outlines the strategic high-impact architectural and feature enhancements proposed for future versions of Synora Studio (v1.1+).

## Enhancement Tracker

| ID | Enhancement Title | Status |
|:---|:---|:---|
| **EN-01** | Real-Time WebSockets (Socket.IO) for Hermes | 🟢 Deployed |
| **EN-02** | Full Dockerization & Kubernetes Helm Charts | 🟡 Pending |
| **EN-03** | Agentic "Tool Calling" UI (Native Function Calling) | 🟡 Pending |
| **EN-04** | Advanced GraphRAG (Knowledge Graphs) | 🟡 Pending |
| **EN-05** | Multi-Agent Swarms | 🟡 Pending |

---

## [x] EN-01: Real-Time WebSockets (Socket.IO) for Hermes
Currently, the Hermes Agent console relies heavily on polling or file-watching to monitor agent activity.
- **The Enhancement:** Implement `Flask-SocketIO` to push live, sub-millisecond agent reasoning logs directly from the detached background `hermes_runner.py` to the PySide6 UI and the Web SaaS Portal. 
- **Impact:** Creates a highly responsive, real-time "matrix code" effect as the agent thinks, completely eliminating polling overhead.

## [ ] EN-02: Full Dockerization & Kubernetes Helm Charts
With a sophisticated Master Orchestrator running a Desktop GUI, a Backend API, and a Web SaaS Portal concurrently, deployment modularity is key.
- **The Enhancement:** Create a comprehensive `docker-compose.yml` to fully containerize the SaaS Portal, the API server, and the Qdrant Vector database. 
- **Impact:** Allows enterprise users to instantly spin up Synora Studio on AWS or Google Cloud with zero dependency issues, completely decoupled from the local PySide6 Desktop executable.

## [ ] EN-03: Agentic "Tool Calling" UI (Native Function Calling)
The backend currently supports external tools via Hermes, but the main chat UI is strictly text and Markdown-based.
- **The Enhancement:** Parse native LLM "Tool Call" JSON payloads (e.g., OpenAI's native function calling format) and render beautiful, interactive widgets in the PySide6 UI when a tool is called. 
- **Impact:** If the AI calls `search_web()`, the chat will render a sleek loading spinner widget labeled *"Searching the web..."* before injecting the result, vastly improving user trust and experience.

## [ ] EN-04: Advanced GraphRAG (Knowledge Graphs)
Synora Studio currently leverages Qdrant for semantic Dense Vector retrieval (finding chunks of text with similar meaning).
- **The Enhancement:** Integrate a Knowledge Graph (like Neo4j or NetworkX) alongside Qdrant. 
- **Impact:** Allows the AI to not just find "similar text," but actually understand and trace relationships (e.g., "Agent A is connected to Skill B which modifies Database C"). This transitions the memory system to GraphRAG, the bleeding edge of AI context retrieval.

## [ ] EN-05: Multi-Agent Swarms
Hermes is currently designed as a single, powerful agent per tenant sandbox.
- **The Enhancement:** Upgrade the `AgentManager` to support "Agent Swarms." 
- **Impact:** Allows a tenant to spin up a "Researcher Agent", a "Coder Agent", and a "Reviewer Agent" that dynamically communicate with each other in the background to solve complex, multi-step tasks before delivering the final validated answer to the user.
