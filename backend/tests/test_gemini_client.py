import json
from unittest.mock import patch, Mock

from backend.gemini_client import RealGeminiClient


def test_real_gemini_client_success():
    fake_resp = Mock()
    fake_resp.raise_for_status = Mock()
    fake_resp.json.return_value = {'text': 'Resposta da IA'}

    with patch('backend.gemini_client.requests.post', return_value=fake_resp) as p:
        client = RealGeminiClient(api_key='k', api_url='https://api.example.com', model='m')
        out = client.send('prompt')
        assert out == 'Resposta da IA'
        p.assert_called_once()


def test_real_gemini_client_error():
    fake_resp = Mock()
    def raise_err():
        raise Exception('boom')
    fake_resp.raise_for_status = raise_err

    with patch('backend.gemini_client.requests.post', return_value=fake_resp):
        client = RealGeminiClient(api_key='k', api_url='https://api.example.com')
        try:
            client.send('p')
            assert False, 'should have raised'
        except RuntimeError:
            pass
