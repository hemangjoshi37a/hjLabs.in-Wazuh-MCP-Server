import sys
import os

# Add the src directory to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from wazuh_mcp_server.main import main
import asyncio

if __name__ == "__main__":
    # Set the environment variables
    os.environ['WAZUH_USER'] = 'wazuh'
    os.environ['WAZUH_PASS'] = 'wTNSUK9gF09XFVrW*PyiiAmj6oy?zVkR'
    os.environ['WAZUH_HOST'] = 'wazuh.gadgetaccess.com'
    os.environ['WAZUH_PORT'] = '55000'
    os.environ['WAZUH_INDEXER_HOST'] = 'wazuh.gadgetaccess.com'
    os.environ['WAZUH_INDEXER_PORT'] = '9200'
    os.environ['WAZUH_INDEXER_USER'] = 'admin'
    os.environ['WAZUH_INDEXER_PASS'] = '?mkKqZqd1+NYfP9J9stca6Bqv*PPqOq6'
    os.environ['VERIFY_SSL'] = 'false'
    os.environ['WAZUH_VERIFY_SSL'] = 'false'
    os.environ['WAZUH_ALLOW_SELF_SIGNED'] = 'true'

    # Run the main function
    sys.exit(asyncio.run(main()))