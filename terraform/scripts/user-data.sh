#!/bin/bash
# ========================================
# USER DATA - SETUP AUTOMÁTICO EC2
# Backend LangGraph Research Agent
# ========================================

set -e  # Para em caso de erro

# Variáveis do Terraform (injetadas via templatefile)
PROJECT_NAME="${project_name}"
AWS_REGION="${aws_region}"
BACKEND_REPO_URL="${backend_repo_url}"
ANTHROPIC_KEY_PATH="${anthropic_key_path}"
TAVILY_KEY_PATH="${tavily_key_path}"

# ----------------------------------------
# 1. Atualizar sistema
# ----------------------------------------

echo "🔄 Atualizando sistema..."
sudo yum update -y

# ----------------------------------------
# 2. Instalar dependências
# ----------------------------------------

echo "📦 Instalando dependências..."
sudo yum install -y \
    python3.11 \
    python3-pip \
    git \
    gcc \
    python3-devel \
    amazon-cloudwatch-agent \
    jq

# Garantir que python3 aponta para 3.11
sudo alternatives --set python3 /usr/bin/python3.11

# ----------------------------------------
# 3. Criar usuário da aplicação
# ----------------------------------------

echo "👤 Criando usuário da aplicação..."
sudo useradd -m -s /bin/bash langgraph || true
sudo usermod -aG wheel langgraph

# ----------------------------------------
# 4. Clonar repositório
# ----------------------------------------

echo "📥 Clonando repositório..."
cd /home/langgraph

# Se você usar repositório privado, configure SSH key ou token
# Por simplicidade, usando público aqui
if [ ! -d "langgraph" ]; then
    sudo -u langgraph git clone $BACKEND_REPO_URL langgraph
fi

cd langgraph

# ----------------------------------------
# 5. Configurar ambiente Python
# ----------------------------------------

echo "🐍 Configurando ambiente Python..."
sudo -u langgraph python3 -m venv venv
sudo -u langgraph /home/langgraph/langgraph/venv/bin/pip install --upgrade pip
sudo -u langgraph /home/langgraph/langgraph/venv/bin/pip install -r requirements.txt

# ----------------------------------------
# 6. Buscar API keys do SSM Parameter Store
# ----------------------------------------

echo "🔑 Buscando API keys do SSM..."
ANTHROPIC_KEY=$(aws ssm get-parameter \
    --name "$ANTHROPIC_KEY_PATH" \
    --with-decryption \
    --region $AWS_REGION \
    --query 'Parameter.Value' \
    --output text)

if [ -n "$TAVILY_KEY_PATH" ]; then
    TAVILY_KEY=$(aws ssm get-parameter \
        --name "$TAVILY_KEY_PATH" \
        --with-decryption \
        --region $AWS_REGION \
        --query 'Parameter.Value' \
        --output text)
else
    TAVILY_KEY=""
fi

# ----------------------------------------
# 7. Criar arquivo .env
# ----------------------------------------

echo "📝 Criando arquivo .env..."
cat <<EOF | sudo -u langgraph tee /home/langgraph/langgraph/.env > /dev/null
# API Keys (carregadas do SSM Parameter Store)
ANTHROPIC_API_KEY=$ANTHROPIC_KEY
TAVILY_API_KEY=$TAVILY_KEY

# Configurações da aplicação
ENVIRONMENT=production
PROJECT_NAME=$PROJECT_NAME
AWS_REGION=$AWS_REGION
EOF

sudo chown langgraph:langgraph /home/langgraph/langgraph/.env
sudo chmod 600 /home/langgraph/langgraph/.env

# ----------------------------------------
# 8. Criar systemd service
# ----------------------------------------

echo "⚙️ Criando systemd service..."
sudo tee /etc/systemd/system/langgraph-backend.service > /dev/null <<EOF
[Unit]
Description=LangGraph Research Agent Backend (FastAPI)
After=network.target

[Service]
Type=simple
User=langgraph
WorkingDirectory=/home/langgraph/langgraph
Environment="PATH=/home/langgraph/langgraph/venv/bin"
ExecStart=/home/langgraph/langgraph/venv/bin/uvicorn backend.api:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Segurança
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/home/langgraph/langgraph

[Install]
WantedBy=multi-user.target
EOF

# ----------------------------------------
# 9. Configurar CloudWatch Agent (logs)
# ----------------------------------------

echo "📊 Configurando CloudWatch Logs..."
sudo tee /opt/aws/amazon-cloudwatch-agent/etc/config.json > /dev/null <<EOF
{
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/var/log/messages",
            "log_group_name": "/aws/ec2/$PROJECT_NAME",
            "log_stream_name": "{instance_id}/system",
            "timezone": "UTC"
          },
          {
            "file_path": "/var/log/cloud-init-output.log",
            "log_group_name": "/aws/ec2/$PROJECT_NAME",
            "log_stream_name": "{instance_id}/cloud-init",
            "timezone": "UTC"
          }
        ]
      },
      "journal": {
        "log_group_name": "/aws/ec2/$PROJECT_NAME",
        "log_stream_name": "{instance_id}/backend",
        "unit_whitelist": ["langgraph-backend.service"]
      }
    }
  }
}
EOF

sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
    -a fetch-config \
    -m ec2 \
    -s \
    -c file:/opt/aws/amazon-cloudwatch-agent/etc/config.json

# ----------------------------------------
# 10. Habilitar e iniciar serviço
# ----------------------------------------

echo "🚀 Iniciando aplicação..."
sudo systemctl daemon-reload
sudo systemctl enable langgraph-backend
sudo systemctl start langgraph-backend

# ----------------------------------------
# 11. Aguardar inicialização
# ----------------------------------------

echo "⏳ Aguardando inicialização..."
sleep 10

# ----------------------------------------
# 12. Verificar status
# ----------------------------------------

echo "✅ Verificando status..."
sudo systemctl status langgraph-backend --no-pager

# ----------------------------------------
# 13. Teste de conectividade
# ----------------------------------------

echo "🧪 Testando API..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ API respondendo corretamente!"
else
    echo "⚠️ API não está respondendo. Verifique os logs:"
    echo "sudo journalctl -u langgraph-backend -n 50"
fi

# ----------------------------------------
# 14. Criar script de atualização
# ----------------------------------------

echo "📝 Criando script de atualização..."
sudo tee /usr/local/bin/update-langgraph.sh > /dev/null <<'EOF'
#!/bin/bash
set -e

echo "🔄 Atualizando LangGraph Backend..."

cd /home/langgraph/langgraph

# Pull latest changes
sudo -u langgraph git pull

# Update dependencies
sudo -u langgraph /home/langgraph/langgraph/venv/bin/pip install -r requirements.txt --upgrade

# Restart service
sudo systemctl restart langgraph-backend

echo "✅ Atualização concluída!"
sudo systemctl status langgraph-backend --no-pager
EOF

sudo chmod +x /usr/local/bin/update-langgraph.sh

# ----------------------------------------
# 15. Finalização
# ----------------------------------------

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 SETUP CONCLUÍDO COM SUCESSO!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📡 Backend rodando em: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8000"
echo "📚 Docs API: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8000/docs"
echo ""
echo "🔧 Comandos úteis:"
echo "  • Ver logs:      sudo journalctl -u langgraph-backend -f"
echo "  • Reiniciar:     sudo systemctl restart langgraph-backend"
echo "  • Status:        sudo systemctl status langgraph-backend"
echo "  • Atualizar:     sudo /usr/local/bin/update-langgraph.sh"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
