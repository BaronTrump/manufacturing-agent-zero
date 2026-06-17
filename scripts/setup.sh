#!/bin/bash
# setup.sh — One-time setup for Manufacturing Agent Zero

set -e

echo "================================================"
echo "  Manufacturing Agent Zero — Local Setup"
echo "================================================"

# Detect OS
OS="$(uname -s)"
ARCH="$(uname -m)"

echo "OS: $OS $ARCH"

# Check Docker
if ! command -v docker &>/dev/null; then
    echo "ERROR: Docker is required. Install Docker first:"
    echo "  https://docs.docker.com/engine/install/"
    exit 1
fi

echo "Docker: $(docker --version)"

# Check Docker Compose
if command -v docker-compose &>/dev/null; then
    COMPOSE="docker-compose"
elif docker compose version &>/dev/null; then
    COMPOSE="docker compose"
else
    echo "ERROR: Docker Compose is required."
    exit 1
fi

echo "Compose: $($COMPOSE version)"

# Create data directories
mkdir -p data/company-kb data/vector-store data/config

# Pull images
echo ""
echo "Pulling Manufacturing Agent Zero image..."
docker pull barontrump/manufacturing-agent:latest || \
    echo "(will build from source if needed)"

# Setup complete
echo ""
echo "================================================"
echo "  Setup Complete!"
echo "================================================"
echo ""
echo "Start the agent:"
echo "  $COMPOSE up -d"
echo ""
echo "Open Web UI:"
echo "  http://localhost"
echo ""
echo "Train with company data:"
echo "  docker exec manufacturing-agent python scripts/train.py --source /a0/data/company-kb"
echo ""
echo "Select language in Web UI → Settings → Language"
echo ""
echo "Supported languages: English, Spanish, 한국어"
echo "================================================"
