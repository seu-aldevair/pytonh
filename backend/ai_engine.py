import random
import json
from backend import template_manager
from backend.gemini_client import get_gemini_client, GeminiClient

class AIEngine:
    def __init__(self):
        self.gemini_client = get_gemini_client()

    def _load_all_templates(self) -> dict:
        """Carrega todos os templates de todas as fontes."""
        return template_manager.get_all_templates()

    def _create_hybrid_template(self, context: str, inspiration_templates: list) -> dict:
        """Cria um novo template híbrido com base em templates de inspiração."""
        prompt = f"""
        Contexto do Cliente: "{context}"

        Modelos de Inspiração:
        """
        for i, template in enumerate(inspiration_templates):
            prompt += f"\n--- Modelo de Inspiração {i+1} ---\n"
            prompt += f"Título: {template['title']}\n"
            prompt += f"Assunto: {template['subject']}\n"
            prompt += f"Corpo: {template['body']}\n"

        prompt += """
        ---
        Tarefa: Crie uma nova proposta de mensagem de vendas (template) que seja uma fusão inteligente das ideias dos modelos de inspiração fornecidos. A nova proposta deve ser perfeitamente adaptada ao contexto do cliente.

        O resultado deve ser um objeto JSON com as seguintes chaves: "title", "subject", "body", "ideal_for".
        - "title": Um título curto e impactante para o novo template.
        - "subject": A linha de assunto do e-mail.
        - "ideal_for": Descreva o cenário ideal de uso para esta nova proposta.
        - "body": O corpo completo da mensagem, em formato de texto simples, usando as melhores técnicas de copywriting dos modelos de inspiração.
        """
        
        response_text = self.gemini_client.generate_content(prompt)
        
        try:
            # Limpa e converte a string de resposta para um dicionário Python
            clean_response = response_text.strip().replace("```json", "").replace("```", "")
            return json.loads(clean_response)
        except json.JSONDecodeError:
            # Se a IA não retornar um JSON válido, cria um template de fallback
            return {
                "title": "Proposta Híbrida (Fallback)",
                "subject": "Uma proposta para você",
                "body": response_text,
                "ideal_for": "Situações onde a IA falhou em gerar um JSON."
            }

    def _generate_creation_report(self, context: str, inspiration_templates: list, new_template: dict) -> str:
        """Gera um relatório explicando como o novo template foi criado."""
        prompt = f"""
        Contexto do Cliente: "{context}"

        Modelos de Inspiração Usados:
        """
        for template in inspiration_templates:
            prompt += f"- {template['title']}\n"

        prompt += f"""
        Novo Template Gerado:
        - Título: {new_template.get('title', 'N/A')}
        - Assunto: {new_template.get('subject', 'N/A')}

        ---
        Tarefa: Escreva um relatório conciso e transparente para o usuário final. Explique, em 2-3 parágrafos, por que você escolheu esses modelos de inspiração e como você combinou as ideias deles para criar a nova proposta, considerando o contexto do cliente. Seja claro sobre a estratégia por trás da fusão.
        """
        return self.gemini_client.generate_content(prompt)

    def generate_proposal(self, context: str, media_files: list = None) -> dict:
        """
        Gera uma proposta inteligente, possivelmente combinando templates existentes.
        """
        all_templates = self._load_all_templates()
        
        # Junta todos os templates disponíveis para a seleção
        human_adm_templates = all_templates.get("human_adm", [])
        human_templates = all_templates.get("human", [])
        ai_templates = all_templates.get("ai", [])

        selectable_templates = human_adm_templates + human_templates + ai_templates

        if not selectable_templates:
            return {
                "proposal": "Nenhum template disponível para gerar uma proposta.",
                "report": "Não há templates no sistema. Adicione alguns para começar."
            }

        # A IA seleciona 2 ou 3 templates relevantes como inspiração
        num_to_select = min(len(selectable_templates), random.randint(2, 3))
        inspiration_templates = random.sample(selectable_templates, num_to_select)

        # Cria um novo template híbrido
        new_template = self._create_hybrid_template(context, inspiration_templates)

        # Salva o novo template gerado pela IA
        if new_template:
            template_name = template_manager.save_ai_template(new_template)
            template_manager.increment_template_usage(template_name)

        # Gera um relatório explicando o processo
        report = self._generate_creation_report(context, inspiration_templates, new_template)

        return {
            "proposal": new_template.get('body', "Erro ao gerar proposta."),
            "report": report
        }