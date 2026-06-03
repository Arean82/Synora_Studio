# Synora Studio: Planned Enhancements & Future Roadmap

This document outlines the strategic high-impact architectural and feature enhancements proposed for future versions of Synora Studio (v1.1+).

## Enhancement Tracker

| ID | Enhancement Title | Status |
|:---|:---|:---|
| **EN-01** | Real-Time WebSockets (Socket.IO) for Hermes | 🟢 Deployed |
| **EN-02** | Full Dockerization & Kubernetes Helm Charts | 🟡 Pending |
| **EN-03** | Agentic "Tool Calling" UI (Native Function Calling) | 🟢 Deployed |
| **EN-04** | Advanced GraphRAG (Knowledge Graphs) | 🟢 Deployed |
| **EN-05** | Multi-Agent Swarms | 🟢 Deployed |

---

## 🟢 EN-01: Real-Time WebSockets (Socket.IO) for Hermes
- **Current State:** The Hermes Agent console relies heavily on polling or file-watching to monitor agent activity.
- **The Enhancement:** Implement `Flask-SocketIO` to push live, sub-millisecond agent reasoning logs directly from the detached background `hermes_runner.py` to the PySide6 UI and the Web SaaS Portal. 
- **How it differs from current:** It pushes data over a persistent WebSocket connection instead of the client repeatedly requesting updates (polling).
- **Impact:** Creates a highly responsive, real-time "matrix code" effect as the agent thinks, completely eliminating polling overhead.

## [ ] EN-02: Full Dockerization & Kubernetes Helm Charts
- **Current State:** Deployment relies on running scripts locally or launching the PySide6 executable without full containerization modularity.
- **The Enhancement:** Create a comprehensive `docker-compose.yml` to fully containerize the SaaS Portal, the API server, and the Qdrant Vector database. 
- **How it differs from current:** Components will be isolated in Docker containers rather than running directly on the host machine OS, allowing for orchestrated deployments.
- **Impact:** Allows enterprise users to instantly spin up Synora Studio on AWS or Google Cloud with zero dependency issues, completely decoupled from the local PySide6 Desktop executable.

## 🟢 EN-03: Agentic "Tool Calling" UI (Native Function Calling)
- **Current State:** The backend supports external tools via Hermes, but the main chat UI is strictly text and Markdown-based.
- **The Enhancement:** Parse native LLM "Tool Call" JSON payloads (e.g., OpenAI's native function calling format) and render beautiful, interactive widgets in the PySide6 UI when a tool is called. 
- **How it differs from current:** Tool execution will be visualized with native GUI widgets and spinners rather than just plain text logs in the chat.
- **Impact:** If the AI calls `search_web()`, the chat will render a sleek loading spinner widget labeled *"Searching the web..."* before injecting the result, vastly improving user trust and experience.
- **Technical Challenges & Mitigations:**
  - *Malformed JSON:* LLMs may hallucinate schemas or generate invalid JSON. **Fix:** Use Structured Outputs/Strict Mode from modern APIs, and implement recursive fallback loops to allow the LLM to auto-correct JSON syntax errors.
  - *Streaming Partial JSON:* Parsing token-by-token breaks standard JSON loaders. **Fix:** Implement a background token buffer or use a Streaming JSON parser to safely read incomplete JSON blocks on the fly before rendering the UI widgets.
  - *Mixed Content:* LLMs often mix conversational text with JSON. **Fix:** Rely on explicit API tool-call metadata (e.g., `finish_reason="tool_calls"`) instead of basic regex to extract the payload.

## 🟢 EN-04: Advanced GraphRAG (Knowledge Graphs)
- **Current State:** Synora Studio leverages Qdrant for semantic Dense Vector retrieval (finding chunks of text with similar meaning).
- **The Enhancement:** Integrate a Knowledge Graph (like Neo4j or NetworkX) alongside Qdrant. 
- **How it differs from current:** Adds structured relational tracing (nodes and edges) to the memory system instead of relying purely on vector distance searches.
- **Impact:** Allows the AI to not just find "similar text," but actually understand and trace relationships (e.g., "Agent A is connected to Skill B which modifies Database C"). This transitions the memory system to GraphRAG, the bleeding edge of AI context retrieval.

## 🟢 EN-05: Multi-Agent Swarms
- **Current State:** Hermes is designed as a single, powerful agent per tenant sandbox.
- **The Enhancement:** Upgrade the `AgentManager` to support "Agent Swarms." 
- **How it differs from current:** Multiple specialized agents will interact and collaborate with each other autonomously, rather than having just one agent doing all the work.
- **Impact:** Allows a tenant to spin up a "Researcher Agent", a "Coder Agent", and a "Reviewer Agent" that dynamically communicate with each other in the background to solve complex, multi-step tasks before delivering the final validated answer to the user.
