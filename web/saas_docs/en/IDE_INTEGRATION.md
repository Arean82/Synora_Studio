# SaaS Portal: IDE Integration

If you use VS Code or JetBrains IDEs, you can connect your code editor directly to your SaaS Portal account using our official extensions.

## Setup
1. Install the `Synora Coder` extension from your IDE's marketplace.
2. In the extension settings, point the `Base URL` to your SaaS Portal's domain (e.g., `https://synora.yourcompany.com`).
3. Click "Login" in the IDE. Your browser will open the SaaS Portal to authenticate via OAuth.
4. Once authenticated, your IDE will route its completion requests through the Web Portal, which in turn securely streams the response from the central API Server using your BYOK credentials.
