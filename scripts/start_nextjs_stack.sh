#!/bin/bash

# Script para iniciar o stack completo Next.js + FastAPI
echo "🚀 Iniciando Stack Completo: Next.js + FastAPI"
echo "=============================================="
echo ""

# Verifica se está no diretório raiz
if [ ! -f "backend/api.py" ] || [ ! -d "frontend" ]; then
    echo "❌ Erro: estrutura do projeto não encontrada!"
    echo "Execute este script do diretório raiz do projeto."
    exit 1
fi

# Função para cleanup
cleanup() {
    echo ""
    echo "🛑 Parando servidores..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

echo "📋 Preparando ambiente..."

# Ativa venv se existir
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Instala dependências Python
echo "📦 Instalando dependências Python..."
pip install -q -r requirements.txt

# Instala dependências npm
echo "📦 Instalando dependências npm..."
cd frontend && npm install --silent && cd ..

echo ""
echo "✅ Dependências instaladas!"
echo ""

# Inicia backend em background
echo "🔧 Iniciando Backend (FastAPI - porta 8000)..."
cd backend && python api.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Aguarda backend iniciar
echo "⏳ Aguardando backend iniciar..."
sleep 3

# Inicia frontend em background
echo "💻 Iniciando Frontend (Next.js - porta 3000)..."
cd frontend && npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Aguarda frontend iniciar
echo "⏳ Aguardando frontend iniciar..."
sleep 5

echo ""
echo "✨ =============================================="
echo "✨ Stack Next.js + FastAPI rodando!"
echo "✨ =============================================="
echo ""
echo "🌐 Frontend (Next.js): http://localhost:3000"
echo "📡 Backend (FastAPI):  http://localhost:8000"
echo "📚 API Docs:           http://localhost:8000/docs"
echo ""
echo "📋 Logs:"
echo "   Backend:  tail -f backend.log"
echo "   Frontend: tail -f frontend.log"
echo ""
echo "⏹️  Para parar: Ctrl+C"
echo ""

# Aguarda processos
wait $BACKEND_PID $FRONTEND_PID
