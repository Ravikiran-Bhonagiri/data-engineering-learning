# Foundation Project 8: Containerization (Docker)

## 🎯 Goal
Master **Code Portability**. We will package a Python ETL script and its dependencies into a lightweight **Docker Image** that can run exactly the same way on your laptop, on an EC2 instance, or inside Kubernetes.

## 🛑 The "Works on My Machine" Problem
*   **Scenario:** You write a script using `pandas==2.0.0`. You send it to a colleague, but they have `pandas==1.5.0` installed. The script crashes.
*   **Operating System:** Your laptop is Mac/Windows, but Production is Linux. Path separators (`\` vs `/`) break the code.
*   **Missing System Libs:** Your script needs `kbt` or `gcc` which isn't installed on the server.

## 🛠️ The Solution: Docker
Docker packages the **Code** + **Dependencies** + **Operating System** into a single artifact called an **Image**.
1.  **Dockerfile:** The recipe for building the image.
2.  **Image:** The frozen, read-only artifact.
3.  **Container:** A running instance of the image.

## 🏗️ Architecture
1.  **Application:** `etl.py` (Using Pandas to process CSV).
2.  **Manifest:** `Dockerfile` (Python 3.9 Slim).
3.  **Registry:** AWS ECR (Elastic Container Registry) - simulation.

## 🚀 How to Run

### 1. Build the Image
```bash
docker build -t my-etl-job:v1 .
```

### 2. Run the Container
```bash
docker run my-etl-job:v1
```
*You will see the script output: "ETL Job Finished Successfully."*

### 3. (Simulation) Push to Registry
In a real environment, you would push this to AWS ECR:
```bash
# docker tag my-etl-job:v1 123456789.dkr.ecr.us-east-1.amazonaws.com/my-repo:v1
# docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/my-repo:v1
```
