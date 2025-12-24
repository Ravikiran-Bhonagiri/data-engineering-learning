# Foundation Project 20: Identity (AWS IAM)

## 🎯 Goal
Master **Least Privilege Security**. We will write a JSON Policy that grants permissions so specific that a user can only upload files to a specific *subfolder* of a bucket, and *only* if they are on the corporate VPN.

## 🛑 The "AdminAccess" Problem
*   **Junior Mistake:** Attaching `AdministratorAccess` to an EC2 instance because "Perimssion Denied" errors are annoying.
*   **Risk:** If that EC2 is hacked, the attacker owns your entire cloud account.
*   **Solution:** Grant *only* what is needed (`s3:PutObject`) on *only* the specific resource (`arn:aws:s3:::my-bucket/uploads/*`).

## 🛠️ The Solution: IAM Condition Keys
Condition Keys add logic to permissions:
1.  `aws:SourceIp`: Restrict access to specific IP ranges (VPN).
2.  `s3:prefix`: Restrict access to specific folders.
3.  `aws:CurrentTime`: Restrict access to business hours.

## 🏗️ Architecture
1.  **Principal:** The User or Role (e.g., `DataLoaderRole`).
2.  **Action:** `s3:PutObject`.
3.  **Resource:** `arn:aws:s3:::finance-data/incoming/*`.
4.  **Condition:** Must be from IP `203.0.113.0/24`.

## 🚀 How to Run (Simulation)
1.  Review `least_privilege_policy.json`.
2.  This is a **JSON artifact**. In a real environment, you not create this via Terraform or the AWS Console.
