# Usa uma imagem oficial do Python estável
FROM python:3.10-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema necessárias (opcional, mas recomendado)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de requisitos e instala as bibliotecas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o resto do seu código
COPY .

# Expõe a porta que o seu Flask/Dashboard usa
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["python", "app.py"]
