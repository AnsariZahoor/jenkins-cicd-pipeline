# Jenkins CI/CD Pipeline with Docker

Jenkins setup using Docker, based on the [official documentation](https://www.jenkins.io/doc/book/installing/docker/).

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

## What's Included

- **Jenkins LTS 2.541.2** on JDK 21
- **Blue Ocean** plugin for modern pipeline UI
- **Docker-in-Docker** (DinD) so Jenkins can build Docker images
- **Docker Workflow** plugin for Docker pipeline steps
- Sample `Jenkinsfile` with Build → Test → Deploy stages

## Stop / Restart

```bash
docker compose down        # stop (data persists in volumes)
docker compose up -d       # restart
docker compose down -v     # stop and destroy all data
```

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
```
