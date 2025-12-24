# Foundation Project 1: Infrastructure as Code (Terraform)

## 🎯 Goal
Master the art of **Infrastructure as Code (IaC)**. We will provision a secure, production-grade Data Lake storage layer on AWS without clicking a single button in the AWS Console.

## 🛑 The "Console Click" Problem
In a junior engineer's workflow, creating a bucket involves logging into the AWS Console, clicking "Create Bucket", typing a name, and hoping they remember to enable encryption.
*   **Problem 1:** It's not reproducible. If you need a "Staging" environment, you have to do it all again manually.
*   **Problem 2:** It's not auditable. There is no git commit history showing *who* created the bucket or *why* public access was enabled.
*   **Problem 3:** Drift. Someone might manually turn off versioning, and no one would know until data is lost.

## 🛠️ The Solution: Terraform
We define our infrastructure in `.tf` files. This allows us to:
1.  **Version Control:** Commit infrastructure changes to Git.
2.  **Reproducibility:** Run `terraform apply` to spin up an identical copy in `prod`.
3.  **Security Standards:** Enforce encryption and block public access via code modules.

## 🏗️ Architecture
We will provision a standard **Medallion Architecture** storage layout:
1.  **Landing Zone:** Transient storage for raw incoming files.
2.  **Bronze:** Raw historical data (Immutable, Versioned).
3.  **Silver:** Cleaned, validated, and enriched data.
4.  **Gold:** Aggregated, business-level data.

## 📝 Implementation Details
*   **Provider:** AWS (`hashicorp/aws`)
*   **Resources:**
    *   `aws_s3_bucket`: The container.
    *   `aws_s3_bucket_versioning`: Enabled for disaster recovery.
    *   `aws_s3_bucket_server_side_encryption_configuration`: AES256 by default.
    *   `aws_s3_bucket_public_access_block`: **Critical** security control to prevent data leaks.

## 🚀 How to Run
1.  Install Terraform.
2.  Configure AWS Credentials (`aws configure`).
3.  Initialize:
    ```bash
    terraform init
    ```
4.  Plan:
    ```bash
    terraform plan
    ```
5.  Apply:
    ```bash
    terraform apply
    ```
