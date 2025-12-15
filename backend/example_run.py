from backend.gemini_client import MockGeminiClient
from backend.ai_engine import create_proposal_flow


def resolver(prompt: str) -> str:
    # Responder Fase1 com HIGH_TICKET e Fase2 com uma proposta
    if 'Biblioteca de Templates' in prompt:
        return 'HIGH_TICKET'
    return (
        "Olá, [Nome do Profissional]! Acompanho seu trabalho e admiro muito. "
        "No entanto, notei que seu site atual não reflete a qualidade do serviço e isso causa perda de clientes. "
        "Nossa solução é um redesign premium que alinha percepção, prova social e precificação, gerando mais conversões e justificando seu preço."
    )


if __name__ == '__main__':
    client = MockGeminiClient(resolver)
    client_info = {
        'Nome do Cliente (Contato Principal)': 'Ana',
        'Nome da Empresa': 'Agência Y',
        'Nicho/Área de Atuação': 'Serviços Premium',
        'Onde o encontrei': 'anúncio no Meta Ads',
        'Ponto Forte (Elogio Inicial)': 'excelente produção de conteúdo',
    }
    problems = [
        'O site atual passa sensação amadora',
        'Alta taxa de abandono no mobile',
    ]

    out = create_proposal_flow(client_info, problems, client)
    print(out)
