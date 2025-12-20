FROM python:3.12-slim-bookworm

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia o requirements da pasta .docker/bin/config para o WORKDIR (/app)
COPY .docker/bin/config/requirements.txt ./requirements.txt

# Instala as dependências do projeto
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copia o restante dos arquivos do projeto
COPY . .

# Expõe a porta padrão do FastAPI
EXPOSE 8080

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]