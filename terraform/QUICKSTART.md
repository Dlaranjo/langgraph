# ⚡ Quick Start - Deploy em 10 minutos

Guia rápido para fazer o primeiro deploy do LangGraph na AWS.

## 📝 Checklist Rápida

- [ ] Conta AWS criada
- [ ] AWS CLI instalado e configurado (`aws configure`)
- [ ] Terraform instalado (`terraform version`)
- [ ] Node.js 18+ instalado (`node --version`)
- [ ] Key pair SSH criado na AWS
- [ ] Chaves API: Anthropic + Tavily

## 🚀 Passo a Passo

### 1. Criar Key Pair SSH (2 min)

```bash
# Criar via CLI
aws ec2 create-key-pair \
  --key-name langgraph-key \
  --query 'KeyMaterial' \
  --output text > ~/.ssh/langgraph-key.pem

chmod 400 ~/.ssh/langgraph-key.pem
```

### 2. Configurar Terraform (2 min)

```bash
cd terraform/

# Copiar arquivo de exemplo
cp terraform.tfvars.example terraform.tfvars

# Editar com seus valores
nano terraform.tfvars
```

**Mude apenas estas 3 linhas:**

```hcl
anthropic_api_key = "sk-ant-api03-SUA-CHAVE-AQUI"
s3_bucket_name    = "langgraph-frontend-SEU-NOME-123"
allowed_ssh_ips   = ["SEU-IP-AQUI/32"]  # curl ifconfig.me
```

### 3. Deploy da Infraestrutura (5 min)

```bash
# Inicializar
terraform init

# Aplicar
terraform apply -auto-approve
```

☕ Aguarde 5-10 minutos enquanto a AWS cria os recursos...

### 4. Deploy do Frontend (1 min)

```bash
# Voltar para raiz
cd ..

# Configurar Next.js para export
# Adicione ao frontend/next.config.js:
# output: 'export',

# Deploy
./terraform/scripts/build-frontend.sh \
  $(terraform -chdir=terraform output -raw backend_api_url) \
  $(terraform -chdir=terraform output -raw s3_bucket_name) \
  $(terraform -chdir=terraform output -raw cloudfront_distribution_id)
```

### 5. Acessar Aplicação

```bash
# Ver URLs
terraform -chdir=terraform output

# Abrir no navegador
echo "Frontend: $(terraform -chdir=terraform output -raw frontend_url)"
echo "Backend:  $(terraform -chdir=terraform output -raw backend_api_url)"
```

## ✅ Pronto!

Sua aplicação está no ar em:
- **Frontend:** https://XXXXX.cloudfront.net
- **Backend:** http://IP-PUBLICO:8000
- **API Docs:** http://IP-PUBLICO:8000/docs

## 🔧 Comandos Úteis

```bash
# Ver logs do backend
ssh -i ~/.ssh/langgraph-key.pem ec2-user@IP-PUBLICO \
  "sudo journalctl -u langgraph-backend -f"

# Parar EC2 (economizar)
aws ec2 stop-instances --instance-ids $(terraform -chdir=terraform output -json | jq -r '.backend_ssh_command.value' | grep -oP 'i-\w+')

# Destruir tudo
cd terraform/ && terraform destroy
```

## 💡 Dica: Automatizar tudo

Crie um script `deploy.sh`:

```bash
#!/bin/bash
set -e

cd terraform/
terraform init
terraform apply -auto-approve
cd ..

./terraform/scripts/build-frontend.sh \
  $(terraform -chdir=terraform output -raw backend_api_url) \
  $(terraform -chdir=terraform output -raw s3_bucket_name) \
  $(terraform -chdir=terraform output -raw cloudfront_distribution_id)

echo "✅ Deploy concluído!"
terraform -chdir=terraform output frontend_url
```

```bash
chmod +x deploy.sh
./deploy.sh
```

## 🐛 Problemas?

Veja o guia completo: [README_TERRAFORM.md](README_TERRAFORM.md)
