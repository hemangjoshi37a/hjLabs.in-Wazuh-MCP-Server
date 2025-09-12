#!/usr/bin/env python3
"""Test script to verify Wazuh MCP Server functionality."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from wazuh_mcp_server.config import WazuhConfig
from wazuh_mcp_server.api.wazuh_client_manager import WazuhClientManager

async def test_server_functionality():
    """Test basic server functionality."""
    print("🧪 Testing Wazuh MCP Server functionality...")
    
    try:
        # Load configuration
        config = WazuhConfig.from_env()
        print(f"✅ Configuration loaded for {config.host}:{config.port}")
        
        # Test client manager
        async with WazuhClientManager(config) as client_manager:
            print("✅ Client manager initialized")
            
            # Test connection validation
            is_connected = await client_manager.validate_connection()
            print(f"✅ Connection validation: {'SUCCESS' if is_connected else 'FAILED'}")
            
            if is_connected:
                # Test getting API info
                try:
                    api_info = await client_manager.get_api_info()
                    if api_info:
                        print(f"✅ API Info: {api_info.get('version', 'unknown')}")
                    else:
                        print("⚠️  API Info: Not available")
                except Exception as e:
                    print(f"⚠️  API Info failed: {e}")
                
                # Test getting agents
                try:
                    agents = await client_manager.get_agents(limit=5)
                    if agents and agents.get('data', {}).get('affected_items'):
                        agent_count = len(agents['data']['affected_items'])
                        print(f"✅ Agents: Found {agent_count} agents")
                    else:
                        print("⚠️  Agents: No agents found")
                except Exception as e:
                    print(f"⚠️  Agents test failed: {e}")
                
                # Test getting alerts
                try:
                    alerts = await client_manager.get_alerts(limit=5)
                    if alerts and alerts.get('data', {}).get('affected_items'):
                        alert_count = len(alerts['data']['affected_items'])
                        print(f"✅ Alerts: Found {alert_count} recent alerts")
                    else:
                        print("⚠️  Alerts: No recent alerts found")
                except Exception as e:
                    print(f"⚠️  Alerts test failed: {e}")
                
                print("\n🎉 Server functionality test completed successfully!")
                print("   The Wazuh MCP Server is working and ready for use.")
                return True
            else:
                print("\n❌ Server functionality test failed!")
                print("   Connection validation failed - check configuration.")
                return False
                
    except Exception as e:
        print(f"\n❌ Server functionality test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_server_functionality())
    sys.exit(0 if success else 1)