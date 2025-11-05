# ========================================
# VARIÁVEIS TERRAFORM - LANGGRAPH AWS DEPLOY
# ========================================

# ----------------------------------------
# Configurações Gerais
# ----------------------------------------

variable "project_name" {
  description = "Nome do projeto (usado em tags e nomes de recursos)"
  type        = string
  default     = "langgraph-research-agent"
}

variable "environment" {
  description = "Ambiente (dev, staging, prod)"
  type        = string
  default     = "prod"
}

variable "aws_region" {
  description = "Região AWS para deploy"
  type        = string
  default     = "us-east-1"
}

# ----------------------------------------
# Configurações de Rede (VPC)
# ----------------------------------------

variable "vpc_cidr" {
  description = "CIDR block para a VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block para subnet pública"
  type        = string
  default     = "10.0.1.0/24"
}

variable "availability_zone" {
  description = "Availability Zone para recursos"
  type        = string
  default     = "us-east-1a"
}

# ----------------------------------------
# Configurações EC2 (Backend)
# ----------------------------------------

variable "ec2_instance_type" {
  description = "Tipo de instância EC2 (t2.micro para Free Tier)"
  type        = string
  default     = "t2.micro"
}

variable "ec2_ami_id" {
  description = "AMI ID (deixe vazio para usar Amazon Linux 2023 mais recente)"
  type        = string
  default     = "" # Será buscado automaticamente
}

variable "ec2_key_pair_name" {
  description = "Nome do key pair SSH (crie manualmente no AWS Console)"
  type        = string
  default     = "langgraph-key"
}

variable "allowed_ssh_ips" {
  description = "IPs permitidos para SSH (seu IP público)"
  type        = list(string)
  default     = ["0.0.0.0/0"] # ⚠️ MUDE para seu IP em produção!
}

# ----------------------------------------
# API Keys (serão armazenadas no SSM)
# ----------------------------------------

variable "anthropic_api_key" {
  description = "Chave API Anthropic Claude"
  type        = string
  sensitive   = true
}

variable "tavily_api_key" {
  description = "Chave API Tavily (opcional)"
  type        = string
  sensitive   = true
  default     = ""
}

# ----------------------------------------
# Configurações S3 + CloudFront (Frontend)
# ----------------------------------------

variable "s3_bucket_name" {
  description = "Nome do bucket S3 (deve ser globalmente único)"
  type        = string
  # Exemplo: langgraph-frontend-12345
}

variable "enable_cloudfront" {
  description = "Habilitar CloudFront CDN"
  type        = bool
  default     = true
}

variable "cloudfront_price_class" {
  description = "Classe de preço CloudFront (PriceClass_100 = mais barato)"
  type        = string
  default     = "PriceClass_100" # Apenas US, Canadá, Europa
}

# ----------------------------------------
# Tags Padrão
# ----------------------------------------

variable "common_tags" {
  description = "Tags comuns para todos os recursos"
  type        = map(string)
  default = {
    Project     = "LangGraph Research Agent"
    ManagedBy   = "Terraform"
    Environment = "Production"
  }
}

# ----------------------------------------
# Configurações de Custo
# ----------------------------------------

variable "enable_auto_shutdown" {
  description = "Habilitar desligamento automático EC2 (economiza Free Tier)"
  type        = bool
  default     = false
}

variable "auto_shutdown_time" {
  description = "Horário para desligar EC2 automaticamente (HH:MM UTC)"
  type        = string
  default     = "02:00" # 2 AM UTC
}

variable "auto_startup_time" {
  description = "Horário para ligar EC2 automaticamente (HH:MM UTC)"
  type        = string
  default     = "12:00" # 12 PM UTC
}
