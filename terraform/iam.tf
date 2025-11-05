# ========================================
# IAM ROLES E POLICIES - LANGGRAPH
# ========================================

# ----------------------------------------
# IAM Role para EC2 (Backend)
# ----------------------------------------

resource "aws_iam_role" "ec2_backend" {
  name = "${var.project_name}-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "${var.project_name}-ec2-role"
  }
}

# ----------------------------------------
# Policy para acessar SSM Parameter Store (API Keys)
# ----------------------------------------

resource "aws_iam_role_policy" "ssm_access" {
  name = "${var.project_name}-ssm-access"
  role = aws_iam_role.ec2_backend.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ssm:GetParameter",
          "ssm:GetParameters",
          "ssm:GetParametersByPath"
        ]
        Resource = [
          "arn:aws:ssm:${var.aws_region}:${data.aws_caller_identity.current.account_id}:parameter/${var.project_name}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "kms:Decrypt"
        ]
        Resource = "*"
      }
    ]
  })
}

# ----------------------------------------
# Policy para CloudWatch Logs (monitoramento)
# ----------------------------------------

resource "aws_iam_role_policy" "cloudwatch_logs" {
  name = "${var.project_name}-cloudwatch-logs"
  role = aws_iam_role.ec2_backend.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:DescribeLogStreams"
        ]
        Resource = "arn:aws:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/ec2/${var.project_name}*"
      }
    ]
  })
}

# ----------------------------------------
# Instance Profile (anexa role à EC2)
# ----------------------------------------

resource "aws_iam_instance_profile" "ec2_backend" {
  name = "${var.project_name}-ec2-profile"
  role = aws_iam_role.ec2_backend.name

  tags = {
    Name = "${var.project_name}-ec2-profile"
  }
}

# ----------------------------------------
# SSM Parameters (armazenamento seguro de API keys)
# ----------------------------------------

resource "aws_ssm_parameter" "anthropic_api_key" {
  name        = "/${var.project_name}/anthropic_api_key"
  description = "Anthropic Claude API Key"
  type        = "SecureString"
  value       = var.anthropic_api_key

  tags = {
    Name = "${var.project_name}-anthropic-key"
  }
}

resource "aws_ssm_parameter" "tavily_api_key" {
  count       = var.tavily_api_key != "" ? 1 : 0
  name        = "/${var.project_name}/tavily_api_key"
  description = "Tavily Search API Key"
  type        = "SecureString"
  value       = var.tavily_api_key

  tags = {
    Name = "${var.project_name}-tavily-key"
  }
}

# ----------------------------------------
# CloudFront Origin Access Identity (para S3)
# ----------------------------------------

resource "aws_cloudfront_origin_access_identity" "main" {
  comment = "${var.project_name} CloudFront OAI"
}
