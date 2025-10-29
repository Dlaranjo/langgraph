"""
Script de Teste do Agente Pesquisador

Exemplos de uso e validação do agente
"""
import os
from src.agent import ResearchAgent
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()


def test_basic_research():
    """Teste básico de pesquisa"""
    print("\n" + "🧪 TESTE 1: Pesquisa Básica".center(80, "="))

    agent = ResearchAgent(max_iterations=1)

    result = agent.research(
        query="O que é LangGraph e para que serve?"
    )

    assert result["report"], "Relatório não foi gerado"
    assert result["references"], "Referências não foram coletadas"
    assert result["confidence"] > 0, "Confiança deve ser maior que 0"

    print("\n✅ TESTE 1 PASSOU")
    print(f"   Relatório: {len(result['report'])} caracteres")
    print(f"   Referências: {len(result['references'])}")
    print(f"   Confiança: {result['confidence']:.0%}")

    return result


def test_complex_research():
    """Teste com pergunta mais complexa"""
    print("\n" + "🧪 TESTE 2: Pesquisa Complexa".center(80, "="))

    agent = ResearchAgent(max_iterations=2)

    result = agent.research(
        query="Compare as vantagens e desvantagens de usar microserviços versus arquitetura monolítica"
    )

    assert result["validations_count"] > 0, "Deve ter validações"
    assert result["search_results_count"] >= 3, "Deve ter múltiplos resultados"

    print("\n✅ TESTE 2 PASSOU")
    print(f"   Validações: {result['validations_count']}")
    print(f"   Resultados: {result['search_results_count']}")
    print(f"   Conflitos: {'Sim' if result['conflicts_detected'] else 'Não'}")

    return result


def test_technical_research():
    """Teste com tópico técnico"""
    print("\n" + "🧪 TESTE 3: Pesquisa Técnica".center(80, "="))

    agent = ResearchAgent(max_iterations=1)

    result = agent.research(
        query="Explique como funciona o algoritmo de consensus Raft em sistemas distribuídos"
    )

    print("\n✅ TESTE 3 PASSOU")
    print(f"   Confiança: {result['confidence']:.0%}")

    return result


def interactive_mode():
    """Modo interativo para testar o agente"""
    print("\n" + "🎮 MODO INTERATIVO".center(80, "="))
    print("Digite suas perguntas (ou 'sair' para terminar)\n")

    agent = ResearchAgent(max_iterations=1)

    while True:
        query = input("\n🔍 Sua pergunta: ").strip()

        if query.lower() in ['sair', 'exit', 'quit', '']:
            print("\n👋 Até logo!")
            break

        try:
            result = agent.research(query)

            print("\n" + "="*80)
            print("📋 RELATÓRIO")
            print("="*80)
            print(result["report"])

            print("\n" + "="*80)
            print("📚 REFERÊNCIAS")
            print("="*80)
            for i, ref in enumerate(result["references"], 1):
                print(f"{i}. {ref['source']}")

            print(f"\n💡 Confiança: {result['confidence']:.0%}")

        except Exception as e:
            print(f"\n❌ Erro: {e}")
            import traceback
            traceback.print_exc()


def demo_visualization():
    """Demonstra visualização do grafo"""
    print("\n" + "🎨 VISUALIZAÇÃO DO GRAFO".center(80, "="))

    agent = ResearchAgent()
    agent.visualize()


def main():
    """Executa todos os testes"""
    print("\n" + "🚀 INICIANDO TESTES DO AGENTE PESQUISADOR".center(80, "=") + "\n")

    # Verifica se tem API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  AVISO: ANTHROPIC_API_KEY não configurada")
        print("   Configure com: export ANTHROPIC_API_KEY='sua-chave'")
        return

    try:
        # Testes automatizados
        test_basic_research()
        test_complex_research()
        test_technical_research()

        # Visualização
        demo_visualization()

        print("\n" + "✅ TODOS OS TESTES PASSARAM".center(80, "=") + "\n")

        # Pergunta se quer modo interativo
        if input("\n🎮 Deseja entrar no modo interativo? (s/n): ").lower() == 's':
            interactive_mode()

    except Exception as e:
        print(f"\n❌ ERRO NOS TESTES: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
