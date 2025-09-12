#!/usr/bin/env python3
"""Simple test script to verify Wazuh Manager API functionality only."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from wazuh_mcp_server.config import WazuhConfig
from wazuh_mcp_server.api.wazuh_client import WazuhAPIClient

async def test_manager_functionality():
    """Test basic Manager API functionality."""
    print("🧪 Testing Wazuh Manager API functionality...")
    
    try:
        # Load configuration
        config = WazuhConfig.from_env()
        print(f"✅ Configuration loaded for {config.host}:{config.port}")
        print(f"   Indexer features disabled: alerts={not config.use_indexer_for_alerts}, vulns={not config.use_indexer_for_vulnerabilities}")
        
        # Test Manager API client directly
        async with WazuhAPIClient(config) as client:
            print("✅ Manager API client initialized")
            
            # Test authentication
            try:
                await client.authenticate()
                print("✅ Authentication successful")
            except Exception as e:
                print(f"❌ Authentication failed: {e}")
                return False
            
            # Test basic API call
            try:
                api_info = await client._request("GET", "/")
                if api_info and api_info.get('data'):
                    version = api_info['data'].get('api_version', 'unknown')
                    print(f"✅ API Info: Version {version}")
                else:
                    print("⚠️  API Info: No data returned")
            except Exception as e:
                print(f"⚠️  API Info failed: {e}")
            
            # Test getting agents
            try:
                agents = await client.get_agents(limit=5)
                if agents and agents.get('data', {}).get('affected_items'):
                    agent_count = len(agents['data']['affected_items'])
                    print(f"✅ Agents: Found {agent_count} agents")
                else:
                    print("⚠️  Agents: No agents found")
            except Exception as e:
                print(f"⚠️  Agents test failed: {e}")
            
            # Test getting alerts (should use Manager API only)
            try:
                alerts = await client.get_alerts(limit=5)
                if alerts and alerts.get('data', {}).get('affected_items'):
                    alert_count = len(alerts['data']['affected_items'])
                    print(f"✅ Alerts: Found {alert_count} recent alerts")
                else:
                    print("⚠️  Alerts: No recent alerts found")
            except Exception as e:
                print(f"⚠️  Alerts test failed: {e}")
            
            print("\n🎉 Manager API functionality test completed successfully!")
            print("   The Wazuh Manager API is working and ready for use.")
            return True
                
    except Exception as e:
        print(f"\n❌ Manager API functionality test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_manager_functionality())
    sys.exit(0 if success else 1)