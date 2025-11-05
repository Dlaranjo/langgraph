# ========================================
# TERRAFORM MAIN CONFIG - LANGGRAPH AWS
# ========================================

terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Backend para estado remoto (opcional, mas recomendado)
  # Descomente após criar bucket S3 para terraform state
  # backend "s3" {
  #   bucket         = "seu-bucket-terraform-state"
  #   key            = "langgraph/terraform.tfstate"
  #   region         = "us-east-1"
  #   encrypt        = true
  #   dynamodb_table = "terraform-state-lock"
  # }
}

# ----------------------------------------
# Provider AWS
# ----------------------------------------

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = var.common_tags
  }
}

# ----------------------------------------
# Data Sources
# ----------------------------------------

# Busca a AMI mais recente do Amazon Linux 2023
data "aws_ami" "amazon_linux_2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Busca availability zones disponíveis
data "aws_availability_zones" "available" {
  state = "available"
}

# Busca account ID atual
data "aws_caller_identity" "current" {}
