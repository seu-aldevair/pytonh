Projeto de exemplo: Engine em duas fases para seleção e geração de propostas usando a API do Gemini.

Uso rápido (exemplo com `MockGeminiClient`):

```py
from backend.gemini_client import MockGeminiClient
from backend.ai_engine import select_template_id, generate_proposal

def resolver(prompt: str) -> str:
    if 'Biblioteca de Templates' in prompt:
        return 'HIGH_TICKET'
    return 'Olá, João! Proposta final personalizada...'

client = MockGeminiClient(resolver)
problems = ['site lento', 'alto abandono mobile']
tid = select_template_id(problems, client)
proposal = generate_proposal({
    'Nome do Cliente (Contato Principal)': 'João',
    'Nome da Empresa': 'Empresa X',
}, problems, tid, client)
print(tid)
print(proposal)
```

Testes:

- Se você tem `pytest`: execute `pytest backend/tests -q`.
- Se não tiver `pytest` ou `python` no PATH, há um runner simples:

```bash
python backend/run_tests.py
```

Observações:
- `GeminiClient` é um stub; substitua por uma implementação real que chame a API.
- `generate_proposal` agora substitui placeholders localmente antes de enviar o prompt.
- `select_template_id` usa uma heurística local como fallback se a API não devolver um ID válido.
- Há um CLI simples em `backend/cli.py` e um runner de exemplo em `backend/example_run.py`.
- Um servidor FastAPI foi adicionado em `backend/server.py` com endpoints para as duas fases e um fluxo completo. Ele também serve o frontend estático em `frontend/`.
- Preview e seleção de templates:
  - Há um endpoint `GET /api/templates` que lista templates disponíveis.
  - No frontend você pode selecionar um template e clicar em "Pré-visualizar template" para ver o template preenchido localmente antes de gerar a proposta.
- Integração com Gemini:
  - Para usar o cliente real (HTTP), defina as variáveis de ambiente `GEMINI_API_KEY` e `GEMINI_API_URL` e opcionalmente `GEMINI_MODEL`.
  - Ative com `GEMINI_ENABLED=1` antes de rodar o servidor.

- Instalação no Windows (rápido): baixe o instalador do Python em https://python.org, marque "Add Python to PATH" e depois execute:

```powershell
python -m pip install -r backend/requirements.txt
# rodar servidor com Mock (padrão):
uvicorn backend.server:app --reload --port 8000
# para usar Gemini real (Linux/Windows PowerShell):
$env:GEMINI_API_KEY='SUA_CHAVE'
$env:GEMINI_API_URL='https://api.gemini.example/v1/generate'
$env:GEMINI_ENABLED='1'
uvicorn backend.server:app --reload --port 8000
# abra http://localhost:8000/ no navegador para ver o frontend
```
