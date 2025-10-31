#!/bin/bash

# Script para iniciar o Frontend Next.js
echo "🚀 Iniciando Frontend Next.js..."
echo "=================================="

# Verifica se está no diretório raiz do projeto
if [ ! -d "frontend" ]; then
    echo "❌ Erro: diretório frontend não encontrado!"
    echo "Execute este script do diretório raiz do projeto."
    exit 1
fi

cd frontend

# Verifica se node_modules existe
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependências npm..."
    npm install
fi

# Inicia o servidor de desenvolvimento
echo ""
echo "✅ Iniciando Next.js dev server..."
echo "🌐 Frontend: http://localhost:3000"
echo "⏹️  Para parar: Ctrl+C"
echo ""

npm run dev
