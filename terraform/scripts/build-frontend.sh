#!/bin/bash
# ========================================
# BUILD E DEPLOY DO FRONTEND NEXT.JS
# ========================================

set -e  # Para em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ----------------------------------------
# Verificar argumentos
# ----------------------------------------

if [ $# -lt 2 ]; then
    echo -e "${RED}Uso: $0 <backend_url> <s3_bucket_name> [cloudfront_distribution_id]${NC}"
    echo ""
    echo "Exemplo:"
    echo "  $0 http://3.85.123.45:8000 langgraph-frontend-12345"
    echo "  $0 http://3.85.123.45:8000 langgraph-frontend-12345 E1234567890ABC"
    exit 1
fi

BACKEND_URL=$1
S3_BUCKET=$2
CLOUDFRONT_DIST_ID=${3:-""}

# ----------------------------------------
# Verificar dependências
# ----------------------------------------

echo -e "${BLUE}🔍 Verificando dependências...${NC}"

if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js não encontrado. Instale Node.js 18+${NC}"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm não encontrado. Instale npm${NC}"
    exit 1
fi

if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI não encontrado. Instale aws-cli${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Todas as dependências instaladas${NC}"

# ----------------------------------------
# Configurar variáveis de ambiente
# ----------------------------------------

echo -e "${BLUE}⚙️ Configurando variáveis de ambiente...${NC}"

# Diretório do projeto
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

# Criar arquivo .env.production no frontend
cat <<EOF > "$FRONTEND_DIR/.env.production"
NEXT_PUBLIC_API_URL=$BACKEND_URL
EOF

echo -e "${GREEN}✅ Variáveis configuradas${NC}"

# ----------------------------------------
# Instalar dependências do frontend
# ----------------------------------------

echo -e "${BLUE}📦 Instalando dependências do frontend...${NC}"

cd "$FRONTEND_DIR"

if [ ! -d "node_modules" ]; then
    npm ci
else
    echo "node_modules já existe, pulando instalação..."
fi

# ----------------------------------------
# Build do Next.js
# ----------------------------------------

echo -e "${BLUE}🏗️ Fazendo build do Next.js...${NC}"

# Limpar build anterior
rm -rf .next out

# Build estático
npm run build

# ----------------------------------------
# Exportar como estático
# ----------------------------------------

echo -e "${BLUE}📤 Exportando Next.js como estático...${NC}"

# Verificar se já existe script export no package.json
if grep -q '"export"' package.json; then
    npm run export
else
    # Next.js 13+ usa output: 'export' no next.config.js
    # Verificar se o build já criou a pasta 'out'
    if [ ! -d "out" ]; then
        echo -e "${YELLOW}⚠️ Pasta 'out' não encontrada.${NC}"
        echo -e "${YELLOW}Adicione 'output: \"export\"' ao next.config.js ou 'export' script ao package.json${NC}"

        # Criar pasta out manualmente copiando .next/standalone
        if [ -d ".next" ]; then
            echo -e "${BLUE}Tentando copiar arquivos da build...${NC}"
            mkdir -p out

            # Copiar arquivos públicos
            if [ -d "public" ]; then
                cp -r public/* out/
            fi

            # Copiar arquivos estáticos do Next
            if [ -d ".next/static" ]; then
                mkdir -p out/_next
                cp -r .next/static out/_next/
            fi

            echo -e "${YELLOW}⚠️ Build manual pode não funcionar corretamente${NC}"
            echo -e "${YELLOW}Recomendado: Configure export no next.config.js${NC}"
        else
            echo -e "${RED}❌ Build falhou${NC}"
            exit 1
        fi
    fi
fi

# ----------------------------------------
# Verificar se build foi criado
# ----------------------------------------

if [ ! -d "out" ]; then
    echo -e "${RED}❌ Pasta 'out' não foi criada. Build falhou.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Build concluído${NC}"

# ----------------------------------------
# Upload para S3
# ----------------------------------------

echo -e "${BLUE}☁️ Fazendo upload para S3...${NC}"

aws s3 sync out/ "s3://$S3_BUCKET" \
    --delete \
    --cache-control "public, max-age=31536000, immutable" \
    --exclude "*.html" \
    --exclude "index.html"

# Upload HTML files com cache menor (para permitir atualizações)
aws s3 sync out/ "s3://$S3_BUCKET" \
    --delete \
    --cache-control "public, max-age=0, must-revalidate" \
    --exclude "*" \
    --include "*.html"

echo -e "${GREEN}✅ Upload para S3 concluído${NC}"

# ----------------------------------------
# Invalidar cache CloudFront (se fornecido)
# ----------------------------------------

if [ -n "$CLOUDFRONT_DIST_ID" ]; then
    echo -e "${BLUE}🔄 Invalidando cache do CloudFront...${NC}"

    INVALIDATION_ID=$(aws cloudfront create-invalidation \
        --distribution-id "$CLOUDFRONT_DIST_ID" \
        --paths "/*" \
        --query 'Invalidation.Id' \
        --output text)

    echo -e "${GREEN}✅ Invalidação criada: $INVALIDATION_ID${NC}"
    echo -e "${YELLOW}⏳ Aguardando invalidação (pode levar 5-10 minutos)...${NC}"

    # Aguardar invalidação (opcional, pode comentar para não esperar)
    # aws cloudfront wait invalidation-completed \
    #     --distribution-id "$CLOUDFRONT_DIST_ID" \
    #     --id "$INVALIDATION_ID"

    echo -e "${GREEN}✅ Cache invalidado${NC}"
else
    echo -e "${YELLOW}⚠️ CloudFront Distribution ID não fornecido, pulando invalidação${NC}"
fi

# ----------------------------------------
# Finalização
# ----------------------------------------

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 DEPLOY DO FRONTEND CONCLUÍDO!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}📦 S3 Bucket:${NC} s3://$S3_BUCKET"
echo -e "${BLUE}🌐 Website URL:${NC} http://$S3_BUCKET.s3-website-$(aws configure get region).amazonaws.com"

if [ -n "$CLOUDFRONT_DIST_ID" ]; then
    CLOUDFRONT_DOMAIN=$(aws cloudfront get-distribution \
        --id "$CLOUDFRONT_DIST_ID" \
        --query 'Distribution.DomainName' \
        --output text)
    echo -e "${BLUE}🚀 CloudFront URL:${NC} https://$CLOUDFRONT_DOMAIN"
fi

echo ""
echo -e "${YELLOW}💡 Dica:${NC} Para atualizar o frontend no futuro, execute:"
echo -e "   ${BLUE}$0 $BACKEND_URL $S3_BUCKET${NC}"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
