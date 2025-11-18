#!/bin/bash
set -e

echo "🚀 Initializing ASFOTEC-MLStack..."

# 1. Install dependencies
echo "📦 Installing dependencies..."
if command -v poetry &> /dev/null; then
    poetry install
else
    echo "⚠️ Poetry not found. Skipping python dependency install (assuming handled or not needed for docker run)."
fi

if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ .env created from .env.example"
    else
        echo "⚠️ .env.example not found, skipping .env creation"
    fi
fi

# 2. Launch Docker Stack
echo "🐳 Launching Docker Stack..."
make up

# 3. Wait for API
echo "⏳ Waiting for API to be ready..."
until curl -s http://localhost:8000/health > /dev/null; do
    sleep 2
    echo -n "."
done
echo ""
echo "✅ API is ready at http://localhost:8000"

# 4. Launch UI
echo "🖥️  Setting up UI..."
cd apps/ui
npm install

echo "🚀 Starting UI (Preview Mode)..."
echo "The UI will be available at http://localhost:4000"
npm run preview
