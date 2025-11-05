# 🚀 Deploy LangGraph na AWS - Guia Completo

Este projeto agora inclui **infraestrutura completa como código (IaC)** para deploy na AWS usando Terraform.

## 📁 Estrutura Criada

```
langgraph/
├── terraform/                       # 📦 Infraestrutura AWS
│   ├── main.tf                      # Provider AWS, data sources
│   ├── variables.tf                 # Variáveis configuráveis
│   ├── vpc.tf                       # VPC, subnets, security groups
│   ├── iam.tf                       # IAM roles, policies, SSM parameters
│   ├── ec2.tf                       # EC2 instance (backend)
│   ├── s3.tf                        # S3 bucket (frontend)
│   ├── cloudfront.tf                # CloudFront CDN
│   ├── outputs.tf                   # URLs e informações úteis
│   ├── terraform.tfvars.example     # Exemplo de configuração
│   ├── .gitignore                   # Ignora arquivos sensíveis
│   │
│   ├── scripts/                     # 🔧 Scripts auxiliares
│   │   ├── user-data.sh             # Setup automático EC2
│   │   └── build-frontend.sh        # Build e deploy do frontend
│   │
│   └── 📚 Documentação completa
│       ├── README_TERRAFORM.md      # Guia detalhado (leia primeiro!)
│       ├── QUICKSTART.md            # Deploy em 10 minutos
│       └── CUSTOS.md                # Análise de custos detalhada
│
├── backend/                         # FastAPI (roda no EC2)
├── frontend/                        # Next.js (hospedado no S3)
└── README.md                        # Documentação principal
```

## ✨ O que foi criado

### Arquivos Terraform (Infrastructure as Code)

1. **main.tf** - Configuração do provider AWS
2. **variables.tf** - Todas as variáveis configuráveis
3. **vpc.tf** - Rede VPC completa com security groups
4. **iam.tf** - Roles, policies, SSM parameters para API keys
5. **ec2.tf** - Instância EC2 t2.micro (Free Tier) para backend
6. **s3.tf** - Bucket S3 para hospedar frontend estático
7. **cloudfront.tf** - CDN global para distribuição do frontend
8. **outputs.tf** - URLs e informações úteis após deploy

### Scripts Auxiliares

1. **user-data.sh** - Setup automático da EC2:
   - Instala Python 3.11, Git, dependências
   - Clona repositório
   - Configura ambiente virtual
   - Busca API keys do SSM Parameter Store
   - Cria systemd service para FastAPI
   - Configura CloudWatch Logs
   - Inicia aplicação automaticamente

2. **build-frontend.sh** - Build e deploy do Next.js:
   - Configura variáveis de ambiente
   - Faz build estático do Next.js
   - Upload otimizado para S3
   - Invalida cache do CloudFront

### Documentação Completa

1. **README_TERRAFORM.md** (10.730 bytes)
   - Arquitetura detalhada
   - Pré-requisitos
   - Configuração passo a passo
   - Comandos de gerenciamento
   - Troubleshooting completo

2. **QUICKSTART.md** (3.020 bytes)
   - Deploy em 10 minutos
   - Checklist rápida
   - Comandos essenciais
   - Script de automação

3. **CUSTOS.md** (7.292 bytes)
   - Análise detalhada de custos
   - Free Tier explicado
   - 3 cenários de uso
   - Estratégias de economia
   - Comparação com alternativas

## 🎯 Free Tier - Primeira Conta AWS

### ✅ SIM, é possível usar Free Tier!

**Cobertura Free Tier (12 meses):**
```
✅ EC2 t2.micro:     750 horas/mês (suficiente para 1 instância 24/7)
✅ S3:               5 GB storage
✅ CloudFront:       50 GB data transfer/mês
✅ Data Transfer:    100 GB out/mês
✅ CloudWatch Logs:  5 GB (sempre grátis)
✅ SSM Parameters:   10.000 parâmetros (sempre grátis)
```

**Custo real no primeiro ano:**
- **AWS:** $0/mês (Free Tier)
- **Anthropic API:** ~$2-10/mês (pago por uso)
- **Tavily API:** $0/mês (1000 créditos grátis)

**Total:** Apenas o custo das APIs! (~$24-120/ano)

### 💰 Após Free Tier (12 meses)

**Custo estimado:** $10-20/mês para uso leve/médio

Veja análise completa em: `terraform/CUSTOS.md`

## 🚀 Como Começar

### Opção 1: Quick Start (10 minutos)

```bash
cd terraform/
cat QUICKSTART.md  # Leia este primeiro!
```

### Opção 2: Guia Completo (recomendado)

```bash
cd terraform/
cat README_TERRAFORM.md  # Guia detalhado com troubleshooting
```

## 📋 Checklist de Deploy

