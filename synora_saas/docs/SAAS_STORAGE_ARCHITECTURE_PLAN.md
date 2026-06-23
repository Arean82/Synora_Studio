# SaaS Storage Architecture

The Synora Web Portal acts as a gateway for multiple tenants to access the backend API Server. To guarantee absolute data privacy between tenants, the ecosystem employs a strict isolation model.

## 🗄️ Relational Data (`synora_saas` PostgreSQL Database)

The Web Portal provisions a dedicated PostgreSQL database upon the first boot.
- **Tenant Isolation:** Users are tied to unique `tenant_id` UUIDs.
- **Data Encapsulation:** A user's Chat History, RAG Document Metadata, and API Keys are strictly segregated by their `tenant_id`.
- **Stateless Server:** The API Server itself holds NO relational state. When the Web Portal makes a request, it passes an authenticated JWT containing the `tenant_id`, which the server uses to temporarily retrieve the required data from the database.

## 🧠 Vector Data (`Qdrant` / `ChromaDB`)

RAG embeddings require a different isolation strategy due to the mechanics of high-dimensional vector search.

- **Collection Isolation:** Each tenant gets a dedicated "Collection" inside the central Qdrant instance.
- **Routing:** When a tenant uploads a document or asks a question, the API Server extracts their `tenant_id` from the JWT and automatically routes the embedding payload into their specific isolated collection.
- **Prevention of Data Bleed:** Because searches are constrained strictly at the collection level, it is mathematically impossible for a semantic search to retrieve a text chunk from a different tenant.
