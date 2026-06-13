# Synora Studio: Planned Enhancements & Future Roadmap

This document outlines the strategic high-impact architectural and feature enhancements proposed for future versions of Synora Studio (v1.1+).

## Enhancement Tracker

| ID                                                               | Enhancement Title                                   | Status                   |
| :--------------------------------------------------------------- | :-------------------------------------------------- | :----------------------- |
| **[EN-01](#-en-01-real-time-websockets-socketio-for-hermes)** | Real-Time WebSockets (Socket.IO) for Hermes         | 🟢 Deployed              |
| **[EN-02](#-en-02-full-dockerization--kubernetes-helm-charts)**                                                  | Full Dockerization & Kubernetes Helm Charts         | 🔵 On Hold / Rejected    |
| **[EN-03](#-en-03-agentic-tool-calling-ui-native-function-calling)**                                                  | Agentic "Tool Calling" UI (Native Function Calling) | 🟢 Deployed              |
| **[EN-04](#-en-04-advanced-graphrag-knowledge-graphs)**                                                  | Advanced GraphRAG (Knowledge Graphs)                | 🟢 Deployed              |
| **[EN-05](#-en-05-multi-agent-swarms)**                                                  | Multi-Agent Swarms                                  | 🟢 Deployed              |
| **[EN-06](#-en-06-flask-route-refactoring--security-decorators)**                                                 | Flask Route Refactoring & Security Decorators       | 🟢 Deployed               |
| **[EN-07](#-en-07-automated-testing-suite-pytest-ci)**                                                  | Automated Testing Suite (PyTest/CI)                 | 🔵 On Hold               |
| **[EN-08](#-en-08-exception-handling--observability-hardening)**                                                  | Exception Handling & Observability Hardening        | 🟢 Deployed              |
| **[EN-09](#-en-09-tool-calling-engine-refactoring)**                                                  | Tool Calling Engine Refactoring                     | 🟢 Deployed              |
| **[EN-10](#-en-10-asynchronous-disk-io-ui-pipeline)**                                                  | Asynchronous Disk I/O UI Pipeline                   | 🟢 Deployed              |
| **[EN-11](#-en-11-thread-safe-turso-libsql-connection-pooling)**                                                  | Thread-Safe Turso/libSQL Connection Pooling         | 🟢 Deployed              |
| **[EN-12](#-en-12-cryptographic-migration-bcryptargon2)**                                                  | Cryptographic Migration (bcrypt/argon2)             | 🟢 Deployed              |
| **[EN-13](#-en-13-sql-injection-remediation-parameterized-queries)**                                                  | SQL Injection Remediation (Parameterized Queries)   | 🟢 False Positive (Safe) |
| **[EN-14](#-en-14-hardcoded-backdoor-removal)**                                                  | Hardcoded Backdoor Removal                          | 🟢 Deployed              |

---

## 🟢 EN-01: Real-Time WebSockets (Socket.IO) for Hermes

- **Current State:** The Hermes Agent console relies heavily on polling or file-watching to monitor agent activity.
- **The Enhancement:** Implement `Flask-SocketIO` to push live, sub-millisecond agent reasoning logs directly from the detached background `hermes_runner.py` to the PySide6 UI and the Web SaaS Portal.
- **How it differs from current:** It pushes data over a persistent WebSocket connection instead of the client repeatedly requesting updates (polling).
- **Impact:** Creates a highly responsive, real-time "matrix code" effect as the agent thinks, completely eliminating polling overhead.

## 🔵 EN-02: Full Dockerization & Kubernetes Helm Charts

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

## 🟢 EN-06: Flask Route Refactoring & Security Decorators

- **Current State:** In `web/app.py`, nearly every administrative endpoint duplicates a large 11-line `try...except` authorization block (e.g., checking `security_svc.check_permission(user, "admin")`).
- **The Enhancement:** Introduce a centralized `@admin_required` Flask route decorator to encapsulate Role-Based Access Control (RBAC) and security audit logging.
- **How it differs from current:** Removes boilerplate copy-paste code from endpoints, ensuring DRY (Don't Repeat Yourself) principles are met.
- **Impact:** Minimizes the risk of authorization bypass vulnerabilities due to copy-paste errors and massively reduces codebase bloat.

## 🔵 EN-07: Automated Testing Suite (PyTest/CI)

- **Current State:** The repository lacks a `tests/` directory and automated test coverage.
- **The Enhancement:** Implement a robust test suite covering core components (storage drivers, API routes, and RAG retrieval) using `pytest`.
- **How it differs from current:** Relies on automated CI checks rather than manual testing.
- **Impact:** Prevents regressions when migrating between local and SaaS architectures and establishes a strong baseline for enterprise stability.

## 🟢 EN-08: Exception Handling & Observability Hardening

- **Current State:** Widespread use of broad, silent `except Exception:` blocks across critical database drivers (e.g., `mysql_tenant_driver.py`) and standard web routes.
- **The Enhancement:** Refactor broad exception handlers to catch specific exceptions (e.g., `SQLAlchemyError`, `KeyError`) or log the complete exception stack trace using `logging.error(e, exc_info=True)`.
- **How it differs from current:** Exceptions are no longer swallowed silently, allowing telemetry services to capture actual root causes.
- **Impact:** Prevents silent failures, eases debugging of backend logic, and greatly improves system observability and reliability.

## 🟢 EN-09: Tool Calling Engine Refactoring

- **Current State:** The "Agentic Tool Calling" feature is structurally a facade. When the LLM calls a tool, `chat_worker.py` catches it but replies with a hardcoded mock string (`"Local search results for query... Found related classes..."`) instead of executing real logic.
- **The Enhancement:** Implement real dynamic tool routing (e.g., executing actual DuckDuckGo/Tavily web searches, or triggering real RAG codebase queries).
- **How it differs from current:** The application will actually fetch live external data rather than pretending it did.
- **Impact:** Makes the tool-calling feature actually functional and reliable for end-users.

## 🟢 EN-10: Asynchronous Disk I/O UI Pipeline

- **Current State:** `desktop/ui/chat_view.py` uses a synchronous `ingest_folder` function to crawl and read hundreds of files sequentially on the main PySide6 UI thread.
- **The Enhancement:** Offload all heavy disk operations (folder crawling, file reading) to a dedicated `QThread` (e.g., `IngestionWorker`).
- **How it differs from current:** File ingestion will happen in the background while displaying a progress bar, rather than locking the UI.
- **Impact:** Eliminates severe application freezes (ANR crashes) when users drag-and-drop large repositories into the chat view.

## 🟢 EN-11: Thread-Safe Turso/libSQL Connection Pooling

- **Current State:** `TenantDatabaseManager` was a Singleton instantiated on the main UI thread, but it is routinely queried from background `QThread`s (like `ChatWorker` checking semantic cache). Because Turso uses local libSQL/SQLite drivers under the hood, this violated the strict single-thread constraint and triggered silent background crashes.
- **The Enhancement:** Removed the global singleton pattern for DB connections. Used `threading.local()` to ensure every thread maintains its own isolated database connection.
- **How it differs from current:** Threads now generate or borrow their own isolated DB connections rather than fighting over a single locked Turso file pointer.
- **Impact:** Restores functional Semantic Caching and completely prevents random background thread crashes.

## 🟢 EN-12: Cryptographic Migration (bcrypt/argon2)

- **Current State:** User passwords in `tenant_db.py` are hashed using a single round of SHA-256 with a static, hardcoded global salt (`SaaS_Passport_Salt_v7_`).
- **The Enhancement:** Migrate to industry-standard cryptographic hashers like `bcrypt` or `argon2`, utilizing securely generated per-user random salts.
- **How it differs from current:** Hashing will become intentionally slow and computationally expensive.
- **Impact:** Closes a major security vulnerability, preventing rapid brute-force dictionary attacks if the `users` table is ever compromised.

## 🟢 EN-13: SQL Injection Remediation (Parameterized Queries) [FALSE POSITIVE]

- **Current State:** A broad AST static analysis initially flagged dynamic SQL construction in `update_user_profile` as a vulnerability due to the presence of `f-strings` and `.join()`.
- **The Enhancement:** None required.
- **How it differs from current:** A deeper semantic manual trace confirmed that the variables being joined (the SQL column names) are strictly hardcoded string literals inside `if` statements (e.g. `updates.append("username = ?")`). The actual user-controlled payload values are properly passed as secure, database-native parameterized bindings (`?` or `%s`).
- **Impact:** The database driver logic is structurally safe from injection attacks. This tracker remains closed as a proven false positive.

## 🟢 EN-14: Hardcoded Backdoor Removal

- **Current State:** The system previously contained hardcoded credentials (`api_key = 'admin_master_passport'`, `password = "admin"`) injected dynamically in the database tenant drivers.
- **The Enhancement:** Removed all static backdoor passwords. The initialization (`init_db`) and reset functions now dynamically generate cryptographically secure, high-entropy tokens via Python's `secrets.token_urlsafe()` module, which are printed securely to the terminal one time.
- **How it differs from current:** Administrators do not have a universal hardcoded backdoor string. The system generates unique, randomized keys on first boot or emergency reset.
- **Impact:** Prevents total unauthorized system takeover in the event the codebase is leaked or reverse-engineered.
