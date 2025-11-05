# ========================================
# S3 BUCKET - FRONTEND ESTÁTICO
# ========================================

# ----------------------------------------
# S3 Bucket para hospedar Next.js build
# ----------------------------------------

resource "aws_s3_bucket" "frontend" {
  bucket = var.s3_bucket_name

  tags = {
    Name = "${var.project_name}-frontend"
  }
}

# ----------------------------------------
# Configuração de versionamento (opcional)
# ----------------------------------------

resource "aws_s3_bucket_versioning" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  versioning_configuration {
    status = "Disabled" # Ative para produção se desejar
  }
}

# ----------------------------------------
# Configuração de criptografia
# ----------------------------------------

resource "aws_s3_bucket_server_side_encryption_configuration" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# ----------------------------------------
# Bloquear acesso público (CloudFront usa OAI)
# ----------------------------------------

resource "aws_s3_bucket_public_access_block" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# ----------------------------------------
# Política do bucket (permite CloudFront OAI)
# ----------------------------------------

resource "aws_s3_bucket_policy" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowCloudFrontOAI"
        Effect = "Allow"
        Principal = {
          AWS = aws_cloudfront_origin_access_identity.main.iam_arn
        }
        Action   = "s3:GetObject"
        Resource = "${aws_s3_bucket.frontend.arn}/*"
      }
    ]
  })
}

# ----------------------------------------
# Configuração de website (para fallback)
# ----------------------------------------

resource "aws_s3_bucket_website_configuration" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "404.html"
  }
}

# ----------------------------------------
# Lifecycle policy para logs (economizar)
# ----------------------------------------

resource "aws_s3_bucket_lifecycle_configuration" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  rule {
    id     = "delete-old-logs"
    status = "Enabled"

    filter {
      prefix = "logs/"
    }

    expiration {
      days = 30
    }
  }

  rule {
    id     = "abort-incomplete-uploads"
    status = "Enabled"

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}

# ----------------------------------------
# Bucket CORS (para APIs)
# ----------------------------------------

resource "aws_s3_bucket_cors_configuration" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "HEAD"]
    allowed_origins = ["*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3600
  }
}
