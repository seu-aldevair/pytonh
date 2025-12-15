"""Pequeno CLI para criar uma proposta.

Uso:
  - Para executar com mock (padrão): `python -m backend.cli --mock`
  - Para usar um cliente real, defina `GEMINI_ENABLED=1` e providencie `GEMINI_API_KEY`.
"""
import os
import argparse

from backend.gemini_client import MockGeminiClient
from backend.ai_engine import create_proposal_flow


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mock", action="store_true", help="Usar MockGeminiClient para teste")
    args = p.parse_args()

    if args.mock or os.getenv("GEMINI_ENABLED") != "1":
        def resolver(prompt: str) -> str:
            if 'Biblioteca de Templates' in prompt:
                return 'HIGH_TICKET'
            return (
                "Olá, [Nome do Profissional]! Acompanho seu trabalho e admiro. "
                "No entanto, notei que seu site atual não reflete a qualidade do serviço. "
                "Nossa solução: redesign premium para justificar o preço e aumentar conversões."
            )

        client = MockGeminiClient(resolver)
    else:
        raise RuntimeError("Integração real com Gemini não implementada. Use --mock ou defina GEMINI_ENABLED=0")

    client_info = {
        'Nome do Cliente (Contato Principal)': 'Cliente Exemplo',
        'Nome da Empresa': 'Empresa Ex',
        'Nicho/Área de Atuação': 'Serviços',
        'Onde o encontrei': 'anúncio',
        'Ponto Forte (Elogio Inicial)': 'bom conteúdo',
    }
    problems = [
        'O site passa sensação amadora',
        'Alta taxa de abandono no mobile',
    ]

    out = create_proposal_flow(client_info, problems, client)
    print(out)


if __name__ == '__main__':
    main()
