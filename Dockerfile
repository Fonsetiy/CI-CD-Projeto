FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /hello-app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do projeto para dentro do container
COPY . .

# Expõe a porta 80 (para o tráfego HTTP)
EXPOSE 80

# Comando para rodar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

