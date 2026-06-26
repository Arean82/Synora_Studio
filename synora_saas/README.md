# Synora Web Portal (`/web`)

The Web Portal is the standalone, multi-tenant SaaS frontend for the Synora Studio ecosystem. It relies on the API Server backend for intelligence, allowing the Web UI to remain entirely focused on user management and billing.

## 🚀 Quick Setup
Please refer to the detailed [INSTALLATION.md](INSTALLATION.md) for step-by-step instructions on how to install and boot the web portal for local development.

## 🏗️ Core Responsibilities

1. **Multi-Tenant Administration:** Handles user registration, JWT-based session management, and role-based access control (RBAC).
2. **BYOK Management (Bring Your Own Key):** Allows individual tenants to securely upload and encrypt their own OpenAI/Google API keys, which are passed off to the Server module securely.
3. **Usage Accounting:** Tracks token consumption and session telemetry per user.
4. **Decoupled Connectivity:** The web portal does not process AI models or RAG chunking locally. It forwards all requests to the central API Server over `REST` and `Socket.IO`.

## 🔗 Auto-Login via URL
External applications or links can automatically authenticate a user into the SaaS workspace by appending a valid JWT token to the URL query string:
`http://localhost:8888/?token=YOUR_JWT_TOKEN`
The frontend will seamlessly intercept this token, validate it, establish a secure session, and drop the user directly into the active dashboard.

## 📚 Advanced Documentation

- [USER_MANUAL_SAAS.md](docs/USER_MANUAL_SAAS.md) - End-user guide for operating the web dashboard.
- [SAAS_STORAGE_ARCHITECTURE_PLAN.md](docs/SAAS_STORAGE_ARCHITECTURE_PLAN.md) - Deep dive into how tenant databases are isolated and synced.
