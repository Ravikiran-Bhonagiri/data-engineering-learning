# Practice Exercises: Interview Questions

**Real-world scenarios you might face in a Databricks interview takeaway.**

---

## Exercise 1: The "Small Files" Fixer (Medium)
**Scenario:** A junior engineer set up a stream that writes to Delta every 10 seconds. The table layout is now millions of tiny files. Query performance has tanked.

**Task:**
1. Write a script to analyze the file distribution of a Delta table (Hint: `DESCRIBE DETAIL`).
2. Implement a fix to repair the table structure immediately.
3. Configure the streaming job properties to prevent this from happening again.

**Success Criteria:**
- Use `OPTIMIZE`.
- Use `ZORDER` on the correct filter column.
- Set `spark.databricks.delta.optimizeWrite.enabled`.
- Adjust streaming trigger or `maxBytesPerTrigger`.

---

## Exercise 2: Implementing SCD Type 2 (Hard)
**Scenario:** You have a `users` table. When a user updates their address, you must keep the old record with an `end_date` and insert a new record with `current_flag=true`.

**Task:**
1. Create a source DataFrame with updates.
2. Write a PySpark `MERGE` statement (or logic) to implement SCD Type 2.
    - Update the old record: `current_flag=false`, `end_date=current_date`.
    - Insert the new record: `current_flag=true`, `end_date=NULL`.

**Success Criteria:**
- Correctly identify which keys match but have changed values.
- Handle the `UNION` of updates and inserts (Hint: Delta Merge can't update and insert the same key in one pass easily—you might need a specific trick or `dlt.apply_changes`).

---

## Exercise 3: Unity Catalog Migration (Hard)
**Scenario:** The company is migrating from Hive Metastore (legacy) to Unity Catalog.

**Task:**
1. Write a script to:
    - List all tables in a legacy database.
    - Create the corresponding Schema in a UC Catalog.
    - CTAS (Create Table As Select) data from Legacy to UC Deep Clone.
    - Grant permissions to a group `analysts`.

**Success Criteria:**
- Use `DEEP CLONE` for efficient data copying.
- Demonstrate correct `catalog.schema.table` syntax.
- Apply `GRANT SELECT` appropriately.

---

## Exercise 4: Parsing Complex JSON (Medium)
**Scenario:** You are ingesting raw API logs. One column `body` contains a complex nested JSON string that changes schema frequently.

**Task:**
1. Use Auto Loader to ingest the files.
2. Use the `schema_of_json` (or similar inference) to handle the `body` column.
3. Flatten the JSON into separate columns for `user_id`, `event_type`, and `payload`.

**Success Criteria:**
- Use `cloudFiles`.
- Handle dirty data (rescue data column).
- Use `from_json`.

---

## Exercise 5: Debugging a Hung Job (Expert)
**Scenario:** A join job runs for 3 hours and gets stuck at 99%.

**Task:**
1. Explain exactly where you would look in the Spark UI.
2. Propose 3 distinct theories for why it is stuck.
3. Propose a solution for each theory.

**Success Criteria:**
- Identify **Data Skew** (Tasks summary min/max duration).
- Identify **Cartesian Product** (Output rows >> Input rows).
- Identify **Bad Broadcast** (Driver OOM).

---

**Treat these as if you are explaining your solution to a hiring manager.**
