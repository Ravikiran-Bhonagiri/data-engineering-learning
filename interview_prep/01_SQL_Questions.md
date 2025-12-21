# SQL Interview Questions Master List (100+)

**Ratio:** ~20% Simple | ~40% Medium | ~40% Hard

---

## 🟢 Simple (Definitions & Syntax - 20 Questions)

1.  **What is the difference between `UNION` and `UNION ALL`?**
    *   `UNION` removes duplicates (distinct sort); `UNION ALL` appends datasets (faster).
2.  **Explain `TRUNCATE` vs `DELETE`.**
    *   `TRUNCATE` is DDL (resets metadata, no transaction log per row, faster, cannot rollback in some DBs without transaction wrappers). `DELETE` is DML (logs every row, slower, can have WHERE clause).
3.  **What is a Primary Key?**
    *   Unique identifier for a record. Cannot be NULL. implicitly indexed.
4.  **What is a Foreign Key?**
    *   A field linking to the Primary Key of another table. Enforces referential integrity.
5.  **Difference between `WHERE` and `HAVING`?**
    *   `WHERE` filters *before* aggregation. `HAVING` filters *after* aggregation (GROUP BY).
6.  **What are the different types of Joins?**
    *   Inner, Left, Right, Full Outer, Cross (Cartesian), Self.
7.  **What is a NULL value?**
    *   Absence of distinct value (Not zero, not empty string). `NULL != NULL`. Using logic with NULL usually returns NULL.
8.  **What is a View?**
    *   A virtual table based on a SELECT query. Does not store data (unless Materialized).
9.  **What is an Index?**
    *   Data structure (B-Tree) to improve lookup speed at cost of write speed and storage.
10. **What is DDL vs DML?**
    *   DDL (Data Definition): CREATE, ALTER, DROP.
    *   DML (Data Manipulation): SELECT, INSERT, UPDATE, DELETE.
11. **What is `DISTINCT`?**
    *   Removes duplicate rows from the result set.
12. **What is `LIMIT` or `TOP`?**
    *   Restricts number of rows returned. Useful for sampling.
13. **What does `LIKE` do?**
    *   Pattern matching using wildcards (`%` for any string, `_` for single char).
14. **What is the `GROUP BY` clause?**
    *   Groups rows that have the same values into summary rows.
15. **What is referencing aliasing?**
    *   Using `AS` to rename columns or tables for readability or self-joins.
16. **What is a constraint?**
    *   Rules enforced on data columns (NOT NULL, UNIQUE, CHECK, DEFAULT).
17. **What is `BETWEEN`?**
    *   Range selection. Inclusive of endpoints.
18. **What is `IN` operator?**
    *   Shorthand for multiple `OR` conditions.
19. **What is an Aggregate Function?**
    *   Calculates on a set of values to return a single scalar (SUM, AVG, MIN, MAX).
20. **Can you JOIN a table to itself?**
    *   Yes, Self Join. Requires aliasing.

---

## 🟡 Medium (Implementation & Scenarios - 40 Questions)

21. **How to find duplicate records?**
    *   `GROUP BY` all columns, `HAVING COUNT(*) > 1`.
22. **Find the 2nd highest salary.**
    *   `SELECT MAX(salary) FROM table WHERE salary < (SELECT MAX(salary) FROM table)` OR `DENSE_RANK()`.
23. **What is a CTE and why use it?**
    *   Common Table Expression (`WITH`). Readability, recursion, usage multiple times in one query.
24. **Exists vs IN performance?**
    *   `EXISTS` allows early exit (stops at first match). `IN` may scan the whole list. `EXISTS` generally faster for subqueries.
25. **What is a Window Function?**
    *   Calculates usage across a set of rows related to specific row (`OVER()`). Does not collapse rows like Group By.
26. **Row_Number vs Rank vs Dense_Rank?**
    *   `Row_Number`: 1,2,3,4. `Rank`: 1,2,2,4. `Dense_Rank`: 1,2,2,3.
27. **How to delete duplicates but keep one?**
    *   Use CTE with `ROW_NUMBER() PARTITION BY keys ORDER BY id`, then DELETE where row_num > 1.
28. **Pattern Matching for 'starts with A'?**
    *   `WHERE name LIKE 'A%'`.
29. **What is Coalesce?**
    *   Returns first non-null value in a list. `COALESCE(col, 0)`.
30. **How to handle NULLs in JOIN keys?**
    *   Nulls do not match. Use `ON a.id = b.id OR (a.id IS NULL AND b.id IS NULL)`.
31. **What is a Cross Join?**
    *   Cartesian product (Row count = A * B). Occurs if no ON condition specified.
