# 🔬 Agente Pesquisador com Validação

Agente de IA construído com **LangGraph** que realiza pesquisas em profundidade, valida informações cruzando múltiplas fontes, e gera relatórios confiáveis com referências.

## 🎨 Interface Visual

**Novidade!** Agora com interface web interativa!

```bash
# Inicie a interface
./scripts/start_app.sh

# Ou diretamente
streamlit run app.py
```

**Acesse:** http://localhost:8501

### Features da Interface:
- 🎯 Pesquisa interativa com feedback visual
- 📊 Gráficos e métricas em tempo real
- 📚 Visualização de referências e validações
- 📜 Histórico de pesquisas
- ⬇️ Download de relatórios
- 🎨 Design moderno e responsivo

**Documentação completa:** [INTERFACE.md](docs/INTERFACE.md)

## 🎯 Características

- **Pesquisa Inteligente**: Gera queries específicas baseadas na pergunta
- **Validação Cruzada**: Compara informações de múltiplas fontes
- **Detecção de Conflitos**: Identifica contradições e informações conflitantes
- **Iteração Adaptativa**: Busca mais informações se necessário
- **Relatórios Estruturados**: Gera relatórios em Markdown com referências
- **Níveis de Confiança**: Calcula confiança nas informações coletadas

## 🏗️ Arquitetura

```
START
  ↓
plan_research (gera queries de busca)
  ↓
search_web (coleta informações)
  ↓
validate_information (cruza fontes e detecta conflitos)
  ↓
decide_next_step (decisão condicional)
  ↓
  ├─→ [needs_more_research] → search_web (loop)
  └─→ [sufficient_info] → synthesize_report
      ↓
    END
```

## 📦 Instalação

```bash
# Clone o repositório
cd langgraph

# Instale as dependências
pip install -r requirements.txt

# Configure as API keys
cp .env.example .env
# Edite .env e adicione sua ANTHROPIC_API_KEY
```

## 🔑 Configuração

### Obrigatório: Anthropic API

1. Acesse https://console.anthropic.com/
2. Crie uma API key
3. Configure no arquivo `.env`:

```bash
ANTHROPIC_API_KEY=sua-chave-aqui
```

### Opcional: Tavily API (Busca Web Real)

**NOVO!** Agora suporta busca web real com Tavily.

1. Acesse https://tavily.com/ (plano FREE: 1.000 créditos/mês)
2. Obtenha sua API key gratuita
3. Configure no `.env`:

```bash
TAVILY_API_KEY=tvly-dev-sua-chave-aqui
```

4. Na interface, marque: ☑️ **Usar Tavily API (busca real)**

**Sem Tavily?** O agente usa simulação com LLM automaticamente.

📖 **Guia completo:** [TAVILY_SETUP.md](docs/TAVILY_SETUP.md)

## 🚀 Uso

### Uso Básico

```python
from src.agent import ResearchAgent

# Inicializa o agente
agent = ResearchAgent(max_iterations=1)

# Realiza uma pesquisa
result = agent.research(
    query="Quais são os principais benefícios da computação quântica?"
)

# Acessa os resultados
print(result["report"])           # Relatório final
print(result["references"])       # Lista de fontes
print(result["confidence"])       # Nível de confiança (0-1)
```

### Exemplo Completo

```python
from src.agent import ResearchAgent

agent = ResearchAgent(max_iterations=2)

result = agent.research(
    query="Compare microserviços vs arquitetura monolítica"
)

print(f"📋 Relatório:\n{result['report']}")
print(f"\n💡 Confiança: {result['confidence']:.0%}")
print(f"📚 Fontes consultadas: {result['search_results_count']}")
print(f"✅ Validações realizadas: {result['validations_count']}")
print(f"⚠️ Conflitos detectados: {result['conflicts_detected']}")
```

### Modo Interativo

```bash
python tests/test_agent.py
```

Isso executará:
1. Testes automatizados
2. Visualização do grafo
3. Modo interativo (opcional)

