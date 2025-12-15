import pytest

from backend.ai_engine import select_template_id, generate_proposal, create_proposal_flow
from backend.ai_engine import _replace_placeholders, fallback_select_template


class DummyClient:
    def __init__(self):
        self.last_prompt = None

    def send(self, prompt: str) -> str:
        self.last_prompt = prompt
        # Phase 1 detection: return a plain valid ID
        if "Biblioteca de Templates" in prompt:
            return "HIGH_TICKET"
        # Phase 2: return a mock filled proposal
        if "Template Base Selecionado" in prompt:
            return "Olá, João! Acompanhei seu trabalho e vejo que seu site não justifica o preço. Nossa proposta: redesign premium que alinha percepção e preço."
        return ""


def test_select_template_id_success():
    client = DummyClient()
    problems = ["site amador", "precisa justificar preço"]
    tid = select_template_id(problems, client)
    assert tid == "HIGH_TICKET"
    assert "Problemas e Dor Central" in client.last_prompt


def test_generate_proposal_success():
    client = DummyClient()
    client_info = {
        "Nome do Cliente (Contato Principal)": "João",
        "Nome da Empresa": "Empresa X",
    }
    problems = ["site amador"]
    proposal = generate_proposal(client_info, problems, "HIGH_TICKET", client)
    assert "Nossa proposta" in proposal or "redesign premium" in proposal


def test_replace_placeholders():
    tpl = "Olá, [NOME_DO_PROFISSIONAL]! Sua empresa [NOME_DA_EMPRESA] está no nicho [NICHO_DA_EMPRESA]."
    info = {
        "Nome do Cliente (Contato Principal)": "Mariana",
        "Nome da Empresa": "Loja Z",
        "Nicho/Área de Atuação": "Moda feminina",
    }
    out = _replace_placeholders(tpl, info)
    assert "Mariana" in out
    assert "Loja Z" in out
    assert "Moda feminina" in out


def test_fallback_select_template():
    assert fallback_select_template(["site lento", "alto abandono mobile"]) == "AUDITORIA_VISUAL"
    assert fallback_select_template(["gastando em Meta Ads e links genéricos"]) == "OTIMIZACAO_TRAFEGO"


def test_create_proposal_flow():
    class FlowClient(DummyClient):
        def send(self, prompt: str) -> str:
            # For phase1
            if 'Biblioteca de Templates' in prompt:
                return 'HIGH_TICKET'
            # For phase2, return a simple proposal text
            return 'Proposta personalizada para [NOME_DO_PROFISSIONAL] da [NOME_DA_EMPRESA]'

    client = FlowClient()
    client_info = {
        'Nome do Cliente (Contato Principal)': 'Carlos',
        'Nome da Empresa': 'Loja C'
    }
    problems = ['site amador']
    out = create_proposal_flow(client_info, problems, client)
    assert 'HIGH_TICKET' in out
    assert 'Carlos' in out or 'Loja C' in out


def test_phase2_prompt_contains_rewrite_instruction():
    client_info = {'Nome do Cliente (Contato Principal)': 'Ana', 'Nome da Empresa': 'Emp'}
    problems = ['site lento', 'alto abandono mobile']
    tpl = 'Olá, [NOME_DO_PROFISSIONAL]! No entanto, notei um detalhe: [PROBLEMAS].'
    from backend.ai_engine import get_phase2_prompt
    p = get_phase2_prompt(client_info, problems, tpl)
    assert 'No entanto' in p
    assert any(s in p.lower() for s in ['reescreva', 're-escreva']) or 'integre' in p.lower() or 'integr' in p.lower()


def test_select_template_invalid_response():
    class BadClient:
        def send(self, prompt: str) -> str:
            return "uma resposta inválida e longa"

    tid = select_template_id(["x"], BadClient())
    from backend.data import TEMPLATES
    assert tid in TEMPLATES
