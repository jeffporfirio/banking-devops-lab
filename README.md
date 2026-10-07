# Banking DevOps Lab

A hands-on DevOps/SRE laboratory built around a simple banking REST API.

The project is designed to progressively implement modern DevOps practices, including automated testing, containerization, CI/CD, artifact management, secrets management, Kubernetes, GitOps and observability.

## Project Status

Current stage:

* Flask REST API
* MongoDB
* Docker
* Docker Compose
* Automated tests with pytest
* Git version control

Planned stages:

* GitLab CI/CD
* Docker image management with JFrog Artifactory
* Secrets management with HashiCorp Vault
* Kubernetes
* ArgoCD / GitOps
* Observability
* Troubleshooting and RCA
* Cloud infrastructure with Terraform

---

## Architecture

Current architecture:

```text
                  ┌───────────────┐
                  │     Client    │
                  │  curl / HTTP  │
                  └───────┬───────┘
                          │
                          │ HTTP :5000
                          ▼
                  ┌───────────────┐
                  │   Flask API   │
                  │   Python      │
                  │   Container   │
                  └───────┬───────┘
                          │
                          │ PyMongo
                          ▼
                  ┌───────────────┐
                  │    MongoDB    │
                  │   Container   │
                  │    :27017     │
                  └───────────────┘
```

The Flask API and MongoDB run as separate Docker Compose services on the same Docker network.

---

## Technologies

### Current

* Python 3.12
* Flask
* PyMongo
* MongoDB 7
* Docker
* Docker Compose
* pytest
* Git

### Planned

* GitLab CI/CD
* JFrog Artifactory
* HashiCorp Vault
* Kubernetes
* ArgoCD
* SonarQube
* Observability tools
* Terraform
* Cloud infrastructure

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
├── .gitignore
├── Dockerfile
├── compose.yaml
├── requirements.txt
└── README.md
```

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

---

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
  }
]
```

---

### Create Transaction

```http
POST /transactions
```

Example:

```bash
curl -X POST http://localhost:5000/transactions \
  -H "Content-Type: application/json" \
  -d '{"reference":"TX002","amount":250.75}'
```

Response:

```json
{
  "message": "Transaction created"
}
```

---

## Running the Application

### Prerequisites

Make sure the following are installed:

* Docker
* Docker Compose
* Python 3.12+
* Git

### Start the application

From the project root:

```bash
docker compose up -d --build
```

Check the containers:

```bash
docker compose ps
```

Expected services:

```text
banking-devops-lab-api-1
banking-devops-lab-mongo-1
```

### Test the API

Health check:

```bash
curl http://localhost:5000/health
```

List transactions:

```bash
curl http://localhost:5000/transactions
```

Create a transaction:

```bash
curl -X POST http://localhost:5000/transactions \
  -H "Content-Type: application/json" \
  -d '{"reference":"TX003","amount":100.00}'
```

---

## Running the Tests

Activate the Python virtual environment:

```bash
source .venv/bin/activate
```

Run the tests:

```bash
python -m pytest
```

The current test suite validates:

* Health endpoint
* Listing transactions
* Creating transactions
* Missing transaction reference
* Missing transaction amount
* Negative transaction amounts

---

## Environment Configuration

The API uses the following environment variable to connect to MongoDB:

```text
MONGO_URI=mongodb://mongo:27017
```

The value is configured by Docker Compose.

The `.env` file is excluded from Git to prevent accidental exposure of configuration or secrets.

---

## Development Roadmap

The project will evolve through the following stages:

### 1. Application

* [x] Flask REST API
* [x] MongoDB integration
* [x] Docker
* [x] Docker Compose

### 2. Testing and Version Control

* [x] pytest
* [x] Automated API tests
* [x] Git repository
* [x] `.gitignore`
* [x] Initial commit
* [ ] Improve test coverage

### 3. CI/CD

* [ ] GitLab repository
* [ ] GitLab Runner
* [ ] GitLab CI pipeline
* [ ] Automated pytest execution
* [ ] Docker image build
* [ ] Docker image publishing

### 4. Artifact and Security Management

* [ ] JFrog Artifactory
* [ ] HashiCorp Vault
* [ ] Secret management
* [ ] Dependency/security scanning
* [ ] SonarQube

### 5. Kubernetes

* [ ] Deployment
* [ ] Service
* [ ] ConfigMap
* [ ] Secret
* [ ] PersistentVolumeClaim
* [ ] Ingress
* [ ] Health probes

### 6. GitOps

* [ ] ArgoCD
* [ ] GitOps repository
* [ ] Automated deployment
* [ ] Rollback

### 7. Observability and SRE

* [ ] Application logging
* [ ] Metrics
* [ ] Monitoring
* [ ] Alerting
* [ ] Troubleshooting scenarios
* [ ] Root Cause Analysis

### 8. Cloud and Infrastructure as Code

* [ ] Terraform
* [ ] Cloud infrastructure
* [ ] Remote state
* [ ] CI/CD for infrastructure

---

## Objective

The goal of this laboratory is to simulate a realistic DevOps/SRE environment and demonstrate practical experience with:

* Software development
* Automated testing
* Containerization
* CI/CD
* Artifact management
* Secrets management
* Kubernetes
* GitOps
* Observability
* Infrastructure as Code
* Troubleshooting and RCA

The project is intentionally developed incrementally to reflect a real-world DevOps delivery lifecycle.

