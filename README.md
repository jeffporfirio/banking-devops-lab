# Banking DevOps Lab

A hands-on DevOps/SRE laboratory simulating an enterprise banking application delivery environment.

This project demonstrates an end-to-end application delivery workflow using CI/CD automation, Docker, Kubernetes, GitOps, artifact management, secrets management, application health checks, and operational logging.

The laboratory is developed incrementally, focusing on practical DevOps/SRE engineering skills and enterprise-oriented practices.

## Project Repositories

- **GitHub:** [banking-devops-lab](https://github.com/jeffporfirio/banking-devops-lab)
- **GitLab:** [banking-devops-lab](https://gitlab.com/jeffporfirio/banking-devops-lab) — CI/CD pipelines and automation.

## Project Status

**Implemented**

- Python Flask REST API
- MongoDB integration with authentication
- Docker containerization and Docker Compose
- Automated application tests with pytest
- GitLab CI/CD pipeline
- Self-hosted GitLab Runner using Shell executor
- Docker image build and publishing
- JFrog Artifactory integration
- HashiCorp Vault integration
- GitLab OIDC/JWT authentication with Vault
- Automated Docker Compose deployment
- Kubernetes deployment using Kind
- Kubernetes Services, StatefulSets and PersistentVolumeClaims
- Kubernetes Liveness and Readiness Probes
- ArgoCD GitOps synchronization
- Application logging with configurable log levels
- MongoDB failure and application recovery testing

**Planned / Future Improvements**

- Prometheus and Grafana
- Centralized log aggregation
- Application and infrastructure metrics
- Alerting and SLO definition
- Troubleshooting scenarios and Root Cause Analysis
- Terraform and cloud infrastructure
- Dependency and security scanning
- SonarQube integration
- Production-grade application server using Gunicorn

---

## Architecture

The laboratory currently demonstrates two complementary application delivery workflows.

### 1. CI/CD — GitLab, JFrog and Vault

```text
                 Developer
                     |
                     | Git Push
                     v
              GitLab Repository
                     |
                     v
             GitLab CI/CD Pipeline
                     |
             +-------+-------+
             |       |       |
             v       v       v
           Pytest  Docker   Vault OIDC
                   Build    Authentication
                     |       |
                     v       v
                   JFrog  MongoDB
                Artifactory Credentials
                     |
                     v
                Docker Image
                     |
                     v
              Docker Compose
                Deployment
                     |
              +------+------+
              |             |
              v             v
           Flask API     MongoDB
              |
              v
          Health Check
```

The GitLab CI/CD pipeline automates testing, image building, publishing, secrets retrieval and Docker Compose deployment.

### 2. Kubernetes — Kind and ArgoCD GitOps

```text
             Git Repository
                    |
                    v
                 ArgoCD
                    |
              GitOps Sync
                    |
                    v
              Kind Cluster
                    |
              Banking Namespace
                    |
           +--------+--------+
           |                 |
           v                 v
      Flask API          MongoDB
      Deployment         StatefulSet
       2 Replicas          1 Replica
           |                 |
           v                 v
       Kubernetes        Persistent
        Service           Volume
           |
           v
      Health Probes
```

The Kubernetes environment is managed separately through ArgoCD.

The application image is loaded into the local Kind cluster using `kind load docker-image`. Kubernetes deployment is not currently an automated stage of the GitLab CI/CD pipeline.

---

## Application Architecture

The application consists of two main components:

- **Flask API:** exposes REST endpoints for health checks and banking transactions.
- **MongoDB:** stores transaction data and requires authentication.

The API connects to MongoDB using PyMongo.

### Health Checks

The application exposes separate health endpoints:

| Endpoint | Purpose |
|---|---|
| `/health` | General application health |
| `/health/live` | Liveness check |
| `/health/ready` | Readiness check, including MongoDB connectivity |

The readiness endpoint checks MongoDB availability and returns HTTP 503 when the database is unavailable.

Kubernetes uses Liveness and Readiness Probes to monitor the application.

### Application Logging

Application logging is centrally configured through `app/logging_config.py`.

The logging level can be controlled using the `LOG_LEVEL` environment variable.

Supported levels include:

- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

Logs are written to standard output (`stdout`), allowing Docker and Kubernetes logging mechanisms to collect them.

The configuration also applies the selected logging level to the Werkzeug logger.

---

## Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python 3.12 |
| API Framework | Flask |
| Database | MongoDB 7 |
| Database Driver | PyMongo |
| Testing | pytest |
| Containerization | Docker |
| Container Orchestration | Docker Compose |
| Kubernetes | Kubernetes / Kind |
| GitOps | ArgoCD |
| CI/CD | GitLab CI/CD |
| CI/CD Runner | GitLab Runner |
| Artifact Management | JFrog Artifactory |
| Secrets Management | HashiCorp Vault |
| Authentication | GitLab OIDC / JWT |
| Version Control | Git |
| Operating System | Linux / Ubuntu |

---

## CI/CD Pipeline

The GitLab pipeline automates the application delivery lifecycle.

### Pipeline Jobs

| Job | Description |
|---|---|
| `test` | Executes automated Python tests |
| `vault-read-test` | Validates GitLab OIDC authentication and Vault secret retrieval |
| `docker-build` | Builds the application Docker image |
| `docker-publish` | Publishes the image to JFrog Artifactory |
| `deploy` | Deploys the application using Docker Compose |

### Docker Image Management

Docker images are tagged using the GitLab commit SHA.

Example:

```text
host.docker.internal:8082/docker-local/banking-api:<commit-sha>
```

The pipeline also publishes a `latest` tag.

### Automated Deployment

The deployment job:

1. Authenticates with HashiCorp Vault using a GitLab-issued OIDC token.
2. Retrieves MongoDB credentials.
3. Authenticates with JFrog Artifactory.
4. Pulls the Docker image corresponding to the current commit.
5. Updates the Flask API using Docker Compose.
6. Verifies the application health endpoint.
7. Removes temporary Docker authentication configuration.
8. Revokes the temporary Vault token.

The API is updated using:

```bash
docker compose up -d --no-deps api
```

This avoids an intentional restart of the MongoDB service.

---

## Kubernetes and GitOps

The project includes a local Kubernetes environment running on Kind.

### Kubernetes Resources

The following resources are implemented:

- Namespace
- API Deployment
- API Service
- MongoDB StatefulSet
- MongoDB Service
- PersistentVolumeClaim
- Kustomize configuration

The API Deployment runs two replicas.

MongoDB runs as a StatefulSet with persistent storage.

### ArgoCD

ArgoCD manages the Kubernetes application through GitOps synchronization.

The application is configured to monitor the Kubernetes manifests stored in the repository.

The observed application state is:

- Sync Status: Synced
- Health Status: Healthy

### Resilience Testing

A MongoDB failure scenario was tested by scaling the MongoDB StatefulSet to zero replicas.

Observed behavior:

1. MongoDB became unavailable.
2. API Pods remained running but became Not Ready.
3. The liveness endpoint continued returning HTTP 200.
4. The readiness endpoint returned HTTP 503.
5. The API Service had no ready endpoints.
6. MongoDB was restored to one replica.
7. API Pods recovered their readiness automatically.
8. The PVC remained bound.
9. ArgoCD returned to Synced / Healthy.

This scenario demonstrates the difference between application liveness and readiness, as well as Kubernetes service endpoint management and recovery behavior.

**Current limitation:** Kubernetes deployment is managed separately through ArgoCD. The GitLab pipeline currently deploys through Docker Compose, not directly to Kubernetes.

---

## Security and Secrets Management

### HashiCorp Vault

Vault stores sensitive application configuration, including MongoDB credentials.

The GitLab pipeline authenticates using JWT/OIDC rather than storing a Vault token as a GitLab CI/CD variable.

The Vault policy follows the principle of least privilege, granting read access to the application secret.

### MongoDB Authentication

MongoDB runs with authentication enabled.

The application retrieves its credentials through environment variables:

```text
MONGO_USERNAME
MONGO_PASSWORD
MONGO_AUTH_SOURCE
```

Credentials are not stored in the Git repository.

**Lab limitation:** Vault currently runs in development mode. This configuration is intended for learning and testing, not production use.

---

## API Endpoints

### Health Check

```http
GET /health
```

```bash
curl http://localhost:5000/health
```

Example response:

```json
{
  "service": "banking_api",
  "status": "ok"
}
```

### Liveness

```http
GET /health/live
```

Checks whether the application process is responding.

### Readiness

```http
GET /health/ready
```

Checks application readiness, including MongoDB connectivity.

Returns HTTP 200 when ready and HTTP 503 when MongoDB is unavailable.

### List Transactions

```http
GET /transactions
```

```bash
curl http://localhost:5000/transactions
```

### Create Transaction

```http
POST /transactions
```

```bash
curl -X POST http://localhost:5000/transactions \
  -H "Content-Type: application/json" \
  -d '{"reference":"TX003","amount":100.00}'
```

Example response:

```json
{
  "message": "Transaction created"
}
```

---

## Deployment and Verification

### Docker Compose

Verify running containers:

```bash
docker compose ps
```

Verify API health:

```bash
curl -i http://localhost:5000/health
```

### Docker Logging

Run the application with a configurable log level:

```bash
docker run -d \
  --name banking-api \
  -p 5000:5000 \
  -e LOG_LEVEL=INFO \
  banking-api:logging
```

Inspect application logs:

```bash
docker logs banking-api
```

### Kubernetes

Verify application resources:

```bash
kubectl get pods -n banking
kubectl get services -n banking
kubectl get pvc -n banking
```

Verify ArgoCD synchronization:

```bash
kubectl get applications -n argocd
```

---

## Testing

The project uses pytest for automated application testing.

Current automated tests cover:

- Health endpoint
- Transaction listing
- Transaction creation
- Missing transaction reference
- Missing transaction amount
- Negative transaction amounts
- Liveness endpoint
- Readiness success
- Readiness failure

Run the tests locally:

```bash
.venv/bin/python -m pytest -v
```

Latest validation: **9 tests passed**.

Python syntax validation:

```bash
python -m py_compile \
  app/__init__.py \
  app/database.py \
  app/logging_config.py \
  app/routes.py
```

---

## Project Structure

```text
banking-devops-lab/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── logging_config.py
│   └── routes.py
│
├── tests/
│   └── test_api.py
│
├── k8s/
│   ├── api-deployment.yaml
│   ├── api-service.yaml
│   ├── kustomization.yaml
│   ├── mongodb-pvc.yaml
│   ├── mongodb-service.yaml
│   ├── mongodb-statefulset.yaml
│   └── namespace.yaml
│
├── .gitlab-ci.yml
├── .gitignore
├── .dockerignore
├── Dockerfile
├── compose.yaml
├── kind-config.yaml
├── requirements.txt
├── vault-gitlab-policy.hcl
├── vault-gitlab-role.json
└── README.md
```

---

## Development Roadmap

### 1. Application Development
- [x] Flask REST API
- [x] MongoDB integration
- [x] Docker
- [x] Docker Compose

### 2. Testing and Version Control
- [x] pytest
- [x] Automated API tests
- [x] Git repository

### 3. CI/CD
- [x] GitLab repository
- [x] GitLab Runner
- [x] Automated pipeline
- [x] Automated test execution
- [x] Docker image build
- [x] Docker image publishing
- [x] Automated Docker Compose deployment

### 4. Artifact and Security Management
- [x] JFrog Artifactory
- [x] HashiCorp Vault
- [x] GitLab OIDC authentication
- [x] Secret retrieval
- [x] MongoDB authentication
- [ ] Dependency and security scanning
- [ ] SonarQube integration

### 5. Kubernetes
- [x] Kind cluster
- [x] Namespace
- [x] Deployment
- [x] Service
- [x] StatefulSet
- [x] PersistentVolumeClaim
- [x] Liveness and Readiness Probes
- [ ] ConfigMap
- [ ] Kubernetes Secret management improvements
- [ ] Ingress

### 6. GitOps
- [x] ArgoCD
- [x] GitOps synchronization
- [x] Application health monitoring
- [ ] Automated CI/CD integration with Kubernetes
- [ ] Rollback strategies

### 7. Observability and SRE
- [x] Application logging
- [x] Configurable log levels
- [x] Docker log collection
- [x] Application health checks
- [x] MongoDB failure and recovery testing
- [ ] Centralized logging
- [ ] Prometheus
- [ ] Grafana
- [ ] Metrics and monitoring
- [ ] Alerting
- [ ] SLO definition
- [ ] Troubleshooting scenarios and Root Cause Analysis

### 8. Cloud and Infrastructure as Code
- [ ] Terraform
- [ ] Cloud infrastructure
- [ ] Remote state
- [ ] Infrastructure CI/CD

---

## Project Objectives

The main objective is to build practical DevOps/SRE experience through the incremental implementation of an application delivery platform.

Key areas of focus:

- CI/CD automation
- Containerization
- Artifact management
- Secrets management
- Authentication and access control
- Kubernetes orchestration
- GitOps
- Application health and resilience
- Logging and observability
- Incident troubleshooting and Root Cause Analysis
- Infrastructure as Code

This project simulates selected components of an enterprise application delivery workflow. It is a learning laboratory and is not intended to represent a production banking platform.