from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Tool:
    """
    Minimal MCP types.Tool fallback used when the 'mcp' package is not installed.

    This class mirrors the basic shape used across the codebase:
      - name: tool name
      - description: human-readable description
      - inputSchema: JSON schema for tool arguments
    """
    name: str
    description: str = ""
    inputSchema: Optional[Dict[str, Any]] = None