# Data Model: Wazuh MCP Server

## Key Entities

### 1. Wazuh Agent
- **Description**: Represents a monitored endpoint in the Wazuh environment.
- **Fields**:
    - `id`: string (unique identifier)
    - `name`: string
    - `ip_address`: string
    - `status`: string (e.g., 'active', 'disconnected', 'never_connected')
    - `os`: string (e.g., 'Linux', 'Windows', 'macOS')
    - `version`: string (Wazuh agent version)

### 2. Wazuh Manager
- **Description**: Represents the central component of the Wazuh infrastructure.
- **Fields**:
    - `id`: string (unique identifier)
    - `hostname`: string
    - `ip_address`: string
    - `status`: string (e.g., 'running', 'stopped')
    - `version`: string (Wazuh manager version)

### 3. MCP Server
- **Description**: The server that this repository implements, which acts as a control plane for the Wazuh managers.
- **Fields**:
    - `id`: string (unique identifier)
    - `start_time`: datetime
    - `status`: string (e.g., 'running', 'degraded', 'stopped')
    - `version`: string (MCP Server version)
