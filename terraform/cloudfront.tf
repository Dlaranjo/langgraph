# ========================================
# CLOUDFRONT CDN - FRONTEND DISTRIBUTION
# ========================================

# ----------------------------------------
# CloudFront Distribution
# ----------------------------------------

resource "aws_cloudfront_distribution" "frontend" {
  count   = var.enable_cloudfront ? 1 : 0
  enabled = true
  comment = "${var.project_name} Frontend CDN"

  # Domínios alternativos (se você tiver um domínio personalizado)
  # aliases = ["seu-dominio.com"]

  # Origem: S3 bucket
  origin {
    domain_name = aws_s3_bucket.frontend.bucket_regional_domain_name
    origin_id   = "S3-${var.s3_bucket_name}"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.main.cloudfront_access_identity_path
    }
  }

  # Configuração padrão de cache
  default_cache_behavior {
    target_origin_id       = "S3-${var.s3_bucket_name}"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD", "OPTIONS"]
    cached_methods         = ["GET", "HEAD", "OPTIONS"]
    compress               = true

    forwarded_values {
      query_string = false
      headers      = []

      cookies {
        forward = "none"
      }
    }

    min_ttl     = 0
    default_ttl = 86400  # 24 horas
    max_ttl     = 604800 # 7 dias
  }

  # Cache behavior para API calls (não cachear)
  ordered_cache_behavior {
    path_pattern           = "/api/*"
    target_origin_id       = "S3-${var.s3_bucket_name}"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"]
    cached_methods         = ["GET", "HEAD"]
    compress               = true

    forwarded_values {
      query_string = true
      headers      = ["Authorization", "Origin"]

      cookies {
        forward = "all"
      }
    }

    min_ttl     = 0
    default_ttl = 0
    max_ttl     = 0
  }

  # Cache behavior para arquivos estáticos (cache agressivo)
  ordered_cache_behavior {
    path_pattern           = "/_next/static/*"
    target_origin_id       = "S3-${var.s3_bucket_name}"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    compress               = true

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    min_ttl     = 31536000 # 1 ano
    default_ttl = 31536000
    max_ttl     = 31536000
  }

  # Configurações de erro personalizadas (SPA routing)
  custom_error_response {
    error_code         = 403
    response_code      = 200
    response_page_path = "/index.html"
  }

  custom_error_response {
    error_code         = 404
    response_code      = 200
    response_page_path = "/index.html"
  }

  # Página padrão
  default_root_object = "index.html"

  # Restrições geográficas (nenhuma por padrão)
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  # Certificado SSL (padrão CloudFront)
  # Para domínio personalizado, use ACM certificate
  viewer_certificate {
    cloudfront_default_certificate = true
    # Para domínio customizado:
    # acm_certificate_arn      = aws_acm_certificate.cert.arn
    # ssl_support_method       = "sni-only"
    # minimum_protocol_version = "TLSv1.2_2021"
  }

  # Classe de preço (otimizado para custo)
  price_class = var.cloudfront_price_class

  # Logs de acesso (opcional)
  # logging_config {
  #   bucket = aws_s3_bucket.logs.bucket_domain_name
  #   prefix = "cloudfront/"
  # }

  tags = {
    Name = "${var.project_name}-cloudfront"
  }
}

# ----------------------------------------
# Invalidação automática de cache (uso manual)
# ----------------------------------------

# Para invalidar cache após deploy:
# aws cloudfront create-invalidation \
#   --distribution-id <ID_DA_DISTRIBUTION> \
#   --paths "/*"

# Ou use o null_resource abaixo (custos: $0.005 por invalidação após as primeiras 1000/mês)

# resource "null_resource" "cloudfront_invalidation" {
#   count = var.enable_cloudfront ? 1 : 0
#
#   triggers = {
#     always_run = timestamp()
#   }
#
#   provisioner "local-exec" {
#     command = <<-EOT
#       aws cloudfront create-invalidation \
#         --distribution-id ${aws_cloudfront_distribution.frontend[0].id} \
#         --paths "/*"
#     EOT
#   }
#
#   depends_on = [aws_cloudfront_distribution.frontend]
# }
