# 🎨 Interface Visual do Agente Pesquisador

Interface web interativa construída com Streamlit para o Agente Pesquisador IA.

## 🚀 Como Usar

### Iniciar a Interface

```bash
# Opção 1: Script automático
./start_app.sh

# Opção 2: Comando direto
streamlit run app.py
```

A interface abrirá automaticamente em: **http://localhost:8501**

## ✨ Funcionalidades

### 1. Pesquisa Interativa

- **Campo de pergunta** expandido para queries longas
- **Botão de pesquisa** com feedback visual
- **Barra de progresso** em tempo real

### 2. Configurações (Sidebar)

- **Máximo de iterações:** Slider de 1-3 ciclos
- **Tavily API:** Toggle para busca real vs simulada
- **Histórico:** Últimas 5 pesquisas com reload

### 3. Visualizações

#### Tab: Relatório
- Relatório completo em Markdown
- Botão de download (.md)

#### Tab: Referências
- Lista expandível de fontes
- URLs e scores de relevância

#### Tab: Análise
- **Gauge de confiança:** Indicador visual de 0-100%
- **Gráfico de métricas:** Barras com fontes, validações, iterações
- **Log de execução:** Timeline de eventos

#### Tab: Detalhes
- Estado completo do grafo (JSON)
- Validações realizadas
- Queries geradas

### 4. Métricas em Tempo Real

Painel lateral com:
- 💯 Confiança (com código de cores)
- 📚 Fontes consultadas
- ✅ Validações realizadas
- 🔄 Iterações executadas
- ⚠️ Alertas de conflitos

### 5. Histórico

- Últimas 5 pesquisas
- Timestamp e confiança
- Botão para recarregar resultados

## 🎨 Design

### Paleta de Cores
- Primária: Gradiente roxo (#667eea → #764ba2)
- Sucesso: Verde (#c8e6c9)
- Aviso: Amarelo (#fff9c4)
- Erro: Vermelho (#ffebee)

### Componentes
- Cards com gradientes
- Progress bars animadas
- Gráficos interativos (Plotly)
- Tabs para organização
- Expanders para detalhes

## 📊 Exemplo de Uso

1. **Digite sua pergunta** no campo principal
   ```
   Quais são os principais benefícios da computação quântica?
   ```

2. **Configure parâmetros** na sidebar
   - Máximo de iterações: 2
   - Tavily: Desativado (simulação)

3. **Clique em Pesquisar** 🚀

4. **Acompanhe o progresso:**
   - 🎯 Inicializando agente...
   - 🔍 Planejando pesquisa...
   - ✅ Pesquisa concluída!

5. **Explore os resultados** nas 4 tabs

6. **Baixe o relatório** se necessário

## 🔧 Configuração

### Variáveis de Ambiente

```bash
# Obrigatória
export ANTHROPIC_API_KEY="sua-chave-aqui"

# Opcional (para busca real)
export TAVILY_API_KEY="sua-chave-tavily"
```

### Sem Variáveis de Ambiente

Você pode inserir as chaves diretamente na sidebar da interface.

## 🎯 Dicas de Uso

### Perguntas Efetivas

✅ **Boas perguntas:**
- "Compare microserviços vs arquitetura monolítica"
- "Quais são os principais riscos da IA generativa?"
- "Explique como funciona o protocolo RAFT"

❌ **Evite:**
- Perguntas muito vagas: "O que é tecnologia?"
- Perguntas fechadas: "Python é bom?"

### Otimizando Resultados

- **Mais iterações:** Aumenta qualidade mas leva mais tempo
- **Busca real (Tavily):** Informações atualizadas
- **Busca simulada (LLM):** Mais rápido para testes

### Performance

- **1 iteração:** ~10-20 segundos
- **2 iterações:** ~20-40 segundos
- **3 iterações:** ~30-60 segundos

## 📱 Responsividade

A interface é responsiva e funciona em:
- 💻 Desktop (recomendado)
- 📱 Tablet
- 📱 Mobile (layout adaptativo)

## 🐛 Troubleshooting

### Interface não abre

```bash
# Verifique se o Streamlit está instalado
python3 -m pip show streamlit

# Reinstale se necessário
pip install streamlit --user
```

### Erro de API Key

```bash
# Configure no terminal
export ANTHROPIC_API_KEY="sk-ant-..."

# Ou insira diretamente na sidebar
```

### Porta 8501 em uso

```bash
# Use outra porta
streamlit run app.py --server.port 8502
```

### Gráficos não aparecem

```bash
# Instale o Plotly
pip install plotly --user
```

## 🔮 Recursos Futuros

- [ ] Tema escuro/claro
- [ ] Exportação em PDF
- [ ] Comparação de pesquisas
- [ ] Modo de apresentação
- [ ] Integração com Notion/Docs
- [ ] Suporte a imagens nos relatórios
- [ ] Chat interativo com o agente
- [ ] Busca em documentos locais

## 💡 Atalhos de Teclado

- `Ctrl + Enter`: Executar pesquisa
- `Ctrl + R`: Recarregar página
- `Ctrl + C` (no terminal): Parar servidor

## 📞 Suporte

Para problemas ou sugestões:
- Abra uma issue no repositório
- Consulte a documentação do Streamlit
- Verifique logs no terminal

---

**Desenvolvido com ❤️ usando Streamlit, LangGraph e Claude**
