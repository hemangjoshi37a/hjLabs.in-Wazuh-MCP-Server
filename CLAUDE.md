# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Wazuh MCP Server v2.1.2** - a production-ready FastMCP server that integrates Wazuh SIEM with Claude Desktop for AI-powered security operations. It uses STDIO transport for secure local connections and provides 29 security tools for comprehensive threat analysis, vulnerability management, and compliance monitoring.

## Architecture

The codebase follows a layered architecture:

```
src/wazuh_mcp_server/
├── api/                    # Wazuh API clients (Server API & Indexer API)
├── features/tools/         # 29 MCP tools organized by category
├── services/               # Core services (server, analyzers, prompt enhancement)
├── utils/                  # Utilities (logging, validation, SSL, error handling)
├── config.py              # Configuration management
├── main.py               # Entry point with graceful fallbacks
└── models.py             # Shared data models
```

### Key Components

- **Dual API Architecture**: Intelligent routing between Wazuh Server API (port 55000) and Wazuh Indexer API (port 9200) based on Wazuh version (4.8.0+ uses Indexer for alerts/vulnerabilities)
- **Tool Categories**: Alerts (4), Agents (6), Vulnerabilities (3), Security Analysis (6), System Monitoring (10)
- **Fallback Design**: The server can operate in degraded mode when FastMCP is unavailable (see main.py:26-46)
- **Production Ready**: Comprehensive error handling, rate limiting, SSL configuration, and health checks

## Development Commands

### Installation & Setup
```bash
# Development installation
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"

# Copy and configure environment
cp .env.example .env
# Edit .env with your Wazuh server details
```

### Testing
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test suites
pytest tests/unit/           # Unit tests
pytest tests/integration/    # Integration tests
pytest tests/phase5/         # Advanced integration tests

# Individual test files for tools
pytest tests/test_get_alerts.py
pytest tests/test_vulnerability_summary.py
```

### Code Quality
```bash
# Format code (Black)
black src/ tests/

# Lint code (Ruff)
ruff check src/ tests/

# Type checking (MyPy)
mypy src/

# Run all quality checks
black src/ tests/ && ruff check src/ tests/ && mypy src/
```

### Validation & Health Checks
```bash
# Validate configuration and connectivity
wazuh-mcp-server --check

# Test connection to Wazuh
python test_connection.py

# Run comprehensive health validation
python validate_server_health.py

# Test MCP integration
python test_mcp_integration.py
```

### Running the Server
```bash
# Start MCP server (production)
wazuh-mcp-server

# Development mode with debug logging
DEBUG=true wazuh-mcp-server

# Show version
wazuh-mcp-server --version
```

## Configuration Essentials

### Environment Variables (.env)
The server requires these critical environment variables:

```bash
# Wazuh Server API (Required)
WAZUH_HOST=your-wazuh-server.com
WAZUH_PORT=55000
WAZUH_USER=your-api-username
WAZUH_PASS=your-secure-password

# Wazuh Indexer (Required for 4.8.0+)
WAZUH_INDEXER_HOST=your-wazuh-server.com
WAZUH_INDEXER_PORT=9200
WAZUH_INDEXER_USER=your-indexer-username
WAZUH_INDEXER_PASS=your-indexer-password

# SSL Configuration (Production defaults)
VERIFY_SSL=true
WAZUH_ALLOW_SELF_SIGNED=true
```

### Version Detection
The server automatically detects Wazuh version and routes API calls appropriately:
- Wazuh 4.7.x and below: Uses Server API for all operations
- Wazuh 4.8.0+: Uses Indexer API for alerts and vulnerabilities, Server API for agents/cluster

## Working with Tools

### Tool Structure
Each tool in `src/wazuh_mcp_server/features/tools/` follows this pattern:
- Inherits from `BaseTool` (base.py)
- Uses `@tool` decorator from FastMCP
- Implements proper error handling and validation
- Returns structured data using models from `models.py`

### Adding New Tools
1. Create tool function in appropriate category file (alerts.py, agents.py, etc.)
2. Use proper type hints and docstrings
3. Add comprehensive error handling
4. Register in `factory.py` if needed
5. Add tests in `tests/test_[tool_name].py`

## Error Handling Strategy

The codebase uses multi-layered error handling:
1. **Tool Level**: Individual tools handle API-specific errors
2. **Client Level**: `wazuh_client.py` and `wazuh_indexer_client.py` handle connection issues
3. **Server Level**: `production_error_handler.py` provides centralized error standardization
4. **Graceful Degradation**: Server continues operating even when some components fail

## SSL & Security

The server defaults to secure SSL configuration:
- `VERIFY_SSL=true` by default
- Supports self-signed certificates via `WAZUH_ALLOW_SELF_SIGNED=true`
- Implements certificate validation and custom CA support
- Uses secure credential handling with environment variables

## Claude Desktop Integration

Add to Claude Desktop config (`~/.config/claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "wazuh": {
      "command": "python",
      "args": ["/path/to/src/wazuh_mcp_server/main.py"],
      "env": {"PYTHONPATH": "/path/to/src"},
      "cwd": "/path/to/project"
    }
  }
}
```

## Key Development Notes

- **Backward Compatibility**: Code maintains compatibility with Python 3.9+ and Wazuh 4.7+
- **Optional Dependencies**: FastMCP is optional - server provides fallback stubs for testing
- **Cross-Platform**: Uses `platform_utils.py` for cross-platform file operations
- **Rate Limiting**: Built-in rate limiting via `rate_limiter.py`
- **Health Monitoring**: Comprehensive health checks in `utils/health_checks.py`

## Common Tasks

- **Add new security analysis**: Extend `services/analyzers/security_analyzer.py`
- **Add compliance framework**: Extend `services/analyzers/compliance_analyzer.py`
- **Add new API endpoint**: Create tool in appropriate `features/tools/` file
- **Modify SSL behavior**: Update `utils/ssl_config.py`
- **Add caching**: Extend `services/prompt_enhancement/cache.py`