# iWAN Python Client

A Python client for Wanchain iWAN (WebSocket) RPC API.

## Installation

```bash
pip install iwan
```

Or from source:

```bash
git clone https://github.com/Nevquit/iWAN.git
cd iWAN
python setup.py install
```

## Usage

```python
import json
from iwan import IwanClient

# Configuration
URL = 'wss://apitest.wanchain.org:8443/ws/v3/'
API_KEY = 'your_api_key'
SECRET_KEY = 'your_secret_key'

# Initialize Client
client = IwanClient(URL, API_KEY, SECRET_KEY)

# Prepare Request
request = {
    "jsonrpc": "2.0",
    "method": "getBalance",
    "params": {
        "address": "your_wanchain_address",
        "chainType": "WAN"
    }
}

# Send Request
try:
    response = client.send_request(request)
    print(json.dumps(response, indent=2))
finally:
    client.close()
```

## Features

- **Automatic Signing**: Automatically generates timestamps and signatures for your requests.
- **Request ID Handling**: Ensures unique IDs for each request using `uuid4` if not provided.
- **Retry Mechanism**: Built-in retry logic for robust WebSocket communication.
- **SSL Support**: Option to skip SSL verification if needed.

## License

This project is licensed under the MIT License.
