# Companion Operation Toolkit (`/companion_operation`)

The Companion Operation Toolkit is an administration utility designed strictly for DevOps and System Administrators managing the Synora ecosystem. 

Because Synora is highly modular, administrative tasks require a dedicated tool that can safely interface with the core PostgreSQL backend without disrupting active Server/Web runtime memory.

## 🚀 Quick Setup
Please refer to the [INSTALLATION.md](INSTALLATION.md) for how to securely boot the toolkit.

## 🏗️ Core Responsibilities

1. **Demo User Injection:** Instantly provisions fully-featured demonstration accounts for SaaS testing.
2. **Global SSH Tunnel Piggybacking:** Establishes secure reverse-tunnels for remote administration.
3. **Service Management:** Generates and installs `systemd` scripts for deploying the API Server and Web Portal in headless Linux environments.
4. **Backups:** Triggers instantaneous snapshots of PostgreSQL databases.

## 🛑 Danger Zone

Tools located in this repository have the capability to permanently erase user data, perform factory resets, and override cryptographic locks. **Do not deploy this module to end-user machines.**