```bash
# 1. Pré-requisitos
[ ] Conta AWS criada (primeira conta = Free Tier 12 meses)
[ ] AWS CLI instalado e configurado (aws configure)
[ ] Terraform instalado (brew install terraform)
[ ] Node.js 18+ instalado

# 2. Criar key pair SSH
aws ec2 create-key-pair \
  --key-name langgraph-key \
  --query 'KeyMaterial' \
  --output text > ~/.ssh/langgraph-key.pem
chmod 400 ~/.ssh/langgraph-key.pem

# 3. Configurar Terraform
cd terraform/
cp terraform.tfvars.example terraform.tfvars
nano terraform.tfvars  # Editar: API keys, bucket name, SSH IP

# 4. Deploy infraestrutura
terraform init
terraform apply

# 5. Deploy frontend
cd ..
./terraform/scripts/build-frontend.sh \
  $(terraform -chdir=terraform output -raw backend_api_url) \
  $(terraform -chdir=terraform output -raw s3_bucket_name) \
  $(terraform -chdir=terraform output -raw cloudfront_distribution_id)

# 6. Acessar aplicação
terraform -chdir=terraform output frontend_url
```

## 🏗️ Arquitetura

```
                    Internet
                       │
          ┌────────────┴────────────┐
          │                         │
    CloudFront (CDN)          EC2 t2.micro
          │                    (Backend)
          │                         │
    S3 Bucket              ┌────────┴────────┐
    (Frontend)             │                 │
                    SSM Parameters   CloudWatch Logs
                    (API Keys)       (Monitoramento)
```

## 🎓 O que você vai aprender

Ao usar essa infraestrutura, você aprenderá:

✅ Terraform (Infrastructure as Code)
✅ AWS VPC, Subnets, Security Groups
✅ EC2 instances e Elastic IPs
✅ S3 bucket policies e static website
✅ CloudFront distributions e CDN
✅ IAM roles, policies e instance profiles
✅ SSM Parameter Store (armazenamento seguro)
✅ CloudWatch Logs (monitoramento)
✅ Systemd services (Linux)
✅ User data scripts (auto-configuration)

## 💡 Dicas Importantes

### Segurança

⚠️ **NUNCA** commite `terraform.tfvars` (contém API keys!)
✅ Já está no `.gitignore`

⚠️ **SEMPRE** configure `allowed_ssh_ips` com seu IP real
❌ `0.0.0.0/0` é INSEGURO!
✅ Use: `$(curl -s ifconfig.me)/32`

### Economia

💰 **Desligar EC2 fora do horário:** Economiza ~70% ($6/mês)
```hcl
enable_auto_shutdown = true
```

💰 **Usar S3 sem CloudFront:** Economiza ~$4-8/mês
```hcl
enable_cloudfront = false
```

### Monitoramento

```bash
# Ver logs do backend
ssh -i ~/.ssh/langgraph-key.pem ec2-user@IP-PUBLICO \
  "sudo journalctl -u langgraph-backend -f"

# Monitorar custos
# AWS Console > Cost Explorer
```

## 📚 Documentação Adicional

| Arquivo | Conteúdo |
|---------|----------|
| `terraform/README_TERRAFORM.md` | Guia completo com troubleshooting |
| `terraform/QUICKSTART.md` | Deploy rápido em 10 minutos |
| `terraform/CUSTOS.md` | Análise detalhada de custos |
| `terraform/terraform.tfvars.example` | Exemplo de configuração |

## 🔧 Comandos Úteis

```bash
# Ver outputs do Terraform
terraform -chdir=terraform output

# Acessar EC2 via SSH
ssh -i ~/.ssh/langgraph-key.pem ec2-user@$(terraform -chdir=terraform output -raw backend_public_ip)

# Ver logs do backend
ssh -i ~/.ssh/langgraph-key.pem ec2-user@IP \
  "sudo journalctl -u langgraph-backend -f"

# Parar EC2 (economizar)
aws ec2 stop-instances --instance-ids INSTANCE-ID

# Atualizar frontend
./terraform/scripts/build-frontend.sh BACKEND_URL S3_BUCKET CLOUDFRONT_ID

# Destruir tudo
terraform -chdir=terraform destroy
```

## ❓ FAQ

**Q: Quanto tempo leva o deploy?**
A: 5-10 minutos para infraestrutura, 1-2 minutos para frontend.

**Q: Posso usar sem CloudFront?**
A: Sim! Configure `enable_cloudfront = false` e economize ~$4-8/mês.

**Q: Como atualizar a aplicação?**
A: Backend: SSH + git pull + restart. Frontend: Re-run build script.

**Q: Free Tier expira, e agora?**
A: Após 12 meses, custa ~$10-20/mês. Veja alternativas em `CUSTOS.md`.

**Q: Posso usar em produção?**
A: Sim, mas recomendo:
- Adicionar certificado SSL (ACM + Route53)
- Configurar domínio personalizado
- Habilitar auto-scaling (se tráfego crescer)
- Implementar CI/CD (GitHub Actions)

## 🤝 Suporte

Problemas com o deploy?

1. ✅ Leia `terraform/README_TERRAFORM.md` (seção Troubleshooting)
2. ✅ Verifique logs: `sudo journalctl -u langgraph-backend`
3. ✅ Teste conectividade: `curl http://IP:8000/health`
4. ❓ Ainda com problemas? Abra uma issue no GitHub

## 🎉 Pronto para começar?

```bash
cd terraform/
cat QUICKSTART.md  # Comece por aqui!
```

---

**Desenvolvido com ❤️ usando Terraform + AWS**

**Free Tier friendly ✅ | Production ready ✅ | Fully documented ✅**
