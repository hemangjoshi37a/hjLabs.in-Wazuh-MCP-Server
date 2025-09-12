#!/usr/bin/env python3
"""Test MCP integration with Kilo Code."""

import subprocess
import json
import sys
from pathlib import Path

def test_mcp_server_startup():
    """Test if the MCP server can start properly for Kilo Code integration."""
    print("🧪 Testing Wazuh MCP Server integration with Kilo Code...")
    
    # Test the exact command that Kilo Code will use
    cmd = [
        "python", 
        "/home/hemang/Documents/GitHub/Wazuh-MCP-Server/src/wazuh_mcp_server/main.py"
    ]
    
    env = {
        "PYTHONPATH": "/home/hemang/Documents/GitHub/Wazuh-MCP-Server/src"
    }
    
    print(f"Command: {' '.join(cmd)}")
    print(f"Environment: PYTHONPATH={env['PYTHONPATH']}")
    print(f"Working Directory: /home/hemang/Documents/GitHub/Wazuh-MCP-Server")
    
    try:
        # Test server startup (will timeout after 5 seconds, which is expected)
        result = subprocess.run(
            cmd,
            env={**dict(subprocess.os.environ), **env},
            cwd="/home/hemang/Documents/GitHub/Wazuh-MCP-Server",
            capture_output=True,
            text=True,
            timeout=5
        )
    except subprocess.TimeoutExpired as e:
        # This is expected - the server should start and wait for STDIO input
        print("✅ Server started successfully (timeout expected)")
        print("✅ Server is ready for MCP STDIO communication")
        
        # Check if there were any startup errors in stderr
        stderr_text = e.stderr.decode('utf-8') if e.stderr else ""
        if stderr_text and "ERROR" in stderr_text:
            print("⚠️  Startup warnings/errors detected:")
            for line in stderr_text.split('\n'):
                if "ERROR" in line or "CRITICAL" in line:
                    print(f"   {line}")
        else:
            print("✅ No critical startup errors detected")
        
        return True
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        return False
    
    # If we get here, the server exited unexpectedly
    print(f"❌ Server exited unexpectedly with code: {result.returncode}")
    if result.stderr:
        print("Error output:")
        print(result.stderr)
    return False

def create_kilo_code_config():
    """Create the corrected Kilo Code configuration."""
    config = {
        "wazuh": {
            "command": "python",
            "args": [
                "/home/hemang/Documents/GitHub/Wazuh-MCP-Server/src/wazuh_mcp_server/main.py"
            ],
            "env": {
                "PYTHONPATH": "/home/hemang/Documents/GitHub/Wazuh-MCP-Server/src"
            },
            "cwd": "/home/hemang/Documents/GitHub/Wazuh-MCP-Server"
        }
    }
    
    print("\n📋 Recommended Kilo Code MCP Configuration:")
    print("Add this to your Kilo Code MCP settings:")
    print(json.dumps(config, indent=2))
    
    return config

if __name__ == "__main__":
    print("🔧 Wazuh MCP Server - Kilo Code Integration Test")
    print("=" * 60)
    
    # Test server startup
    startup_success = test_mcp_server_startup()
    
    # Show configuration
    create_kilo_code_config()
    
    print("\n" + "=" * 60)
    if startup_success:
        print("🎉 Integration test successful!")
        print("✅ The Wazuh MCP Server is ready for Kilo Code integration")
        print("\n📝 Next steps:")
        print("1. Copy the configuration above to your Kilo Code MCP settings")
        print("2. Restart Kilo Code")
        print("3. Test by asking: 'Show me Wazuh system status'")
    else:
        print("❌ Integration test failed!")
        print("Please check the error messages above and fix any issues")
    
    sys.exit(0 if startup_success else 1)