"""
Script de teste rápido para Tavily API
"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_tavily():
    """Testa se Tavily está configurado corretamente"""
    tavily_key = os.getenv("TAVILY_API_KEY")

    print("🧪 Testando Tavily API\n")
    print(f"TAVILY_API_KEY carregada: {'✓ Sim' if tavily_key else '✗ Não'}")

    if not tavily_key or tavily_key == "sua-chave-tavily-aqui":
        print("\n⚠️  Tavily não configurada. Configure com:")
        print("   export TAVILY_API_KEY='sua-chave'")
        print("\n   Obtenha gratuitamente em: https://tavily.com/")
        return False

    print(f"Key: {tavily_key[:20]}...")

    try:
        from tavily import TavilyClient
        print("✓ Biblioteca tavily-python instalada")

        client = TavilyClient(api_key=tavily_key)
        print("✓ Cliente Tavily inicializado")

        # Teste simples
        print("\n🔍 Testando busca...")
        response = client.search(
            query="LangGraph tutorial",
            search_depth="basic",
            max_results=2
        )

        print(f"✓ Busca realizada com sucesso!")
        print(f"  Resultados obtidos: {len(response.get('results', []))}")

        for i, result in enumerate(response.get('results', [])[:2], 1):
            print(f"\n  {i}. {result.get('title', 'Sem título')}")
            print(f"     URL: {result.get('url', 'N/A')}")
            print(f"     Score: {result.get('score', 0):.2f}")

        print("\n✅ Tavily API está funcionando corretamente!")
        return True

    except ImportError:
        print("\n❌ Biblioteca tavily-python não instalada")
        print("   Instale com: pip install tavily-python")
        return False
    except Exception as e:
        print(f"\n❌ Erro ao testar Tavily: {e}")
        print(f"   Tipo do erro: {type(e).__name__}")
        return False

if __name__ == "__main__":
    test_tavily()
