# 🚀 Deploy LangGraph na AWS com Terraform

Infraestrutura completa como código (IaC) para deploy do LangGraph Research Agent na AWS usando Free Tier.

## 📋 Índice

- [Arquitetura](#-arquitetura)
- [Pré-requisitos](#-pré-requisitos)
- [Configuração Inicial](#-configuração-inicial)
- [Deploy](#-deploy)
- [Gerenciamento](#-gerenciamento)
- [Custos](#-custos)
- [Troubleshooting](#-troubleshooting)

## 🏗️ Arquitetura

```
Internet
   │
   ├─→ CloudFront (CDN)
   │      │
   │      └─→ S3 Bucket (Frontend Next.js)
   │
   └─→ EC2 t2.micro (Backend FastAPI)
          │
          ├─→ SSM Parameter Store (API Keys)
          └─→ CloudWatch Logs (Monitoramento)
```

### Recursos criados:

- **VPC** com subnet pública, Internet Gateway, Route Tables
- **EC2 t2.micro** (Free Tier) rodando FastAPI backend
- **Elastic IP** para IP público fixo
- **S3 Bucket** para frontend estático (Next.js)
- **CloudFront Distribution** para CDN global
- **IAM Roles** e policies para acesso seguro
- **SSM Parameter Store** para API keys (criptografadas)
- **Security Groups** com regras de firewall
- **CloudWatch Logs** para monitoramento

## 📦 Pré-requisitos

### 1. Conta AWS

- Criar conta em https://aws.amazon.com/
- **Free Tier** ativo (12 meses após criação)
- Cartão de crédito válido (não será cobrado se dentro do Free Tier)

### 2. Ferramentas instaladas

```bash
# Terraform (versão 1.0+)
# macOS
brew install terraform

# Linux
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Verificar
terraform version

# AWS CLI
# macOS
brew install awscli

# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Verificar
aws --version

# Node.js 18+ (para build do frontend)
node --version
npm --version
```

### 3. Credenciais AWS

```bash
# Configurar AWS CLI
aws configure

# Será solicitado:
# AWS Access Key ID: [sua key]
# AWS Secret Access Key: [sua secret]
# Default region name: us-east-1
# Default output format: json

# Para obter as credenciais:
# AWS Console > IAM > Users > [seu usuário] > Security credentials > Create access key
```

## ⚙️ Configuração Inicial

### 1. Criar Key Pair SSH

```bash
# Opção 1: Via AWS Console (recomendado)
# AWS Console > EC2 > Key Pairs > Create Key Pair
# Nome: langgraph-key
# Tipo: RSA
# Formato: .pem
# Salvar em: ~/.ssh/langgraph-key.pem

# Ajustar permissões
chmod 400 ~/.ssh/langgraph-key.pem

# Opção 2: Via CLI
aws ec2 create-key-pair \
  --key-name langgraph-key \
  --query 'KeyMaterial' \
  --output text > ~/.ssh/langgraph-key.pem

chmod 400 ~/.ssh/langgraph-key.pem
```

### 2. Configurar variáveis

```bash
# Copiar arquivo de exemplo
cd terraform/
cp terraform.tfvars.example terraform.tfvars

# Editar terraform.tfvars
nano terraform.tfvars  # ou vim, code, etc
```

**Edite os seguintes valores obrigatórios:**

```hcl
# API Keys (obrigatório!)
anthropic_api_key = "sk-ant-api03-XXXXX"  # Sua chave Anthropic
tavily_api_key    = "tvly-dev-XXXXX"      # Sua chave Tavily (opcional)

# Bucket S3 (deve ser único globalmente!)
s3_bucket_name = "langgraph-frontend-SEU-USERNAME-123"

# Seu IP público (para SSH seguro)
allowed_ssh_ips = ["123.456.789.0/32"]  # Descubra: curl ifconfig.me
```

### 3. Configurar Next.js para export estático

Edite `frontend/next.config.js`:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',  // ⚠️ ADICIONE ESTA LINHA!
  // ... resto da configuração
}

module.exports = nextConfig
```

## 🚀 Deploy

### 1. Inicializar Terraform

```bash
cd terraform/
terraform init
```

### 2. Validar configuração

```bash
# Verificar sintaxe
terraform validate

# Ver plano de execução
terraform plan
```

**Revise os recursos que serão criados:**
- ✅ VPC, subnets, security groups
- ✅ EC2 instance, Elastic IP
- ✅ S3 bucket, CloudFront distribution
- ✅ IAM roles, SSM parameters

### 3. Aplicar infraestrutura

```bash
# Aplicar (vai pedir confirmação)
terraform apply

# Ou sem confirmação (não recomendado)
terraform apply -auto-approve
```

**Tempo estimado:** 5-10 minutos

### 4. Salvar outputs

```bash
# Ver todos os outputs
terraform output

# Salvar em arquivo
terraform output > ../deploy-info.txt

# Copiar URLs importantes
terraform output backend_api_url
terraform output frontend_url
```

### 5. Deploy do frontend

```bash
# Voltar para raiz do projeto
cd ..

# Executar script de build e deploy
./terraform/scripts/build-frontend.sh \
  $(terraform -chdir=terraform output -raw backend_api_url) \
  $(terraform -chdir=terraform output -raw s3_bucket_name) \
  $(terraform -chdir=terraform output -raw cloudfront_distribution_id)
```

### 6. Testar aplicação

```bash
# Testar backend
BACKEND_URL=$(terraform -chdir=terraform output -raw backend_api_url)
curl $BACKEND_URL/health

# Abrir frontend no navegador
FRONTEND_URL=$(terraform -chdir=terraform output -raw frontend_url)
echo "Frontend: $FRONTEND_URL"
open $FRONTEND_URL  # macOS
xdg-open $FRONTEND_URL  # Linux
```

## 🔧 Gerenciamento

### Acessar EC2 via SSH

```bash
# Obter IP público
EC2_IP=$(terraform -chdir=terraform output -raw backend_public_ip)

# Conectar
ssh -i ~/.ssh/langgraph-key.pem ec2-user@$EC2_IP
```

### Ver logs do backend

```bash
# Via SSH
ssh -i ~/.ssh/langgraph-key.pem ec2-user@$EC2_IP \
  "sudo journalctl -u langgraph-backend -f"

# Via CloudWatch (AWS Console)
# CloudWatch > Logs > Log groups > /aws/ec2/langgraph-research-agent
```

### Atualizar backend

```bash
# Conectar via SSH
ssh -i ~/.ssh/langgraph-key.pem ec2-user@$EC2_IP

# Executar script de atualização
sudo /usr/local/bin/update-langgraph.sh
```

### Atualizar frontend

```bash
# Fazer mudanças no código frontend
cd frontend/
# ... editar arquivos ...

# Re-deploy
cd ..
./terraform/scripts/build-frontend.sh \
  $(terraform -chdir=terraform output -raw backend_api_url) \
  $(terraform -chdir=terraform output -raw s3_bucket_name) \
  $(terraform -chdir=terraform output -raw cloudfront_distribution_id)
```

### Parar/Iniciar EC2 (economizar Free Tier)

```bash
# Parar instância
INSTANCE_ID=$(terraform -chdir=terraform output -json | jq -r '.backend_ssh_command.value' | grep -oP 'i-\w+')
aws ec2 stop-instances --instance-ids $INSTANCE_ID

# Iniciar instância
aws ec2 start-instances --instance-ids $INSTANCE_ID
```

### Atualizar infraestrutura

```bash
# Após mudar variáveis ou código Terraform
cd terraform/
terraform plan  # Verificar mudanças
terraform apply
```

### Destruir tudo

```bash
cd terraform/

# ATENÇÃO: Isso vai deletar TUDO!
terraform destroy

# Confirme digitando: yes
```

## 💰 Custos

### Free Tier (12 meses)

| Recurso | Free Tier | Custo após |
|---------|-----------|------------|
| EC2 t2.micro | 750h/mês | ~$8.50/mês |
| S3 | 5GB storage | $0.023/GB/mês |
| CloudFront | 50GB data transfer | $0.085/GB |
| Data Transfer | 100GB out | $0.09/GB |
| **TOTAL** | **$0/mês** | **~$12-20/mês** |

### Custos adicionais (APIs externas)

| API | Custo |
|-----|-------|
| Anthropic Claude | ~$0.003-0.015 / 1K tokens |
| Tavily Search | 1000 créditos grátis/mês, depois paga |

### Dicas para economizar

1. **Desligar EC2 fora do horário:**
   ```bash
   # Configurar auto-shutdown
   # Editar terraform.tfvars:
   enable_auto_shutdown = true
   auto_shutdown_time   = "02:00"  # 2 AM UTC
   auto_startup_time    = "12:00"  # 12 PM UTC
   ```

2. **Usar apenas S3 (sem CloudFront):**
   ```hcl
   enable_cloudfront = false
   ```
   Economia: ~$4-5/mês

3. **Monitorar custos:**
   - AWS Console > Cost Explorer
   - Configurar billing alerts
   - Revisar monthly bill

## 🐛 Troubleshooting

### Erro: "BucketAlreadyExists"

```bash
# Bucket S3 já existe (nome não é único)
# Solução: Mudar nome em terraform.tfvars
s3_bucket_name = "langgraph-frontend-SEU-USERNAME-123"
```

### Erro: "InvalidKeyPair.NotFound"

```bash
# Key pair não existe
# Solução: Criar key pair primeiro
aws ec2 create-key-pair \
  --key-name langgraph-key \
  --query 'KeyMaterial' \
  --output text > ~/.ssh/langgraph-key.pem

chmod 400 ~/.ssh/langgraph-key.pem
```

### Backend não responde (502/timeout)

```bash
# 1. Verificar se EC2 está rodando
EC2_IP=$(terraform -chdir=terraform output -raw backend_public_ip)
ping $EC2_IP

# 2. Verificar logs
ssh -i ~/.ssh/langgraph-key.pem ec2-user@$EC2_IP \
  "sudo journalctl -u langgraph-backend -n 100"

# 3. Verificar status do serviço
ssh -i ~/.ssh/langgraph-key.pem ec2-user@$EC2_IP \
  "sudo systemctl status langgraph-backend"

# 4. Reiniciar serviço
ssh -i ~/.ssh/langgraph-key.pem ec2-user@$EC2_IP \
  "sudo systemctl restart langgraph-backend"
```

### Frontend não carrega

```bash
# 1. Verificar se build foi feito
ls frontend/out/

# 2. Verificar bucket S3
S3_BUCKET=$(terraform -chdir=terraform output -raw s3_bucket_name)
aws s3 ls s3://$S3_BUCKET/

# 3. Re-fazer deploy
./terraform/scripts/build-frontend.sh \
  $(terraform -chdir=terraform output -raw backend_api_url) \
  $(terraform -chdir=terraform output -raw s3_bucket_name) \
  $(terraform -chdir=terraform output -raw cloudfront_distribution_id)
```

### Erro: "UnauthorizedOperation"

```bash
# Permissões IAM insuficientes
# Solução: Adicionar policies ao seu usuário IAM:
# - AmazonEC2FullAccess
# - AmazonS3FullAccess
# - CloudFrontFullAccess
# - IAMFullAccess
# - AWSCloudFormationFullAccess
```

### API Keys não funcionam

```bash
# Verificar se foram criadas no SSM
aws ssm get-parameter \
  --name "/langgraph-research-agent/anthropic_api_key" \
  --with-decryption

# Atualizar API key
aws ssm put-parameter \
  --name "/langgraph-research-agent/anthropic_api_key" \
  --value "sk-ant-api03-NOVA-CHAVE" \
  --type SecureString \
  --overwrite

# Reiniciar backend
EC2_IP=$(terraform -chdir=terraform output -raw backend_public_ip)
ssh -i ~/.ssh/langgraph-key.pem ec2-user@$EC2_IP \
  "sudo systemctl restart langgraph-backend"
```

## 📚 Recursos Adicionais

- [Terraform AWS Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS Free Tier](https://aws.amazon.com/free/)
- [Next.js Static Export](https://nextjs.org/docs/app/building-your-application/deploying/static-exports)
- [AWS CLI Reference](https://docs.aws.amazon.com/cli/latest/)

## 🤝 Suporte

Se encontrar problemas:

1. Verificar logs do CloudWatch
2. Revisar security groups (portas abertas?)
3. Testar conexão: `curl http://EC2_IP:8000/health`
4. Abrir issue no GitHub com logs completos

---

**Desenvolvido com Terraform + AWS 🚀**
