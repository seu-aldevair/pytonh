"""Templates de propostas usados pela Fase 2.

Fornece um dicionário `TEMPLATES` com texto-base e utilitários simples.
"""

TEMPLATES = {
    "OTIMIZACAO_TRAFEGO": {
        "default": (
            "Olá, [NOME_DO_PROFISSIONAL]! Notei que vocês anunciam ativamente, mas parte do tráfego está sendo desperdiçado em links genéricos. "
            "Nossa proposta é alinhar anúncios a landing pages específicas, aplicar testes A/B e otimizar o funnel para reduzir CPL e aumentar a qualidade dos leads. "
            "No entanto, notei um detalhe que impacta eficiência: [PROBLEMAS]."
        ),
        "formal": (
            "Prezado [NOME_DO_PROFISSIONAL], identifiquei que o tráfego proveniente de anúncios está sendo direcionado a destinos genéricos, reduzindo a eficiência das campanhas. "
            "Nossa abordagem consiste em alinhar criativos a landing pages dedicadas, implementar testes A/B e otimizar o funil para reduzir o CPL e elevar a qualidade dos leads. "
            "Observação crítica: [PROBLEMAS]."
        ),
        "conversational": (
            "Oi [NOME_DO_PROFISSIONAL]! Percebi que parte do tráfego dos anúncios acaba se perdendo em links genéricos. "
            "A gente pode criar landings específicas, testar variações e deixar o funil mais eficiente — assim você paga menos por cada lead e recebe melhores contatos. "
            "Um ponto que chama atenção: [PROBLEMAS]."
        ),
    },
    "AUDITORIA_VISUAL": {
        "default": (
            "Olá, [NOME_DO_PROFISSIONAL]! A experiência mobile do site apresenta pontos críticos que geram alto abandono. "
            "Oferecemos uma auditoria técnica e de usabilidade com correções rápidas de performance e fluxo de compra. "
            "No entanto, notei um detalhe: [PROBLEMAS]."
        ),
        "formal": (
            "Prezado [NOME_DO_PROFISSIONAL], a atual experiência móvel do site revela gargalos que contribuem para elevada taxa de abandono. "
            "Propomos uma auditoria de performance e usabilidade seguida de correções priorizadas para reduzir desistências e recuperar conversões. "
            "Ponto identificado: [PROBLEMAS]."
        ),
        "conversational": (
            "Olá [NOME_DO_PROFISSIONAL]! Seu site no celular está perdendo visitantes por pequenos problemas. "
            "A gente faz uma auditoria rápida, corrige o que mais pesa e melhora a taxa de conversão em pouco tempo. "
            "Notei: [PROBLEMAS]."
        ),
    },
    "HIGH_TICKET": {
        "default": (
            "Olá, [NOME_DO_PROFISSIONAL]! Seu posicionamento premium exige uma presença online que justifique valores mais altos. "
            "Propomos uma landing page com design de autoridade, provas sociais selecionadas e copy que alinha percepções à precificação. "
            "No entanto, notei um detalhe: [PROBLEMAS]."
        ),
        "formal": (
            "Prezado [NOME_DO_PROFISSIONAL], para sustentar uma precificação premium é essencial que sua presença digital transmita autoridade e confiança. "
            "Sugerimos uma landing com design de alto padrão, provas sociais estratégicas e copy que valide o investimento. "
            "Questão a resolver: [PROBLEMAS]."
        ),
        "conversational": (
            "Oi [NOME_DO_PROFISSIONAL]! Para cobrar mais, seu site precisa provar que vale — e hoje ele não está ajudando nisso. "
            "Vamos criar uma landing que mostra autoridade, provas certas e argumentos que fazem a venda acontecer. "
            "Destaque: [PROBLEMAS]."
        ),
    },
    "ROI": {
        "default": (
            "Olá, [NOME_DO_PROFISSIONAL]! Vamos focar em resultados financeiros claros: identificar oportunidades de CRO, otimizar canais e aumentar o faturamento mensurável. "
            "No entanto, notei um detalhe: [PROBLEMAS]."
        ),
        "formal": (
            "Prezado [NOME_DO_PROFISSIONAL], propomos uma abordagem orientada a ROI: diagnóstico de canais, testes e priorização de ações que impactem o faturamento. "
            "Constatamos: [PROBLEMAS]."
        ),
        "conversational": (
            "Vamos direto aos números: identificar o que traz receita e aumentar isso com otimizações simples. "
            "Problema observado: [PROBLEMAS]."
        ),
    },
    "LANCAMENTO": {
        "default": (
            "Olá, [NOME_DO_PROFISSIONAL]! Precisamos de uma página de vendas otimizada para lançamento com urgência: copy focada em benefícios, provas sociais e sequência de pré-lançamento. "
            "No entanto, notei um detalhe: [PROBLEMAS]."
        ),
        "formal": (
            "Sugerimos uma página de vendas otimizada para lançamento, com foco em benefícios, provas sociais e fluxo de pré-lançamento para conversão rápida. "
            "Observação: [PROBLEMAS]."
        ),
        "conversational": (
            "Vamos montar uma página de lançamento que vende: benefícios claros, provas e urgência. "
            "Notei: [PROBLEMAS]."
        ),
    },
    "PARCERIA": {
        "default": (
            "Olá, [NOME_DO_PROFISSIONAL]! Posicionamos nossa entrega como otimização do 'meio de campo' do funil, conectando conteúdo ao checkout e melhorando taxas entre tráfego e compra. "
            "No entanto, notei um detalhe: [PROBLEMAS]."
        ),
        "formal": (
            "Propomos otimizar a etapa intermediária do funil, conectando conteúdo ao checkout e elevando a taxa de conversão entre tráfego e compra. "
            "Ponto: [PROBLEMAS]."
        ),
        "conversational": (
            "Posso ajudar a ligar o conteúdo que você tem ao checkout, para transformar curiosos em clientes. "
            "Percebi: [PROBLEMAS]."
        ),
    },
    "SOLUCAO_SIMPLES": {
        "default": (
            "Olá, [NOME_DO_PROFISSIONAL]! Se o WhatsApp está sobrecarregado, implementamos um fluxo simples de qualificação para priorizar leads de maior valor e reduzir distrações. "
            "No entanto, notei um detalhe: [PROBLEMAS]."
        ),
        "formal": (
            "Oferecemos um fluxo de qualificação e automação para reduzir sobrecarga no WhatsApp e priorizar leads com maior potencial. "
            "Observação: [PROBLEMAS]."
        ),
        "conversational": (
            "Se o zap está lotado, a gente monta um filtro simples pra você responder só quem importa. "
            "Notei: [PROBLEMAS]."
        ),
    },
    "ESSENCIAL_COMEÇAR": {
        "default": (
            "Olá, [NOME_DO_PROFISSIONAL]! Para quem está começando, desenvolvemos uma presença online essencial e profissional que gera confiança e primeiras conversões rápidas. "
            "No entanto, notei um detalhe: [PROBLEMAS]."
        ),
        "formal": (
            "Desenvolvemos uma presença online essencial, simples e profissional para gerar confiança e as primeiras conversões. "
            "Ponto: [PROBLEMAS]."
        ),
        "conversational": (
            "Vamos montar sua primeira presença online profissional, sem glamour — só confiança que converte. "
            "Percebi: [PROBLEMAS]."
        ),
    },
    "VALIDACAO_IDEIA": {
        "default": (
            "Olá, [NOME_DO_PROFISSIONAL]! Vamos validar sua ideia com uma landing MVP para testar demanda antes de maiores investimentos. "
            "No entanto, notei um detalhe: [PROBLEMAS]."
        ),
        "formal": (
            "Sugerimos um MVP de landing para validar demanda antes de comprometer recursos significativos. "
            "Observação: [PROBLEMAS]."
        ),
        "conversational": (
            "Vamos testar sua ideia com uma landing simples e ver se as pessoas compram. "
            "Notei: [PROBLEMAS]."
        ),
    },
    "ESCASSEZ_PORTFOLIO": {
        "default": (
            "Olá, [NOME_DO_PROFISSIONAL]! Vou criar uma oferta limitada para captar os primeiros clientes e montar um portfólio com provas sociais rápidas. "
            "No entanto, notei um detalhe: [PROBLEMAS]."
        ),
        "formal": (
            "Proponho uma oferta limitada e estruturada para captar os primeiros clientes e construir provas sociais iniciais. "
            "Ponto: [PROBLEMAS]."
        ),
        "conversational": (
            "Oferta relâmpago para conseguir os primeiros clientes e montar um portfólio que impressione. "
            "Notei: [PROBLEMAS]."
        ),
    },
}


def get_template_text(template_id: str, variant: str = 'default') -> str:
    """Retorna o texto do template e variante solicitada (padrão: 'default').

    Lança KeyError se `template_id` ou `variant` não existirem.
    """
    tpl = TEMPLATES[template_id]
    if isinstance(tpl, dict):
        return tpl[variant]
    return tpl


TEMPLATE_METADATA = {}
for k, v in TEMPLATES.items():
    if isinstance(v, dict):
        TEMPLATE_METADATA[k] = {"id": k, "variants": list(v.keys()), "description": v.get('default', '')[:200]}
    else:
        TEMPLATE_METADATA[k] = {"id": k, "variants": ['default'], 'description': v[:200]}


def get_template_metadata(template_id: str) -> dict:
    return TEMPLATE_METADATA[template_id]
