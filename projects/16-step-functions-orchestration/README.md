# Foundation Project 16: Native Orchestration (AWS Step Functions)

## 🎯 Goal
Master **Serverless Orchestration**. We will define a **State Machine** using JSON (Amazon States Language) to coordinate a multi-step workflow with Retries, Catch blocks, and intuitive Branching.

## 🛑 The "Lambda Chain" Problem
*   **Anti-Pattern:** Lambda A calls Lambda B, which calls Lambda C.
*   **Result:** Application logic is hidden in code. If Lambda B times out, Lambda A is still paying for execution time waiting for it. Debugging is a nightmare.
*   **Solution:** **Step Functions** acts as the external coordinator. It triggers Lambda A, waits for the result, checks the output, and *then* triggers Lambda B.

## 🛠️ The Solution: Amazon States Language (ASL)
ASL is a JSON-based language to define your workflow:
1.  **Task State:** Do some work (Invoke Lambda, Run Glue Job).
2.  **Choice State:** If/Else logic based on data inputs.
3.  **Wait State:** Pause for X seconds.
4.  **Parallel State:** Run branches concurrently.

## 🏗️ Architecture
**Microservice Orchestration:**
1.  `ValidateInput`: Checks if data is clean.
2.  `ProcessOrder`: (Mock) processed payment.
3.  `SendEmail`: (Mock) notifies user.
4.  **Error Handling:** If `ProcessOrder` fails, go to `Refund` state.

## 🚀 How to Run (Simulation)
1.  **Definition:** `workflow.asl.json` contains the logic.
2.  **Deploy:** `deploy_statemachine.py` uses `boto3` to register this JSON with AWS.
    ```bash
    python deploy_statemachine.py
    ```
