# Synora API Server Reference

The Synora Server functions as the core intelligence engine. It sits on port `5000` and multiplexes connections from multiple tenants (via the Web Portal) and native local users (via the Desktop GUI).

## 🔌 Socket.IO Connections

The server uses persistent, bidrectional Socket.IO streams for low-latency chat streaming and RAG chunk status updates.

- **Endpoint:** `ws://localhost:5000/socket.io/`
- **Events (Listen):**
  - `stream_token`: Received when the LLM generates a partial token.
  - `rag_progress`: Received when the embedding service is indexing an attached document.
  - `error_fatal`: Received if the provider SDK drops the connection.
- **Events (Emit):**
  - `start_inference`: Trigger LLM generation. Requires payload: `{"prompt": "...", "provider": "...", "history": [...]}`
  - `cancel_inference`: Forces the server to drop the active stream and recover memory.

## 🌐 REST API Endpoints

The server exposes standard HTTP endpoints for synchronous, non-streaming operations.

### `POST /api/v1/auth/verify`
Verifies an incoming API key against a provider SDK (e.g., checks if an OpenAI key has billing enabled) before the Web Portal saves it to the tenant database.

### `POST /api/v1/rag/upload`
Accepts a binary file upload (`multipart/form-data`) and queues it for asynchronous parsing and embedding into the Vector DB.

### `GET /api/v1/telemetry/health`
Returns the status of the embedding queue, GPU VRAM usage, and active socket connections. Used by load balancers and system monitoring tools.