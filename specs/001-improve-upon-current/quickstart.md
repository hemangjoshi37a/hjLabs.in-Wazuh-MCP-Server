# Quickstart: Wazuh MCP Server

This guide provides a quick way to get started with the Wazuh MCP Server.

## Prerequisites

- Python >= 3.9
- A running Wazuh manager instance

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/gensecaihq/Wazuh-MCP-Server.git
    cd Wazuh-MCP-Server
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  Create a `.env` file from the example:
    ```bash
    cp .env.example .env
    ```

2.  Edit the `.env` file with your Wazuh API credentials and other settings.

## Running the server

```bash
python src/wazuh_mcp_server/main.py
```

## Testing

To run the test suite:

```bash
pytest
```
