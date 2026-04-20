# TROUBLESHOOTING - Dashboard MikroTik

## Erro: ERR_CONNECTION_REFUSED

### 1. Verificar Status do Container
```bash
docker ps
docker logs [container_id]
```

### 2. Testar Endpoint de Health
Se o container está rodando, teste:
```bash
curl http://seu-url/health
```

Esperado:
```json
{"status": "ok", "message": "Dashboard is running"}
```

### 3. Se o Container está em Restart Loop

**No Coolify:**
- Configuration → Build
  - Install Command: **DEIXE VAZIO**
  - Build Command: **DEIXE VAZIO**
  - Start Command: **DEIXE VAZIO**
- Clique em **Force Rebuild**

### 4. Verificar Logs
Na aba **Logs** do Coolify, procure por:

❌ **Erros:**
- `/bin/bash: -c: option requires an argument`
- `ModuleNotFoundError`
- `ConnectionRefusedError`

✅ **Sucesso:**
- `✅ Configurações OK - INICIANDO APLICAÇÃO`
- `🚀 DASHBOARD ONLINE em http://0.0.0.0:8000`

### 5. Debugar Localmente
```bash
# No seu PC
python start.py

# Ou com Docker
docker build -t dashboard .
docker run -p 8000:8000 dashboard

# Testar
curl http://localhost:8000/health
```

## Configurações Críticas

### app.py
```python
# ✅ CORRETO
app.run(host='0.0.0.0', port=8000)

# ❌ ERRADO
app.run()  # Só aceita localhost
```

### Dockerfile
```dockerfile
# ✅ CORRETO
EXPOSE 8000
CMD ["python", "start.py"]

# ❌ ERRADO
CMD python app.py  # Precisa de /bin/bash
RUN python app.py  # Executa na build, não no run
```

### requirements.txt
Certifique-se que tem:
```
flask
routeros-api
requests
speedtest-cli
```

## Porta Exposta

**Coolify:** Configuration → Network
- Ports Exposed: **8000**

## Checklist Final

- [ ] Dockerfile salvo no GitHub
- [ ] start.py salvo no GitHub
- [ ] requirements.txt tem todas as dependências
- [ ] app.py tem `host='0.0.0.0'`
- [ ] Coolify Build fields estão VAZIOS
- [ ] Coolify Network has port 8000
- [ ] Force Rebuild executado
- [ ] Status está VERDE (Running)
- [ ] `/health` retorna JSON

Se tudo OK, você verá o Dashboard funcionando! 🚀
