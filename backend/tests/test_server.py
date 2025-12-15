from fastapi.testclient import TestClient

from backend.server import app


client = TestClient(app)


def test_select_endpoint():
    r = client.post('/api/select', json={'problems': ['site amador', 'precisa justificar preço']})
    assert r.status_code == 200
    data = r.json()
    assert 'template_id' in data
    assert 'prompt' in data


def test_generate_endpoint():
    body = {
        'client_info': {'Nome do Cliente (Contato Principal)': 'Ana', 'Nome da Empresa': 'Emp'},
        'problems': ['site amador'],
        'template_id': 'HIGH_TICKET'
    }
    r = client.post('/api/generate', json=body)
    assert r.status_code == 200
    data = r.json()
    assert 'prompt' in data and 'response' in data


def test_flow_endpoint():
    body = {
        'client_info': {'Nome do Cliente (Contato Principal)': 'Ana', 'Nome da Empresa': 'Emp'},
        'problems': ['site amador']
    }
    r = client.post('/api/flow', json=body)
    assert r.status_code == 200
    data = r.json()
    assert 'template_id' in data and 'phase1_prompt' in data and 'phase2_prompt' in data


def test_flow_with_real_client(monkeypatch):
    # Simula GEMINI_ENABLED=1 com requests.post retornando JSON
    import os
    os.environ['GEMINI_ENABLED'] = '1'
    os.environ['GEMINI_API_KEY'] = 'k'
    os.environ['GEMINI_API_URL'] = 'https://api.example.com'

    class FakeResp:
        def raise_for_status(self):
            return None
        def json(self):
            return {'text': 'Resposta real'}

    def fake_post(url, json, headers, timeout):
        return FakeResp()

    monkeypatch.setattr('backend.gemini_client.requests.post', fake_post)

    body = {
        'client_info': {'Nome do Cliente (Contato Principal)': 'Ana', 'Nome da Empresa': 'Emp'},
        'problems': ['site amador']
    }
    r = client.post('/api/flow', json=body)
    assert r.status_code == 200
    data = r.json()
    assert 'phase2_response' in data and 'Resposta real' in data['phase2_response']
    # cleanup
    del os.environ['GEMINI_ENABLED']
    del os.environ['GEMINI_API_KEY']
    del os.environ['GEMINI_API_URL']


def test_preview_endpoint():
    body = {
        'client_info': {'Nome do Cliente (Contato Principal)': 'Ana', 'Nome da Empresa': 'Emp'},
        'template_id': 'HIGH_TICKET'
    }
    r = client.post('/api/preview', json=body)
    assert r.status_code == 200
    data = r.json()
    assert 'preview' in data and 'Olá' in data['preview']


def test_templates_endpoint():
    r = client.get('/api/templates')
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert 'HIGH_TICKET' in data
    # variants present
    assert 'variants' in data['HIGH_TICKET'] and isinstance(data['HIGH_TICKET']['variants'], list)
