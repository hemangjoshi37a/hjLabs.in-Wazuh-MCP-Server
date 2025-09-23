"""Wazuh API Client for MCP Server - Uses Basic Auth (working method)."""

import aiohttp
import asyncio
import ssl
import json
import base64
from typing import Optional, Dict, Any, List
from ..config import WazuhConfig

class WazuhClient:
    """Wazuh API client using Basic Auth (proven working method)."""

    def __init__(self, config: WazuhConfig):
        self.config = config
        self.token: Optional[str] = None
        self.session: Optional[aiohttp.ClientSession] = None

        # Create SSL context
        self.ssl_context = ssl.create_default_context()
        if not config.verify_ssl or config.allow_self_signed:
            self.ssl_context.check_hostname = False
            self.ssl_context.verify_mode = ssl.CERT_NONE

        # Prepare Basic Auth header
        credentials = f"{config.username}:{config.password}"
        self.basic_auth = base64.b64encode(credentials.encode()).decode('ascii')

    async def __aenter__(self):
        """Async context manager entry."""
        connector = aiohttp.TCPConnector(ssl=self.ssl_context)
        self.session = aiohttp.ClientSession(connector=connector)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    async def close(self):
        """Close the client session."""
        if self.session:
            await self.session.close()
            self.session = None

    async def authenticate(self) -> Optional[str]:
        """Authenticate with Wazuh API using Basic Auth."""
        if not self.session:
            connector = aiohttp.TCPConnector(ssl=self.ssl_context)
            self.session = aiohttp.ClientSession(connector=connector)

        auth_url = f"{self.config.base_url}/security/user/authenticate"
        headers = {
            "Authorization": f"Basic {self.basic_auth}",
            "Content-Type": "application/json"
        }

        try:
            async with self.session.post(auth_url, headers=headers, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    self.token = data.get('data', {}).get('token')
                    return self.token
                else:
                    error_text = await resp.text()
                    raise Exception(f"Authentication failed: {resp.status} - {error_text}")
        except Exception as e:
            raise Exception(f"Authentication error: {e}")

    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[Any, Any]:
        """Make authenticated API request."""
        if not self.token:
            await self.authenticate()

        if not self.session:
            connector = aiohttp.TCPConnector(ssl=self.ssl_context)
            self.session = aiohttp.ClientSession(connector=connector)

        url = f"{self.config.base_url}{endpoint}"
        headers = kwargs.pop('headers', {})
        headers['Authorization'] = f'Bearer {self.token}'

        try:
            async with self.session.request(method, url, headers=headers, timeout=30, **kwargs) as resp:
                if resp.status == 401:
                    # Token might be expired, re-authenticate
                    await self.authenticate()
                    headers['Authorization'] = f'Bearer {self.token}'
                    async with self.session.request(method, url, headers=headers, timeout=30, **kwargs) as retry_resp:
                        if retry_resp.status >= 400:
                            error_text = await retry_resp.text()
                            raise Exception(f"API request failed: {retry_resp.status} - {error_text}")
                        return await retry_resp.json()
                elif resp.status >= 400:
                    error_text = await resp.text()
                    raise Exception(f"API request failed: {resp.status} - {error_text}")

                return await resp.json()
        except asyncio.TimeoutError:
            raise Exception("Request timeout - server may be overloaded")

    async def get_agents(self, limit: int = 100, **params) -> List[Dict[str, Any]]:
        """Get list of agents."""
        params.update({'limit': limit})
        try:
            result = await self._make_request('GET', '/agents', params=params)
            return result.get('data', {}).get('affected_items', [])
        except Exception as e:
            print(f"Warning: Could not fetch agents: {e}")
            return []

    async def get_agent(self, agent_id: str) -> Dict[str, Any]:
        """Get specific agent info."""
        result = await self._make_request('GET', f'/agents/{agent_id}')
        items = result.get('data', {}).get('affected_items', [])
        return items[0] if items else {}

    async def get_security_events(self, limit: int = 100, **params) -> List[Dict[str, Any]]:
        """Get security events."""
        params.update({'limit': limit})
        try:
            result = await self._make_request('GET', '/security/events', params=params)
            return result.get('data', {}).get('affected_items', [])
        except Exception as e:
            print(f"Warning: Could not fetch security events: {e}")
            return []

    async def get_rules(self, limit: int = 100, **params) -> List[Dict[str, Any]]:
        """Get rules."""
        params.update({'limit': limit})
        try:
            result = await self._make_request('GET', '/rules', params=params)
            return result.get('data', {}).get('affected_items', [])
        except Exception as e:
            print(f"Warning: Could not fetch rules: {e}")
            return []

    async def get_cluster_status(self) -> Dict[str, Any]:
        """Get cluster status."""
        try:
            result = await self._make_request('GET', '/cluster/status')
            return result.get('data', {})
        except Exception as e:
            print(f"Warning: Could not fetch cluster status: {e}")
            return {"enabled": False}

    async def test_connection(self) -> bool:
        """Test if connection and authentication work."""
        try:
            await self.authenticate()
            if self.token:
                # Try a simple API call
                await self._make_request('GET', '/agents', params={'limit': 1})
                return True
        except Exception as e:
            print(f"Connection test failed: {e}")
        return False
