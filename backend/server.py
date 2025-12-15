import os
import json
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List, Dict, Any, Optional

from backend import template_manager
from backend.ai_engine import AIEngine

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ai_engine = AIEngine()
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")

# Endpoints da API
@app.get("/templates")
def get_all_templates_endpoint():
    try:
        return template_manager.get_all_templates()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/templates/human")
async def create_human_template(template_data: Dict[str, Any]):
    try:
        template_name = template_manager.save_human_template(template_data)
        return {"message": "Template criado com sucesso", "template_name": template_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/templates/{template_type}/{template_name}")
def delete_template_endpoint(template_type: str, template_name: str):
    try:
        if template_type not in ["human", "ai", "human_adm"]:
            raise HTTPException(status_code=400, detail="Tipo de template inválido.")
        
        template_manager.delete_template(template_type, template_name)
        return {"message": f"Template '{template_name}' deletado."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-proposal")
async def generate_proposal(
    nome: str = Form(...),
    empresa: str = Form(...),
    nicho: str = Form(...),
    onde: str = Form(...),
    ponto: Optional[str] = Form(None),
    problems: str = Form(...), # JSON string
    media_url: Optional[str] = Form(None),
    media_files: List[UploadFile] = File(None),
):
    file_contents = []
    if media_files:
        for file in media_files:
            content = await file.read()
            file_contents.append({"filename": file.filename, "content": content})

    try:
        # Combina todos os dados de texto em um único contexto para a IA
        problem_list = json.loads(problems)
        full_context = f"""
        Nome do Cliente: {nome}
        Nome da Empresa: {empresa}
        Nicho de Atuação: {nicho}
        Onde foi encontrado: {onde}
        Ponto Forte (Elogio): {ponto or 'Nenhum'}
        Problemas a resolver: {', '.join(problem_list)}
        """
        
        result = ai_engine.generate_proposal(full_context, file_contents, media_url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar proposta: {str(e)}")

# Servir arquivos estáticos e o index.html
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

if __name__ == "__main__":
    for folder in ["human_templates", "ai_templates", "human_adm_templates"]:
        path = os.path.join(os.path.dirname(__file__), folder)
        if not os.path.exists(path):
            os.makedirs(path)
            
    uvicorn.run(app, host="0.0.0.0", port=8000)