# Advance Project 29: Container Orchestration (Amazon EKS)

## 🎯 Goal
Master **Cluster Management**. We will define the Infrastructure-as-Code (YAML) to deploy a scalable Python Data API to **Amazon EKS (Elastic Kubernetes Service)**.

## 🛑 The "Docker Compose" Problem
*   **Project 8 (Docker):** Great for running *one* container on your laptop.
*   **Production:** You have 50 containers. Container A crashes. Container B needs more RAM. Node 1 fails.
*   **Solution (Kubernetes):** The "Operating System" of the Cloud. It self-heals (restarts crashed pods) and auto-scales (adds more pods).

## 🛠️ The Solution: K8s Manifests
Using declarative YAML to tell K8s what we want:
1.  **Deployment:** "Run 3 replicas of `my-data-api:v1`".
2.  **Service:** "Expose these 3 replicas behind a single internal Load Balancer".

## 🏗️ Architecture
1.  **Cluster:** EKS Control Plane.
2.  **Nodes:** EC2 Worker Nodes.
3.  **Pod:** The wrapper around our Docker container.

## 🚀 How to Run (Simulation)
1.  **Manifest:** `data-api.yaml`.
2.  **Apply:**
    ```bash
    kubectl apply -f data-api.yaml
    ```
    *(Requires a running K8s cluster and kubectl configured).*
