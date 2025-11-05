# ========================================
# TERRAFORM OUTPUTS - LANGGRAPH
# ========================================

# ----------------------------------------
# Backend (EC2)
# ----------------------------------------

output "backend_public_ip" {
  description = "IP público do backend (EC2)"
  value       = aws_eip.backend.public_ip
}

output "backend_public_dns" {
  description = "DNS público do backend (EC2)"
  value       = aws_eip.backend.public_dns
}

output "backend_api_url" {
  description = "URL da API FastAPI"
  value       = "http://${aws_eip.backend.public_ip}:8000"
}

output "backend_api_docs" {
  description = "URL da documentação Swagger"
  value       = "http://${aws_eip.backend.public_ip}:8000/docs"
}

output "backend_ssh_command" {
  description = "Comando SSH para acessar o backend"
  value       = "ssh -i ~/.ssh/${var.ec2_key_pair_name}.pem ec2-user@${aws_eip.backend.public_ip}"
}

# ----------------------------------------
# Frontend (S3 + CloudFront)
# ----------------------------------------

output "s3_bucket_name" {
  description = "Nome do bucket S3 do frontend"
  value       = aws_s3_bucket.frontend.id
}

output "s3_bucket_website_endpoint" {
  description = "Endpoint do website S3"
  value       = aws_s3_bucket_website_configuration.frontend.website_endpoint
}

output "cloudfront_distribution_id" {
  description = "ID da distribuição CloudFront"
  value       = var.enable_cloudfront ? aws_cloudfront_distribution.frontend[0].id : "CloudFront desabilitado"
}

output "cloudfront_domain_name" {
  description = "Domain name do CloudFront (URL principal do frontend)"
  value       = var.enable_cloudfront ? "https://${aws_cloudfront_distribution.frontend[0].domain_name}" : "CloudFront desabilitado"
}

output "frontend_url" {
  description = "URL principal do frontend"
  value       = var.enable_cloudfront ? "https://${aws_cloudfront_distribution.frontend[0].domain_name}" : "http://${aws_s3_bucket_website_configuration.frontend.website_endpoint}"
}

# ----------------------------------------
# Rede (VPC)
# ----------------------------------------

output "vpc_id" {
  description = "ID da VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_id" {
  description = "ID da subnet pública"
  value       = aws_subnet.public.id
}

# ----------------------------------------
# Segurança (IAM)
# ----------------------------------------

output "ssm_anthropic_key_path" {
  description = "Caminho do parâmetro SSM com a chave Anthropic"
  value       = aws_ssm_parameter.anthropic_api_key.name
  sensitive   = true
}

output "ssm_tavily_key_path" {
  description = "Caminho do parâmetro SSM com a chave Tavily"
  value       = var.tavily_api_key != "" ? aws_ssm_parameter.tavily_api_key[0].name : "Tavily não configurado"
  sensitive   = true
}

# ----------------------------------------
# Comandos úteis
# ----------------------------------------

output "useful_commands" {
  description = "Comandos úteis para gerenciar a infraestrutura"
  value = <<-EOT

    🚀 DEPLOY CONCLUÍDO!

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📱 URLs DA APLICAÇÃO
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    Frontend: ${var.enable_cloudfront ? "https://${aws_cloudfront_distribution.frontend[0].domain_name}" : "http://${aws_s3_bucket_website_configuration.frontend.website_endpoint}"}
    Backend:  http://${aws_eip.backend.public_ip}:8000
    API Docs: http://${aws_eip.backend.public_ip}:8000/docs

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🔧 COMANDOS DE GERENCIAMENTO
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    # Acessar backend via SSH:
    ssh -i ~/.ssh/${var.ec2_key_pair_name}.pem ec2-user@${aws_eip.backend.public_ip}

    # Ver logs do backend:
    ssh -i ~/.ssh/${var.ec2_key_pair_name}.pem ec2-user@${aws_eip.backend.public_ip} \
      "sudo journalctl -u langgraph-backend -f"

    # Upload arquivos frontend para S3:
    aws s3 sync ./frontend/out s3://${aws_s3_bucket.frontend.id} --delete

    # Invalidar cache CloudFront (após deploy):
    ${var.enable_cloudfront ? "aws cloudfront create-invalidation --distribution-id ${aws_cloudfront_distribution.frontend[0].id} --paths \"/*\"" : "N/A - CloudFront desabilitado"}

    # Parar EC2 (economizar Free Tier):
    aws ec2 stop-instances --instance-ids ${aws_instance.backend.id}

    # Iniciar EC2:
    aws ec2 start-instances --instance-ids ${aws_instance.backend.id}

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📊 MONITORAMENTO
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    CloudWatch Logs: https://console.aws.amazon.com/cloudwatch/home?region=${var.aws_region}#logsV2:log-groups/log-group/${replace(aws_cloudwatch_log_group.backend.name, "/", "$252F")}

    EC2 Console: https://console.aws.amazon.com/ec2/home?region=${var.aws_region}#Instances:instanceId=${aws_instance.backend.id}

    S3 Console: https://s3.console.aws.amazon.com/s3/buckets/${aws_s3_bucket.frontend.id}

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  EOT
}

# ----------------------------------------
# Custos estimados
# ----------------------------------------

output "estimated_costs" {
  description = "Custos estimados mensais (após Free Tier)"
  value = <<-EOT

    💰 CUSTOS ESTIMADOS (após 12 meses de Free Tier):

    • EC2 t2.micro (24/7):     ~$8-10/mês
    • S3 (5GB):                ~$0.12/mês
    • CloudFront (50GB):       ~$4.25/mês
    • Data Transfer:           ~$0-5/mês

    TOTAL: ~$12-20/mês

    💡 DICAS PARA ECONOMIZAR:
    • Desligar EC2 fora do horário (economiza ~70%)
    • Usar apenas S3 sem CloudFront (economiza ~$4/mês)
    • Monitorar uso no AWS Cost Explorer

  EOT
}
