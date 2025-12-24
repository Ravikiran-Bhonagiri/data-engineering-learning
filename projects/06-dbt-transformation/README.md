# Foundation Project 6: Transformation (dbt Core)

## 🎯 Goal
Master **Analytics Engineering**. We will use **dbt (data build tool)** to bring software engineering best practices (Version Control, Testing, Documentation) to SQL transformations.

## 🛑 The "Spaghetti SQL" Problem
In traditional warehousing:
*   **No Lineage:** A 500-line stored procedure reads from 10 tables. If you change a column in Table A, does the procedure break? No one knows.
*   **No Testing:** You find out data is null only when the CEO yells about the dashboard.
*   **No Docs:** "Ask Bob what `cust_type_2` means." (Bob left 2 years ago).

## 🛠️ The Solution: dbt
dbt treats SQL as code:
1.  **DAGs:** It infers dependencies (`ref('stg_users')`) automatically, building a graph of your data flow.
2.  **Tests:** You define simple YAML tests (`not_null`, `unique`) and dbt runs them every time.
3.  **Jinja:** It allows using variables and control structures in SQL.

## 🏗️ Architecture
1.  **Sources:** Raw tables (defined in `sources.yml`).
2.  **Staging (Views):** Light cleaning, renaming columns to snake_case. 1:1 with source.
3.  **Marts (Tables):** Business logic, joins, aggregations. The "Gold" layer.

## 🚀 How to Run
*Requires dbt installed (`pip install dbt-core dbt-duckdb` for local demo)*

1.  **Check Config:**
    ```bash
    dbt debug
    ```
2.  **Run Models:**
    ```bash
    dbt run
    ```
3.  **Test Data:**
    ```bash
    dbt test
    ```
    *This runs the assertions defined in schema.yml file.*
