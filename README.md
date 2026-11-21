# Banking DevOps Lab

A hands-on DevOps/SRE laboratory simulating a banking application delivery environment.

This project demonstrates the implementation of a containerized REST API and an automated CI/CD workflow, integrating testing, artifact management, secrets management and application deployment.

The laboratory is developed incrementally, following practices commonly used in enterprise and banking environments.

## Project Status

**Implemented:**
- Flask REST API
- MongoDB integration with authentication
- Docker and Docker Compose
- Automated tests with pytest
- Git version control
- GitLab CI/CD
- GitLab Runner with Shell executor
- Docker image build and publishing
- JFrog Artifactory
- HashiCorp Vault integration
- GitLab OIDC authentication with Vault
- Automated deployment using Docker Compose
- API health verification after deployment

**Planned:**
- Kubernetes
- ArgoCD / GitOps
- Prometheus and Grafana
- Centralized logging
- Troubleshooting scenarios and Root Cause Analysis
- Terraform and cloud infrastructure

---

## Architecture

### Current Architecture

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
          +-------------+-------------+
          |             |             |
          v             v             v
       Pytest        Docker        Vault OIDC
       Tests         Build         Authentication
                        |             |
                        v             v
                  JFrog          MongoDB
                 Artifactory    Credentials
                        |
                        v
                 Docker Image
                        |
                        v
                 Automated Deploy
                        |
                        v
                 Docker Compose
                   |         |
                   v         v
                Flask API  MongoDB
                   |
                   v
               Health Check
```

### Application Architecture

The application consists of two Docker Compose services:

- **Flask API:** exposes REST endpoints on port 5000.
- **MongoDB:** stores banking transaction data and requires authentication.

The API connects to MongoDB using PyMongo.

### CI/CD Architecture

The CI/CD workflow is executed by a self-hosted GitLab Runner using the Shell executor.

The pipeline implements the following stages:

1. **Test:** creates a Python virtual environment, installs dependencies and executes pytest.
2. **Build:** builds the Docker image using the commit SHA as its tag.
3. **Publish:** authenticates with JFrog and publishes the Docker image.
4. **Deploy:** authenticates with Vault through GitLab OIDC, retrieves MongoDB credentials, pulls the image and updates the API service.

After deployment, the pipeline verifies the API health endpoint.

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
| CI/CD | GitLab CI/CD |
| CI/CD Runner | GitLab Runner |
| Artifact Management | JFrog Artifactory |
| Secrets Management | HashiCorp Vault |
| Authentication | GitLab OIDC / JWT |
| Version Control | Git |

---

## CI/CD Pipeline

The GitLab pipeline automates the application delivery lifecycle.

### Pipeline stages

| Job | Description |
|---|---|
| `test` | Executes automated Python tests |
| `vault-read-test` | Validates GitLab OIDC authentication and Vault secret retrieval |
| `docker-build` | Builds the application Docker image |
| `docker-publish` | Publishes the image to JFrog Artifactory |
| `deploy` | Deploys the new application version |

### Docker image management

Docker images are tagged using the GitLab commit SHA.

Example:

```text
host.docker.internal:8082/docker-local/banking-api:<commit-sha>
```

The pipeline also publishes a `latest` tag.

### Automated deployment

The deployment job:

1. Authenticates with HashiCorp Vault using a GitLab-issued OIDC token.
2. Retrieves the MongoDB username and password.
3. Authenticates with JFrog Artifactory.
4. Pulls the Docker image corresponding to the current commit.
5. Updates the Flask API using Docker Compose.
6. Verifies the application health endpoint.
7. Removes temporary Docker authentication configuration.
8. Revokes the temporary Vault token.

The API is updated using `docker compose up -d --no-deps api`, avoiding an intentional restart of the MongoDB service.

---

## Security and Secrets Management

### HashiCorp Vault

Vault is used to store sensitive application configuration, including MongoDB credentials.

The GitLab pipeline authenticates using JWT/OIDC rather than storing a Vault token as a GitLab CI/CD variable.

The Vault policy follows the principle of least privilege, allowing:
- Read access to the application secret.
- Revocation of the temporary Vault token.

### MongoDB Authentication

MongoDB runs with authentication enabled.

The application retrieves its credentials through environment variables:

```text
MONGO_USERNAME
MONGO_PASSWORD
MONGO_AUTH_SOURCE
```

Credentials are not stored in the Git repository.

**Lab limitation:** Vault currently runs in development mode for this laboratory. This configuration is intended for learning and testing, not production use.

---

## API Endpoints

### Health Check

```http
GET /health
```

Example:

```bash
curl http://localhost:5000/health
```

Response:

```json
{
  "service": "banking_api",
  "status": "ok"
}
```

### List Transactions

```http
GET /transactions
```

Example:

```bash
curl http://localhost:5000/transactions
```

Example response:

```json
[
  {
    "reference": "TX001",
    "amount": 150.5
  },
  {
    "reference": "TX002",
    "amount": 250.75
  }
]
```

### Create Transaction

```http
POST /transactions
```

Example:

```bash
curl -X POST http://localhost:5000/transactions \
  -H "Content-Type: application/json" \
  -d '{"reference":"TX003","amount":100.00}'
