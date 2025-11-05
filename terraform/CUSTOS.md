# 💰 Guia Completo de Custos AWS

Análise detalhada dos custos para hospedar o LangGraph Research Agent na AWS.

## 📊 Free Tier (12 meses após criar conta)

### O que está incluído GRÁTIS:

| Serviço | Free Tier | Duração |
|---------|-----------|---------|
| **EC2 t2.micro** | 750 horas/mês | 12 meses |
| **S3 Storage** | 5 GB | 12 meses |
| **S3 Requests** | 20.000 GET, 2.000 PUT | 12 meses |
| **CloudFront Data Transfer** | 50 GB/mês | 12 meses |
| **CloudFront Requests** | 2.000.000/mês | 12 meses |
| **Data Transfer Out** | 100 GB/mês | 12 meses |
| **CloudWatch Logs** | 5 GB | Sempre grátis |
| **SSM Parameter Store** | 10.000 parâmetros | Sempre grátis |

### Cálculo: 1 instância EC2 24/7

```
750 horas/mês ÷ 730 horas (média/mês) = 1,03 instâncias

✅ Você PODE rodar 1 instância t2.micro 24/7 no Free Tier!
```

## 💵 Custos APÓS Free Tier (12 meses)

### Cenário 1: Uso Leve (recomendado)
**Perfil:** 10-20 usuários/dia, 100 pesquisas/mês

| Serviço | Uso | Custo/mês |
|---------|-----|-----------|
| **EC2 t2.micro** | 24/7 | $8.50 |
| **Elastic IP** | 1 IP | $0 (free se attached) |
| **S3 Storage** | 2 GB | $0.05 |
| **CloudFront** | 20 GB data transfer | $1.70 |
| **Data Transfer** | 5 GB out | $0.45 |
| **CloudWatch Logs** | < 5GB | $0 (free tier) |
| **TOTAL** | | **~$10.70/mês** |

### Cenário 2: Uso Médio
**Perfil:** 50-100 usuários/dia, 500 pesquisas/mês

| Serviço | Uso | Custo/mês |
|---------|-----|-----------|
| **EC2 t2.micro** | 24/7 | $8.50 |
| **S3 Storage** | 5 GB | $0.12 |
| **CloudFront** | 100 GB data transfer | $8.50 |
| **Data Transfer** | 20 GB out | $1.80 |
| **TOTAL** | | **~$18.92/mês** |

### Cenário 3: Uso Pesado
**Perfil:** 200+ usuários/dia, 2000 pesquisas/mês

| Serviço | Uso | Custo/mês |
|---------|-----|-----------|
| **EC2 t2.small** (upgrade) | 24/7 | $16.70 |
| **S3 Storage** | 10 GB | $0.23 |
| **CloudFront** | 300 GB data transfer | $25.50 |
| **Data Transfer** | 50 GB out | $4.50 |
| **TOTAL** | | **~$46.93/mês** |

## 🔥 Custos das APIs Externas

### Anthropic Claude (modelo usado: Claude 3.5 Sonnet)

| Operação | Custo | Estimativa |
|----------|-------|-----------|
| **Input tokens** | $3 / 1M tokens | 100 pesquisas = $0.30-0.60 |
| **Output tokens** | $15 / 1M tokens | 100 pesquisas = $1.50-3.00 |
| **Estimativa/pesquisa** | | ~$0.02-0.04 |

**Exemplo mensal:**
- 100 pesquisas/mês = $2-4/mês
- 500 pesquisas/mês = $10-20/mês
- 2000 pesquisas/mês = $40-80/mês

### Tavily Search API

| Plano | Custo | Créditos/mês |
|-------|-------|--------------|
| **Free** | $0 | 1.000 |
| **Basic** | $29 | 10.000 |
| **Pro** | $99 | 50.000 |

**1 pesquisa = 1 crédito**

## 💡 Estratégias para ECONOMIZAR

### 1. Desligar EC2 fora do horário (⭐ Maior economia)

```hcl
# terraform.tfvars
enable_auto_shutdown = true
auto_shutdown_time   = "02:00"  # Desliga 2 AM UTC
auto_startup_time    = "12:00"  # Liga 12 PM UTC
```

**Economia:** ~$6/mês (70% do custo EC2)

### 2. Usar S3 sem CloudFront

```hcl
# terraform.tfvars
enable_cloudfront = false
```

**Economia:** ~$4-8/mês
**Trade-off:** Latência maior para usuários distantes

### 3. Usar região mais barata

| Região | EC2 t2.micro/mês | Diferença |
|--------|------------------|-----------|
| **us-east-1** (N. Virginia) | $8.50 | Baseline |
| **us-west-2** (Oregon) | $8.76 | +3% |
| **eu-west-1** (Irlanda) | $9.50 | +12% |
| **ap-southeast-1** (Singapura) | $10.20 | +20% |

