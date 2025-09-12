#!/usr/bin/env python3.13
"""Test Wazuh MCP Server connection."""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from wazuh_mcp_server.config import WazuhConfig
    from wazuh_mcp_server.client import WazuhClient
    import asyncio
    import aiohttp

    async def test_connection():
        try:
            # Load configuration
            config = WazuhConfig.from_env()
            print(f"✅ Configuration loaded successfully")
            print(f"   Host: {config.host}")
            print(f"   Port: {config.port}")
            print(f"   Username: {config.username}")
            print(f"   SSL Verification: {config.verify_ssl}")

            # Test API connection
            client = WazuhClient(config)

            # Test authentication
            print(f"\n🔐 Testing authentication...")
            token = await client.authenticate()
            if token:
                print(f"✅ Authentication successful!")
                print(f"   Token: {token[:20]}...")

                # Test a basic API call
                print(f"\n📊 Testing basic API call...")
                try:
                    agents = await client.get_agents(limit=1)
                    print(f"✅ API call successful! Found {len(agents)} agents")
                except Exception as e:
                    print(f"⚠️ API call failed but auth worked: {e}")

            else:
                print(f"❌ Authentication failed")
                return False

        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            if 'client' in locals():
                await client.close()

        return True

    # Run the test
    if __name__ == "__main__":
        result = asyncio.run(test_connection())
        sys.exit(0 if result else 1)

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure wazuh-mcp-server is installed correctly")
    sys.exit(1)
