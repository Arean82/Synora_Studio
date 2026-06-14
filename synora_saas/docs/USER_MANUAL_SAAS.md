# Synora SaaS Web Portal: User Manual

Welcome to the **Synora Web Portal**. This web dashboard provides a robust, multi-tenant interface that connects remote users to your centralized API server.

## 🚀 Getting Started

**Step 1:** Ensure the API Server is running in the background. The Web Portal has no built-in AI logic; it simply forwards your requests to the server.

**Step 2:** Open your web browser and navigate to `http://localhost:8080`.

**Step 3:** Register a new user account. 
*Note: Because Synora uses isolated tenant databases, you cannot log in with the Desktop GUI's internal credentials. You must create a dedicated Web SaaS account.*

## 💳 Bring Your Own Key (BYOK)

To keep server operations decoupled and secure, the Synora Web Portal uses a BYOK architecture. This means the server administrator does not pay for your AI API usage. 

1. Click on the **Settings** gear icon in the bottom-left corner.
2. Select **API Keys**.
3. Enter your OpenAI, Gemini, Anthropic, or Groq API keys.
4. These keys are heavily encrypted in your isolated `tenant_db.sqlite` profile and are passed securely to the API Server during inference.

## 📁 RAG Documents & Cloud Storage

When you upload a document in the chat interface:
1. The web portal securely transmits the file to the API Server.
2. The server parses the text, generates vector embeddings, and stores them in your tenant's dedicated Qdrant collection.
3. Your documents remain strictly isolated from other tenants on the SaaS platform.
