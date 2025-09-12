#!/usr/bin/env python3.13
"""Simple test of Wazuh connection without client module."""

import aiohttp
import asyncio
import json
import ssl
import os
from dotenv import load_dotenv

load_dotenv()

async def test_wazuh_direct():
    """Test Wazuh connection directly without client module."""

    host = os.getenv('WAZUH_HOST', 'wazuh.gadgetaccess.com')
    user = os.getenv('WAZUH_USER', 'wazuh')
    password = os.getenv('WAZUH_PASS', 'wTNSUK9gF09XFVrW*PyiiAmj6oy?zVkR')

    # Create SSL context that ignores certificate errors
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    connector = aiohttp.TCPConnector(ssl=ssl_context)

    async with aiohttp.ClientSession(connector=connector) as session:
        # Test authentication
        auth_url = f"https://{host}:55000/security/user/authenticate"
        auth_data = {"user": user, "password": password}

        print(f"🔐 Testing authentication with {user}@{host}...")

        try:
            async with session.post(auth_url, json=auth_data, timeout=10) as resp:
                print(f"   Status: {resp.status}")
                response_text = await resp.text()
                print(f"   Response: {response_text[:200]}...")

                if resp.status == 200:
                    data = await resp.json()
                    token = data.get('data', {}).get('token')
                    if token:
                        print(f"✅ Authentication successful!")
                        print(f"   Token: {token[:30]}...")

                        # Test a simple API call
                        headers = {'Authorization': f'Bearer {token}'}
                        async with session.get(f"https://{host}:55000/agents",
                                             headers=headers,
                                             params={'limit': 1}) as api_resp:
                            print(f"📊 API test status: {api_resp.status}")
                            api_text = await api_resp.text()
                            print(f"   Response: {api_text[:200]}...")

                        return True
                else:
                    print(f"❌ Authentication failed")
                    return False

        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False

if __name__ == "__main__":
    result = asyncio.run(test_wazuh_direct())
    print(f"\n{'✅ SUCCESS' if result else '❌ FAILED'}")
