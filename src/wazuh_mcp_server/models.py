from pydantic import BaseModel
from datetime import datetime

class WazuhAgent(BaseModel):
    """Represents a monitored endpoint in the Wazuh environment."""
    id: str
    name: str
    ip_address: str
    status: str
    os: str
    version: str

class WazuhManager(BaseModel):
    """Represents the central component of the Wazuh infrastructure."""
    id: str
    hostname: str
    ip_address: str
    status: str
    version: str

class MCPServer(BaseModel):
    """The server that this repository implements, which acts as a control plane for the Wazuh managers."""
    id: str
    start_time: datetime
    status: str
    version: str
