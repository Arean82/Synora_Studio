# SaaS Portal: Administrator Guide

As the administrator of the Synora Web Portal, your primary role is infrastructure management. 
Because the platform relies on the backend API Server for intelligence, the web portal is extremely lightweight.

## Admin Responsibilities
1. **User Moderation:** You have the ability to ban or suspend tenants from accessing the portal.
2. **Health Monitoring:** You must ensure that the `API Server` remains running on port `5000`. If the API server goes down, your tenants will receive a "Gateway Timeout" error.

*Note: You do NOT pay for your tenants' API usage. Tenants are required to supply their own BYOK credentials in their settings.*