32. **Explain `LEAD` and `LAG`.**
    *   Access next row (`LEAD`) or previous row (`LAG`) value without self-join.
33. **Calculate running total.**
    *   `SUM(val) OVER (ORDER BY date)`.
34. **Find rows that exist in Table A but not Table B.**
    *   `LEFT JOIN ... WHERE b.id IS NULL` OR `EXCEPT` / `MINUS`.
35. **Count non-null values vs Count(*)?**
    *   `COUNT(col)` ignores NULLs. `COUNT(*)` counts rows including NULLs.
36. **Update with Join.**
    *   Standard: `UPDATE t1 SET col = t2.val FROM t2 WHERE t1.id = t2.id`.
37. **What is a Stored Procedure?**
    *   Stored code that can take parameters, execute logic/control flow, and return results.
38. **Trigger vs Stored Procedure?**
    *   Trigger activates automatically on event (INSERT/UPDATE). SP must be called explicitly.
39. **What is a Clustered Index?**
    *   Physical sort of data. Only 1 per table.
40. **What is Non-Clustered Index?**
    *   Pointer structure. Many per table.
41. **Difference between char and varchar?**
    *   `CHAR` is fixed length (pads with spaces). `VARCHAR` is variable.
42. **Convert string to date.**
    *   `CAST(str AS DATE)` or `TO_DATE()`.
43. **What is GROUP_CONCAT (or STRING_AGG)?**
    *   Aggregates strings from group into one string with separator.
44. **CASE WHEN usage.**
    *   Conditional logic: `CASE WHEN x > 10 THEN 'High' ELSE 'Low' END`.
45. **How to optimize `SELECT *`?**
    *   Don't use it. Specify columns to reduce I/O and network.
46. **What is an Execution Plan?**
    *   The roadmap the DB engine generates to run query (indexes used, join types, scans).
47. **What is Normalization?**
    *   Structuring data to minimize redundancy (1NF, 2NF, 3NF).
48. **What is Denormalization?**
    *   Adding redundancy (joins) to read optimize for OLAP.
49. **Temporary Table vs Table Variable?**
    *   Temp Table (`#table`) stored in tempdb, supports indexes. Variable (`@table`) memory-only, limited scope.
50. **Recursive CTE?**
    *   Referencing the CTE name inside itself. Used for hierarchies (Org charts).
51. **Safe way to drop table?**
    *   `DROP TABLE IF EXISTS name`.
52. **Pivot data (Rows to Cols).**
    *   `MAX(CASE WHEN...) GROUP BY id`.
53. **Unpivot (Cols to Rows).**
    *   `UNION ALL` or `UNPIVOT` operator.
54. **Find nth highest salary for each department.**
    *   `ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) WHERE rnk = n`.
55. **Difference between Deterministic and Non-Deterministic functions?**
    *   Deterministic (ABS, SUM) always return same result for same input. Non-deterministic (GETDATE, UUID) change.
56. **What is a Composite Key?**
    *   PK made of 2+ columns.
57. **ACID Properties?**
    *   Atomicity, Consistency, Isolation, Durability.
58. **Dirty Read?**
    *   Reading uncommitted data (Isolation violation).
59. **Optimistic vs Pessimistic Locking?**
    *   Optimistic (Version checks). Pessimistic (Lock rows).
60. **Function vs Stored Procedure?**
    *   Function must return value, cannot change DB state (mostly). SP can change state, no return required.

---

## 🔴 Hard (Architecture, Tuning, & Complex Puzzles - 40 Questions)

61. **Find Gaps and Islands.**
    *   (See detailed answer in Q13 of previous file).
62. **Explain Index Scan vs Index Seek.**
    *   **Seek:** Pinpoint specific rows using B-Tree (Fast). **Scan:** Reading every leaf page (Slow).
63. **What is a Covering Index?**
    *   Index containing all columns in SELECT list, avoiding lookup to base table (Key Map lookup).
64. **How to optimize a query with leading wildcard `%text`?**
    *   Standard index fails. Solutions: Reverse string index, Full Text Search, or Trigram Index.
65. **Write a query to calculate Day 1 Retention.**
    *   Self Join on `date = date + 1`.
66. **Handle "Cartesian Explosion" in Many-to-Many joins?**
    *   Aggregate/Dedupe before joining.
67. **Explain Partitioning in Databases.**
    *   Horizontal splitting of massive table (by Date/Region). Improves query pruning and management.
68. **Sharding vs Partitioning?**
    *   Partitioning = Same Server. Sharding = Different Servers (Horizontal Scaling).
