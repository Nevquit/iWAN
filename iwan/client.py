import hmac
import json
import base64
import collections
import time
import ssl
import copy
import logging
import traceback
from uuid import uuid4
from websocket import create_connection

logger = logging.getLogger(__name__)

class IwanClient:
    def __init__(self, url, api_key, secret_key, timeout=30, skip_ssl_verify=False):
        """
        Initialize the iWAN client.

        :param url: The WebSocket URL (e.g., 'wss://apitest.wanchain.org:8443/ws/v3/')
        :param api_key: Your API Key
        :param secret_key: Your Secret Key
        :param timeout: Connection timeout in seconds
        :param skip_ssl_verify: Whether to skip SSL certificate verification
        """
        self.url = url
        if not self.url.endswith('/'):
            self.url += '/'

        self.api_key = api_key
        self.secret_key = secret_key
        self.timeout = timeout

        sslopt = {}
        if skip_ssl_verify:
            sslopt = {"cert_reqs": ssl.CERT_NONE}

        full_url = self.url + self.api_key
        self.ws = create_connection(full_url, timeout=self.timeout, sslopt=sslopt)

    def get_timestamp(self):
        """Get current timestamp in milliseconds."""
        return int(round(time.time() * 1000))

    def gensig(self, request_src):
        """
        Generate signature for the request.

        :param request_src: The request dictionary
        :return: Base64 encoded signature string
        """
        message = json.dumps(request_src, separators=(',', ':'))
        hmac_src = hmac.new(
            bytes(self.secret_key, encoding='utf-8'),
            bytes(message, encoding='utf-8'),
            digestmod='sha256'
        )
        sig = base64.b64encode(hmac_src.digest()).decode('utf-8')
        return sig

    def gen_api_request(self, request_src):
        """
        Prepare the API request with timestamp and signature.

        :param request_src: Original request dictionary
        :return: JSON string of the signed request
        """
        request_src_dic = collections.OrderedDict(request_src)
        if 'params' not in request_src_dic:
            request_src_dic['params'] = {}

        request_src_dic['params']['timestamp'] = self.get_timestamp()
        sig = self.gensig(request_src_dic)
        request_src_dic['params']['signature'] = sig

        return json.dumps(request_src_dic, separators=(',', ':'))

    def send_request(self, request_src, retry=10):
        """
        Send a request and wait for the response.

        :param request_src: Request dictionary
        :param retry: Number of retries on failure
        :return: Response dictionary
        """
        request = copy.deepcopy(request_src)

        # Ensure a unique ID for the request
        if "id" not in request or request["id"] in [1, "1"]:
            request["id"] = str(uuid4())

        n = retry
        while n > 0:
            try:
                payload = self.gen_api_request(request)
                self.ws.send(payload)
                rsp = self.ws.recv()
                rsp_dic = json.loads(rsp)

                # Validate response ID matches request ID
                if rsp_dic.get("id") != request["id"]:
                    logger.warning(f"ID mismatch! Request ID: {request['id']}, Response ID: {rsp_dic.get('id')}")
                    n -= 1
                    continue

                return rsp_dic
            except Exception as e:
                logger.error(f"iWAN Service Error: {traceback.format_exc()}")
                n -= 1
                if n == 0:
                    return {"result": f"Error: {str(e)}", "id": request.get("id")}

        return {"result": "Error: Maximum retries reached", "id": request.get("id")}

    def close(self):
        """Close the WebSocket connection."""
        if self.ws:
            self.ws.close()
