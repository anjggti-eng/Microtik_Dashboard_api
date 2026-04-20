# Configurações do Roteador MikroTik
# IP do seu MikroTik
import os

# Configurações do Roteador MikroTik
# Prioriza variáveis de ambiente, com fallback para valores padrão
ROUTER_IP = os.getenv("ROUTER_IP", "192.168.15.2")
USERNAME = os.getenv("USERNAME", "admin")
PASSWORD = os.getenv("PASSWORD", "123")

# Configurações do Bot do Telegram
TELEGRAM_TOKEN = "TOKEN_DO_BOT"
TELEGRAM_CHAT = "CHAT_ID"
