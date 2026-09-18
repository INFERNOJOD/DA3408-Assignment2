# AI Operations Assignment 2

## Overview

This assignment implements a spam-detection REST API and demonstrates
Docker containerization, Docker Compose with Redis caching, and
Kubernetes orchestration.

The API provides:
- `POST /predict` — predicts whether a message is `spam` or `ham`.
- `GET /healthz` — checks whether the API is running.

The model uses TF-IDF with a Multinomial Naive Bayes classifier.

---

## Repository Structure

- `train.py` — trains and saves the spam-detection model.
- `app.py` — REST API implementation with Redis caching.
- `app_v2.py` — API version used for the Kubernetes rolling update.
- `requirements.txt` — Python dependencies.
- `spam_dataset.csv` — generated spam-detection dataset.

### Docker

- `Dockerfile` — single-stage Docker build.
- `Dockerfile.multistage` — multi-stage Docker build.
- `Dockerfile.q4` — Dockerfile used to build the Q4 version.
- `docker-compose.yml` — API and Redis Compose services.

### Kubernetes

- `generate_shards.py` — generates the 8 validation shards.
- `validate.py` — validates one shard.
- `Dockerfile.validator` — container image for the shard validator.
- `q3-job.yaml` — Kubernetes Indexed Job.
- `q4-deployment.yaml` — Kubernetes Deployment and Service.

### Other

- `shards/` — 8 generated CSV shards for Q3.
- `evidence/` — screenshots showing the results for Q1–Q4.
- `AI_DISCLOSURE.md` — AI tool usage disclosure.
- `report.pdf` — 2-page assignment write-up.

---

## Setup

Create and activate a Python virtual environment if required:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Train the model:

```bash
python3 train.py
```

This creates `model.joblib`.

## Q1: Docker

Build the single-stage image:

```bash
docker build -t spam-api:single .
```

Build the multi-stage image:

```bash
docker build -f Dockerfile.multistage -t spam-api:multi .
```

Run the API:

```bash
docker run -d --name spam-api-multi -p 8000:8000 spam-api:multi
```

Test the health endpoint:

```bash
curl http://localhost:8000/healthz
```

Test prediction:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"WIN a FREE laptop now!"}'
```

## Q2: Docker Compose and Redis

Start the API and Redis services:

```bash
docker compose up -d
```

The API connects to Redis using the Compose service name `cache`.

To stop the services:

```bash
docker compose down
```

The first prediction for an input is a cache miss. The result is stored
in Redis with a TTL, and repeated identical inputs are served from the
cache.

## Q3: Kubernetes Indexed Job

Generate the validation shards:

```bash
python3 generate_shards.py
```

Build the validator image:

```bash
docker build -f Dockerfile.validator -t q3-validator:latest .
```

Load the image into Minikube:

```bash
minikube image load q3-validator:latest
```

Apply the Indexed Job:

```bash
kubectl apply -f q3-job.yaml
```

Check the pods:

```bash
kubectl get pods -o wide
```

Read the logs of the completed validator pods:

```bash
kubectl logs <pod-name>
```

The Job validates one shard per pod and reports the invalid-row count.

## Q4: Kubernetes Deployment

Load the Q1 multi-stage image into Minikube:

```bash
minikube image load spam-api:multi
```

Apply the Deployment and Service:

```bash
kubectl apply -f q4-deployment.yaml
```

Check the Deployment:

```bash
kubectl get deployments
```

Check the API pods:

```bash
kubectl get pods -l app=spam-api -o wide
```

Check the Service:

```bash
kubectl get services
```

### Self-Healing

A running API pod can be deleted manually:

```bash
kubectl delete pod <pod-name>
```

Kubernetes recreates the pod to maintain the desired two replicas.

### Rolling Update

Build and load the v2 image:

```bash
docker build -f Dockerfile.q4 -t spam-api:v2 .
minikube image load spam-api:v2
```

Update the Deployment:

```bash
kubectl set image deployment/spam-api spam-api=spam-api:v2
```

Check the rollout:

```bash
kubectl rollout status deployment/spam-api
kubectl rollout history deployment/spam-api
```

## Evidence

The `evidence/` directory contains screenshots for the completed
requirements of Q1, Q2, Q3, and Q4.

The detailed results and explanations are provided in `report.pdf`.

## Results

- **Q1:** Multi-stage image reduced the reported image size from 723 MB to 710 MB.
- **Q2:** The repeated cached request was approximately 8.15 times faster.
- **Q3:** 8 shards were processed, with 3 invalid rows per shard and 24 invalid rows in total.
- **Q4:** The API was deployed with 2 replicas and demonstrated self-healing and a rolling update.
