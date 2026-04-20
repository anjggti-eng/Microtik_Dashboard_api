#!/usr/bin/env python3
"""
Script de inicialização da aplicação Flask
Garante que tudo está configurado corretamente
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

def check_config():
    """Verificar configurações antes de iniciar"""
    logger.info("=" * 60)
    logger.info("DASHBOARD INICIALIZANDO")
    logger.info("=" * 60)
    
    # Verificar arquivos necessários
    required_files = ['app.py', 'config.py', 'requirements.txt']
    for file in required_files:
        if not os.path.exists(file):
            logger.error(f"❌ ERRO CRÍTICO: {file} não encontrado!")
            sys.exit(1)
    
    logger.info("✅ Arquivos necessários OK")
    
    # Verificar templates
    if not os.path.exists('templates'):
        logger.warning("⚠️  Pasta templates não encontrada")
    else:
        logger.info("✅ Pasta templates OK")
    
    # Importar dependências
    try:
        import flask
        logger.info(f"✅ Flask versão {flask.__version__} OK")
    except ImportError:
        logger.error("❌ Flask não instalado!")
        sys.exit(1)
    
    try:
        import routeros_api
        logger.info("✅ routeros_api OK")
    except ImportError:
        logger.warning("⚠️  routeros_api não instalado - funcionalidade MikroTik desativada")
    
    try:
        import config
        logger.info(f"✅ config.py OK - Router: {config.ROUTER_IP}")
    except Exception as e:
        logger.error(f"❌ Erro ao carregar config.py: {e}")
        sys.exit(1)
    
    logger.info("=" * 60)
    logger.info("CONFIGURAÇÕES OK - INICIANDO APLICAÇÃO")
    logger.info("=" * 60)

if __name__ == "__main__":
    check_config()
    
    # Importar e rodar a aplicação
    from app import app
    
    logger.info("\n🚀 DASHBOARD ONLINE em http://0.0.0.0:8000")
    logger.info("📡 Endpoints disponíveis:")
    logger.info("   - GET  /health        -> Health check")
    logger.info("   - GET  /              -> Dashboard principal")
    logger.info("   - GET  /interfaces    -> Lista de interfaces")
    logger.info("   - GET  /hosts        -> Hosts conectados")
    logger.info("\n")
    
    app.run(host='0.0.0.0', port=8000, threaded=False, debug=False)
