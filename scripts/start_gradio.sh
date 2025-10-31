#!/bin/bash

# Script para iniciar a aplicação Gradio
echo "🚀 Iniciando Agente Pesquisador IA (Gradio)..."
echo "=================================="

# Verifica se está no diretório raiz do projeto
if [ ! -f "app_gradio.py" ]; then
    echo "❌ Erro: app_gradio.py não encontrado!"
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
echo "✅ Iniciando aplicação Gradio..."
echo "🌐 Acesse: http://localhost:7860"
echo "⏹️  Para parar: Ctrl+C"
echo ""

python app_gradio.py
