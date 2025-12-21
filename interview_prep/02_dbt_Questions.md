# dbt Interview Questions Master List (100+)

**Ratio:** ~20% Simple | ~40% Medium | ~40% Hard

---

## 🟢 Simple (Basics - 20 Questions)

1.  **What does dbt stand for?**
    *   Data Build Tool.
2.  **What is the core function of dbt?**
    *   Transformation (The 'T' in ELT).
3.  **What language is dbt code written in?**
    *   SQL + Jinja.
4.  **What is a dbt model?**
    *   A `.sql` file executing a SELECT statement.
5.  **What is `dbt run`?**
    *   Command to execute models against the warehouse.
6.  **What is `dbt test`?**
    *   Runs data integrity checks defined in YAML or SQL.
7.  **What is `ref()`?**
    *   Function to reference other models, building dependency graph.
8.  **What is `source()`?**
    *   Function to reference raw data loaded by EL tools.
9.  **What is `materialized='table'`?**
    *   Config to save model as a physical table.
10. **What is `materialized='view'`?**
    *   Config to save model as a View.
11. **Where do you configure database connections?**
    *   `profiles.yml`.
12. **What is `schema.yml` used for?**
    *   Defining model properties, documentation, and tests.
13. **What is `dbt_project.yml`?**
    *   Main configuration file for the project (paths, global vars).
14. **What is a DAG?**
    *   Directed Acyclic Graph (Dependency tree of models).
15. **What is a "Seed"?**
    *   CSV file in `seeds/` folder loaded into DB by dbt (static data).
16. **What is `dbt docs generate`?**
    *   Builds lineage graph and documentation site.
17. **What is a Package?**
    *   Reusable dbt code (libs) installed via `packages.yml`.
18. **What is Jinja?**
    *   Templating language used for control structures (`{% if %}`).
19. **What is `dbt debug`?**
    *   Checks connection and configuration validity.
20. **Can dbt extract data?**
    *   No, dbt expects data to be in the warehouse already.

---

## 🟡 Medium (Workflow & Logic - 40 Questions)

21. **Explain Ephemeral materialization.**
    *   CTE functionality. No object created in DB. Injected code.
22. **Explain Incremental materialization.**
    *   Processes only new data. Uses `is_incremental()` macro.
23. **What is a Snapshot?**
    *   Implements SCD Type 2 (History tracking) on raw tables.
24. **Differences: `source` vs `ref`?**
    *   Source = Raw data (Root nodes). Ref = dbt models (Internal nodes).
25. **How to run only one model?**
    *   `dbt run --select model_name`.
26. **How to run a model and its children?**
    *   `dbt run --select model_name+`.
27. **What are the 4 generic built-in tests?**
    *   Unique, Not Null, Accepted Values, Relationships (FK).
28. **What is a Custom (Singular) Test?**
    *   A SQL file in `tests/`. If it returns rows, test fails.
29. **What is `dbt run --full-refresh`?**
    *   Drops and recreates all tables, ignoring incremental logic.
30. **What are "Vars"?**
    *   Global variables defined in `dbt_project.yml` or passed via CLI.
31. **What is a Macro?**
    *   Reusable, parameterized SQL/Jinja snippet (function).
32. **What is `dbt deps`?**
    *   Installs dependencies from `packages.yml`.
33. **Explain "Freshness" in sources.**
    *   Config `freshness:` block to warn/error if raw data is stale.
34. **What is the `target` directory?**
    *   Artifacts folder (compiled SQL, run results). Do not commit to Git.
35. **What is `dbt compile`?**
    *   Compiles Jinja/SQL into pure SQL in `target/` without running it.
36. **How to use Environment Variables?**
    *   `{{ env_var('KEY') }}`.
37. **What are "tags"?**
    *   Labels for models to group execution (`dbt run --select tag:daily`).
38. **Explain the "Target" in profiles.**
    *   Defines connection details (Dev, Prod, CI).
39. **What is `run_results.json`?**
    *   Output file containing status/timing of the last run.
40. **How to document a column?**
    *   `description:` field in `schema.yml`.
41. **What are Doc Blocks?**
    *   Markdown snippets `{% docs %}` to reuse descriptions.
42. **What is the `analysis/` folder?**
    *   For analytical queries that don't become tables/views (compiled only).
43. **How to handle PII columns?**
    *   Hashing or masking macros in the staging layer.
44. **What is `dbt build`?**
    *   Runs models, tests, snapshots, seeds in DAG order (Smart runner).
45. **Difference between `check` and `timestamp` strategy in Snapshots?**
    *   Timestamp relies on `updated_at`. Check creates hash of row to detect changes (slower).
46. **What is an "Exposure"?**
    *   Defining downstream dependencies (Dashboards) in YAML for lineage.
47. **How to ignore a model?**
    *   `enabled: false` in config.
48. **What is `dbt clean`?**
    *   Deletes the `target/` directory.
49. **Explain "Hooks" (pre/post).**
    *   SQL to run before/after model execution (e.g., GRANT permissions).
50. **What is `dbt seed` vs `COPY INTO`?**
    *   Seed is for tiny static reference data (Country codes). Not for loading big data.
51. **How to handle schema drift in Incremental models?**
    *   `on_schema_change: sync_all_columns` configuration.
52. **What is a "Hub" or "Spoke" in dbt mesh?**
    *   Cross-project references (Advanced).
53. **What is `state:modified`?**
    *   Selector to run only changed models (Slim CI).
54. **What is `defer`?**
    *   Using production artifacts for referenced models that constitute "state".
55. **How to troubleshoot a "Cycle Error"?**
    *   Model A refs B, B refs A. Fix by using Staging layers.
