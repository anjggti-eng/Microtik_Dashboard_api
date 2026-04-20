# Usa uma imagem oficial do Python estável
FROM python:3.10-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de requisitos e instala as bibliotecas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o resto do seu código
COPY . .

# Expõe a porta que o seu Flask/Dashboard usa
EXPOSE 8000

# Health check para verificar se o app está rodando
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Usar Gunicorn para produção - bind em 0.0.0.0:8000
# workers=1 pois MikroTik API não gosta de múltiplas conexões simultâneas
# threads=2 para melhor performance com I/O
# timeout=120 para operações longas no MikroTik
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "1", \
     "--threads", "2", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "wsgi:app"]
