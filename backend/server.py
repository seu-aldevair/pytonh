import os
import json
import uvicorn
from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Dict, Any, Optional
from starlette.responses import HTMLResponse
from backend.template_manager import get_template_report

from backend import template_manager
from backend.ai_engine import AIEngine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ai_engine = AIEngine()

frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")

@app.get("/templates")
def get_all_templates_endpoint():
    """Retorna todos os templates disponíveis."""
    try:
        return template_manager.get_all_templates()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/templates/human")
async def create_human_template(template_data: Dict[str, Any]):
    """Cria um novo template humano."""
    try:
        template_name = template_manager.save_human_template(template_data)
        return {"message": "Template criado com sucesso", "template_name": template_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/templates/{template_type}/{template_name}")
def delete_template_endpoint(template_type: str, template_name: str):
    """Deleta um template específico."""
    try:
        if template_type not in ["human", "ai", "human_adm"]:
            raise HTTPException(status_code=400, detail="Tipo de template inválido.")
        
        template_manager.delete_template(template_type, template_name)
        return {"message": f"Template '{template_name}' deletado."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/templates/report/{template_name}")
async def get_template_report_page(template_name: str):
    """Serves a simple HTML page with the template content."""
    report = get_template_report(template_name)
    if not report:
        return HTMLResponse(content="<h1>Template não encontrado</h1>", status_code=404)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Relatório do Template: {report.get('filename', 'N/A')}</title>
        <style>
            body {{ font-family: sans-serif; line-height: 1.6; padding: 20px; }}
            pre {{ background-color: #f4f4f4; padding: 15px; border-radius: 5px; white-space: pre-wrap; }}
        </style>
    </head>
    <body>
        <h1>Relatório do Template</h1>
        <p><strong>Arquivo:</strong> {report.get('filename', 'N/A')}</p>
        <p><strong>Contagem de Uso:</strong> {report.get('usage_count', 0)}</p>
        <p><strong>Último Uso:</strong> {report.get('last_used', 'Nunca')}</p>
        <h2>Conteúdo do Template</h2>
        <pre>{report.get('content', 'Conteúdo não disponível.')}</pre>
        <h2>Análises da IA</h2>
        {'<br>'.join(report.get('ai_analysis', ['Nenhuma análise.']))}
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/generate-proposal")
async def generate_proposal(
    nome: str = Form(...),
    empresa: str = Form(...),
    nicho: str = Form(...),
    onde: str = Form(...),
    ponto: Optional[str] = Form(None),
    problems: str = Form(...),  # JSON string
):
    """Gera uma nova proposta com base nos dados do formulário."""
    try:
        problem_list = json.loads(problems)
        full_context = f"""
        Nome do Cliente: {nome}
        Nome da Empresa: {empresa}
        Nicho de Atuação: {nicho}
        Onde foi encontrado: {onde}
        Ponto Forte (Elogio): {ponto or 'Nenhum'}
        Problemas a resolver: {', '.join(problem_list)}
        """
        
        result = ai_engine.generate_proposal(full_context)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar proposta: {str(e)}")

app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")

if __name__ == "__main__":
    for folder in ["human_templates", "ai_templates"]:
        path = os.path.join(os.path.dirname(__file__), folder)
        if not os.path.exists(path):
            os.makedirs(path)
            
    uvicorn.run(app, host="0.0.0.0", port=8000)