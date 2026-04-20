#!/usr/bin/env python3
"""
WSGI entry point para Gunicorn
Garante que a aplicação Flask está pronta para produção
"""
import sys
import os
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def validate_environment():
    """Validar configurações antes de iniciar"""
    logger.info("=" * 70)
    logger.info("🔍 VALIDANDO CONFIGURAÇÕES DE DEPLOY")
    logger.info("=" * 70)
    
    # Verificar arquivos necessários
    required_files = ['app.py', 'config.py']
    for file in required_files:
        if not os.path.exists(file):
            logger.error(f"❌ ERRO CRÍTICO: {file} não encontrado!")
            sys.exit(1)
    
    logger.info("✅ Arquivos necessários encontrados")
    
    # Verificar templates
    if not os.path.exists('templates'):
        logger.warning("⚠️  Pasta templates não encontrada")
    else:
        logger.info("✅ Pasta templates encontrada")
    
    # Importar dependências
    try:
        import flask
        logger.info(f"✅ Flask {flask.__version__} OK")
    except ImportError as e:
        logger.error(f"❌ Flask não instalado: {e}")
        sys.exit(1)
    
    try:
        import config
        router_ip = config.ROUTER_IP
        logger.info(f"✅ config.py OK - Router: {router_ip}")
    except Exception as e:
        logger.error(f"❌ Erro ao carregar config.py: {e}")
        sys.exit(1)
    
    logger.info("=" * 70)
    logger.info("✅ TODAS AS VALIDAÇÕES PASSARAM")
    logger.info("=" * 70)
    logger.info("")

# Validar antes de importar a app
validate_environment()

# Importar a aplicação Flask
from app import app

# Exportar para Gunicorn
if __name__ == "__main__":
    logger.info("🚀 INICIANDO COM GUNICORN")
    logger.info("📡 Servidor ouvindo em 0.0.0.0:8000")
    logger.info("🌐 Endpoints disponíveis:")
    logger.info("   - GET  /health        -> Health check")
    logger.info("   - GET  /              -> Dashboard principal")
    logger.info("   - GET  /interfaces    -> Lista de interfaces")
    logger.info("   - GET  /hosts         -> Hosts conectados")
    logger.info("")
    app.run(host='0.0.0.0', port=8000, threaded=False, debug=False)
