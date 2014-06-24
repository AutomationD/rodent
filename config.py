import os

# Statement for enabling the development environment
DEBUG = True

# Define the application directory

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define bind IP address
BIND_IP = '0.0.0.0'

DNS_ENABLED = True

# DNS_SERVER_IP = '192.168.1.11'
DNS_SERVER_IP = '127.0.0.1'