56. **What is `adapter.dispatch`?**
    *   Writing macros that support multiple warehouses (Snowflake & Postgres versions).
57. **How does dbt handle transactions?**
    *   Most warehouse adapters run models transactionally (Create Temp -> Swap).
58. **Can you define a test on a source?**
    *   Yes, in `sources.yml`.
59. **What is `generate_schema_name` macro?**
    *   Controls custom schema naming logic (e.g., `analytics_dev_dept` vs `analytics`).
60. **What is the `dbt-utils` package?**
    *   Common macros (surrogate_key, date_spine, pivot).

---

## 🔴 Hard (Architecture & Advanced - 40 Questions)

61. **Design a Blue/Green deployment pattern in dbt.**
    *   Run strict "production" build to `_blue` schema, run tests, then swap schemas.
62. **Optimize a clear bottlenecks in dbt lineage.**
    *   Identify blocking models (high fan-out). Materialize them as Tables.
63. **Strategies for huge Incremental Backfills?**
    *   Batched backfills using `--vars` for date ranges. Clone zero-copy.
64. **How to debug a Jinja compilation error?**
    *   Use `dbt compile`. Check whitespace/block closure.
65. **Explain "Jinja Context".**
    *   What variables are available at parse time vs run time (execute flag).
66. **Write a macro to create a Masking Policy.**
    *   `using CREATE MASKING POLICY...` as a post-hook.
67. **How to unit test complex SQL logic in dbt?**
    *   Use `dbt-unit-tests` (mock inputs with CTEs, assert output).
68. **Explain the issue of "Late Arriving Facts" in incremental models.**
    *   Events arrive after the window. Need lookback window `where date > max(date) - interval 3 days`.
69. **Handling "Hard Deletes" in incremental models.**
    *   Need to track deleted source keys. config(`incremental_strategy='merge'`) usually handles updates, not deletes unless specified.
70. **Orchestrating dbt with Airflow?**
    *   `BashOperator` (`dbt run`). `Cosmos` or `Astronomer` provider to parse manifest and split into Airflow Tasks.
71. **How to query run_results.json programmatically?**
    *   Parse JSON to push metrics (rows, duration) to Datadog/CloudWatch.
72. **What is "Introspection" in dbt?**
    *   dbt querying `information_schema` to know existing table states.
73. **Managing 5000 models: Compilation slowness.**
    *   Use Partial Parsing. Limit `source` freshness checks.
74. **Explain `ref` vs `source` in lineage terms.**
    *   Source breaks lineage (Start). Ref ensures connectivity.
75. **How to version control dbt packages?**
    *   Specify version/git tag in `packages.yml`.
76. **What are Analysis files useful for?**
    *   Code auditing / sharing queries that don't need persistence.
77. **Custom Materializations use cases?**
    *   Lambda views, Materialized Views (Snowflake), insert-only logs.
78. **Using Python models in dbt (v1.3+).**
    *   Return a DataFrame. Use `dbt.ref()`. Runs on Snowpark/Databricks Python.
79. **How to assure Idempotency in standard loads?**
    *   `DELETE WHERE... INSERT` or `MERGE`. dbt handles this.
80. **Explain `dbt-metrics` (Deprecated) vs Semantic Layer.**
    *   Defining metrics (revenue) in YAML. dbt is moving logic to Semantic Layer for dynamic query generation.
81. **Securely handling credentials in CI/CD?**
    *   GitHub Secrets inject into `profiles.yml` via Environment Vars.
82. **What happens if a Unique test fails in Production?**
    *   Alert triggers. downstream data might be bad.
    *   *Advanced:* Config test with `severity: warn` or use `store_failures` to debug.
    3. **"Store Failures" feature.**
    *   Saves failing rows to a table in `dbt_test__audit` schema.
84. **Incremental logic for 'append-only' immutable logs.**
    *   `strategy='append'`. Fast. No key check.
85. **Resolving Circular Dependencies in architecture.**
    *   Create a Bridge/Staging table.
86. **How to audit dbt runs?**
    *   `dbt_artifacts` package. Ingest `run_results.json` into a table for dashboarding.
87. **Explain the `config` inheritance hierarchy.**
    *   `dbt_project.yml` < `schema.yml` < In-file `config()`.
88. **Using `run_query` macro.**
    *   Execute SQL and return results to Jinja context (e.g., Get list of states to iterate loop).
89. **What is `execute` mode in Jinja?**
    *   Flag checking if dbt is actually running or just resolving refs. Use `{% if execute %}` for wrapping query calls.
90. **Can you define Custom Schemas per model?**
    *   Yes, `schema='marketing'`.
91. **What is the `generated_at` timestamp?**
    *   Found in artifacts.
92. **Handling different SQL dialects (Redshift vs BigQuery).**
    *   `dbt.type_string()` or `adapter.dispatch`.
93. **What is `elementary` package?**
    *   Advanced observability companion for dbt.
94. **How to implement a "Date Spine"?**
    *   Generating a table of all dates to `LEFT JOIN` against sparse data.
95. **Explain `meta` config.**
    *   Store arbitrary metadata (owner, tier) for 3rd party tool consumption.
96. **How to disable a model in one environment only?**
    *   `enabled: "{{ target.name == 'prod' }}"`.
97. **What is `alias` config?**
    *   Rename physical table, keep logical file name.
98. **Does dbt support UDFs?**
    *   Yes, via macros creating the UDF DDL.
99. **How to implement Role Based Access Control (RBAC)?**
    *   Post-hooks running `GRANT SELECT...`.
100. **What is the future of dbt?**
    *   Semantic Layer, Mesh, Python models.
