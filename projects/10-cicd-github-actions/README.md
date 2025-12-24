# Foundation Project 10: DevOps (CI/CD)

## 🎯 Goal
Master **Continuous Integration / Continuous Deployment (CI/CD)**. We will automate the "Quality Control" process so that every time you push code to Git, a robot (`GitHub Actions`) runs your tests for you.

## 🛑 The "Bad Merge" Problem
Without CI:
*   **Broken Code:** Developer A pushes a change that breaks the ETL pipeline.
*   **Manual Testing:** You have to remember to run `pytest` locally before every commit (you will forget).
*   **Production Outages:** The broken code merges to `main` and deploys to production.

## 🛠️ The Solution: GitHub Actions
We define a **Workflow** (`ci.yml`) that triggers on every `push`.
1.  **Checkout:** Downloads the code.
2.  **Setup:** Installs Python.
3.  **Lint:** Checks for style errors (flake8).
4.  **Test:** Runs unit tests (pytest).

**If any step fails, the merge is blocked.**

## 🏗️ Architecture
1.  **Code:** `app.py` (Simple function).
2.  **Test:** `test_app.py` (Assertions).
3.  **Pipeline:** `.github/workflows/ci.yml`.

## 🚀 How to Run (Simulation)
Since this repository isn't connected to a live GitHub Actions runner, we simulate the structure.
1.  Navigate to this folder.
2.  Run the checks manually to see what the robot would do:
    ```bash
    pip install pytest flake8
    flake8 .
    pytest
    ```
