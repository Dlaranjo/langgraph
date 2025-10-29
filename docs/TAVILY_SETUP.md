# 🌐 Guia de Configuração do Tavily

## O que mudou?

O agente agora suporta **busca web REAL** usando a API do Tavily! Antes só simulava buscas usando o LLM.

### Antes (Simulação):
```
fonte-simulada-221.com
fonte-simulada-191.com
```

### Depois (Tavily Real):
```
https://www.datacamp.com/tutorial/langgraph-tutorial
https://langchain-ai.github.io/langgraph/concepts/
https://python.langchain.com/docs/langgraph/
```

---

## 🎯 Como Configurar

### 1. Obtenha uma API Key Gratuita

1. Acesse: https://tavily.com/
2. Faça cadastro (gratuito)
3. Copie sua API Key
4. **Plano FREE:** 1.000 créditos/mês (suficiente!)

### 2. Configure a Key

#### Opção A: Variável de Ambiente (Recomendado)

```bash
export TAVILY_API_KEY="tvly-dev-sua-chave-aqui"
```

Ou adicione no arquivo `.env`:
```bash
TAVILY_API_KEY=tvly-dev-sua-chave-aqui
```

#### Opção B: Direto na Interface

1. Abra a interface: `./start_app.sh`
2. Na sidebar, marque: ☑️ **Usar Tavily API (busca real)**
3. Cole sua API Key no campo que aparecer
4. Verá: ✓ Tavily API Key configurada

---

## 🔍 Testando

### Teste Rápido

```bash
python3 test_tavily.py
```

Resultado esperado:
```
🧪 Testando Tavily API
✓ Busca realizada com sucesso!
✅ Tavily API está funcionando corretamente!
```

### Teste na Interface

1. Inicie: `./start_app.sh`
2. Na sidebar:
   - ☑️ **Usar Tavily API (busca real)**
   - Insira sua key
3. Faça uma pergunta
4. Veja no log:
   ```
   🌐 Usando Tavily API (busca real)
   ✓ Busca real: [query]... (3 resultados)
   ```

---

## 📊 Como Funciona

### Fluxo de Decisão

```
┌─────────────────────┐
│ Usuário faz         │
│ uma pergunta        │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Tavily Key          │
│ configurada?        │
└──────┬──────────────┘
       │
  SIM  │  NÃO
   ┌───┴───┐
   │       │
   ▼       ▼
┌─────┐ ┌─────────┐
│Tavily│ │Simulação│
│(real)│ │  (LLM) │
└─────┘ └─────────┘
   │       │
   └───┬───┘
       ▼
┌─────────────────────┐
│ Resultados da       │
│ pesquisa            │
└─────────────────────┘
```

### Código (nodes.py)

```python
# Verifica se Tavily está configurada
use_tavily = self.tavily_key and self.tavily_key != "sua-chave-tavily-aqui"

if use_tavily:
    # Busca REAL
    from tavily import TavilyClient
    tavily_client = TavilyClient(api_key=self.tavily_key)
    response = tavily_client.search(query=query, max_results=3)
    # Usa resultados reais
else:
    # Simulação com LLM
    # Gera conteúdo simulado
```

---

## 🎨 Na Interface

### Indicadores Visuais

Quando Tavily está ativo, você verá:

```
🔍 BUSCANDO INFORMAÇÕES (5 queries)
  🌐 Usando Tavily API (busca real)
  ✓ Busca real: benefits of AI... (3 resultados)
  ✓ Busca real: risks of AI... (3 resultados)
```

Quando está simulando:

```
🔍 BUSCANDO INFORMAÇÕES (5 queries)
  🤖 Usando simulação com LLM
  ✓ Busca simulada: benefits of AI...
  ✓ Busca simulada: risks of AI...
```

### Referências

Com Tavily (real):
```
📚 Fontes Consultadas

📌 Fonte 1: LangGraph Tutorial: What Is LangGraph
   URL: https://www.datacamp.com/tutorial/langgraph-tutorial
   Relevância: 87%

📌 Fonte 2: Learn LangGraph basics
   URL: https://langchain-ai.github.io/langgraph/
   Relevância: 79%
```

Sem Tavily (simulado):
```
📚 Fontes Consultadas

📌 Fonte 1: Resultado para: benefits of AI
   URL: fonte-simulada-453.com
   Relevância: 85%
```

---

## 💰 Uso de Créditos

### Plano FREE (1.000 créditos/mês)

- **1 busca básica** = 1 crédito
- **3 resultados por busca** = padrão
- **5 queries por pesquisa** = média

**Cálculo:**
- 1 pesquisa completa ≈ 5 créditos
- **200 pesquisas/mês** com plano FREE
- **~7 pesquisas/dia**

### Otimizando Créditos

1. **Use 1 iteração** para perguntas simples
2. **Use 2 iterações** para comparações
3. **Tavily para tópicos atuais**, simulação para conceitos
4. **Max 3 resultados** por query (padrão eficiente)

---

## 🔧 Troubleshooting

### Erro: "API Key inválida"

```bash
# Verifique se copiou corretamente
echo $TAVILY_API_KEY

# Deve começar com: tvly-dev-...
```

### Ainda mostra "fonte-simulada"

1. **Recarregue a página** da interface
2. **Marque o checkbox** "Usar Tavily API"
3. **Insira a key** novamente
4. **Faça nova pesquisa**

### ImportError: tavily

```bash
# Instale a biblioteca
pip install tavily-python --user
```

### Erro: "Rate limit exceeded"

Você atingiu o limite de 1.000 créditos/mês. Opções:

1. **Aguarde** o reset mensal
2. **Upgrade** para plano pago ($30/mês)
3. **Use simulação** temporariamente

---

## 📈 Comparação

| Aspecto | Simulação (LLM) | Tavily (Real) |
|---------|-----------------|---------------|
| **Velocidade** | Médio (depende do LLM) | Rápido |
| **Qualidade** | Boa (conhecimento geral) | Excelente (atual) |
| **Custo** | Baixo (tokens) | Grátis até 1k |
| **Fontes** | Fictícias | URLs reais |
| **Atualidade** | Jan 2025 (cutoff) | Tempo real |
| **Verificável** | Não | Sim |

---

## 🎓 Quando Usar Cada Modo

### Use Tavily (Real) para:

✅ Tópicos atuais e notícias
✅ Informações técnicas específicas
✅ Comparações de produtos/serviços
✅ Pesquisa acadêmica
✅ Verificação de fatos

### Use Simulação para:

✅ Conceitos teóricos gerais
✅ Testes e desenvolvimento
✅ Sem acesso à internet
✅ Economia de créditos
✅ Perguntas filosóficas/abstratas

---

## 🚀 Exemplo Prático

### Sem Tavily

**Pergunta:** "Quais são as últimas atualizações do Python 3.13?"

**Resultado:**
```
Fontes: fonte-simulada-*.com
Conteúdo: [Informações até jan/2025]
```

### Com Tavily

**Pergunta:** "Quais são as últimas atualizações do Python 3.13?"

**Resultado:**
```
Fontes:
- python.org/downloads/release/python-313/
- realpython.com/python313-new-features/
- docs.python.org/3.13/whatsnew/

Conteúdo: [Informações atualizadas em tempo real]
```

---

## 🆘 Suporte

- **Tavily Docs:** https://docs.tavily.com/
- **LangGraph Docs:** https://langchain-ai.github.io/langgraph/
- **Issues:** Reporte bugs no repositório

---

**Pronto para usar busca real! 🌐** Configure sua key e experimente a diferença.
