import os
from dotenv import load_dotenv, find_dotenv

# Find and load the .env file
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

print(f"Loaded .env file: {dotenv_path}")
print(f"WAZUH_USER: {os.getenv('WAZUH_USER')}")
print(f"WAZUH_PASS: {os.getenv('WAZUH_PASS')}")