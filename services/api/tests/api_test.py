import unittest
from unittest.mock import patch, MagicMock

from src.api import app


class TestApi(unittest.TestCase):

    def test_api_root_returns_empty_body(self):
        response = app.test_client().get('/')
        assert response.status_code == 200
        assert response.data == b'Hello World!'

    @patch("src.api.ServiceRpcProxy")
    def test_api_ping_endpoint_delegates_to_rpc_proxy(self, mock_rpc_proxy):
        mock_rpc = mock_rpc_proxy.return_value.__enter__.return_value
        mock_rpc.ping.return_value = {"message": "ping"}
        response = app.test_client().get('/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{"message": "ping"}')
        mock_rpc.ping.assert_called_once_with()

    @patch("src.api.ServiceRpcProxy")
    def test_api_pong_endpoint_delegates_to_rpc_proxy(self, mock_rpc_proxy):
        mock_rpc = mock_rpc_proxy.return_value.__enter__.return_value
        mock_rpc.pong.return_value = {"message": "pong"}
        response = app.test_client().get('/pong')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{"message": "pong"}')


if __name__ == '__main__':
    unittest.main()
