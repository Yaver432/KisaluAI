import json
import os
from typing import Callable, Dict, List, Any

# Constantes e ramos esperados pelo app.py
RAMOS_PREDEFINIDOS = [
    "Tecnologia e Informática",
    "Engenharia e Construção",
    "Banca e Finanças",
    "Recursos Humanos",
    "Petróleo e Gás",
    "Saúde e Farmacêutica",
    "Comércio e Vendas"
]

TERMOS_POR_RAMO = {ramo: ramo for ramo in RAMOS_PREDEFINIDOS}

ARQUIVO_VAGAS = "vagas.json"
ARQUIVO_POSTS = "publicacoes.json"

def carregar_dados_locais() -> Dict[str, List[Dict[str, Any]]]:
    """Carrega as vagas do arquivo local ou retorna um dicionário vazio."""
    if os.path.exists(ARQUIVO_VAGAS):
        try:
            with open(ARQUIVO_VAGAS, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def carregar_publicacoes() -> List[Dict[str, Any]]:
    """Carrega as publicações informais de redes."""
    if os.path.exists(ARQUIVO_POSTS):
        try:
            with open(ARQUIVO_POSTS, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def executar_pipeline_completo(localizacao: str, ramo: str, limite: int, progress_callback: Callable = None):
    """Executa a extração/sincronização de vagas consolidadas."""
    if progress_callback:
        progress_callback(0.2, "Buscando oportunidades...")
        progress_callback(0.6, "Processando requisitos com IA...")
        progress_callback(1.0, "Concluído!")
    
    # Exemplo de persistência dos dados:
    dados = carregar_dados_locais()
    # Insira aqui a sua lógica de scraping real
    return dados

# Alias caso use executar_pipeline_vagas
executar_pipeline_vagas = executar_pipeline_completo

def executar_pipeline_publicacoes(localizacao: str, progress_callback: Callable = None):
    """Executa a captura de posts e anúncios informais."""
    if progress_callback:
        progress_callback(0.5, "Monitorando publicações...")
        progress_callback(1.0, "Finalizado!")
    return carregar_publicacoes()

def responder_duvida_rh(pergunta: str, historico_chat: list, dados_vagas: dict) -> str:
    """Processa a dúvida com o LLM/IA baseado nas vagas existentes."""
    # Coloque aqui a chamada para sua API de IA (ex: OpenAI, Anthropic, Gemini, Groq)
    return f"Resposta Kisalu.IA: Analisei a sua pergunta '{pergunta}'. Atualmente existem vagas mapeadas no sistema prontas para consulta."