**Recomendação:** Use `us-east-1` (mais barato)

### 4. Parar/iniciar manualmente

```bash
# Parar quando não usar (ex: finais de semana)
aws ec2 stop-instances --instance-ids i-xxxxx

# Economia: ~$2.50 por dia parado
```

### 5. Limitar uso das APIs

- Cache resultados de pesquisas similares
- Configurar `max_iterations=1` (menos tokens)
- Implementar rate limiting

### 6. Otimizar CloudFront

```hcl
# Usar apenas edge locations baratos
cloudfront_price_class = "PriceClass_100"  # US, Canadá, Europa
```

**Economia:** ~30% vs PriceClass_All

## 📈 Comparação: AWS vs Alternativas

### AWS (nossa solução)
- **Custo:** $10-20/mês após Free Tier
- **Controle:** Total
- **Escalabilidade:** Ilimitada
- **Complexidade:** Média-Alta

### Vercel (Frontend) + Railway (Backend)
- **Custo:** $5-15/mês
- **Controle:** Limitado
- **Escalabilidade:** Boa
- **Complexidade:** Baixa

### Fly.io (tudo em um)
- **Custo:** $5-10/mês (1 máquina shared-cpu)
- **Controle:** Médio
- **Escalabilidade:** Boa
- **Complexidade:** Baixa

### Heroku
- **Custo:** $7/mês (Eco Dynos)
- **Controle:** Limitado
- **Escalabilidade:** Média
- **Complexidade:** Muito Baixa

## 🎯 Custo Total Real (primeiro ano)

### Cenário: Uso pessoal/estudo

| Item | Custo |
|------|-------|
| **AWS (meses 1-12)** | $0 (Free Tier) |
| **Anthropic API** | ~$2-10/mês = $24-120/ano |
| **Tavily API** | $0 (Free tier) |
| **TOTAL ano 1** | **$24-120** |

### Cenário: Projeto real (após Free Tier)

| Item | Custo |
|------|-------|
| **AWS** | $10-20/mês |
| **Anthropic API** | $20-50/mês (500+ pesquisas) |
| **Tavily API** | $0-29/mês |
| **TOTAL/mês** | **$30-99/mês** |
| **TOTAL/ano** | **$360-1188/ano** |

## ⚠️ Custos Ocultos a Evitar

### 1. Elastic IP não utilizado
**Custo:** $3.60/mês
**Solução:** Sempre keep attached ou delete

### 2. Snapshots de EBS esquecidos
**Custo:** $0.05/GB/mês
**Solução:** Delete snapshots antigos

### 3. Data transfer entre regiões
**Custo:** $0.02/GB
**Solução:** Keep tudo na mesma região

### 4. CloudFront invalidações excessivas
**Custo:** $0.005 por path após 1000/mês
**Solução:** Use wildcards (`/*`) ao invés de múltiplos paths

### 5. CloudWatch Logs acumulados
**Custo:** $0.50/GB após 5GB
**Solução:** Configure retention (7 dias)

## 🔍 Monitorar Custos

### Habilitar Cost Explorer

```bash
# Via AWS Console
AWS Console > Cost Management > Cost Explorer > Enable

# Criar orçamento
AWS Console > Billing > Budgets > Create budget
# Alerta: $10/mês (se ultrapassar Free Tier)
```

### Ver custos em tempo real

```bash
# Via CLI
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost
```

### Alertas de custo

```bash
# Criar SNS topic para alertas
aws sns create-topic --name billing-alerts

# Criar CloudWatch alarm
aws cloudwatch put-metric-alarm \
  --alarm-name billing-alarm \
  --alarm-description "Alert when bill exceeds $15" \
  --metric-name EstimatedCharges \
  --namespace AWS/Billing \
  --statistic Maximum \
  --period 21600 \
  --threshold 15 \
  --comparison-operator GreaterThanThreshold
```

## 📝 Resumo: Vale a Pena?

### ✅ AWS Free Tier é ideal se:
- É seu primeiro cadastro
- Vai usar por até 12 meses
- Quer aprender AWS
- Uso é < 500 pesquisas/mês

### ✅ Alternativas são melhores se:
- Não quer gerenciar infraestrutura
- Precisa de deploy rápido
- Orçamento < $20/mês garantido
- Não precisa de Free Tier

### 💡 Recomendação Final

**Para aprendizado:** Use AWS Free Tier (custo real: apenas APIs)

**Para produção leve:** Vercel + Railway ($5-15/mês total)

**Para produção pesada:** AWS com otimizações ($20-50/mês)

---

**📧 Dúvidas sobre custos? Abra uma issue no GitHub!**
