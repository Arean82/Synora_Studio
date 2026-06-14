# SaaS Portal: Security & Privacy

Synora takes multi-tenant isolation extremely seriously. 

## 1. Database Isolation
Every tenant is assigned a unique `tenant_id`. Chat logs, metadata, and user settings are strictly segmented. The API Server acts statelessly, only accessing data explicitly authorized by the active session token.

## 2. API Key Encryption (BYOK)
When you submit an API key to the portal:
- The key is immediately encrypted using `Argon2id` salts before touching the hard drive.
- The web portal does NOT use the key itself. It passes the encrypted payload securely to the API Server during inference.
- The platform administrators CANNOT view your plaintext API key.

## 3. Ephemeral Vector Storage
While document embeddings are stored in Qdrant, they are mathematically partitioned into tenant-specific Collections. No semantic search query can cross the boundaries of a tenant's collection.
