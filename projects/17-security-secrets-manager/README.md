# Foundation Project 17: Security (AWS Secrets Manager)

## 🎯 Goal
Master **Cloud Security Best Practices**. We will write a Python script that retrieves database credentials from **AWS Secrets Manager** at runtime, ensuring no passwords ever appear in our source code (Git).

## 🛑 The "Hardcoded Password" Problem
*   **Junior Mistake:** `password = "SuperSecret123!"` in `main.py`.
*   **Risk:** You push `main.py` to GitHub. Processors scan GitHub public repos and steal your AWS keys in seconds.
*   **Solution:** Store the secret in a dedicated vault (Secrets Manager). The code only contains the *name* of the secret, not the value.

## 🛠️ The Solution: AWS Secrets Manager
1.  **Storage:** Encrypted vault for keys/passwords.
2.  **Rotation:** Can automatically rotate passwords every 30 days (with Lambda).
3.  **SDK:** `boto3.client('secretsmanager').get_secret_value()`.

## 🏗️ Architecture
1.  **Secret:** `prod/redshift/admin` (Contains `{"user": "admin", "password": "..."}`).
2.  **IAM Role:** The EC2/Lambda running the code has permission `secretsmanager:GetSecretValue`.
3.  **Code:** `db_connector.py` fetches the secret, parses the JSON, and connects.

## 🚀 How to Run (Simulation)
1.  **Code:** `db_connector.py` uses `boto3`.
2.  **Run:**
    ```bash
    python db_connector.py
    ```
    *Note: The script includes a mock fallback so you can run it locally without a real AWS account.*
