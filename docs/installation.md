# Installation Guide

This guide covers all installation methods for Wazuh MCP Server v2.1.2 across different platforms.

## 📋 Prerequisites

### System Requirements
- **Python**: 3.11+ (recommended) or 3.9+ (minimum)
- **Operating System**: Windows 10+, macOS 10.15+, or Linux
- **Memory**: 512MB+ available RAM
- **Disk Space**: 100MB+ free space

### Wazuh Requirements
- **Wazuh Server**: 4.8.0+ (recommended) or 4.0.0+ (minimum)
- **Network Access**: HTTP/HTTPS connectivity to Wazuh server
- **Credentials**: Valid Wazuh user account with API access

### Claude Desktop
- **Claude Desktop**: Latest version
- **Configuration Access**: Ability to modify Claude Desktop configuration file

## 🚀 Quick Installation

Choose your platform and run the appropriate installer:

### Universal Python Installer (Recommended)
```bash
git clone https://github.com/gensecaihq/Wazuh-MCP-Server.git
cd Wazuh-MCP-Server
python3 installers/install.py
```

### Platform-Specific Installers

#### Windows
```cmd
git clone https://github.com/gensecaihq/Wazuh-MCP-Server.git
cd Wazuh-MCP-Server
installers\platform\install-windows.bat
```

#### macOS
```bash
git clone https://github.com/your-repo/wazuh-mcp-server.git
cd wazuh-mcp-server
chmod +x installers/platform/install-macos.sh
./installers/platform/install-macos.sh
```

#### Debian/Ubuntu/Linux Mint
```bash
git clone https://github.com/your-repo/wazuh-mcp-server.git
cd wazuh-mcp-server
chmod +x installers/platform/install-debian.sh
./installers/platform/install-debian.sh
```

#### Fedora/RHEL/CentOS
```bash
git clone https://github.com/your-repo/wazuh-mcp-server.git
cd wazuh-mcp-server
chmod +x installers/platform/install-fedora.sh
./installers/platform/install-fedora.sh
```

#### Arch Linux/Manjaro
```bash
git clone https://github.com/your-repo/wazuh-mcp-server.git
cd wazuh-mcp-server
chmod +x installers/platform/install-arch.sh
./installers/platform/install-arch.sh
```

## 🔧 Manual Installation

If you prefer manual installation or need more control:

### 1. Clone Repository
```bash
git clone https://github.com/your-repo/wazuh-mcp-server.git
cd wazuh-mcp-server
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### 4. Create Configuration
```bash
# Copy example configuration
cp .env.example .env

# Edit configuration with your Wazuh details
# Windows: notepad .env
# macOS: open -a TextEdit .env
# Linux: nano .env
```

### 5. Test Installation
```bash
# Run connection validation
python src/wazuh_mcp_server/main.py --check

# Or run comprehensive health validation
python validate_server_health.py
```

## ⚙️ Configuration

### 1. Wazuh Server Configuration

Edit `.env` with your Wazuh server details:

```bash
# === REQUIRED SETTINGS ===
# Wazuh Manager Connection
WAZUH_HOST=your-wazuh-server.com
WAZUH_USER=your-username
WAZUH_PASS=your-password

# === OPTIONAL SETTINGS ===
# Wazuh Manager Port (default: 55000)
WAZUH_PORT=55000

# SSL Verification (default: true)
# For production, this should be set to true
VERIFY_SSL=false

# === INDEXER SETTINGS (Optional) ===
# Enable these only if you have Wazuh Indexer installed
# Provides enhanced search, analytics, and vulnerability data
# If Indexer is not accessible, disable these features:
USE_INDEXER_FOR_ALERTS=false
USE_INDEXER_FOR_VULNERABILITIES=false

# WAZUH_INDEXER_HOST=your-wazuh-server.com
# WAZUH_INDEXER_USER=admin
# WAZUH_INDEXER_PASS=your-indexer-password
# WAZUH_INDEXER_PORT=9200

# === TRANSPORT MODE ===
# How the MCP server communicates (default: stdio for Claude Desktop)
MCP_TRANSPORT=stdio

# === LOGGING ===
LOG_LEVEL=INFO
```

### 2. Claude Desktop Configuration

#### Windows
Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "wazuh": {
      "command": "C:\\path\\to\\wazuh-mcp-server\\bin\\wazuh-mcp-server.exe",
      "args": ["--stdio"]
    }
  }
}
```

#### macOS/Linux
Edit `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "wazuh": {
      "command": "/path/to/wazuh-mcp-server/bin/wazuh-mcp-server",
      "args": ["--stdio"]
    }
  }
}
```

## ✅ Verification

### 1. Connection Validation
```bash
python src/wazuh_mcp_server/main.py --check
```

Expected output:
```
🔍 Validating Wazuh MCP Server configuration and connectivity...
📡 Testing Wazuh Manager: your-server.com:55000
   ✅ CONNECTED & AUTHENTICATED
   📋 API Version: 4.9.2
   🔐 Authentication: ✅ SUCCESS

✅ Configuration and connectivity check passed!
   Manager connection working - MCP server should be functional
```

