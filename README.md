# 📊 MikroTik Dashboard API

Dashboard interativo para gerenciar e monitorar roteadores MikroTik via API.

## ✨ Funcionalidades

- 📡 **Monitoramento de Interfaces**: Visualize o status de todas as interfaces
- 🖥️ **Hosts Conectados**: Veja todos os dispositivos na rede
- 📈 **DHCP Leases**: Gerencie concessões DHCP
- ⚡ **Controle de Velocidade**: Ajuste limites de banda por fila
- 🚀 **Boost de Rede**: Limpe cache DNS e otimize performance
- 🗺️ **Mapa de Rede**: Visualize a topologia da rede
- 📊 **Análise de Recursos**: Monitore CPU, memória e disco
- 🔌 **PPP e Hotspot**: Gerencie conexões PPP e hotspot

---

## 🚀 Deployment no Orbitan/Coolify

### Pré-requisitos

- Repositório GitHub com este código
- Acesso ao Orbitan/Coolify
- MikroTik com API habilitada (porta 8728)

### Passo 1: Conectar Repositório

1. No Orbitan, clique em **New Application**
2. Selecione **Docker**
3. Conecte seu repositório GitHub

### Passo 2: Configurar Rede

Na aba **Configuration → Network**:
- Defina **Ports Exposed**: `8000`

### Passo 3: Limpar Build

Na aba **Configuration → Build**:
- **Install Command**: deixe vazio
- **Build Command**: deixe vazio
- **Start Command**: deixe vazio

### Passo 4: Configurar MikroTik

Na aba **Environment Variables**, adicione:
```
ROUTER_IP=192.168.15.2
USERNAME=admin
PASSWORD=123
```

Substitua pelos dados reais do seu MikroTik.

### Passo 5: Deploy

Clique em **Force Rebuild** e aguarde até que o status mude para 🟢 **Running**.

---

## 🧪 Teste Local com Docker Compose

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/Microtik_Dashboard_api.git
cd Microtik_Dashboard_api

# Edite docker-compose.yml com os dados do seu MikroTik
# Depois execute:
docker-compose up --build

# Teste em outro terminal
curl http://localhost:8000/health

# Abra no navegador
open http://localhost:8000
```

---

## 📦 Instalação Local (Desenvolvimento)

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/Microtik_Dashboard_api.git
cd Microtik_Dashboard_api

# Crie um ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure o MikroTik em config.py
# Depois execute:
python wsgi.py

# Abra no navegador
open http://localhost:8000
```

---

## 📡 Endpoints da API

### Health Check
```
GET /health
```
Resposta:
```json
{"status": "ok", "message": "Dashboard is running"}
```

### Interfaces
```
GET /interfaces
```
Retorna lista de interfaces do MikroTik.

### Hosts Conectados
```
GET /hosts
```
Retorna tabela ARP com hosts conectados.

### DHCP Leases
```
GET /leases
```
Retorna concessões DHCP ativas.

### Análise de Recursos
```
GET /analysis
```
Retorna CPU, memória, disco e identidade do roteador.

### Filas de Velocidade
```
GET /queues
```
Retorna todas as filas de velocidade configuradas.

### Definir Velocidade
```
POST /set_speed
Content-Type: application/json

{
  "name": "NomeDaFila",
  "limit": "10M/10M"
}
```

### Boost de Rede
```
POST /boost_network
```
Limpa cache DNS para melhorar performance.

### Limpar ARP
```
POST /clear_arp
```
Remove entradas dinâmicas da tabela ARP.

### Limpar DHCP
```
POST /clear_leases
```
Libera IPs não utilizados no DHCP.

### Boost do Jorge (Porta 20)
```
POST /boost_jorge
```
Aplica boost máximo na fila do Jorge/Porta 20.

### Boost Geral
```
POST /boost_all
```
Aplica boost máximo em todas as filas.

### PPP Ativo
```
GET /ppp_active
```
Retorna conexões PPP ativas.

### Hotspot Ativo
```
GET /hotspot_active
```
Retorna usuários hotspot ativos.

### Logs
```
GET /logs?count=100&topics=error,warning
```
Retorna logs do MikroTik.

### Terminal
```
POST /terminal
Content-Type: application/json

{
  "command": "ip address print"
}
```
Executa comandos MikroTik via API.

---

## 🔧 Configuração

### config.py

```python
import os

# MikroTik
ROUTER_IP = os.getenv("ROUTER_IP", "192.168.15.2")
USERNAME = os.getenv("USERNAME", "admin")
PASSWORD = os.getenv("PASSWORD", "123")

# Telegram (opcional)
TELEGRAM_TOKEN = "TOKEN_DO_BOT"
TELEGRAM_CHAT = "CHAT_ID"
```

Todas as configurações podem ser definidas via variáveis de ambiente.

---

## 🐛 Troubleshooting

Se receber erro `ERR_CONNECTION_REFUSED`:

1. Verifique se a porta 8000 está exposta no Orbitan
2. Confirme que os Build commands estão vazios
3. Clique em **Force Rebuild**
4. Verifique os logs no Orbitan

Para mais detalhes, veja [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

---

## 📝 Estrutura do Projeto

```
.
├── app.py                  # Aplicação Flask principal
├── config.py              # Configurações (suporta env vars)
├── wsgi.py               # Entry point para Gunicorn
├── requirements.txt      # Dependências Python
├── Dockerfile            # Configuração Docker
├── docker-compose.yml    # Compose para testes locais
├── start.py             # Script de inicialização (legado)
├── health_check.sh      # Script de health check
├── TROUBLESHOOTING.md   # Guia de troubleshooting
├── README.md            # Este arquivo
├── templates/
│   └── index.html       # Interface do dashboard
└── Desktop/
    └── MIcrotik api/    # Versão alternativa (legada)
```

---

## 🔐 Segurança

⚠️ **IMPORTANTE**: 
- Nunca commite credenciais no Git
- Use variáveis de ambiente para produção
- Certifique-se que a API do MikroTik está protegida por firewall
- Considere usar HTTPS em produção

---

## 📄 Licença

Este projeto é fornecido como está. Use por sua conta e risco.

---

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

---

## 📞 Suporte

Para problemas ou dúvidas, abra uma issue no repositório GitHub.