```

Response:

```json
{
  "message": "Transaction created"
}
```

---

## Deployment and Verification

The application is deployed using Docker Compose.

The deployment pipeline uses the image published in JFrog Artifactory.

### Verify running containers

```bash
docker compose ps
```

### Verify API health

```bash
curl -i http://localhost:5000/health
```

Expected HTTP status:

```text
HTTP/1.1 200 OK
```

### Verify transactions

```bash
curl http://localhost:5000/transactions
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
├── .gitlab-ci.yml
├── .gitignore
├── .dockerignore
├── Dockerfile
├── compose.yaml
├── requirements.txt
└── README.md
```

---

## Testing

The project uses pytest for automated application testing.

Current test coverage includes:

- Health endpoint
- Listing transactions
- Creating transactions
- Missing transaction reference
- Missing transaction amount
- Negative transaction amounts

Tests are executed automatically by GitLab CI/CD before the Docker image is built and published.

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
- [x] Automated application deployment

### 4. Artifact and Security Management
- [x] JFrog Artifactory
- [x] HashiCorp Vault
- [x] GitLab OIDC authentication
- [x] Secret retrieval
- [x] MongoDB authentication
- [ ] Dependency and security scanning
- [ ] SonarQube integration

### 5. Kubernetes
- [ ] Deployment
- [ ] Service
- [ ] ConfigMap
- [ ] Secret
- [ ] PersistentVolumeClaim
- [ ] Ingress
- [ ] Health probes

### 6. GitOps
- [ ] ArgoCD
- [ ] GitOps repository
- [ ] Automated synchronization
- [ ] Rollback strategies

### 7. Observability and SRE
- [ ] Centralized logging
- [ ] Prometheus
- [ ] Grafana
- [ ] Metrics and monitoring
- [ ] Alerting
- [ ] Troubleshooting scenarios
- [ ] Root Cause Analysis

### 8. Cloud and Infrastructure as Code
- [ ] Terraform
- [ ] Cloud infrastructure
- [ ] Remote state
- [ ] Infrastructure CI/CD

---

## Project Objectives

The main objective is to build practical DevOps/SRE experience through an incremental implementation of an application delivery platform.

Key areas of focus:

- CI/CD automation
- Containerization
- Artifact management
- Secrets management
- Authentication and access control
- Application deployment
- Kubernetes and GitOps
- Observability
- Incident troubleshooting and RCA
- Infrastructure as Code

The project simulates selected components of an enterprise application delivery workflow. It is a learning laboratory and is not intended to represent a production banking platform.