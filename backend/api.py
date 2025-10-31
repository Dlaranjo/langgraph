"""
FastAPI Backend para Agente Pesquisador
API REST para integração com frontend moderno (Next.js)
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import sys
import os
from datetime import datetime

# Adiciona o diretório pai ao path para importar src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import ResearchAgent

# Modelos Pydantic
class ResearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Pergunta de pesquisa")
    max_iterations: int = Field(default=1, ge=1, le=3, description="Número máximo de iterações")
    anthropic_api_key: str = Field(..., min_length=1, description="Chave API Anthropic")
    tavily_api_key: Optional[str] = Field(None, description="Chave API Tavily (opcional)")

class ResearchResponse(BaseModel):
    query: str
    timestamp: str
    report: str
    confidence: float
    search_results_count: int
    validations_count: int
    iterations: int
    conflicts_detected: bool
    references: List[Dict[str, Any]]
    full_state: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str

# Inicializa FastAPI
app = FastAPI(
    title="Agente Pesquisador API",
    description="API REST para pesquisa inteligente com validação de fontes",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS - permite requisições do frontend Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "*"  # Permite todas (dev apenas - remover em produção)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints
@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check detalhado"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/research", response_model=ResearchResponse)
async def research(request: ResearchRequest):
    """
    Executa uma pesquisa usando o ResearchAgent

    Args:
        request: Requisição com query e configurações

    Returns:
        ResearchResponse com resultados completos
    """
    try:
        # Inicializa o agente
        agent = ResearchAgent(
            anthropic_api_key=request.anthropic_api_key,
            tavily_api_key=request.tavily_api_key,
            max_iterations=request.max_iterations
        )

        # Executa a pesquisa
        result = agent.research(
            query=request.query,
            max_iterations=request.max_iterations
        )

        # Adiciona metadados
        result['query'] = request.query
        result['timestamp'] = datetime.now().isoformat()

        # Garante que references existe
        if 'references' not in result:
            result['references'] = []

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro durante a pesquisa: {str(e)}"
        )

@app.get("/api/config")
async def get_config():
    """
    Retorna configurações do servidor
    """
    return {
        "max_iterations_allowed": 3,
        "min_iterations_allowed": 1,
        "default_iterations": 1,
        "tavily_optional": True,
        "supported_features": [
            "research",
            "validation",
            "references",
            "confidence_scoring",
            "conflict_detection"
        ]
    }

if __name__ == "__main__":
    import uvicorn

    print("🚀 Iniciando FastAPI Backend...")
    print("📡 API Docs: http://localhost:8000/docs")
    print("🔬 Agente Pesquisador pronto!")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
