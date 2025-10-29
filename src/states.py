"""
Estados do Agente Pesquisador
Define a estrutura de dados que flui pelo grafo
"""
from typing import List, Dict, Optional, Annotated
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
import operator


class SearchResult(BaseModel):
    """Resultado de uma busca individual"""
    source: str = Field(description="URL ou nome da fonte")
    title: str = Field(description="Título do conteúdo")
    content: str = Field(description="Conteúdo extraído")
    relevance_score: float = Field(default=0.0, description="Score de relevância (0-1)")
    timestamp: str = Field(default="", description="Timestamp da busca")


class ValidationResult(BaseModel):
    """Resultado da validação de uma informação"""
    claim: str = Field(description="Afirmação sendo validada")
    is_validated: bool = Field(description="Se a informação foi validada")
    confidence: float = Field(description="Confiança na validação (0-1)")
    supporting_sources: List[str] = Field(default_factory=list)
    conflicting_info: Optional[str] = None
    reasoning: str = Field(default="", description="Raciocínio da validação")


class ResearchState(TypedDict):
    """
    Estado global do agente de pesquisa

    Esse estado é passado entre todos os nós do grafo
    """
    # Input inicial
    query: str
    max_iterations: int

    # Resultados de busca
    search_results: Annotated[List[SearchResult], operator.add]
    search_queries: Annotated[List[str], operator.add]

    # Validação
    validations: Annotated[List[ValidationResult], operator.add]
    conflicts_detected: bool

    # Síntese final
    final_report: str
    references: List[Dict[str, str]]
    confidence_level: float

    # Controle de fluxo
    current_iteration: int
    needs_more_research: bool
    error: Optional[str]

    # Mensagens intermediárias (para debug)
    messages: Annotated[List[str], operator.add]
