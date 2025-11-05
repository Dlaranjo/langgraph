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
import re
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()


def clean_json_string(json_str: str) -> str:
    """
    Limpa string JSON removendo caracteres de controle inválidos
    """
    # Remove caracteres de controle (exceto \n, \r, \t que são válidos quando escapados)
    # Remove controle characters ASCII (0-31) exceto os permitidos
    cleaned = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', json_str)
    return cleaned


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

        # Mensagens de log detalhadas
        log_messages = [
            f"🎯 PLANEJANDO PESQUISA: {state['query']}",
            f"✓ {len(queries)} queries de busca geradas:"
        ]
        for i, q in enumerate(queries, 1):
            log_messages.append(f"  {i}. {q}")

        return {
            "search_queries": queries,
            "messages": log_messages,
            "current_iteration": 0
        }

    def search_web(self, state: ResearchState) -> Dict[str, Any]:
        """
        Nó de busca: executa as queries e coleta resultados
        """
        queries = state.get('search_queries', [])
        print(f"\n🔍 BUSCANDO INFORMAÇÕES ({len(queries)} queries)")

        search_results = []
        log_messages = [f"🔍 BUSCANDO INFORMAÇÕES ({len(queries)} queries)"]

        # Verifica se deve usar Tavily ou simulação
        use_tavily = self.tavily_key and self.tavily_key != "sua-chave-tavily-aqui"

        if use_tavily:
            # Busca REAL com Tavily API
            try:
                from tavily import TavilyClient
                tavily_client = TavilyClient(api_key=self.tavily_key)
                print("  🌐 Usando Tavily API (busca real)")
                log_messages.append("  🌐 Usando Tavily API (busca real)")

                for query in queries:
                    try:
                        # Busca real
                        response = tavily_client.search(
                            query=query,
                            search_depth="basic",
                            max_results=3
                        )

                        # Processa resultados
                        num_results = len(response.get('results', []))
                        for item in response.get('results', []):
                            result = SearchResult(
                                source=item.get('url', 'N/A'),
                                title=item.get('title', query),
                                content=item.get('content', ''),
                                relevance_score=item.get('score', 0.5),
                                timestamp=datetime.now().isoformat()
                            )
                            search_results.append(result)

                        log_msg = f"  ✓ Busca real: \"{query[:60]}...\" ({num_results} resultados)"
                        print(log_msg)
                        log_messages.append(log_msg)

                    except Exception as e:
                        error_msg = f"  ⚠️  Erro na busca '{query}': {e}"
                        print(error_msg)
                        log_messages.append(error_msg)
                        # Fallback para simulação em caso de erro
                        result = self._simulate_search(query)
                        search_results.append(result)
                        log_messages.append(f"  → Usando simulação como fallback")

            except ImportError:
                fallback_msg = "  ⚠️  Tavily não instalado, usando simulação"
                print(fallback_msg)
                log_messages.append(fallback_msg)
                use_tavily = False

        if not use_tavily:
            # Simulação com LLM
            sim_msg = "  🤖 Usando simulação com LLM"
            print(sim_msg)
            log_messages.append(sim_msg)

            for query in queries:
                result = self._simulate_search(query)
                search_results.append(result)
                log_msg = f"  ✓ Busca simulada: \"{query[:60]}...\""
                print(log_msg)
                log_messages.append(log_msg)

        log_messages.append(f"✓ Total: {len(search_results)} resultados coletados")

        return {
            "search_results": search_results,
            "messages": log_messages
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
        log_messages = ["✅ VALIDANDO INFORMAÇÕES"]

        results = state.get('search_results', [])
        if not results:
            log_messages.append("  ⚠️  Nenhum resultado para validar")
            return {"validations": [], "conflicts_detected": False, "messages": log_messages}

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

            # Limpa caracteres de controle inválidos
            content = clean_json_string(content)

            validation_data = json.loads(content)

            validations = [
                ValidationResult(**v) for v in validation_data.get('validations', [])
            ]

            conflicts = validation_data.get('conflicts_detected', False)

            log_msg_valid = f"  ✓ {len(validations)} afirmações validadas"
            print(log_msg_valid)
            log_messages.append(log_msg_valid)

            if conflicts:
                conflict_msg = "  ⚠️  Conflitos detectados!"
                print(conflict_msg)
                log_messages.append(conflict_msg)
            else:
                no_conflict_msg = "  ✓ Sem conflitos detectados"
                log_messages.append(no_conflict_msg)

            # Adiciona resumo das validações
            for i, val in enumerate(validations, 1):
                log_messages.append(f"    {i}. {val.claim[:60]}... (confiança: {val.confidence:.0%})")

            log_messages.append(validation_data.get('summary', 'Validação completa'))

            return {
                "validations": validations,
                "conflicts_detected": conflicts,
                "messages": log_messages
            }

        except json.JSONDecodeError as e:
            error_msg = f"  ⚠️  Erro ao parsear validação: {e}"
            print(error_msg)
            log_messages.append(error_msg)

            # Log do conteúdo que falhou (primeiros 200 chars para debug)
            print(f"  Debug: Conteúdo recebido (primeiros 200 chars): {content[:200] if 'content' in locals() else 'N/A'}")

            # Fallback: cria validação básica
            print("  → Criando validação fallback...")
            fallback_validation = ValidationResult(
                claim=f"Informações coletadas sobre: {state['query']}",
                is_validated=True,
                confidence=0.6,
                supporting_sources=[r.source for r in results[:3]],
                reasoning="Validação automática devido a erro no parse. Informações coletadas mas não validadas completamente."
            )

            log_messages.append("  → Usando validação fallback")

            return {
                "validations": [fallback_validation],
                "conflicts_detected": False,
                "messages": log_messages
            }
        except Exception as e:
            error_msg = f"  ⚠️  Erro inesperado na validação: {e}"
            print(error_msg)
            log_messages.append(error_msg)

            # Fallback genérico
            fallback_validation = ValidationResult(
                claim=f"Pesquisa sobre: {state['query']}",
                is_validated=True,
                confidence=0.5,
                supporting_sources=[],
                reasoning="Validação básica devido a erro no processamento."
            )

            return {
                "validations": [fallback_validation],
                "conflicts_detected": False,
                "messages": log_messages
            }

    def synthesize_report(self, state: ResearchState) -> Dict[str, Any]:
        """
        Nó de síntese: cria relatório final com referências
        """
        print(f"\n📝 SINTETIZANDO RELATÓRIO FINAL")
        log_messages = ["📝 SINTETIZANDO RELATÓRIO FINAL"]

        try:
            results = state.get('search_results', [])
            validations = state.get('validations', [])

            log_messages.append(f"  → Processando {len(results)} fontes")
            log_messages.append(f"  → Integrando {len(validations)} validações")

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

Formato do relatório: Markdown profissional

IMPORTANTE: Retorne apenas o conteúdo do relatório em Markdown puro, sem blocos de código ou formatação extra."""

            response = self.llm.invoke([
                SystemMessage(content="Você é um pesquisador acadêmico que escreve relatórios claros e bem referenciados em Markdown."),
                HumanMessage(content=prompt)
            ])

            # Limpa o conteúdo do relatório (remove markdown code blocks se houver)
            report_content = response.content.strip()
            if "```markdown" in report_content:
                report_content = report_content.split("```markdown")[1].split("```")[0].strip()
            elif report_content.startswith("```") and report_content.endswith("```"):
                report_content = report_content[3:-3].strip()

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

            final_msg = f"  ✓ Relatório gerado (confiança: {avg_confidence:.0%})"
            print(final_msg)
            log_messages.append(final_msg)
            log_messages.append(f"  ✓ {len(references)} referências incluídas")
            log_messages.append("✅ Síntese completa")

            return {
                "final_report": report_content,
                "references": references,
                "confidence_level": avg_confidence,
                "messages": log_messages
            }

        except Exception as e:
            error_msg = f"  ⚠️  Erro ao gerar relatório: {e}"
            print(error_msg)
            log_messages.append(error_msg)

            # Relatório fallback
            fallback_report = f"""# Relatório de Pesquisa: {state['query']}

## Resumo

Ocorreu um erro ao gerar o relatório completo, mas a pesquisa foi realizada com sucesso.

### Fontes Consultadas

{len(state.get('search_results', []))} fontes foram consultadas.

### Nível de Confiança

Confiança média: 50%

---

*Relatório gerado automaticamente com informações limitadas devido a erro no processamento.*
"""

            return {
                "final_report": fallback_report,
                "references": [],
                "confidence_level": 0.5,
                "messages": log_messages
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