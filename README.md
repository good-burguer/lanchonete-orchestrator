# Lanchonete Orchestrator

O **Lanchonete Orchestrator** é o serviço responsável por coordenar chamadas entre os microserviços do ecossistema *Good Burguer*.  
Ele atua como um gateway interno, realizando orquestrações, validações, chamadas assíncronas e integração com serviços externos.

Este repositório inclui:

- Código do microserviço FastAPI (orquestrador)
- Testes automatizados (pytest)
- Configuração de CI (Test + SonarCloud)
- Configuração de CD (Build Docker + Deploy automático em EKS)
- Manifests Kubernetes (Deployment + Service)
- Suporte completo ao fluxo GitHub → ECR → EKS

---

## 📦 Arquitetura do Microserviço

### **Tecnologias principais**

- **Python 3.12**
- **FastAPI** (framework principal)
- **Uvicorn** (servidor ASGI)
- **Pytest + Coverage** (testes automatizados)
- **SonarCloud** (qualidade de código)
- **Docker** (containerização)
- **AWS ECR** (registro de imagens)
- **AWS EKS** (cluster Kubernetes)
- **GitHub Actions** (CI/CD)
- **Probes Kubernetes** (health/readiness)
- **Envsubst** para injeção dinâmica da imagem no deploy

---

## 🗂 Estrutura de Pastas

```
lanchonete-orchestrator/
├── app/
│   ├── api/                 → Rotas do orquestrador
│   ├── services/            → Clientes HTTP, integrações
│   ├── adapters/            → DTOs e enums
│   ├── utils/               → Logs e ferramentas
│   ├── infrastructure/      → API server (FastAPI bootstrap)
│
├── tests/                   → Testes unitários
│
├── k8s/
│   ├── deployment.yaml      → Deployment + probes + imagem via envsubst
│   └── service.yaml         → Exposição ClusterIP
│
├── .docker/
│   └── bin/Dockerfile       → Dockerfile oficial do serviço
│
├── .github/workflows/
│   ├── ci-orchestrator.yml  → Testes + SonarCloud (PR)
│   └── cd-orchestrator.yml  → Build + Push ECR + Deploy EKS (main)
│
└── README.md
```

---

## 🔍 Fluxo de CI – Testes + SonarCloud

O CI roda **somente em Pull Requests** e garante que nada chega na `main` com erros.

Etapas:

1. Instala dependências
2. Executa `pytest` + coverage (configurado via `pyproject.toml` e gerando `coverage.xml` na raiz do repositório)
3. Envia resultados ao SonarCloud
4. Bloqueia merge se o pipeline falhar

Check obrigatório sugerido:  
✔ `Run Tests + SonarCloud`

---

## 🚀 Fluxo de CD – Build + Deploy Automático

O CD roda **somente na main**, após o merge aprovado.

Etapas:

1. OIDC assume a role `gb-dev-gha-lanchonete-orchestrator`
2. Build da imagem Docker
3. Push para o **Amazon ECR**
4. Geração automática do `IMAGE_URI`
5. Substituição via `envsubst` no `deployment.yaml`
6. Aplicação no EKS via `kubectl apply`
7. Aguardar rollout (`kubectl rollout status`)
8. (Em caso de falha) logs completos do pod + describe

> Nota: O CD **não gera coverage**, apenas consome os resultados já validados no CI.

---

## 🏥 Health Check e Probes

O serviço expõe um endpoint de saúde:

```
GET /health
→ 200 OK
```

O Kubernetes utiliza:

```
livenessProbe:
  httpGet:
    path: /health
    port: 8080

readinessProbe:
  httpGet:
    path: /health
    port: 8080
```

Isso garante que:

- O pod só entra no balanceamento quando estiver pronto
- Se travar, o Kubernetes reinicia automaticamente

---

## 🐳 Docker

O build é feito usando o arquivo:

```
.docker/bin/Dockerfile
```

Exemplo local:

```
docker build -t orchestrator .
docker run -p 8080:8080 orchestrator
```

---

## ☸ Deploy Manual (caso necessário)

Para testar o deploy localmente:

```
export IMAGE_URI="ECR_URI_AQUI"
envsubst < k8s/deployment.yaml | kubectl apply -n app -f -
kubectl apply -n app -f k8s/service.yaml
```

Ver pods:

```
kubectl get pods -n app -l app=lanchonete-orchestrator
```

Logs:

```
kubectl logs -n app -l app=lanchonete-orchestrator
```

---

## 🔐 IAM + OIDC (Acesso Seguro)

O GitHub Actions autentica na AWS sem chaves estáticas usando OIDC.

A role utilizada no deploy é:

```
arn:aws:iam::<ACCOUNT_ID>:role/gb-dev-gha-lanchonete-orchestrator
```

Com políticas mínimas para:

- ECR push
- Kubernetes apply (via IRSA da máquina)
- Descrição e atualização do cluster

---

## ✔ Como contribuir

Fluxo recomendado:

1. Criar branch feature/hotfix
2. Abrir PR para `main`
3. Aguardar CI
4. Passou? Revisão + merge
5. CD executa automaticamente

---

## 📞 Suporte / Dúvidas

Para dúvidas sobre:

- FastAPI → consulte o diretório `app/`
- Deploy → ver workflows em `.github/workflows`
- Infraestrutura → repositório `lanchonete-infra`

---

## 🎉 Status Atual

- CI + cobertura + SonarCloud → **100% funcional**
- CD automático para EKS → **ativo**
- Probes → **funcionando**
- Deploy saudável no cluster → **OK**
- Cobertura centralizada via `pyproject.toml` e compartilhada entre todos os serviços Good Burguer

Este microserviço está **totalmente pronto para produção** dentro da arquitetura Good Burguer.
---