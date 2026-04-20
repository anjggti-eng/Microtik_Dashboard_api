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

# Usar gunicorn para produção, ouvindo em todas as interfaces na porta 8000
# O script start.py pode ser usado para validação pré-vôo se necessário, 
# mas para o servidor HTTP o gunicorn é mais robusto.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "--threads", "2", "app:app"]
