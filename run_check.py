#!/usr/bin/env python3.13
"""Comprehensive Wazuh MCP Server Test."""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_wazuh_mcp():
    """Test the Wazuh MCP Server setup."""
    print("🧪 Comprehensive Wazuh MCP Server Test")
    print("=" * 45)
    
    # Test environment loading
    print("\n📋 Environment Check:")
    for var in ['WAZUH_HOST', 'WAZUH_USER', 'WAZUH_PASS', 'VERIFY_SSL']:
        value = os.getenv(var)
        if var.endswith('PASS'):
            print(f"  {var}: {'*' * len(value) if value else 'NOT SET'}")
        else:
            print(f"  {var}: {value}")
    
    # Test imports
    print("\n🔧 Testing imports...")
    try:
        from wazuh_mcp_server.config import WazuhConfig
        print("✅ WazuhConfig imported")
        
        from wazuh_mcp_server.client import WazuhClient
        print("✅ WazuhClient imported")
        
        config = WazuhConfig.from_env()
        print("✅ Configuration loaded")
        print(f"  - Host: {config.host}")
        print(f"  - Username: {config.username}")
        print(f"  - SSL Verify: {config.verify_ssl}")
        
    except Exception as e:
        print(f"❌ Import/Config error: {e}")
        return False
    
    # Test connection
    print("\n🌐 Testing connection...")
    try:
        async with WazuhClient(config) as client:
            print("🔐 Authenticating...")
            token = await client.authenticate()
            
            if token:
                print(f"✅ Authentication successful! Token: {token[:20]}...")
                
                print("🧪 Testing connection...")
                connection_ok = await client.test_connection()
                
                if connection_ok:
                    print("✅ Full connection test passed!")
                    
                    print("📊 Testing API calls...")
                    try:
                        agents = await client.get_agents(limit=1)
                        print(f"✅ Agents query: {len(agents)} agents")
                        
                        cluster = await client.get_cluster_status()
                        print(f"✅ Cluster status: {cluster.get('enabled', False)}")
                        
                    except Exception as e:
                        print(f"⚠️ Some API calls failed: {e}")
                    
                    return True
                else:
                    print("❌ Connection test failed")
            else:
                print("❌ Authentication failed")
                
    except Exception as e:
        print(f"❌ Connection error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return False

if __name__ == "__main__":
    try:
        result = asyncio.run(test_wazuh_mcp())
        print(f"\n🎯 Final Result: {'✅ SUCCESS' if result else '❌ FAILED'}")
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"❌ Test script error: {e}")
        sys.exit(1)
