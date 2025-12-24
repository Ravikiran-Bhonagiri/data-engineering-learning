# Foundation Project 9: Governance (Unity Catalog)

## 🎯 Goal
Master **Data Governance**. We will define a secure, 3-level namespace hierarchy and enforce "Need-to-Know" access control using **Unity Catalog (UC)**.

## 🛑 The "Bucket Soup" Problem
In legacy Data Lakes:
*   **No Hierarchy:** Everything is just a folder in S3 (`s3://my-bucket/contracts/`).
*   **No Fine-Grained ACLs:** You can't say "Bob can read Column A but not Column B." You either give access to the whole bucket or nothing.
*   **No Discovery:** There is no "Search" bar to find datasets.

## 🛠️ The Solution: Unity Catalog
UC adds a logical layer above S3:
1.  **3-Level Namespace:** `Catalog` -> `Schema` (Database) -> `Table/Volume`.
2.  **Volumes:** Secure storage for non-tabular files (PDFs, Images) governed just like tables.
3.  **Grants:** Standard SQL `GRANT SELECT ON ...` syntax.

## 🏗️ Architecture
1.  **Catalog (`finance_prod`):** Top-level container.
2.  **Schema (`reporting`):** Logical grouping.
3.  **Table (`daily_revenue`):** Managed Delta Table.
4.  **Volume (`raw_pdfs`):** Managed storage for unstructured documents.

## 🚀 How to Run (on Databricks SQL)
Copy and paste the `setup_governance.sql` script into a Databricks SQL Editor.
*Note: You need "Account Admin" or "Metastore Admin" privileges to create Catalogs.*