### 2. Comprehensive Health Check
```bash
python validate_server_health.py
```

Expected output:
```
🏥 Starting comprehensive Wazuh MCP Server health validation...
📋 Testing Configuration...
   ✅ Configuration loaded: your-server.com:55000
🔗 Testing Manager API Connectivity...
   ✅ Connected to https://your-server.com:55000
🔐 Testing Authentication...
   ✅ Authentication successful for user: your-username
🎯 Testing Core API Endpoints...
   ✅ API information: Working
   ✅ Agent management: Working
   ✅ Detection rules: Working
⚡ Testing Performance...
   ✅ API response time: 0.26s (good)

🟢 OVERALL STATUS: HEALTHY
📊 Test Results: 4/5 passed (80.0%)
```

### 2. Test Connection
```bash
# Activate virtual environment if not already active
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Test basic connectivity
python tools/validate_setup.py
```

### 3. Claude Desktop Test
1. Restart Claude Desktop
2. Ask Claude: "Show me Wazuh system status"
3. You should see connection information and system statistics

## 🔍 Troubleshooting Installation

### Common Issues

#### Python Version Issues
```bash
# Check Python version
python3 --version

# If version is too old, install newer Python:
# Windows: Download from python.org
# macOS: brew install python@3.11
# Ubuntu: sudo apt install python3.11
# Fedora: sudo dnf install python3.11
```

#### Virtual Environment Issues
```bash
# If venv creation fails:
python3 -m pip install --user virtualenv
python3 -m virtualenv venv
```

#### Dependency Installation Issues
```bash
# Clear pip cache and retry
pip cache purge
pip install -r requirements.txt --no-cache-dir

# On macOS, if compiler errors:
xcode-select --install

# On Linux, if missing headers:
sudo apt install python3-dev build-essential  # Debian/Ubuntu
sudo dnf install python3-devel gcc gcc-c++    # Fedora/RHEL
```

#### Permission Issues
```bash
# On Linux/macOS, if permission denied:
chmod +x bin/wazuh-mcp-server
chmod +x installers/platform/*.sh

# On Windows, run as Administrator if needed
```

### Platform-Specific Issues

#### Windows
- **PowerShell Execution Policy**: Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- **Long Path Issues**: Enable long paths in Windows settings
- **Antivirus**: Add project folder to antivirus exclusions

#### macOS
- **Gatekeeper**: Run `xattr -d com.apple.quarantine bin/wazuh-mcp-server` if blocked
- **Homebrew**: Install Homebrew first for dependencies
- **M1/M2 Macs**: Ensure you're using native Python, not Rosetta

#### Linux
- **SELinux**: Check SELinux policies if connection issues
- **Firewall**: Ensure outbound HTTPS (443) and Wazuh port (55000) are open
- **AppArmor**: May need to configure AppArmor profiles

### Wazuh-Specific Issues

#### SSL/TLS Connection Issues
If you see SSL verification errors:
```bash
# For development/testing, disable SSL verification in .env:
VERIFY_SSL=false

# For production, ensure proper SSL certificates or use:
VERIFY_SSL=true
ALLOW_SELF_SIGNED=true
```

#### Protocol Issues
The server always uses HTTPS for Wazuh API connections. If you see HTTP protocol errors:
- Ensure your Wazuh server supports HTTPS on port 55000
- Check firewall rules allow HTTPS traffic
- Verify SSL certificates are properly configured

#### Indexer Connection Issues
If you see Indexer timeout errors:
```bash
# Disable Indexer features in .env if not accessible:
USE_INDEXER_FOR_ALERTS=false
USE_INDEXER_FOR_VULNERABILITIES=false

# Comment out Indexer settings:
# WAZUH_INDEXER_HOST=your-server.com
# WAZUH_INDEXER_USER=admin
# WAZUH_INDEXER_PASS=your-password
```

#### Authentication Issues
If authentication fails:
- Verify credentials are correct in .env file
- Ensure the Wazuh user has API access permissions
- Check if the user account is not locked or expired
- Test credentials manually: `curl -u username:password https://your-server:55000/security/user/authenticate`

#### "Degraded Mode" Warnings
If you see "Running in degraded mode" warnings:
- This is normal when Indexer is not accessible
- The server will work in Manager-only mode with full functionality
- All core features (agents, alerts, rules) remain available

## 🔄 Upgrading

### From v2.0.x to v2.1.0
```bash
# Backup configuration
cp .env .env.backup

# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run migration tool
python tools/migrate_v1_to_v2.sh

# Test upgrade
./bin/wazuh-mcp-server --health-check
```

### Clean Installation (if upgrade issues)
```bash
# Remove virtual environment
rm -rf venv

# Reinstall
python3 installers/install.py

# Restore configuration
cp .env.backup .env
```

## 📞 Getting Help

If installation fails:

1. **Check [Troubleshooting Guide](troubleshooting/README.md)**
2. **Run health check** with verbose output: `./bin/wazuh-mcp-server --health-check --verbose`
3. **Check logs** in `logs/` directory
4. **Create an issue** with installation logs and system information

---

**Next Steps**: Once installation is complete, see the [Configuration Guide](configuration.md) for detailed configuration options.