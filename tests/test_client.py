import unittest
import json
import collections
from unittest.mock import patch, MagicMock
from iwan import IwanClient

class TestIwanClient(unittest.TestCase):
    def setUp(self):
        self.url = "wss://example.com/ws/v3/"
        self.api_key = "test_api_key"
        self.secret_key = "test_secret_key"

        with patch('iwan.client.create_connection') as mock_create_connection:
            self.client = IwanClient(self.url, self.api_key, self.secret_key)
            self.mock_ws = mock_create_connection.return_value

    def test_get_timestamp(self):
        timestamp = self.client.get_timestamp()
        self.assertIsInstance(timestamp, int)
        self.assertTrue(timestamp > 0)

    def test_gensig(self):
        request_src = {"jsonrpc": "2.0", "method": "testMethod", "params": {"timestamp": 12345}}
        sig = self.client.gensig(request_src)
        self.assertIsInstance(sig, str)
        self.assertTrue(len(sig) > 0)

    def test_gen_api_request(self):
        request_src = {"jsonrpc": "2.0", "method": "testMethod", "params": {}}
        with patch.object(self.client, 'get_timestamp', return_value=12345):
            payload_str = self.client.gen_api_request(request_src)
            payload = json.loads(payload_str)

            self.assertEqual(payload['params']['timestamp'], 12345)
            self.assertIn('signature', payload['params'])

    def test_send_request_success(self):
        request_src = {"jsonrpc": "2.0", "method": "testMethod", "params": {}, "id": "test_id"}
        expected_response = {"jsonrpc": "2.0", "result": "ok", "id": "test_id"}

        self.mock_ws.recv.return_value = json.dumps(expected_response)

        response = self.client.send_request(request_src)
        self.assertEqual(response, expected_response)
        self.mock_ws.send.assert_called()

    def test_send_request_retry_on_id_mismatch(self):
        request_src = {"jsonrpc": "2.0", "method": "testMethod", "params": {}, "id": "test_id"}
        wrong_response = {"jsonrpc": "2.0", "result": "wrong", "id": "wrong_id"}
        correct_response = {"jsonrpc": "2.0", "result": "ok", "id": "test_id"}

        self.mock_ws.recv.side_effect = [json.dumps(wrong_response), json.dumps(correct_response)]

        response = self.client.send_request(request_src, retry=2)
        self.assertEqual(response, correct_response)
        self.assertEqual(self.mock_ws.recv.call_count, 2)

    def test_send_request_error(self):
        request_src = {"jsonrpc": "2.0", "method": "testMethod", "params": {}, "id": "test_id"}
        self.mock_ws.send.side_effect = Exception("Network error")

        response = self.client.send_request(request_src, retry=1)
        self.assertIn("Error: Network error", response["result"])
        self.assertEqual(response["id"], "test_id")

if __name__ == '__main__':
    unittest.main()
