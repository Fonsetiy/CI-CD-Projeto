# CI/CD com o Github Actions

A adoção de CI/CD (Integração Contínua e Entrega Contínua) tornou-se essencial para empresas que buscam entregar software com velocidade e confiabilidade. Ferramentas como GitHub Actions e ArgoCD são fundamentais nesse contexto: o primeiro automatiza pipelines de build, teste e publicação de containers, enquanto o segundo implementa GitOps para gerenciar deploys em Kubernetes de forma declarativa.

Dominar essas tecnologias é crucial para profissionais de DevOps e desenvolvimento moderno, sendo este projeto uma demonstração prática dessa integração.

## Objetivo
Este projeto tem como objetivo automatizar o ciclo completo de desenvolvimento, build, deploy e execução de uma aplicação FastAPI, implementando um pipeline de CI/CD utilizando GitHub Actions, com Docker Hub como registro de imagens, e ArgoCD para entrega contínua em um cluster Kubernetes local gerenciado pelo Rancher Desktop.

## Pré-requisitos
• Conta no GitHub (repo público) 

• Conta no Docker Hub com token de acesso 

• Rancher Desktop com Kubernetes habilitado 

• kubectl configurado corretamente (kubectl get nodes)

• ArgoCD instalado no cluster local

• Git instalado

• Python 3 e Docker instalados

## Tecnologias Utilizadas
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/)
[![Python 3](https://img.shields.io/badge/Python_3-00ABD1?style=for-the-badge&logo=python&logoColor=white)](https://docs.python.org/3/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)](https://kubernetes.io/docs/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://docs.github.com/)
[![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)](https://git-scm.com/doc)
[![Rancher Desktop](https://img.shields.io/badge/Rancher_Desktop-0075A8?style=for-the-badge&logo=rancher&logoColor=white)](https://docs.rancherdesktop.io/)
[![Argo CD](https://img.shields.io/badge/ArgoCD-EF7B4D?style=for-the-badge&logo=argo&logoColor=white)](https://argo-cd.readthedocs.io/)
[![Docker Hub](https://img.shields.io/badge/Docker_Hub-140664?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/)
[![Visual Studio Code](https://img.shields.io/badge/Visual_Studio_Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)](https://code.visualstudio.com/docs)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-6E7474?style=for-the-badge&logo=githubactions&logoColor=white)](https://docs.github.com/en/actions)

## Etapa 1 - Estruturação do Projeto, Aplicação FastAPI e Dockerfile
Criaremos os respositórios do projeto, uma aplicação FastAPI simples e a containerizaremos com Docker, preparando a base do projeto.

#### Etapa 1.1 🠒 Criação dos repositórios no GitHub
Seguindo a arquitetura GitOps, o projeto será organizado em dois repositórios independentes com propósitos específicos:

- ```hello-app```: Destinado ao desenvolvimento da aplicação, contendo todo o código-fonte, arquivos de configuração Docker e os workflows de CI/CD que automatizam o processo de build e publicação.

- ```hello-manifests```: Focado na infraestrutura, armazena exclusivamente os arquivos de configuração Kubernetes (Deployment, Service) que definem o estado desejado do cluster, servindo como fonte da verdade para o ArgoCD.

Essa separação proporciona maior segurança e controle, isolando as mudanças de código das alterações de infraestrutura.

[****Linkar repositório]

#### Etapa 1.2 - Criação da aplicação FastAPI
Foi criado o arquivo ```main.py``` com o código:

``` python 
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
 return {"message": "Hello World"}
``` 
### Teste de COmmit