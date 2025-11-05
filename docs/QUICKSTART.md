# 🚀 Guia Rápido - Interface Next.js

## Em 3 Passos

### 1️⃣ Instale as Dependências

```bash
# Dependências Python
pip install -r requirements.txt --user

# Dependências Node.js
cd frontend && npm install
```

### 2️⃣ Configure a API Key

```bash
# Opção A: Variável de ambiente
export ANTHROPIC_API_KEY="sua-chave-aqui"

# Opção B: Arquivo .env
cp .env.example .env
# Edite .env e adicione sua chave
```

### 3️⃣ Inicie a Stack

```bash
./scripts/start_nextjs_stack.sh
```

**Pronto!** A interface abrirá em http://localhost:3000

---

## 📸 Visão Geral da Interface

```
┌─────────────────────────────────────────────────────────────────┐
│                   🔬 Agente Pesquisador IA                     │
│        Pesquisa inteligente com validação de fontes            │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  💭 Faça sua pergunta                                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  Digite sua pergunta aqui...                             │   │
│  │                                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ⚙️ Configurações:                                              │
│  • Máximo de Iterações: [2 ▼]                                  │
│  • ☑️ Usar Tavily API (busca real)                             │
│                                                                  │
│  [🚀 Pesquisar]  [🔄 Limpar]                                   │
│                                                                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                  │
│  📋 Resultados da Pesquisa                                      │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ 📄 Relatório │ 📚 Referências │ 📊 Análise │ 📝 Logs  │    │
│  ├────────────────────────────────────────────────────────┤    │
│  │                                                        │    │
│  │  [Conteúdo da Tab Selecionada]                        │    │
│  │                                                        │    │
│  └────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Exemplo de Uso

### Passo a Passo:

1. **Abra a interface** no navegador (http://localhost:3000)

2. **Digite sua pergunta** no campo principal:
   ```
   Quais são os principais benefícios da IA generativa?
   ```

3. **Configure** (opcional):
   - Máximo de iterações: `2`
   - ☑️ Usar Tavily API (busca real)

4. **Clique em Pesquisar** 🚀

5. **Acompanhe o progresso**:
   - A interface mostra o status em tempo real
   - Indicadores visuais do processo

6. **Visualize os resultados** nas tabs:
   - **📄 Relatório:** Texto completo em Markdown renderizado
   - **📚 Referências:** Lista de fontes consultadas com scores
   - **📊 Análise:** Métricas de confiança e validações
   - **📝 Logs:** Histórico detalhado da execução

---

## 🎨 Features da Interface

### ✨ Design Moderno
- Interface limpa e intuitiva com shadcn/ui
- Tema dark/light automático
- Componentes acessíveis e responsivos
- Animações suaves e feedback visual

### 📊 Visualizações
- Markdown renderizado com syntax highlighting
- Cards de referências com scores de confiança
- Métricas visuais de validação
- Badges para status e categorias

### ⚡ Performance
- Server-side rendering com Next.js 14
- API REST com FastAPI (alta performance)
- Atualizações em tempo real
- Cache inteligente

---

## 🏗️ Arquitetura

```
┌──────────────┐    HTTP/REST    ┌──────────────┐
│              │ ───────────────> │              │
│  Next.js     │                  │   FastAPI    │
│  Frontend    │ <─────────────── │   Backend    │
│              │     JSON         │              │
└──────────────┘                  └──────────────┘
   Port 3000                         Port 8000
                                         │
                                         ▼
                                  ┌──────────────┐
                                  │  LangGraph   │
                                  │  Agent       │
                                  └──────────────┘
```

---

## ⌨️ Comandos Úteis

### Desenvolvimento

```bash
# Iniciar apenas o backend
./scripts/start_backend.sh

# Iniciar apenas o frontend
./scripts/start_frontend.sh

# Iniciar stack completa
./scripts/start_nextjs_stack.sh
```

### Frontend (Next.js)

```bash
cd frontend

# Desenvolvimento
npm run dev

# Build de produção
npm run build

# Iniciar produção
npm start
```

### Backend (FastAPI)

```bash
cd backend

# Desenvolvimento
python api.py

# Verificar documentação da API
# Abra: http://localhost:8000/docs
```

---

## 🔧 Troubleshooting Rápido

### Erro: "API Key não encontrada"
```bash
export ANTHROPIC_API_KEY="sua-chave"
```

### Porta 3000 ou 8000 em uso
```bash
# Encontre o processo
lsof -i :3000
lsof -i :8000

# Mate o processo
kill -9 [PID]
```

### Módulos não encontrados (Frontend)
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Erro de conexão Backend-Frontend
Verifique se o backend está rodando em http://localhost:8000

```bash
curl http://localhost:8000/health
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

## 🎓 Próximos Passos

1. Teste com diferentes tipos de perguntas
2. Explore as tabs de resultados
3. Compare resultados com diferentes configurações
4. Leia a documentação completa: [NEXTJS_GUIDE.md](../NEXTJS_GUIDE.md)
5. Contribua com melhorias!

---

**Pronto para começar? Execute:** `./scripts/start_nextjs_stack.sh` 🚀
