# Jenkins CI/CD Pipeline — FastAPI to AWS ECS

Fully containerized Jenkins CI/CD pipeline that builds a FastAPI app, runs tests, pushes the Docker image to AWS ECR, and redeploys an ECS service. Based on the [official Jenkins Docker docs](https://www.jenkins.io/doc/book/installing/docker/).

## Pipeline Flow

```
Push to GitHub → Checkout → Build Docker Image → Run Tests → Push to ECR → Redeploy ECS
```

| Stage | What it does |
|-------|-------------|
| **Checkout** | Pulls source from GitHub |
| **Build** | Builds production image via multi-stage `app.Dockerfile` (linux/amd64) |
| **Test** | Builds the test target — runs `pytest`, fails pipeline if tests break |
| **Push to ECR** | Authenticates to AWS ECR and pushes `:<build_number>` + `:latest` tags |
| **Deploy to ECS** | Runs `aws ecs update-service --force-new-deployment` to roll out new tasks |

## Quick Start

```bash
docker compose up -d --build
```

## Access Jenkins

1. Open http://localhost:8080
2. Get the initial admin password:
   ```bash
   docker exec jenkins-blueocean cat /var/jenkins_home/secrets/initialAdminPassword
   ```
3. Paste the password, install suggested plugins, and create your admin user.

## Project Structure

```
├── app/
│   ├── __init__.py
│   └── main.py              # FastAPI app (health check, /items CRUD)
├── tests/
│   ├── __init__.py
│   └── test_main.py          # pytest tests using FastAPI TestClient
├── app.Dockerfile             # Multi-stage: test + production image
├── Dockerfile                 # Jenkins image (Docker CLI + AWS CLI + Blue Ocean)
├── docker-compose.yml         # Jenkins + Docker-in-Docker orchestration
├── Jenkinsfile                # CI/CD pipeline definition
└── requirements.txt           # Python dependencies
```

## AWS Setup

### Prerequisites

- An ECR repository (e.g. `fastapi-app`) in `ap-south-1`
- An ECS cluster and service configured to pull from that ECR repo
- IAM user with `ecr:*` and `ecs:UpdateService` permissions

### Jenkins Credentials

1. Install the **CloudBees AWS Credentials** plugin
2. Go to **Manage Jenkins → Credentials → Add Credentials**
3. Kind: **AWS Credentials**
4. Enter your `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
5. Update the `credentialsId` in `Jenkinsfile` with the generated credential ID

### Jenkinsfile Configuration

Update these values in the `environment` block of `Jenkinsfile`:

```groovy
ECR_REGISTRY = '<ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com'
ECR_REPO     = 'fastapi-app'
ECS_CLUSTER  = 'fastapi-cluster'
ECS_SERVICE  = 'fastapi-app'
```

## What's Included

- **Jenkins LTS 2.541.2** on JDK 21
- **AWS CLI v2** for ECR/ECS operations
- **Docker-in-Docker** (DinD) so Jenkins can build and push images
- **Blue Ocean** plugin for modern pipeline UI
- **FastAPI** sample app with tests

## Architecture

```
┌─────────────────────┐     ┌──────────────────────┐
│  jenkins-blueocean  │────▶│   jenkins-docker     │
│  (Jenkins server)   │     │   (Docker DinD)      │
│  Port 8080          │     │   Port 2376          │
└─────────────────────┘     └──────────────────────┘
         │                            │
         └────── jenkins network ─────┘
         │                            │
    jenkins-data              jenkins-docker-certs
    (shared volume)           (TLS certs)
              │
              ▼
         ┌────────────────┐     ┌────────────────┐
         │    AWS ECR     │────▶│    AWS ECS     │
         │  (Image Store) │     │  (Deployment)  │
         └────────────────┘     └────────────────┘
```

## Stop / Restart

```bash
docker compose down        # stop (data persists in volumes)
docker compose up -d       # restart
docker compose down -v     # stop and destroy all data
```
