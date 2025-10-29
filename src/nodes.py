"""
Nós do Grafo - Implementação da lógica de cada etapa
"""
from typing import Any, Dict, Optional
from datetime import datetime
from .states import ResearchState, SearchResult, ValidationResult
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
import json
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()


class ResearchNodes:
    """Implementação de todos os nós do grafo de pesquisa"""

    def __init__(self, api_key: Optional[str] = None, tavily_api_key: Optional[str] = None):
        """Inicializa os nós com as APIs necessárias"""
        self.llm = ChatAnthropic(
            model="claude-3-haiku-20240307",
            api_key=api_key or os.getenv("ANTHROPIC_API_KEY"),
            temperature=0.3
        )

        # Para busca web, vamos usar Tavily (você pode substituir por outra API)
        self.tavily_key = tavily_api_key or os.getenv("TAVILY_API_KEY")

    def plan_research(self, state: ResearchState) -> Dict[str, Any]:
        """
        Nó inicial: planeja a pesquisa e gera queries de busca
        """
        print(f"\n🎯 PLANEJANDO PESQUISA: {state['query']}")

        prompt = f"""Você é um pesquisador experiente. Dada a seguinte pergunta de pesquisa,
gere 3-5 queries de busca específicas e complementares que ajudarão a obter uma resposta completa.

Pergunta: {state['query']}

Retorne apenas as queries, uma por linha, sem numeração ou formatação extra."""

        response = self.llm.invoke([
            SystemMessage(content="Você é um assistente de pesquisa expert."),
            HumanMessage(content=prompt)
        ])

        queries = [q.strip() for q in response.content.strip().split('\n') if q.strip()]

        return {
            "search_queries": queries,
            "messages": [f"Planejamento completo: {len(queries)} queries geradas"],
            "current_iteration": 0
        }

    def search_web(self, state: ResearchState) -> Dict[str, Any]:
        """
        Nó de busca: executa as queries e coleta resultados
        """
        print(f"\n🔍 BUSCANDO INFORMAÇÕES ({len(state.get('search_queries', []))} queries)")

        search_results = []

        # Verifica se deve usar Tavily ou simulação
        use_tavily = self.tavily_key and self.tavily_key != "sua-chave-tavily-aqui"

        if use_tavily:
            # Busca REAL com Tavily API
            try:
                from tavily import TavilyClient
                tavily_client = TavilyClient(api_key=self.tavily_key)
                print("  🌐 Usando Tavily API (busca real)")

                for query in state.get('search_queries', []):
                    try:
                        # Busca real
                        response = tavily_client.search(
                            query=query,
                            search_depth="basic",
                            max_results=3
                        )

                        # Processa resultados
                        for item in response.get('results', []):
                            result = SearchResult(
                                source=item.get('url', 'N/A'),
                                title=item.get('title', query),
                                content=item.get('content', ''),
                                relevance_score=item.get('score', 0.5),
                                timestamp=datetime.now().isoformat()
                            )
                            search_results.append(result)

                        print(f"  ✓ Busca real: {query[:60]}... ({len(response.get('results', []))} resultados)")

                    except Exception as e:
                        print(f"  ⚠️  Erro na busca '{query}': {e}")
                        # Fallback para simulação em caso de erro
                        result = self._simulate_search(query)
                        search_results.append(result)

            except ImportError:
                print("  ⚠️  Tavily não instalado, usando simulação")
                use_tavily = False

        if not use_tavily:
            # Simulação com LLM
            print("  🤖 Usando simulação com LLM")
            for query in state.get('search_queries', []):
                result = self._simulate_search(query)
                search_results.append(result)
                print(f"  ✓ Busca simulada: {query[:60]}...")

        return {
            "search_results": search_results,
            "messages": [f"Busca completa: {len(search_results)} resultados coletados"]
        }

    def _simulate_search(self, query: str) -> SearchResult:
        """Simulação de busca com LLM"""
        prompt = f"""Simule um resultado de busca para: "{query}"

Forneça informações factuais e realistas sobre este tópico.
Seja específico e inclua detalhes verificáveis."""

        response = self.llm.invoke([
            SystemMessage(content="Você é um motor de busca que retorna informações factuais."),
            HumanMessage(content=prompt)
        ])

        return SearchResult(
            source=f"fonte-simulada-{hash(query) % 1000}.com",
            title=f"Resultado para: {query[:50]}",
            content=response.content,
            relevance_score=0.85,
            timestamp=datetime.now().isoformat()
        )

    def validate_information(self, state: ResearchState) -> Dict[str, Any]:
        """
        Nó de validação: cruza informações e detecta conflitos
        """
        print(f"\n✅ VALIDANDO INFORMAÇÕES")

        results = state.get('search_results', [])
        if not results:
            return {"validations": [], "conflicts_detected": False}

        # Extrai claims principais de cada resultado
        all_content = "\n\n---\n\n".join([
            f"FONTE {i+1} ({r.source}):\n{r.content}"
            for i, r in enumerate(results)
        ])

        prompt = f"""Analise as seguintes informações de múltiplas fontes sobre: "{state['query']}"

{all_content}

Sua tarefa:
1. Identifique as principais afirmações/claims
2. Verifique se há consenso entre as fontes
3. Detecte conflitos ou contradições
4. Avalie a confiabilidade de cada afirmação

Retorne um JSON com este formato:
{{
  "validations": [
    {{
      "claim": "afirmação identificada",
      "is_validated": true/false,
      "confidence": 0.0-1.0,
      "supporting_sources": ["fonte1", "fonte2"],
      "conflicting_info": "descrição de conflitos se houver",
      "reasoning": "explicação da validação"
    }}
  ],
  "conflicts_detected": true/false,
  "summary": "resumo da validação"
}}"""

        response = self.llm.invoke([
            SystemMessage(content="Você é um analista de informações que valida fatos cruzando fontes."),
            HumanMessage(content=prompt)
        ])

        # Parse da resposta
        try:
            # Extrai JSON da resposta
            content = response.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            validation_data = json.loads(content)

            validations = [
                ValidationResult(**v) for v in validation_data.get('validations', [])
            ]

            conflicts = validation_data.get('conflicts_detected', False)

            print(f"  ✓ {len(validations)} afirmações validadas")
            if conflicts:
                print(f"  ⚠️  Conflitos detectados!")

            return {
                "validations": validations,
                "conflicts_detected": conflicts,
                "messages": [validation_data.get('summary', 'Validação completa')]
            }

        except json.JSONDecodeError as e:
            print(f"  ⚠️  Erro ao parsear validação: {e}")
            return {
                "validations": [],
                "conflicts_detected": False,
                "messages": ["Erro na validação - usando resposta como texto"],
                "error": str(e)
            }

    def synthesize_report(self, state: ResearchState) -> Dict[str, Any]:
        """
        Nó de síntese: cria relatório final com referências
        """
        print(f"\n📝 SINTETIZANDO RELATÓRIO FINAL")

        results = state.get('search_results', [])
        validations = state.get('validations', [])

        # Prepara contexto para síntese
        sources_summary = "\n\n".join([
            f"FONTE {i+1}: {r.source}\n{r.content[:500]}..."
            for i, r in enumerate(results)
        ])

        validations_summary = "\n".join([
            f"- {v.claim} (confiança: {v.confidence:.0%})"
            for v in validations
        ])

        prompt = f"""Com base na pesquisa realizada sobre "{state['query']}", crie um relatório final completo.

FONTES CONSULTADAS:
{sources_summary}

VALIDAÇÕES:
{validations_summary}

Crie um relatório que:
1. Responda diretamente à pergunta original
2. Apresente as informações validadas
3. Mencione incertezas ou conflitos encontrados
4. Cite as fontes apropriadamente
5. Indique o nível de confiança geral

Formato do relatório: Markdown profissional"""

        response = self.llm.invoke([
            SystemMessage(content="Você é um pesquisador acadêmico que escreve relatórios claros e bem referenciados."),
            HumanMessage(content=prompt)
        ])

        # Calcula confiança média
        avg_confidence = sum(v.confidence for v in validations) / len(validations) if validations else 0.5

        # Prepara referências
        references = [
            {
                "source": r.source,
                "title": r.title,
                "url": r.source
            }
            for r in results
        ]

        print(f"  ✓ Relatório gerado (confiança: {avg_confidence:.0%})")

        return {
            "final_report": response.content,
            "references": references,
            "confidence_level": avg_confidence,
            "messages": ["Síntese completa"]
        }

    def decide_next_step(self, state: ResearchState) -> str:
        """
        Nó de decisão: determina se precisa de mais pesquisa
        """
        current_iter = state.get('current_iteration', 0)
        max_iter = state.get('max_iterations', 1)
        conflicts = state.get('conflicts_detected', False)
        validations = state.get('validations', [])

        # Se tem conflitos e ainda tem iterações disponíveis
        if conflicts and current_iter < max_iter:
            print(f"\n🔄 Conflitos detectados - Nova iteração necessária")
            return "research_more"

        # Se tem poucas validações e ainda pode iterar
        if len(validations) < 3 and current_iter < max_iter:
            print(f"\n🔄 Informações insuficientes - Nova iteração necessária")
            return "research_more"

        print(f"\n✅ Pesquisa completa - Gerando relatório final")
        return "synthesize"