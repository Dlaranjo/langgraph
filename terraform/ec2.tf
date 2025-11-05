# ========================================
# EC2 INSTANCE - BACKEND FASTAPI
# ========================================

# ----------------------------------------
# EC2 Instance (t2.micro - Free Tier)
# ----------------------------------------

resource "aws_instance" "backend" {
  ami                    = var.ec2_ami_id != "" ? var.ec2_ami_id : data.aws_ami.amazon_linux_2023.id
  instance_type          = var.ec2_instance_type
  key_name               = var.ec2_key_pair_name
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.backend.id]
  iam_instance_profile   = aws_iam_instance_profile.ec2_backend.name

  # User data para configuração automática
  user_data = templatefile("${path.module}/scripts/user-data.sh", {
    project_name       = var.project_name
    aws_region         = var.aws_region
    backend_repo_url   = "https://github.com/seu-usuario/langgraph.git" # Mude para seu repo
    anthropic_key_path = aws_ssm_parameter.anthropic_api_key.name
    tavily_key_path    = var.tavily_api_key != "" ? aws_ssm_parameter.tavily_api_key[0].name : ""
  })

  # Disco root (8GB é suficiente, Free Tier oferece até 30GB)
  root_block_device {
    volume_size           = 8
    volume_type           = "gp3"
    delete_on_termination = true
    encrypted             = true

    tags = {
      Name = "${var.project_name}-root-volume"
    }
  }

  # Metadados
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required" # IMDSv2 obrigatório (segurança)
    http_put_response_hop_limit = 1
  }

  tags = {
    Name = "${var.project_name}-backend"
  }

  lifecycle {
    ignore_changes = [
      ami, # Ignora mudanças na AMI após criação
    ]
  }
}

# ----------------------------------------
# Elastic IP (IP público fixo)
# ----------------------------------------

resource "aws_eip" "backend" {
  domain   = "vpc"
  instance = aws_instance.backend.id

  tags = {
    Name = "${var.project_name}-backend-eip"
  }

  depends_on = [aws_internet_gateway.main]
}

# ----------------------------------------
# CloudWatch Log Group (logs da aplicação)
# ----------------------------------------

resource "aws_cloudwatch_log_group" "backend" {
  name              = "/aws/ec2/${var.project_name}"
  retention_in_days = 7 # Free tier: até 5GB

  tags = {
    Name = "${var.project_name}-logs"
  }
}

# ----------------------------------------
# EventBridge para Auto Shutdown (opcional)
# ----------------------------------------

resource "aws_cloudwatch_event_rule" "auto_shutdown" {
  count               = var.enable_auto_shutdown ? 1 : 0
  name                = "${var.project_name}-auto-shutdown"
  description         = "Desliga EC2 automaticamente para economizar"
  schedule_expression = "cron(0 ${split(":", var.auto_shutdown_time)[0]} * * ? *)"

  tags = {
    Name = "${var.project_name}-auto-shutdown-rule"
  }
}

resource "aws_cloudwatch_event_target" "auto_shutdown" {
  count     = var.enable_auto_shutdown ? 1 : 0
  rule      = aws_cloudwatch_event_rule.auto_shutdown[0].name
  target_id = "StopEC2Instance"
  arn       = "arn:aws:ssm:${var.aws_region}::document/AWS-StopEC2Instance"
  role_arn  = aws_iam_role.eventbridge[0].arn

  input = jsonencode({
    InstanceId = [aws_instance.backend.id]
  })
}

resource "aws_cloudwatch_event_rule" "auto_startup" {
  count               = var.enable_auto_shutdown ? 1 : 0
  name                = "${var.project_name}-auto-startup"
  description         = "Liga EC2 automaticamente"
  schedule_expression = "cron(0 ${split(":", var.auto_startup_time)[0]} * * ? *)"

  tags = {
    Name = "${var.project_name}-auto-startup-rule"
  }
}

resource "aws_cloudwatch_event_target" "auto_startup" {
  count     = var.enable_auto_shutdown ? 1 : 0
  rule      = aws_cloudwatch_event_rule.auto_startup[0].name
  target_id = "StartEC2Instance"
  arn       = "arn:aws:ssm:${var.aws_region}::document/AWS-StartEC2Instance"
  role_arn  = aws_iam_role.eventbridge[0].arn

  input = jsonencode({
    InstanceId = [aws_instance.backend.id]
  })
}

# ----------------------------------------
# IAM Role para EventBridge (shutdown/startup)
# ----------------------------------------

resource "aws_iam_role" "eventbridge" {
  count = var.enable_auto_shutdown ? 1 : 0
  name  = "${var.project_name}-eventbridge-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "events.amazonaws.com"
        }
      }
    ]
  })

  inline_policy {
    name = "ec2-start-stop"
    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Effect = "Allow"
          Action = [
            "ec2:StartInstances",
            "ec2:StopInstances"
          ]
          Resource = aws_instance.backend.arn
        }
      ]
    })
  }
}
