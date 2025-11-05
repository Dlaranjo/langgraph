# 🚀 Guia Completo - Stack Next.js + shadcn/ui + FastAPI

## 🎯 Arquitetura

```
┌──────────────────────────────────────────────────────┐
│  Frontend (Next.js + shadcn/ui + Tailwind)          │
│  Porta: 3000                                         │
│  - TypeScript                                        │
│  - Componentes React modernos                       │
│  - Design system shadcn/ui                          │
└───────────────────┬──────────────────────────────────┘
                    │ HTTP/REST
                    ↓
┌──────────────────────────────────────────────────────┐
│  Backend (FastAPI)                                   │
│  Porta: 8000                                         │
│  - API REST                                          │
│  - Endpoints /research, /health                     │
└───────────────────┬──────────────────────────────────┘
                    │
                    ↓
┌──────────────────────────────────────────────────────┐
│  ResearchAgent (LangGraph + Claude)                  │
│  - Busca e validação de informações                 │
│  - Geração de relatórios                            │
└──────────────────────────────────────────────────────┘
```

---

## ✨ O que há de novo?

### Frontend Moderno
- ✅ **Next.js 14** - Framework React de produção
- ✅ **TypeScript** - Type safety completo
- ✅ **shadcn/ui** - Componentes lindos e customizáveis
- ✅ **Tailwind CSS** - Styling moderno e responsivo
- ✅ **Lucide Icons** - Ícones modernos
- ✅ **Recharts** - Gráficos (preparado, não usado ainda)

### Backend API
- ✅ **FastAPI** - API REST rápida e moderna
- ✅ **CORS** - Configurado para frontend
- ✅ **Docs automáticas** - Swagger UI em `/docs`
- ✅ **Type validation** - Pydantic models

### Visual
- ✅ **Gradiente purple/pink** - Design moderno
- ✅ **Componentes arredondados** - Bordas suaves
- ✅ **Animações sutis** - Transições smooth
- ✅ **Dark mode ready** - Preparado para tema escuro
- ✅ **Responsivo** - Mobile, tablet, desktop

---

## 🚀 Como Executar

### Opção 1: Stack Completo (Recomendado)
Inicia frontend e backend automaticamente:
```bash
./scripts/start_nextjs_stack.sh
```

Acesse:
- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### Opção 2: Separado

**Backend:**
```bash
./scripts/start_backend.sh
# http://localhost:8000
```

**Frontend (em outro terminal):**
```bash
./scripts/start_frontend.sh
# http://localhost:3000
```

### Opção 3: Manual

**Backend:**
```bash
source venv/bin/activate
pip install -r requirements.txt
cd backend && python api.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## 📁 Estrutura do Projeto

```
langgraph/
├── frontend/                    # Next.js App
│   ├── app/
│   │   ├── layout.tsx          # Layout raiz
│   │   ├── page.tsx            # Página principal
│   │   └── globals.css         # Estilos globais
│   ├── components/
│   │   └── ui/                 # Componentes shadcn/ui
│   │       ├── button.tsx
│   │       ├── card.tsx
│   │       ├── tabs.tsx
│   │       ├── input.tsx
│   │       ├── textarea.tsx
│   │       ├── label.tsx
│   │       ├── badge.tsx
│   │       └── separator.tsx
│   ├── lib/
│   │   └── utils.ts            # Utilitários (cn function)
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── postcss.config.js
│   └── next.config.js
│
├── backend/
│   └── api.py                  # FastAPI server
│
├── src/                        # Código Python existente
│   └── agent.py                # ResearchAgent
│
├── scripts/
│   ├── start_nextjs_stack.sh   # Inicia tudo
│   ├── start_backend.sh        # Só backend
│   └── start_frontend.sh       # Só frontend
│
├── requirements.txt            # Dependências Python
├── NEXTJS_GUIDE.md            # Este guia
└── README.md                  # README principal
```

---

## 🎨 Componentes shadcn/ui Usados

| Componente | Uso | Arquivo |
|------------|-----|---------|
| **Button** | Pesquisar, Limpar, Download | `button.tsx` |
| **Card** | Containers de conteúdo | `card.tsx` |
| **Tabs** | Organização de resultados | `tabs.tsx` |
| **Input** | API keys, iterações | `input.tsx` |
| **Textarea** | Query de pesquisa | `textarea.tsx` |
| **Label** | Labels de formulários | `label.tsx` |
| **Badge** | Métricas, status | `badge.tsx` |
| **Separator** | Divisores visuais | `separator.tsx` |

---

## 🔌 API Endpoints (FastAPI)

### `GET /`
Health check básico

**Response:**
```json
{
  "status": "online",
  "version": "1.0.0",
  "timestamp": "2025-10-31T10:00:00"
}
```

### `GET /health`
Health check detalhado

### `POST /research`
Executa pesquisa

**Request:**
```json
{
  "query": "Como funciona GPT-4?",
  "max_iterations": 1,
  "anthropic_api_key": "sk-ant-...",
  "tavily_api_key": "tvly-..." // opcional
}
```

**Response:**
```json
{
  "query": "Como funciona GPT-4?",
  "timestamp": "2025-10-31T10:05:00",
  "report": "# Relatório...",
  "confidence": 0.85,
  "search_results_count": 5,
  "validations_count": 3,
  "iterations": 1,
  "conflicts_detected": false,
  "references": [...],
  "full_state": {...}
}
```

### `GET /api/config`
Retorna configurações do servidor

---

## 💻 Interface do Usuário

### Layout

```
┌─────────────────────────────────────────────────────────┐
│           🔬 Agente Pesquisador IA                      │
│     Pesquisa inteligente com validação...               │
├──────────────────────────┬──────────────────────────────┤
│                          │                              │
│  💭 Faça sua pergunta    │  ⚙️ Configurações            │
│  ┌───────────────────┐   │  - ANTHROPIC_API_KEY         │
│  │ Textarea          │   │  - Max iterações (1-3)       │
│  └───────────────────┘   │  - [ ] Usar Tavily           │
│  🔍 Pesquisar  Limpar    │    - Tavily API Key          │
│                          │                              │
│  ━━━━━━━━━━━━━━━━━━━━━━│  📊 Status (após pesquisa)   │
│  📋 Resultados           │  - Confiança: 85%            │
│                          │  - Fontes: 5                 │
│  📄 | 📚 | 📊 | 📋 | 🔍  │  - Validações: 3             │
│  ┌───────────────────┐   │  - Iterações: 1              │
│  │ Conteúdo da tab   │   │  - ✓ Sem conflitos           │
│  │                   │   │                              │
│  └───────────────────┘   │                              │
│                          │                              │
└──────────────────────────┴──────────────────────────────┘
│  🤖 Powered by LangGraph + Claude | 💻 Next.js...      │
└─────────────────────────────────────────────────────────┘
```

### Tabs de Resultados

1. **📄 Relatório** - Texto completo gerado
2. **📚 Fontes** - Referências com scores de relevância
3. **📊 Análise** - Confiança + métricas visuais
4. **📋 Logs** - Histórico de execução
5. **🔍 Detalhes** - Validações e queries técnicas

---

## 🎨 Customização

### Cores (Tailwind)
Edite `frontend/app/globals.css`:
```css
:root {
  --primary: 262.1 83.3% 57.8%;  /* Purple */
  /* ... outras cores ... */
}
```

### Componentes
Todos em `frontend/components/ui/` são 100% customizáveis.

### Layout
Edite `frontend/app/page.tsx` para mudar a interface.

---

## 🚢 Build para Produção

### Frontend
```bash
cd frontend
npm run build
npm start  # Produção na porta 3000
```

### Backend
```bash
# Via uvicorn
uvicorn backend.api:app --host 0.0.0.0 --port 8000

