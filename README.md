# iWAN Python Client

A Python client for Wanchain iWAN (WebSocket) RPC API.

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## English

### Installation

```bash
pip install iwan
```

Or from source:

```bash
git clone https://github.com/Nevquit/iWAN.git
cd iWAN
python setup.py install
```

### Usage

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

### Features

- **Automatic Signing**: Automatically generates timestamps and signatures for your requests.
- **Request ID Handling**: Ensures unique IDs for each request using `uuid4` if not provided.
- **Retry Mechanism**: Built-in retry logic that validates response IDs.
- **SSL Support**: Option to skip SSL verification if needed.

### API Reference

#### `IwanClient(url, api_key, secret_key, timeout=30, skip_ssl_verify=False)`
- `url`: WebSocket endpoint (e.g., `wss://api.wanchain.org:8443/ws/v3/`).
- `api_key`: Your iWAN API key.
- `secret_key`: Your iWAN secret key.
- `timeout`: Connection timeout in seconds.
- `skip_ssl_verify`: Set to `True` to skip SSL certificate verification.

#### `send_request(request_src, retry=10)`
- `request_src`: Dictionary containing the JSON-RPC request.
- `retry`: Number of retries on network error or ID mismatch.

---

<a name="中文"></a>
## 中文

### 安装

```bash
pip install iwan
```

或从源码安装：

```bash
git clone https://github.com/Nevquit/iWAN.git
cd iWAN
python setup.py install
```

### 使用示例

```python
import json
from iwan import IwanClient

# 配置信息
URL = 'wss://apitest.wanchain.org:8443/ws/v3/'
API_KEY = 'your_api_key'
SECRET_KEY = 'your_secret_key'

# 初始化客户端
client = IwanClient(URL, API_KEY, SECRET_KEY)

# 准备请求
request = {
    "jsonrpc": "2.0",
    "method": "getBalance",
    "params": {
        "address": "your_wanchain_address",
        "chainType": "WAN"
    }
}

# 发送请求
try:
    response = client.send_request(request)
    print(json.dumps(response, indent=2))
finally:
    client.close()
```

### 项目特性

- **自动签名**：自动为请求生成时间戳（timestamp）和签名（signature）。
- **请求 ID 处理**：如果请求中未提供 ID，自动使用 `uuid4` 生成唯一 ID。
- **重试机制**：内置重试逻辑，并校验响应中的 ID 是否与请求匹配。
- **SSL 支持**：支持跳过 SSL 证书校验。

### 项目结构

```text
iwan_project/
├── src/
│   └── iwan/               # 源代码目录
│       ├── __init__.py
│       └── client.py       # 核心客户端逻辑
├── tests/                  # 测试代码
├── pyproject.toml          # 核心配置文件
├── README.md               # 项目说明
└── LICENSE                 # 许可证
```

## License

This project is licensed under the MIT License.
