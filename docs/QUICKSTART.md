# 🚀 Guia Rápido - Interface Visual

## Em 3 Passos

### 1️⃣ Instale as Dependências

```bash
pip install -r requirements.txt --user
```

### 2️⃣ Configure a API Key

```bash
# Opção A: Variável de ambiente
export ANTHROPIC_API_KEY="sua-chave-aqui"

# Opção B: Arquivo .env
cp .env.example .env
# Edite .env e adicione sua chave
```

### 3️⃣ Inicie a Interface

```bash
./start_app.sh
```

**Pronto!** A interface abrirá em http://localhost:8501

---

## 📸 Visão Geral da Interface

```
┌─────────────────────────────────────────────────────────────────┐
│                   🔬 Agente Pesquisador IA                     │
│        Pesquisa inteligente com validação de fontes            │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐  ┌────────────────────────────────────────────┐
│              │  │                                            │
│  SIDEBAR     │  │  💭 Faça sua pergunta                      │
│              │  │  ┌──────────────────────────────────────┐  │
│  ⚙️ Config   │  │  │                                      │  │
│  • Iterações │  │  │  Digite sua pergunta aqui...         │  │
│  • Tavily    │  │  │                                      │  │
│              │  │  └──────────────────────────────────────┘  │
│  📊 Status   │  │                                            │
│  • Confiança │  │  [🚀 Pesquisar]  [🔄 Limpar]             │
│  • Fontes    │  │                                            │
│  • Validações│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│              │  │                                            │
│  📜 Histórico│  │  📋 Resultados da Pesquisa                │
│  • Pesquisa 1│  │  ┌──────────────────────────────────────┐ │
│  • Pesquisa 2│  │  │ Relatório │ Refs │ Análise │ Detalhes│ │
│  • Pesquisa 3│  │  ├──────────────────────────────────────┤ │
│              │  │  │                                      │ │
└──────────────┘  │  │  [Conteúdo da Tab Selecionada]      │ │
                  │  │                                      │ │
                  │  └──────────────────────────────────────┘ │
                  └────────────────────────────────────────────┘
```

---

## 🎯 Exemplo de Uso

### Passo a Passo:

1. **Abra a interface** no navegador

2. **Digite sua pergunta** no campo principal:
   ```
   Quais são os principais benefícios da IA generativa?
   ```

3. **Configure** (opcional):
   - Máximo de iterações: `2`
   - Tavily: `Desativado`

4. **Clique em Pesquisar** 🚀

5. **Acompanhe o progresso**:
   ```
   ████████░░ 80% - Validando informações...
   ```

6. **Visualize os resultados** nas tabs:
   - **Relatório:** Texto completo em Markdown
   - **Referências:** Lista de fontes consultadas
   - **Análise:** Gráficos de confiança e métricas
   - **Detalhes:** JSON completo e validações

7. **Baixe o relatório** se desejar (botão no final)

---

## 🎨 Features Visuais

### 📊 Gauge de Confiança
```
    100%  ┌─────────────┐
          │      ██     │
     75%  │    ██████   │
          │   ████████  │  ← 85%
     50%  │  ██████████ │
          │ ███████████ │
     25%  │ ███████████ │
          └─────────────┘
       0%
```

### 📈 Gráfico de Métricas
```
 Valor
   10 ┤     ┌──┐
    8 ┤     │  │
    6 ┤     │  │  ┌──┐
    4 ┤  ┌──┤  ├──┤  │
    2 ┤  │  │  │  │  │
    0 └──┴──┴──┴──┴──┴──
        Fontes  Val  Iter
```

### 📜 Histórico
```
┌────────────────────────┐
│ 📜 Histórico          │
├────────────────────────┤
│ 🔍 IA generativa...   │
│    ⏰ 2025-10-29 17:30 │
│    💯 85%              │
│    [Recarregar]        │
├────────────────────────┤
│ 🔍 Computação quân...  │
│    ⏰ 2025-10-29 17:25 │
│    💯 78%              │
│    [Recarregar]        │
└────────────────────────┘
```

---

## ⌨️ Atalhos

- **Ctrl + Enter**: Executar pesquisa (foco no campo)
- **Ctrl + R**: Recarregar página
- **Ctrl + C** (terminal): Parar servidor
- **?**: Ajuda (na interface)

---

## 🔧 Troubleshooting Rápido

### Erro: "API Key não encontrada"
```bash
export ANTHROPIC_API_KEY="sua-chave"
```

### Porta 8501 em uso
```bash
streamlit run app.py --server.port 8502
```

### Gráficos não aparecem
```bash
pip install plotly --user
```

### Interface não carrega
```bash
# Limpe o cache
rm -rf ~/.streamlit/
streamlit cache clear
```

---

## 💡 Dicas

### Para Melhores Resultados:

✅ **Faça perguntas específicas**
```
Bom: "Compare vantagens de GraphQL vs REST API"
Ruim: "O que é API?"
```

✅ **Use 2 iterações para tópicos complexos**
```
Configuração → Máximo de iterações: 2
```

✅ **Ative Tavily para informações atualizadas**
```
☑️ Usar Tavily API (busca real)
```

---

## 📱 Acesso Remoto

Para acessar de outro dispositivo na rede:

```bash
streamlit run app.py --server.address 0.0.0.0
```

Acesse via: `http://[seu-ip]:8501`

---

## 🎓 Próximos Passos

1. Teste com diferentes tipos de perguntas
2. Explore as visualizações e métricas
3. Compare resultados com diferentes configurações
4. Baixe e compartilhe relatórios
5. Contribua com melhorias!

---

**Pronto para começar? Execute:** `./start_app.sh` 🚀
