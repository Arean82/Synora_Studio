# SaaS Portal: Public API Specification

The Web Portal exposes several HTTP endpoints strictly for account and session management. 
*(For AI Inference endpoints, see `/server/docs/API_SERVER.md`)*

## `POST /auth/register`
Creates a new isolated tenant profile in `tenant_db.sqlite`.

## `POST /auth/login`
Validates credentials using `Argon2id` and returns a secure JWT containing the user's `tenant_id`.

## `POST /tenant/keys/update`
Receives an API key, encrypts it securely, and stores it in the tenant's isolated settings table. This key is forwarded to the API server during inference.
