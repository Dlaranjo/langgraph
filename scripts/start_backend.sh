#!/bin/bash

# Script para iniciar o Backend FastAPI
echo "🚀 Iniciando Backend FastAPI..."
echo "=================================="

# Verifica se está no diretório raiz do projeto
if [ ! -f "backend/api.py" ]; then
    echo "❌ Erro: backend/api.py não encontrado!"
    echo "Execute este script do diretório raiz do projeto."
    exit 1
fi

# Verifica se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "⚠️  Ambiente virtual não encontrado. Criando..."
    python3 -m venv venv
fi

# Ativa o ambiente virtual
echo "📦 Ativando ambiente virtual..."
source venv/bin/activate

# Instala/atualiza dependências
echo "📚 Instalando dependências..."
pip install -q -r requirements.txt

# Verifica arquivo .env
if [ ! -f ".env" ]; then
    echo "⚠️  Arquivo .env não encontrado!"
    echo "Crie um arquivo .env com:"
    echo "ANTHROPIC_API_KEY=sua_chave_aqui"
    echo "TAVILY_API_KEY=sua_chave_aqui (opcional)"
fi

# Inicia a aplicação
echo ""
echo "✅ Iniciando API FastAPI..."
echo "🌐 API: http://localhost:8000"
echo "📚 Docs: http://localhost:8000/docs"
echo "⏹️  Para parar: Ctrl+C"
echo ""

cd backend && python api.py
