#!/bin/bash
# Script de health check para debug

echo "Status da Aplicação Flask"
echo "=========================="
echo "Verificando Python..."
python --version

echo ""
echo "Verificando Dependências..."
pip list | grep -E "flask|routeros|requests"

echo ""
echo "Testando conexão local..."
curl -v http://localhost:8000/ 2>&1 | head -20

echo ""
echo "Logs do Flask..."
tail -50 /tmp/flask.log 2>/dev/null || echo "Log não disponível"
