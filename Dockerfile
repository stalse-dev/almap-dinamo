
FROM python:3.10

# Dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Diretório de trabalho
WORKDIR /backend

# Copia os arquivos
COPY . .

# Variável de ambiente para ignorar secrets no build
ENV IS_BUILD=true

# Instala dependências do Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Coleta os arquivos estáticos (ignora falha durante build)
# Esta linha garante que os arquivos estáticos sejam coletados em STATIC_ROOT
RUN python manage.py collectstatic --noinput --clear || echo "Collectstatic falhou durante o build, mas continuando..."

# Expõe a porta padrão do Cloud Run
EXPOSE 8080

# CMD ajustado para apenas iniciar o Gunicorn, pois o collectstatic já rodou no build.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "datahub_base.wsgi:application"]