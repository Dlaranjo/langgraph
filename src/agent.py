"""
Agente Pesquisador com Validação usando LangGraph

Arquitetura do Grafo:
    START
      ↓
    plan_research (gera queries)
      ↓
    search_web (busca informações)
      ↓
    validate_information (cruza fontes)
      ↓
    decide_next_step
      ↓
    [se needs_more_research] → search_web (loop)
    [senão] → synthesize_report
      ↓
    END
"""
from typing import Optional
from langgraph.graph import StateGraph, END
from .states import ResearchState
from .nodes import ResearchNodes
import os


class ResearchAgent:
    """Agente de Pesquisa com Validação de Fontes"""

    def __init__(
        self,
        anthropic_api_key: Optional[str] = None,
        tavily_api_key: Optional[str] = None,
        max_iterations: int = 2
    ):
        """
        Inicializa o agente de pesquisa

        Args:
            anthropic_api_key: API key da Anthropic (ou via ANTHROPIC_API_KEY env)
            tavily_api_key: API key do Tavily (ou via TAVILY_API_KEY env)
            max_iterations: Número máximo de iterações de pesquisa
        """
        self.nodes = ResearchNodes(
            api_key=anthropic_api_key,
            tavily_api_key=tavily_api_key
        )
        self.max_iterations = max_iterations
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Constrói o grafo do agente"""

        # Define o grafo com o estado
        workflow = StateGraph(ResearchState)

        # Adiciona os nós
        workflow.add_node("plan_research", self.nodes.plan_research)
        workflow.add_node("search_web", self.nodes.search_web)
        workflow.add_node("validate_information", self.nodes.validate_information)
        workflow.add_node("synthesize_report", self.nodes.synthesize_report)

        # Define o fluxo
        workflow.set_entry_point("plan_research")

        # plan_research → search_web
        workflow.add_edge("plan_research", "search_web")

        # search_web → validate_information
        workflow.add_edge("search_web", "validate_information")

        # validate_information → decide_next_step (condicional)
        workflow.add_conditional_edges(
            "validate_information",
            self.nodes.decide_next_step,
            {
                "research_more": "search_web",  # Loop para mais pesquisa
                "synthesize": "synthesize_report"  # Vai para síntese
            }
        )

        # synthesize_report → END
        workflow.add_edge("synthesize_report", END)

        # Compila o grafo
        return workflow.compile()

    def research(self, query: str, max_iterations: Optional[int] = None) -> dict:
        """
        Executa uma pesquisa completa sobre um tópico

        Args:
            query: Pergunta ou tópico de pesquisa
            max_iterations: Override do número máximo de iterações

        Returns:
            Dict com o relatório final, referências e metadados
        """
        print("\n" + "="*80)
        print(f"🔬 INICIANDO PESQUISA: {query}")
        print("="*80)

        # Estado inicial
        initial_state = {
            "query": query,
            "max_iterations": max_iterations or self.max_iterations,
            "search_results": [],
            "search_queries": [],
            "validations": [],
            "conflicts_detected": False,
            "final_report": "",
            "references": [],
            "confidence_level": 0.0,
            "current_iteration": 0,
            "needs_more_research": True,
            "error": None,
            "messages": []
        }

        # Executa o grafo
        try:
            final_state = self.graph.invoke(initial_state)

            print("\n" + "="*80)
            print("✅ PESQUISA CONCLUÍDA")
            print("="*80)

            # Garante que todos os campos existem com valores padrão
            return {
                "report": final_state.get("final_report", "Erro ao gerar relatório"),
                "references": final_state.get("references", []),
                "confidence": final_state.get("confidence_level", 0.0),
                "search_results_count": len(final_state.get("search_results", [])),
                "validations_count": len(final_state.get("validations", [])),
                "conflicts_detected": final_state.get("conflicts_detected", False),
                "iterations": final_state.get("current_iteration", 0),
                "full_state": final_state
            }

        except Exception as e:
            print(f"\n❌ ERRO NO GRAFO: {e}")
            import traceback
            traceback.print_exc()

            # Retorna erro estruturado
            return {
                "report": f"# Erro ao Executar Pesquisa\n\nOcorreu um erro durante a pesquisa: {str(e)}",
                "references": [],
                "confidence": 0.0,
                "search_results_count": 0,
                "validations_count": 0,
                "conflicts_detected": False,
                "iterations": 0,
                "full_state": {"error": str(e)}
            }

    async def aresearch(self, query: str, max_iterations: Optional[int] = None) -> dict:
        """Versão assíncrona de research()"""
        initial_state = {
            "query": query,
            "max_iterations": max_iterations or self.max_iterations,
            "search_results": [],
            "search_queries": [],
            "validations": [],
            "conflicts_detected": False,
            "final_report": "",
            "references": [],
            "confidence_level": 0.0,
            "current_iteration": 0,
            "needs_more_research": True,
            "error": None,
            "messages": []
        }

        final_state = await self.graph.ainvoke(initial_state)

        return {
            "report": final_state["final_report"],
            "references": final_state["references"],
            "confidence": final_state["confidence_level"],
            "full_state": final_state
        }

    def visualize(self, output_path: str = "research_agent_graph.png"):
        """
        Gera visualização do grafo (requer graphviz)

        Args:
            output_path: Caminho para salvar a imagem
        """
        try:
            from langchain_core.runnables.graph import MermaidDrawMethod

            # Gera a visualização em formato Mermaid
            mermaid_code = self.graph.get_graph().draw_mermaid()

            print(f"\n📊 Código Mermaid do Grafo:")
            print(mermaid_code)

            # Salva o código Mermaid em arquivo
            mermaid_path = output_path.replace('.png', '.mmd')
            with open(mermaid_path, 'w') as f:
                f.write(mermaid_code)

            print(f"\n✅ Código Mermaid salvo em: {mermaid_path}")
            print(f"   Visualize em: https://mermaid.live/")

        except Exception as e:
            print(f"⚠️  Erro ao gerar visualização: {e}")
            print("    Para visualizar, instale: pip install grandalf")


def main():
    """Exemplo de uso"""
    # Certifique-se de ter a API key configurada
    # export ANTHROPIC_API_KEY="sua-chave-aqui"

    agent = ResearchAgent(max_iterations=1)

    # Exemplo de pesquisa
    result = agent.research(
        query="Quais são os principais benefícios e riscos da inteligência artificial generativa?"
    )

    print("\n" + "="*80)
    print("📋 RELATÓRIO FINAL")
    print("="*80)
    print(result["report"])

    print("\n" + "="*80)
    print("📚 REFERÊNCIAS")
    print("="*80)
    for i, ref in enumerate(result["references"], 1):
        print(f"{i}. {ref['title']}")
        print(f"   {ref['source']}")

    print("\n" + "="*80)
    print("📊 METADADOS")
    print("="*80)
    print(f"Confiança: {result['confidence']:.0%}")
    print(f"Resultados: {result['search_results_count']}")
    print(f"Validações: {result['validations_count']}")
    print(f"Conflitos detectados: {result['conflicts_detected']}")
    print(f"Iterações: {result['iterations']}")

    # Visualiza o grafo
    agent.visualize()


if __name__ == "__main__":
    main()
