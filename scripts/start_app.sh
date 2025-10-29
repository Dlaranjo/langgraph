#!/bin/bash
# Script para iniciar a interface Streamlit

echo "🚀 Iniciando Agente Pesquisador..."
echo ""

# Verifica se as dependências estão instaladas
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "📦 Instalando dependências..."
    pip install -r requirements.txt --user
fi

# Verifica se a API key está configurada
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  AVISO: ANTHROPIC_API_KEY não está configurada"
    echo "   Configure com: export ANTHROPIC_API_KEY='sua-chave'"
    echo ""
fi

echo "🌐 Abrindo interface no navegador..."
echo "   URL: http://localhost:8501"
echo ""
echo "   Para parar: Ctrl+C"
echo ""

# Inicia o Streamlit
streamlit run app.py
