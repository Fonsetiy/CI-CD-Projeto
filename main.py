from fastapi import FastAPI
from datetime import datetime
import socket

app = FastAPI(
    title="🚀 Projeto CI/CD - Compass UOL",
    description="Aplicação FastAPI utilizada para demonstrar pipeline automatizado de Integração e Entrega Contínua (CI/CD) com Docker, Kubernetes e ArgoCD.",
    version="2.0.0"
)

@app.get("/")
def root():
    """Endpoint principal que retorna informações do ambiente e horário atual."""
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    hostname = socket.gethostname()
    return {
        "empresa": "🏢 Compass UOL",
        "mensagem": "✅ Deploy automatizado funcionando perfeitamente!",
        "horário_atual": current_time,
        "servidor": hostname,
        "versão": "2.0.0",
        "tecnologias": ["FastAPI", "Docker", "Kubernetes", "ArgoCD", "GitHub Actions"]
    }

@app.get("/healthz")
def health():
    """Endpoint usado pelo Kubernetes para verificar se o serviço está saudável."""
    return {"status": "ok"}

@app.get("/info")
def info():
    """Endpoint adicional com informações sobre o projeto."""
    return {
        "projeto": "Pipeline CI/CD Compass UOL",
        "autora": "Julya 🐧",
        "linguagem": "Python 3.11 + FastAPI",
        "finalidade": "Demonstração de automação de build, push e deploy contínuo."
    }


