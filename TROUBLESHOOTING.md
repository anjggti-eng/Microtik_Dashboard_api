# TROUBLESHOOTING - Dashboard MikroTik

## ⚠️ Erro: ERR_CONNECTION_REFUSED

Este erro significa que a aplicação não está respondendo na porta 8000. Pode ser causado por:
- Servidor não está ouvindo em `0.0.0.0`
- Porta 8000 não está exposta no container
- Aplicação não iniciou corretamente
- Configurações de rede do Orbitan/Coolify incorretas

---

## 🔧 Solução Passo a Passo no Orbitan/Coolify

### 1️⃣ Verificar Configurações de Rede

Na aba **Configuration → Network**:
- ✅ **Ports Exposed**: `8000`
- ✅ Certifique-se que o container está acessível

### 2️⃣ Limpar Configurações de Build

Na aba **Configuration → Build**:
- ✅ **Install Command**: `DEIXE VAZIO`
- ✅ **Build Command**: `DEIXE VAZIO`
- ✅ **Start Command**: `DEIXE VAZIO`

O Dockerfile cuidará de tudo automaticamente.

### 3️⃣ Configurar Variáveis de Ambiente (Opcional)

Na aba **Environment Variables**, adicione:
```
ROUTER_IP=192.168.15.2
USERNAME=admin
PASSWORD=123
```

Substitua pelos dados reais do seu MikroTik.

### 4️⃣ Fazer Force Rebuild

Clique em **Force Rebuild** para aplicar todas as mudanças.

### 5️⃣ Verificar Status

- Aguarde até que o status mude para **🟢 Running**
- Verifique os logs para mensagens de sucesso

---

## ✅ Sinais de Sucesso

Procure por estas mensagens nos logs:

```
✅ TODAS AS VALIDAÇÕES PASSARAM
🚀 INICIANDO COM GUNICORN
📡 Servidor ouvindo em 0.0.0.0:8000
```

---

## 🧪 Testar o Endpoint de Health

Após o deploy, teste:

```bash
curl https://seu-url/health
```

Resposta esperada:
```json
{"status": "ok", "message": "Dashboard is running"}
```

---

## 🐛 Debugar Localmente

### Testar com Docker Compose

```bash
# Build e run
docker-compose up --build

# Testar
curl http://localhost:8000/health

# Ver logs
docker-compose logs -f dashboard

# Parar
docker-compose down
```

### Testar sem Docker

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar
python wsgi.py

# Testar em outro terminal
curl http://localhost:8000/health
```

---

## 📋 Checklist Final

- [ ] Dockerfile está no repositório
- [ ] wsgi.py está no repositório
- [ ] requirements.txt tem gunicorn
- [ ] config.py suporta variáveis de ambiente
- [ ] Orbitan Network tem porta 8000
- [ ] Orbitan Build fields estão VAZIOS
- [ ] Force Rebuild foi executado
- [ ] Status está 🟢 Running
- [ ] `/health` retorna JSON
- [ ] Dashboard abre sem erros

---

## 🚀 Se Tudo Estiver OK

O dashboard deve abrir normalmente em:
```
https://seu-url-orbitan/
```

Você verá a interface com:
- 📊 Gráficos de interfaces
- 🖥️ Hosts conectados
- 📈 Estatísticas de DHCP
- ⚡ Controles de velocidade

---

## 💡 Dicas Importantes

1. **MikroTik API**: Certifique-se que a porta 8728 está aberta no MikroTik
2. **Credenciais**: Use variáveis de ambiente, não hardcode no código
3. **Timeout**: Operações no MikroTik podem ser lentas (120s timeout configurado)
4. **Logs**: Sempre verifique os logs do Orbitan para diagnosticar problemas

---

## 📞 Ainda com problemas?

1. Verifique os logs completos no Orbitan
2. Teste localmente com `docker-compose up`
3. Confirme que o MikroTik está acessível da rede
4. Valide as credenciais do MikroTik