## 📊 Estrutura do Projeto

```
langgraph/
├── src/                  # Código fonte
│   ├── __init__.py
│   ├── agent.py          # Grafo principal e orquestração
│   ├── states.py         # Definição de estados (TypedDict)
│   └── nodes.py          # Implementação dos nós do grafo
├── tests/                # Testes
│   ├── __init__.py
│   ├── test_agent.py     # Testes do agente
│   └── test_tavily.py    # Testes da API Tavily
├── docs/                 # Documentação
│   ├── INTERFACE.md      # Guia da interface
│   ├── TAVILY_SETUP.md   # Guia de configuração Tavily
│   └── QUICKSTART.md     # Guia rápido
├── scripts/              # Scripts utilitários
│   └── start_app.sh      # Script para iniciar a interface
├── app.py                # Interface Streamlit
├── requirements.txt      # Dependências
├── .env                  # Variáveis de ambiente (não versionado)
├── .gitignore            # Arquivos ignorados pelo Git
└── README.md             # Este arquivo
```

## 🧩 Componentes

### Estados (src/states.py)

Define a estrutura de dados que flui pelo grafo:

- `ResearchState`: Estado global
- `SearchResult`: Resultado individual de busca
- `ValidationResult`: Resultado de validação

### Nós (src/nodes.py)

Implementa a lógica de cada etapa:

- `plan_research`: Gera queries de busca inteligentes
- `search_web`: Executa buscas e coleta informações
- `validate_information`: Cruza fontes e detecta conflitos
- `synthesize_report`: Gera relatório final
- `decide_next_step`: Decide se precisa mais pesquisa

### Agente (src/agent.py)

Orquestra o grafo e fornece a interface principal.

## 🎨 Visualização do Grafo

```python
agent = ResearchAgent()
agent.visualize()
```

Isso gerará um arquivo `.mmd` que você pode visualizar em https://mermaid.live/

## 🧪 Testes

O arquivo `tests/test_agent.py` inclui:

- `test_basic_research()`: Teste de pesquisa simples
- `test_complex_research()`: Teste com comparação
- `test_technical_research()`: Teste técnico
- `interactive_mode()`: Modo interativo de perguntas

Execute todos os testes:

```bash
python tests/test_agent.py
```

## 🔧 Configurações Avançadas

### Personalizar Iterações

```python
agent = ResearchAgent(max_iterations=3)  # Até 3 rodadas de pesquisa
```

### Usar API de Busca Real

Por padrão, o agente simula resultados de busca usando o LLM. Para usar busca web real:

1. Obtenha uma API key do Tavily: https://tavily.com/
2. Configure no `.env`:
   ```bash
   TAVILY_API_KEY=sua-chave-tavily
   ```
3. Na interface, marque a opção "Usar Tavily API (busca real)"

## 💡 Casos de Uso

- **Pesquisa Acadêmica**: Coleta e valida informações para trabalhos
- **Due Diligence**: Investiga empresas/produtos
- **Fact-Checking**: Verifica afirmações cruzando fontes
- **Análise Competitiva**: Compara soluções/tecnologias
- **Revisão de Literatura**: Mapeia estado da arte de um tópico

## 🚧 Melhorias Futuras

- [ ] Integração com mais APIs de busca (Serper, Brave, etc)
- [ ] Sistema de cache de resultados
- [ ] Exportação de relatórios (PDF, HTML)
- [ ] Interface web com Streamlit
- [ ] Suporte a documentos locais (PDFs, etc)
- [ ] Busca em bases acadêmicas (arXiv, PubMed)
- [ ] Sistema de citações acadêmicas (ABNT, APA)

## 📚 Recursos

- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [Anthropic API](https://docs.anthropic.com/)
- [Tavily Search API](https://docs.tavily.com/)

## 🤝 Contribuindo

Sugestões e PRs são bem-vindos!

## 📄 Licença

MIT License

---

**Desenvolvido com LangGraph e Claude 🚀**