69. **How to handle concurrency (Lost Update problem)?**
    *   Isolation levels (`Repeatable Read` or `Serializable`) or explicit Locking.
70. **Materialized View vs View?**
    *   Materialized stores physical result, needs refresh. Fast read. Std View runs query every time.
71. **What is `VACUUM` (Postgres) or `OPTIMIZE` (Delta)?**
    *   Reclaiming space from dead tuples (MVCC artifacts) and analyzing stats.
72. **How to debug a slow Join?**
    *   Check statistics, distribution (skew), index usage, or spill-to-disk events.
73. **Correlated Subquery Optimization?**
    *   Rewrite as `JOIN`.
74. **What consists of "Selectivity" in an index?**
    *   Ratio of unique values to total rows. High selectivity (User ID) = Good Index. Low (Gender) = Bad Index.
75. **Columnar Storage benefits?**
    *   Compression (RLE), skipping unused columns, vectorized processing (OLAP).
76. **Write a query for Year-Over-Year growth.**
    *   `LAG(sales, 1) OVER (PARTITION BY product ORDER BY year)`.
77. **How does `MERGE` (Upsert) work internally?**
    *   Joins source/target. If match -> Update. If not -> Insert. Atomic.
78. **What is a SARGable query?**
    *   Search ARGument ABLE. Query that can use an index (e.g., Avoid functions on LHS: `WHERE YEAR(date) = 2021` is bad. `WHERE date BETWEEN '2021-01-01' AND '2021-12-31'` is SARGable).
79. **Explain Isolation Levels.**
    *   Read Uncommitted, Read Committed, Repeatable Read, Serializable. Tradeoff between Consistency and Concurrency.
80. **Deadlock handling?**
    *   DB kills one transaction (victim). App should retry.
81. **Write a query to find median.**
    *   `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY val)`.
82. **Explain 3NF.**
    *   Transitive dependencies removed. Non-key cols depend only on Key. "The Key, the whole Key, and nothing but the Key".
83. **Surrogate Key vs Natural Key.**
    *   Natural (SSN, Email) has business meaning. Surrogate (ID 1,2,3) is artificial, stable, integer.
84. **What is a Bitmap Index?**
    *   Good for low cardinality columns (Gender, Status) in Data Warehouses.
85. **OLTP vs OLAP modeling.**
    *   OLTP: 3NF (Write speed). OLAP: Star Schema/Dimensional (Read speed).
86. **Effect of large IN clause?**
    *   Can exceed parsing limits or force Full Scan. Better to load list into temp table and Join.
87. **Querying Hierarchical Data (Parent-Child) without Recursion?**
    *   Nested Sets model or Path Enumeration string.
88. **What is `LATERAL` or `OUTER APPLY`?**
    *   For-each loop in SQL. Joins row to output of a function/subquery evaluated for that row.
89. **What is Write Amplification?**
    *   One logical write causes multiple physical IOs (Index updates, Page splits).
90. **Bloom Filters in SQL Engines?**
    *   Probabilistic structure to quickly test set membership. Used in Distributed Joins to filter data early.
91. **Data Skew in Distributed SQL?**
    *   Keys unevenly distributed. Causes straggler nodes. Salt keys to fix.
92. **Difference between `COUNT(DISTINCT)` and `APPROX_COUNT_DISTINCT`?**
    *   Exact (Slow, memory heavy) vs HyperLogLog usage (Fast, low memory, error ~1%).
93. **How does `GROUP BY` work physically?**
    *   Hash Aggregate (Memory map) or Sort Aggregate (Sort then iter).
94. **Constraints influence on Optimizer?**
    *   Yes. `NOT NULL`, `CHECK`, `FK` allow optimizer to remove redundant checks or joins.
95. **Finding overlapping date ranges.**
    *   `WHERE a.start < b.end AND a.end > b.start`.
96. **Running Total with Reset condition.**
    *   Complex Window Logic: `SUM(CASE WHEN val < 0 THEN 1 ELSE 0 END) OVER (...)` to create groups.
97. **Calculate simple moving average.**
    *   `AVG(val) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)`.
98. **CTE Materialization (Postgres specific but concept applies).**
    *   CTEs were optimization fences (always materialized). Newer engines treat them like inline views unless specified.
99. **Explain Star vs Snowflake Schema.**
    *   Star: 1 Fact, De-normalized Dims. Snowflake: Normalized Dims. Star is preferred for speed.
100. **SQL Injection?**
    *   Attacker input changes query logic. Prevention: Prepared Statements / Parameterization.

---
**Summary:** This list covers everything from "SELECT * FROM" to complex execution plan tuning.
