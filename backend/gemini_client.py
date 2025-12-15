# -*- coding: utf-8 -*-
"""Cliente mínimo para interagir com a API do Gemini."""

import base64
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List

import google.generativeai as genai
import magic
from dotenv import load_dotenv

load_dotenv()

class GeminiClient(ABC):
    @abstractmethod
    def generate_content(self, prompt: str, media_files: List[Dict[str, Any]] | None = None) -> str:
        """Gera conteúdo com base no prompt e, opcionalmente, em arquivos de mídia."""
        pass

class RealGeminiClient(GeminiClient):
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("API key for Gemini not found. Please set the GEMINI_API_KEY environment variable.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')

    def _prepare_media(self, media_files: List[Dict[str, Any]]) -> List[Any]:
        parts = []
        for file_info in media_files:
            file_content_b64 = file_info["content"]
            
            # Decodifica o conteúdo de base64
            file_bytes = base64.b64decode(file_content_b64)
            
            # Detecta o tipo MIME
            mime_type = magic.from_buffer(file_bytes, mime=True)
            
            if not mime_type.startswith(("image/", "video/")):
                continue

            parts.append({"mime_type": mime_type, "data": file_bytes})
        return parts

    def generate_content(self, prompt: str, media_files: List[Dict[str, Any]] | None = None) -> str:
        try:
            request_parts = [prompt]
            if media_files:
                media_parts = self._prepare_media(media_files)
                request_parts.extend(media_parts)
            
            response = self.model.generate_content(request_parts)
            return response.text
        except Exception as e:
            print(f"Error generating content with Gemini: {e}")
            return f"Erro ao gerar conteúdo: {e}"

class MockGeminiClient(GeminiClient):
    def generate_content(self, prompt: str, media_files: List[Dict[str, Any]] | None = None) -> str:
        media_info = ""
        if media_files:
            media_info = f" (com análise de {len(media_files)} arquivos de mídia)"
        
        if "Explique em um relatório conciso" in prompt:
            return f"[Relatório Mock] Esta proposta foi gerada para ser eficaz, combinando o template base com a análise de mídia{media_info}."
        
        return f"[Proposta Mock] Conteúdo gerado com base no prompt e no template{media_info}."

def get_gemini_client() -> GeminiClient:
    if os.getenv("USE_MOCK_AI", "true").lower() == "true":
        print("Using Mock Gemini Client")
        return MockGeminiClient()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("WARNING: GEMINI_API_KEY not found. Using Mock Gemini Client.")
        return MockGeminiClient()
    
    print("Using Real Gemini Client")
    return RealGeminiClient(api_key=api_key)