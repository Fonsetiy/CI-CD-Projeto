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
[![Docker Hub](https://img.shields.io/badge/Docker_Hub-140664?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/)
[![Python 3](https://img.shields.io/badge/Python_3-00ABD1?style=for-the-badge&logo=python&logoColor=white)](https://docs.python.org/3/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://docs.github.com/)
[![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)](https://git-scm.com/doc)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-6E7474?style=for-the-badge&logo=githubactions&logoColor=white)](https://docs.github.com/en/actions)
[![Argo CD](https://img.shields.io/badge/ArgoCD-EF7B4D?style=for-the-badge&logo=argo&logoColor=white)](https://argo-cd.readthedocs.io/)
[![Visual Studio Code](https://img.shields.io/badge/Visual_Studio_Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)](https://code.visualstudio.com/docs)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)](https://kubernetes.io/docs/)
[![Minikube](https://img.shields.io/badge/Minikube-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)](https://minikube.sigs.k8s.io/docs/)

## 🔷 Etapa 1 - Estruturação do Projeto, Aplicação FastAPI e Dockerfile
Criaremos os respositórios do projeto, uma aplicação FastAPI simples e a containerizaremos com Docker, preparando a base do projeto.

#### 🔹 Etapa 1.1 🠒 Criação dos repositórios no GitHub
Seguindo a arquitetura GitOps, o projeto será organizado em dois repositórios independentes com propósitos específicos:

- ```hello-app```: Destinado ao desenvolvimento da aplicação, contendo todo o código-fonte, arquivos de configuração Docker e os workflows de CI/CD que automatizam o processo de build e publicação.

- ```hello-manifests```: Focado na infraestrutura, armazena exclusivamente os arquivos de configuração Kubernetes (Deployment, Service) que definem o estado desejado do cluster, servindo como fonte da verdade para o ArgoCD.

Essa separação proporciona maior segurança e controle, isolando as mudanças de código das alterações de infraestrutura.

[Repositório do Projeto - Manifests](https://github.com/Fonsetiy/hello-manifests)

#### 🔹 Etapa 1.2 - Criação da aplicação FastAPI
Foi criado o arquivo ```main.py``` com o código:

``` python 
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
 return {"message": "Hello World"}
 ```

#### 🔹 Etapa 1.3 - Criação do Dockerfile
Para empacotar e executar a aplicação do FastAPI em um container.

``` dockerfile 
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

```

## 🔷 Etapa 2 - Configurar GitHub Actions CI/CD
Nesta etapa, foi configurado o pipeline de Integração e Entrega Contínua (CI/CD) com o GitHub Actions, com o propósito de automatizar todo o fluxo de entrega da aplicação.

- Construir e enviar automaticamente a imagem Docker da aplicação FastAPI para o Docker Hub;

- Atualizar o arquivo deployment.yaml no repositório de manifests (utilizado pelo Kubernetes);

- Gerar um Pull Request automático nesse repositório, permitindo que o ArgoCD detecte a nova versão e realize o deploy contínuo no cluster Kubernetes.

#### 🔹 Estapa 2.1 - Arquitetura do Workflow
O fluxo de automação foi implementado no diretório .github/workflows/ci-cd.yml, funcionando como o centro do processo de entrega contínua.

Funcionamento do Pipeline:
- Ativação Automática: Executado em todo push para o repositório principal
- Autenticação Segura: Login no Docker Hub utilizando variáveis secretas
- Versionamento Inteligente: Geração de imagens com tags única (commit SHA) e flutuante (latest)
- Sincronização Automatizada: Clone e atualização do repositório de infraestrutura
- Governança Controlada: Criação de Pull Requests para revisão das alterações de deployment

#### 🔹 Etapa 2.2 - Arquivo Yaml do CI-CD
``` yaml
name: CI/CD - Build & Update Manifests

on:
  push:
    branches: [ "main" ]

jobs:
  build-and-push:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout source
        uses: actions/checkout@v4

      - name: Setup QEMU
        uses: docker/setup-qemu-action@v3

      - name: Setup Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ secrets.DOCKER_USERNAME }}/hello-app:${{ github.sha }}

      # ✅ CONFIGURAÇÃO SSH
      - name: Setup SSH
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/id_ed25519
          chmod 600 ~/.ssh/id_ed25519
          ssh-keyscan github.com >> ~/.ssh/known_hosts

      - name: Configure Git
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "actions@github.com"

      - name: Update manifests repo (SSH)
        run: |
          git clone git@github.com:Fonsetiy/hello-manifests.git hello-manifests
          cd hello-manifests
          sed -i "s| ${{secrets.DOCKER_USERNAME}}/hello-app:.*| ${{secrets.DOCKER_USERNAME}}/hello-app:${{ github.sha }}|g" deployment.yaml
          git add .
          git commit -m "ci: update image to ${{ github.sha }}"
          git push origin main
      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v6
        with:
          token: ${{ secrets.token}}
          commit-message: "ci: update image to ${{ github.sha }}"
          title: "Atualizar imagem para ${{ github.sha }}"
          body: "Atualização automática da imagem para ${{ github.sha }}"
          branch: "update-image-${{ github.sha }}"
          base: "main"
```

#### 🔹 Etapa 2.3 - Secrets no GitHub
Para garantir que o pipeline CI/CD possa executar ações automatizadas com segurança e autenticação, foram configurados segredos no repositório hello-app, acessíveis em:

Settings → Secrets and variables → Actions → Repository secrets

Esses segredos são variáveis protegidas utilizadas pelo GitHub Actions durante o processo de build, push e atualização dos manifests. Eles substituem o uso de credenciais expostas no código, evitando vazamento de informações sensíveis (como senhas e chaves privadas).

| Nome                 | Valor                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------- |
| `DOCKER_USERNAME`    | Nome de usuário do Docker Hub                                                         |
| `DOCKER_PASSWORD`    | Senha ou *Access Token* do Docker Hub                                                 |
| `SSH_PRIVATE_KEY`    | Chave privada usada para autenticação via SSH no repositório `hello-manifests`        |
| `TOKEN` *(ou `PAT`)* | Personal Access Token (Classic) com permissão de escrita no repositório dos manifests |


Print de referência:

<img width="1265" height="639" alt="Captura de tela de 2025-11-07 16-42-11" src="https://github.com/user-attachments/assets/7b2de911-2a17-4f85-b08b-f37d3b5c56fc" />

#### 🔶 Como gerar o Token:
Para permitir que o GitHub Actions interaja automaticamente com o repositório de manifests, é necessário configurar um Personal Access Token (Classic).

Procedimento para criação do PAT:
1. Acesso: Navegue até https://github.com/settings/tokens
2. Inicialização: Clique em "Generate new token (classic)"
3. Configuração:
 - Nome descritivo: ci-cd-github-actions
 - Validade: Defina expiração ou "No expiration"
 - Permissões: Marque exclusivamente a opção repo
4. Geração: Clique em "Generate token" e copie imediatamente o código
5. Armazenamento Seguro: Adicione o token como segredo no repositório da aplicação com o nome PAT
Este token concederá permissão para o workflow realizar commits e abrir Pull Requests automaticamente no repositório de manifests.

#### Etapa 2.4 - Publicação de Imagens no Docker Hub
O workflow demonstrou eficiência ao construir e publicar automaticamente a imagem hello-app no Docker Hub, utilizando um sistema de versionamento duplo que inclui tanto a tag latest quanto o identificador único do commit (${{ github.sha }}).

<img width="1292" height="639" alt="Captura de tela de 2025-11-07 17-12-40" src="https://github.com/user-attachments/assets/1465b678-93a5-47e9-b383-c507dcc857e4" />

#### Etapa 2.5 - Sincronização Automatizada de Manifestos
O pipeline executou com sucesso a atualização do arquivo de deployment, criando automaticamente um Pull Request no repositório hello-manifests com a nova tag da imagem.

<img width="1298" height="360" alt="Captura de tela de 2025-11-07 17-15-09" src="https://github.com/user-attachments/assets/bf4486c3-ec54-4e3a-9f2e-65fda9eccc52" />


## Etapa 3 - Criação dos Manifests
Nesta fase, foram desenvolvidos os arquivos de configuração do Kubernetes que definem o estado desejado da aplicação no cluster. Esses manifestos servem como fonte da verdade para o ArgoCD, seguindo a metodologia GitOps.

O repositório de infraestrutura mantém uma sincronização automática com o pipeline de CI/CD, recebendo atualizações sempre que uma nova versão da imagem Docker é gerada. O ArgoCD monitora continuamente este repositório, garantindo que o estado real do cluster corresponda exatamente às definições versionadas no Git.

#### Etapa 3.1 - Reposotório dos manifests
Os arquivos desta etapa podem ser encontrados no repositório: [hello-manifests](https://github.com/Fonsetiy/hello-manifests)

🔸 Arquivo Deployment:
``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hello-app
  template:
    metadata:
      labels:
        app: hello-app
    spec:
      containers:
        - name: hello-app
          image: julyalf/hello-app:30f027446074f7ef17e02c87c70d3fa016bea6c6
          ports:
            - containerPort: 80
          readinessProbe:
            httpGet:
              path: /healthz
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 10
```
Especifica a configuração de implantação do container, definindo réplicas, estratégia de atualização e políticas de reinício para garantir a disponibilidade da aplicação.

🔸 Arquivo Service:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: hello-service
spec:
  selector:
    app: hello-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: ClusterIP
```
Define qual o serviço responsável por expor a aplicação dentro do cluster Kubernetes.
Com esses arquivos configurados corretamente, o ArgoCD poderá sincronizar automaticamente os deploys conforme as atualizações de imagem feitas via GitHub Actions.

## Etapa 4 - Criação e Integração do App no ArgoCD
Nesta fase, foi estabelecida a conexão entre o ArgoCD e o repositório de manifestos, criando uma aplicação que atua como ponte de sincronização contínua.

A aplicação configurada no ArgoCD monitora permanentemente o repositório Git de infraestrutura, detectando automaticamente qualquer modificação nos arquivos Kubernetes e replicando essas alterações no cluster local, mantendo o ambiente sempre alinhado com o estado desejado definido no versionamento.

#### Etapa 4.1 - Acesso ao painel do ArgoCD (via port-forward)
Para acessar o painel web do ArgoCD, utilize o comando:
``` bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Acesse o painel através do navegador pelo endereço:
```
https://localhost:808
```

#### Etapa 4.2 -  Obter a senha de acesso
User padrão: `admin`
Senha: utilize o comando abaixo para obter a senha gerada automaticamente:
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```
#### Etapa 4.3 - Criação do App no ArgoCD
Após o acesso no painel do ArgoCD, clique em "Applications" no menu lateral, e em seguida clique no botão "+ New App".
Preencha os campos da aplicação da seguinte forma:

- Application Name: hello-app

- Project: default

- Habilitar:

  ▪︎ Sync Policy → Automatic
  
  ▪︎ Prune Resources
  
  ▪︎ Self Heal
  
  ▪︎ Set Deletion Finalizer
  
  ▪︎ Auto-Create Namespace
  
  
<img width="1300" height="653" alt="Captura de tela de 2025-11-07 11-25-05" src="https://github.com/user-attachments/assets/650bf4b3-9487-445f-b9e3-207776311d90" />


Na seção inferior da interface, configure os parâmetros de conexão com o repositório:

- Repository URL: https://github.com/Fonsetiy/hello-manifests

- Revision: main

- Path: . (indica que os manifests estão no diretório raiz)

- Cluster Name: in-cluster

- Namespace: hello-app


Finalize clicando em Create para registrar a aplicação.

<img width="1303" height="653" alt="Captura de tela de 2025-11-07 11-27-34" src="https://github.com/user-attachments/assets/3af0c062-4bc1-4141-9784-ee625393a2c5" />

#### Etapa 4.4 - Status de Sincronização da Aplicação
Após a criação, o ArgoCD inicia automaticamente o processo de sincronização. Aguarde alguns instantes para verificação do status.

Indicadores de sucesso:

- Healthy - Todos os recursos (Pods, Services) operando normalmente

- Synced - Manifestos aplicados com sucesso no cluster

<img width="1071" height="640" alt="Captura de tela de 2025-11-07 14-09-37" src="https://github.com/user-attachments/assets/8c51b3a0-c22d-49d9-8c4a-2f52c2f11f65" />

<img width="1302" height="648" alt="Captura de tela de 2025-11-07 18-06-08" src="https://github.com/user-attachments/assets/720d90b2-9dcc-47b0-946e-f90758513310" />

---------

## Etapa 5 - Acessando e testando a aplicação localmente
Para acessar a aplicação via port-forward, execute o seguinte comando no terminal para criar um túnel de redirecionamento de portas:
```bash
kubectl port-forward svc/hello-app-service 8081:80 -n hello-app
```

Explicação do comando:

`kubectl port-forward`: Estabelece o redirecionamento de porta

`svc/hello-app-service`: Referencia o serviço Kubernetes criado

`8081:8000`: Mapeia a porta 8000 do cluster para a porta 8081 local

`-n hello-app`: Especifica o namespace onde o serviço está implantado

Resultado esperado:
``` text
Forwarding from 127.0.0.1:8081 -> 8000
Forwarding from [::1]:8081 -> 8000
```
A aplicação estará acessível através do endereço: 
``` bash
http://localhost:8080`
```
Print da aplicação:

<img width="1157" height="138" alt="Captura de tela de 2025-11-07 18-19-20" src="https://github.com/user-attachments/assets/d58d0f2e-7c13-4e79-8265-73e97e46abb6" />