# Via Docker (exemplo)
# Dockerfile não incluído - criar se necessário
```

---

## 🔧 Troubleshooting

### Frontend não inicia
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Backend não conecta
- Verifique se porta 8000 está livre: `lsof -i :8000`
- Confirme ANTHROPIC_API_KEY configurada

### CORS errors
Backend já configurado com `allow_origins=["*"]` (dev).
Para produção, configure URLs específicas em `backend/api.py`.

### TypeScript errors
```bash
cd frontend
npm run build  # Verifica erros
```

---

## 🆕 Próximos Passos

Melhorias possíveis:

1. **Dark Mode** - Adicionar toggle de tema
2. **Histórico** - Salvar pesquisas no localStorage
3. **Streaming** - Resultados em tempo real (SSE)
4. **Gráficos** - Usar Recharts para visualizações
5. **Auth** - Adicionar autenticação de usuários
6. **Deploy** - Vercel (frontend) + Railway/Render (backend)

---

## 📚 Documentação de Referência

- **Next.js:** https://nextjs.org/docs
- **shadcn/ui:** https://ui.shadcn.com
- **Tailwind CSS:** https://tailwindcss.com/docs
- **FastAPI:** https://fastapi.tiangolo.com
- **TypeScript:** https://www.typescriptlang.org/docs

---

## 🎯 Stack Technologies

### Frontend
- Next.js 14.2.0
- React 18.3.0
- TypeScript 5.3.0
- Tailwind CSS 3.4.0
- shadcn/ui (Radix UI primitives)
- Lucide Icons

### Backend
- FastAPI 0.104.0+
- Uvicorn 0.24.0+
- Pydantic 2.0.0+

### AI/Agent
- LangGraph 0.2.0+
- LangChain 0.1.0+
- Anthropic Claude (API)
- Tavily (opcional)

---

## ❓ FAQ

**P: Em quais portas a aplicação roda?**
R:
- Frontend (Next.js): http://localhost:3000
- Backend (FastAPI): http://localhost:8000
- Documentação da API: http://localhost:8000/docs

**P: Posso rodar apenas o backend ou frontend?**
R: Sim! Use os scripts individuais:
- Backend: `./scripts/start_backend.sh`
- Frontend: `./scripts/start_frontend.sh`
- Ambos: `./scripts/start_nextjs_stack.sh`

**P: Como adicionar novos componentes shadcn?**
R: Copie de https://ui.shadcn.com e cole em `components/ui/`

**P: Preciso saber React?**
R: Sim, para customizar o Next.js. Mas o código já está pronto!

**P: Como fazer deploy?**
R:
- **Frontend:** Vercel (grátis) - `vercel deploy`
- **Backend:** Railway/Render/Fly.io
- Configure variáveis de ambiente

---

## 🎉 Pronto para Usar!

```bash
# Inicie tudo com 1 comando:
./scripts/start_nextjs_stack.sh

# Acesse: http://localhost:3000
```

**🌟 Aproveite sua interface moderna de nível profissional!**

---

*Última atualização: 2025-10-31*
*Stack: Next.js 14 + shadcn/ui + FastAPI + LangGraph + Claude*
