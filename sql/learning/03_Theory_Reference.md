# 📖 SQL Theory Reference Guide

A comprehensive theory reference for SQL concepts, organized by topic.

---

## 📋 Table of Contents
1. [SQL Basics & Data Types](#1-sql-basics--data-types)
2. [Constraints & Keys](#2-constraints--keys)
3. [Query Execution Order](#3-query-execution-order)
4. [Aggregations](#4-aggregations)
5. [Joins](#5-joins)
6. [Subqueries](#6-subqueries)
7. [CTEs (Common Table Expressions)](#7-ctes)
8. [Window Functions](#8-window-functions)
9. [Transactions & ACID](#9-transactions--acid)
10. [Indexing](#10-indexing)
11. [Query Optimization](#11-query-optimization)
12. [Data Modeling](#12-data-modeling)

---

## 1. SQL Basics & Data Types

### SQL Statement Categories

| Category | Commands | Purpose |
|----------|----------|---------|
| **DDL** (Data Definition) | CREATE, ALTER, DROP, TRUNCATE | Define database structure |
| **DML** (Data Manipulation) | SELECT, INSERT, UPDATE, DELETE | Manipulate data |
| **DCL** (Data Control) | GRANT, REVOKE | Manage permissions |
| **TCL** (Transaction Control) | BEGIN, COMMIT, ROLLBACK | Manage transactions |

### Common Data Types

| Type | PostgreSQL | MySQL | Description |
|------|------------|-------|-------------|
| Integer | INTEGER, BIGINT | INT, BIGINT | Whole numbers |
| Decimal | NUMERIC(p,s), DECIMAL | DECIMAL(p,s) | Exact decimals |
| Float | REAL, DOUBLE PRECISION | FLOAT, DOUBLE | Approximate decimals |
| String | VARCHAR(n), TEXT | VARCHAR(n), TEXT | Character data |
| Date | DATE | DATE | Calendar date |
| Timestamp | TIMESTAMP | DATETIME | Date with time |
| Boolean | BOOLEAN | BOOLEAN, TINYINT(1) | True/False |
| UUID | UUID | CHAR(36) | Unique identifier |

### NULL Handling

```sql
-- NULL is not equal to anything, including NULL
NULL = NULL  -- Returns NULL (not TRUE!)
NULL <> NULL -- Returns NULL (not TRUE!)

-- Correct ways to check NULL
WHERE column IS NULL
WHERE column IS NOT NULL

-- COALESCE returns first non-NULL value
SELECT COALESCE(column, 'default') FROM table;

-- NULLIF returns NULL if values are equal
SELECT NULLIF(value, 0)  -- Returns NULL if value is 0
```

**NULL in aggregations:**
- `COUNT(*)` counts all rows including NULL
- `COUNT(column)` counts only non-NULL values
- `SUM`, `AVG`, `MIN`, `MAX` ignore NULL values

### Date/Time Functions

**Getting Current Date/Time:**
```sql
-- Current date (no time)
SELECT CURRENT_DATE;                    -- PostgreSQL, MySQL
SELECT GETDATE();                       -- SQL Server

-- Current timestamp (date + time)
SELECT NOW();                           -- PostgreSQL, MySQL
SELECT CURRENT_TIMESTAMP;               -- Standard SQL
SELECT GETDATE();                       -- SQL Server
```

**Extracting Parts from Dates:**
```sql
-- EXTRACT function (PostgreSQL, MySQL)
SELECT EXTRACT(YEAR FROM order_date) AS year;
SELECT EXTRACT(MONTH FROM order_date) AS month;
SELECT EXTRACT(DAY FROM order_date) AS day;
SELECT EXTRACT(DOW FROM order_date) AS day_of_week;  -- 0=Sun, 6=Sat
SELECT EXTRACT(QUARTER FROM order_date) AS quarter;

-- DATE_PART (PostgreSQL)
SELECT DATE_PART('year', order_date);
SELECT DATE_PART('month', order_date);

-- MySQL specific
SELECT YEAR(order_date), MONTH(order_date), DAY(order_date);

-- SQL Server
SELECT DATEPART(year, order_date);
SELECT YEAR(order_date), MONTH(order_date), DAY(order_date);
```

**Formatting Dates:**
```sql
-- PostgreSQL
SELECT TO_CHAR(order_date, 'YYYY-MM-DD') AS formatted;
SELECT TO_CHAR(order_date, 'Mon DD, YYYY') AS formatted;
SELECT TO_CHAR(order_date, 'YYYY-MM') AS month_year;

-- MySQL
SELECT DATE_FORMAT(order_date, '%Y-%m-%d');
SELECT DATE_FORMAT(order_date, '%M %d, %Y');

-- SQL Server
SELECT FORMAT(order_date, 'yyyy-MM-dd');
SELECT CONVERT(VARCHAR, order_date, 23);
```

**Date Arithmetic:**
```sql
-- Adding/subtracting intervals (PostgreSQL)
SELECT order_date + INTERVAL '7 days';
SELECT order_date - INTERVAL '1 month';
SELECT order_date + INTERVAL '1 year';

-- MySQL
SELECT DATE_ADD(order_date, INTERVAL 7 DAY);
SELECT DATE_SUB(order_date, INTERVAL 1 MONTH);

-- SQL Server
SELECT DATEADD(day, 7, order_date);
SELECT DATEADD(month, -1, order_date);
```

**Date Differences:**
```sql
-- PostgreSQL (returns interval or days)
SELECT order_date - hire_date AS days_diff;
SELECT AGE(order_date, hire_date);  -- Returns interval

-- MySQL
SELECT DATEDIFF(order_date, hire_date);  -- Days difference
SELECT TIMESTAMPDIFF(MONTH, hire_date, order_date);

-- SQL Server
SELECT DATEDIFF(day, hire_date, order_date);
SELECT DATEDIFF(month, hire_date, order_date);
```

**Truncating Dates:**
```sql
-- PostgreSQL: DATE_TRUNC
SELECT DATE_TRUNC('month', order_date);  -- First day of month
SELECT DATE_TRUNC('year', order_date);   -- First day of year
SELECT DATE_TRUNC('week', order_date);   -- Monday of week

-- MySQL: DATE() for date only
SELECT DATE(created_at);  -- Remove time portion

-- SQL Server: CAST/CONVERT
SELECT CAST(order_date AS DATE);
```

**Common Date Patterns:**
```sql
-- Orders this month
WHERE order_date >= DATE_TRUNC('month', CURRENT_DATE)
  AND order_date < DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month'

-- Last 30 days
WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'

-- Same day last year
WHERE order_date = CURRENT_DATE - INTERVAL '1 year'

-- Beginning of quarter
SELECT DATE_TRUNC('quarter', CURRENT_DATE);
```

### String Functions

```sql
-- Concatenation
SELECT CONCAT(first_name, ' ', last_name);    -- All databases
SELECT first_name || ' ' || last_name;        -- PostgreSQL, Oracle

-- Substring
SELECT SUBSTRING(name FROM 1 FOR 3);          -- PostgreSQL
SELECT SUBSTRING(name, 1, 3);                 -- MySQL, SQL Server
SELECT SUBSTR(name, 1, 3);                    -- Oracle

-- Length
SELECT LENGTH(name);                          -- PostgreSQL, MySQL
SELECT LEN(name);                             -- SQL Server

-- Case conversion
SELECT UPPER(name), LOWER(name);
SELECT INITCAP(name);                         -- PostgreSQL: Title Case

-- Trim whitespace
SELECT TRIM(name);
SELECT LTRIM(name), RTRIM(name);

-- Replace
SELECT REPLACE(email, '@old.com', '@new.com');

-- Position/Location
SELECT POSITION('@' IN email);                -- PostgreSQL
SELECT INSTR(email, '@');                     -- MySQL, Oracle
SELECT CHARINDEX('@', email);                 -- SQL Server

-- Split and extract
SELECT SPLIT_PART(email, '@', 2);             -- PostgreSQL: domain
SELECT SUBSTRING_INDEX(email, '@', -1);       -- MySQL: domain
```

### DISTINCT and Duplicates

```sql
-- Remove duplicate rows
SELECT DISTINCT city FROM customers;

-- Count unique values
SELECT COUNT(DISTINCT city) FROM customers;

-- Multiple columns (unique combinations)
SELECT DISTINCT city, status FROM orders;

-- Find duplicates
SELECT email, COUNT(*) 
FROM employees 
GROUP BY email 
HAVING COUNT(*) > 1;

-- Delete duplicates (keep one)
DELETE FROM employees a
USING employees b
WHERE a.id > b.id AND a.email = b.email;
```

## 2. Constraints & Keys

### Primary Key
- Uniquely identifies each row
- Cannot be NULL
- Only ONE per table
- Automatically creates a unique index

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,  -- Auto-incrementing
    -- or
    id INT PRIMARY KEY
);
```

### Foreign Key
- References primary key in another table
- Enforces referential integrity
- Controls cascade behavior

```sql
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(id)
        ON DELETE CASCADE    -- Delete orders when customer deleted
        ON UPDATE CASCADE    -- Update if customer ID changes
);
```

**ON DELETE/UPDATE Options:**
| Option | Behavior |
|--------|----------|
| CASCADE | Propagate the action |
| SET NULL | Set FK to NULL |
| SET DEFAULT | Set FK to default value |
| RESTRICT | Prevent the action |
| NO ACTION | Similar to RESTRICT (deferred check) |

### Other Constraints

```sql
-- UNIQUE: No duplicates allowed (NULL allowed usually)
email VARCHAR(100) UNIQUE

-- NOT NULL: Must have a value
name VARCHAR(100) NOT NULL

-- CHECK: Custom validation
salary DECIMAL CHECK (salary > 0)
age INT CHECK (age BETWEEN 0 AND 150)

-- DEFAULT: Automatic value if not provided
created_at TIMESTAMP DEFAULT NOW()
status VARCHAR(20) DEFAULT 'pending'
```

---

## 3. Query Execution Order

**Logical order (how SQL processes):**
```
1. FROM        - Identify tables
2. JOIN        - Combine tables  
3. WHERE       - Filter rows
4. GROUP BY    - Create groups
5. HAVING      - Filter groups
6. SELECT      - Choose columns
7. DISTINCT    - Remove duplicates
8. ORDER BY    - Sort results
9. LIMIT       - Restrict rows
```

**Written order (how you type it):**
```sql
SELECT columns     -- 6
FROM table         -- 1
JOIN other_table   -- 2
WHERE condition    -- 3
GROUP BY columns   -- 4
HAVING condition   -- 5
ORDER BY columns   -- 7
LIMIT n OFFSET m   -- 8
```

**Key implications:**
- Cannot use SELECT aliases in WHERE (SELECT runs after WHERE)
- Can use SELECT aliases in ORDER BY (runs after SELECT)
- HAVING can use aggregate functions (runs after GROUP BY)
- WHERE cannot use aggregate functions

### LIMIT and OFFSET (Pagination)

```sql
-- First 10 rows
SELECT * FROM employees ORDER BY salary DESC LIMIT 10;

-- Skip first 20, get next 10 (page 3)
SELECT * FROM employees ORDER BY salary DESC LIMIT 10 OFFSET 20;

-- SQL Server (different syntax)
SELECT * FROM employees ORDER BY salary DESC
OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY;

-- Oracle (before 12c)
SELECT * FROM (
    SELECT e.*, ROWNUM rn FROM employees e WHERE ROWNUM <= 30
) WHERE rn > 20;
```

**Pagination pattern:**
```sql
-- Page N with page_size items
LIMIT page_size OFFSET (page_number - 1) * page_size

-- Example: Page 3, 10 items per page
LIMIT 10 OFFSET 20
```

### Set Operations (UNION, INTERSECT, EXCEPT)

```sql
-- UNION: Combine results, remove duplicates
SELECT city FROM customers
UNION
SELECT location AS city FROM departments;

-- UNION ALL: Combine results, keep duplicates (faster)
SELECT name, 'Employee' AS type FROM employees
UNION ALL
SELECT name, 'Customer' AS type FROM customers;

-- INTERSECT: Rows in BOTH queries
SELECT customer_id FROM orders WHERE status = 'completed'
INTERSECT
SELECT customer_id FROM orders WHERE amount > 1000;

-- EXCEPT (MINUS in Oracle): Rows in first but NOT in second
SELECT customer_id FROM customers
EXCEPT
SELECT customer_id FROM orders;  -- Customers who never ordered
```

**Set operation rules:**
- All queries must have same number of columns
- Column data types must be compatible
- Column names from first query are used
- ORDER BY applies to final result only

---

## 4. Aggregations

### Aggregate Functions

| Function | Description | NULL Handling |
|----------|-------------|---------------|
| COUNT(*) | Count all rows | Counts NULLs |
| COUNT(col) | Count non-NULL values | Ignores NULLs |
| COUNT(DISTINCT col) | Count unique values | Ignores NULLs |
| SUM(col) | Sum of values | Ignores NULLs |
| AVG(col) | Average of values | Ignores NULLs |
| MIN(col) | Minimum value | Ignores NULLs |
| MAX(col) | Maximum value | Ignores NULLs |

### GROUP BY Rules

1. Every non-aggregated column in SELECT must be in GROUP BY
2. GROUP BY can include columns not in SELECT
3. Use HAVING to filter groups (not WHERE)

```sql
SELECT 
    department_id,           -- must be in GROUP BY
    COUNT(*) AS total,       -- aggregate function
    AVG(salary) AS avg_sal   -- aggregate function
FROM employees
WHERE hire_date > '2020-01-01'  -- filters BEFORE grouping
GROUP BY department_id
HAVING COUNT(*) > 5             -- filters AFTER grouping
```

### WHERE vs HAVING

| WHERE | HAVING |
|-------|--------|
| Filters rows BEFORE grouping | Filters groups AFTER aggregation |
| Cannot use aggregate functions | Can use aggregate functions |
| Applied to individual rows | Applied to grouped results |
| Faster (reduces data early) | Slower (processes more data) |

---

## 5. Joins

### Join Types Visualized

```
Table A          Table B
┌───────┐        ┌───────┐
│ A B C │        │ C D E │
└───────┘        └───────┘
```

**INNER JOIN** - Only matching rows from both tables
```
     A ∩ B
```

**LEFT JOIN** - All from A + matching from B
```
     A (including non-matching)
```

**RIGHT JOIN** - All from B + matching from A
```
     B (including non-matching)
```

**FULL OUTER JOIN** - All from both tables
```
     A ∪ B
```

**CROSS JOIN** - Cartesian product (every A with every B)
```
     A × B = |A| × |B| rows
```

### Self-Join
Same table joined to itself, useful for:
- Hierarchies (employee → manager)
- Comparing rows within same table
- Finding pairs

```sql
SELECT 
    e.name AS employee,
    m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id
```

### Join Condition Placement

**ON clause** - Applied during join
```sql
SELECT * FROM a
LEFT JOIN b ON a.id = b.a_id AND b.status = 'active'
-- Non-matching rows from A preserved with NULLs
```

**WHERE clause** - Applied after join
```sql
SELECT * FROM a
LEFT JOIN b ON a.id = b.a_id
WHERE b.status = 'active'
-- Non-matching rows from A are filtered OUT
```

---

## 6. Subqueries

### Types of Subqueries

**1. Scalar Subquery** - Returns single value
```sql
SELECT name, salary,
    (SELECT AVG(salary) FROM employees) AS company_avg
FROM employees
```

**2. Row Subquery** - Returns single row
```sql
SELECT * FROM employees
WHERE (department_id, salary) = (
    SELECT department_id, MAX(salary)
    FROM employees 
    GROUP BY department_id
    LIMIT 1
)
```

**3. Table Subquery** - Returns multiple rows/columns
```sql
SELECT * FROM (
    SELECT department_id, COUNT(*) AS cnt
    FROM employees
    GROUP BY department_id
) AS dept_counts
WHERE cnt > 5
```

### Correlated vs Non-Correlated

**Non-correlated** - Runs once, independent of outer query
```sql
SELECT * FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)
-- Inner query runs ONCE
```

**Correlated** - References outer query, runs for each row
```sql
SELECT * FROM employees e
WHERE salary > (
    SELECT AVG(salary) FROM employees
    WHERE department_id = e.department_id  -- Reference to outer
)
-- Inner query runs ONCE PER ROW in outer query
```

### EXISTS vs IN

**IN** - Checks if value is in a list
```sql
WHERE customer_id IN (SELECT id FROM customers WHERE city = 'NYC')
```

**EXISTS** - Checks if subquery returns any rows
```sql
WHERE EXISTS (SELECT 1 FROM orders WHERE customer_id = c.id)
```

**When to use which:**
| Scenario | Best Choice |
|----------|-------------|
| Subquery returns few rows | IN |
| Subquery returns many rows | EXISTS |
| Checking for existence | EXISTS |
| Comparing specific values | IN |
| Outer table is small | EXISTS |
| Outer table is large | IN |

---

## 7. CTEs

### Basic CTE Syntax

```sql
WITH cte_name AS (
    SELECT columns
    FROM table
    WHERE conditions
)
SELECT * FROM cte_name;
```

### Benefits over Subqueries
1. **Readability** - Named, easier to understand
2. **Reusability** - Reference multiple times in same query
3. **Recursion** - Can self-reference
4. **Modularity** - Break complex queries into steps

### Chaining Multiple CTEs

```sql
WITH 
    step1 AS (
        SELECT customer_id, SUM(amount) AS total
        FROM orders GROUP BY customer_id
    ),
    step2 AS (
        SELECT customer_id, total,
            CASE WHEN total > 1000 THEN 'Gold'
                 WHEN total > 500 THEN 'Silver'
                 ELSE 'Bronze' END AS tier
        FROM step1
    )
SELECT c.name, s.total, s.tier
FROM step2 s
JOIN customers c ON s.customer_id = c.id;
```

### Recursive CTE

Structure:
```sql
WITH RECURSIVE cte_name AS (
    -- Base case (non-recursive)
    SELECT initial_columns
    FROM table
    WHERE starting_condition
    
    UNION ALL
    
    -- Recursive case
    SELECT next_columns
    FROM table
    JOIN cte_name ON join_condition
)
SELECT * FROM cte_name;
```

Example - Employee hierarchy:
```sql
WITH RECURSIVE hierarchy AS (
    SELECT id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL  -- Start with CEO
    
    UNION ALL
    
    SELECT e.id, e.name, e.manager_id, h.level + 1
    FROM employees e
    JOIN hierarchy h ON e.manager_id = h.id
)
SELECT * FROM hierarchy ORDER BY level;
```

---

## 8. Window Functions

### Syntax

```sql
function_name() OVER (
    [PARTITION BY columns]   -- Group rows (optional)
    [ORDER BY columns]       -- Order within partition
    [frame_clause]           -- Define window frame
)
```

### Ranking Functions

| Function | Ties | Gaps | Example (3 people tie for 2nd) |
|----------|------|------|-------------------------------|
| ROW_NUMBER() | No (always unique) | N/A | 1, 2, 3, 4, 5 |
| RANK() | Yes (same rank) | Yes | 1, 2, 2, 2, 5 |
| DENSE_RANK() | Yes (same rank) | No | 1, 2, 2, 2, 3 |
| NTILE(n) | Distributes into n buckets | N/A | 1, 1, 2, 2, 3 |

### Value Functions

| Function | Description |
|----------|-------------|
| LAG(col, n, default) | Value from n rows before |
| LEAD(col, n, default) | Value from n rows after |
| FIRST_VALUE(col) | First value in partition |
| LAST_VALUE(col) | Last value in partition |
| NTH_VALUE(col, n) | Nth value in partition |

### Aggregate as Window

```sql
-- Running total
SUM(amount) OVER (ORDER BY date)

-- Per-partition average
AVG(salary) OVER (PARTITION BY department_id)

-- Running count
COUNT(*) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING)
```

### Window Frame Clause

```sql
ROWS BETWEEN start AND end
RANGE BETWEEN start AND end
```

**Frame boundaries:**
- `UNBOUNDED PRECEDING` - First row of partition
- `n PRECEDING` - n rows before current
- `CURRENT ROW` - Current row
- `n FOLLOWING` - n rows after current
- `UNBOUNDED FOLLOWING` - Last row of partition

**Common frames:**
```sql
-- Default (cumulative from start)
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW

-- Moving average (3 rows)
ROWS BETWEEN 2 PRECEDING AND CURRENT ROW

-- Entire partition
ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
```

---

## 9. Transactions & ACID

### ACID Properties

| Property | Description | Example |
|----------|-------------|---------|
| **Atomicity** | All or nothing | Transfer: debit AND credit both happen |
| **Consistency** | Valid state after | Constraints not violated |
| **Isolation** | Concurrent safety | Two transfers don't interfere |
| **Durability** | Survives crashes | Committed data persists |

### Transaction Control

```sql
BEGIN;                    -- Start transaction
-- SQL statements
SAVEPOINT save1;          -- Create savepoint
-- More SQL statements
ROLLBACK TO save1;        -- Partial rollback
COMMIT;                   -- Make permanent

-- Or cancel everything
ROLLBACK;
```

### Isolation Levels

| Level | Dirty Read | Non-Repeat Read | Phantom |
|-------|------------|-----------------|---------|
| READ UNCOMMITTED | ✓ | ✓ | ✓ |
| READ COMMITTED | ✗ | ✓ | ✓ |
| REPEATABLE READ | ✗ | ✗ | ✓ |
| SERIALIZABLE | ✗ | ✗ | ✗ |

**Anomalies explained:**
- **Dirty Read**: Reading uncommitted changes from another transaction
- **Non-Repeatable Read**: Same query returns different results within transaction
- **Phantom Read**: New rows appear in repeated query (inserts by others)

```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN;
-- Your queries run with strictest isolation
COMMIT;
```

---

## 10. Indexing

### Index Types

| Type | Use Case | Structure |
|------|----------|-----------|
| B-tree | Default, most queries | Balanced tree |
| Hash | Equality only (=) | Hash table |
| GIN | Arrays, full-text | Inverted index |
| GiST | Geometric, range | Generalized tree |
| BRIN | Large sorted tables | Block ranges |

### Clustered vs Non-Clustered

**Clustered Index:**
- Data physically sorted by index
- ONE per table (usually primary key)
- Fast for range queries
- Slower to insert/update

**Non-Clustered Index:**
- Separate structure with pointers
- Multiple per table
- Extra lookup to get data
- Faster to insert/update

### Index Design Guidelines

**CREATE index when:**
- Column frequently in WHERE
- Column used in JOIN
- Column used in ORDER BY
- High selectivity (many unique values)

**AVOID index when:**
- Small tables
- Heavily updated columns
- Low selectivity (few unique values)
- Column rarely queried

### Composite Index

```sql
CREATE INDEX idx_name ON table(col1, col2, col3);
```

**Order matters!** Index on (A, B, C) helps:
- ✓ WHERE A = 1
- ✓ WHERE A = 1 AND B = 2
- ✓ WHERE A = 1 AND B = 2 AND C = 3
- ✗ WHERE B = 2 (A not used)
- ✗ WHERE C = 3 (A, B not used)

---

## 11. Query Optimization

### Common Anti-Patterns

```sql
-- ❌ SELECT * fetches unused columns
SELECT * FROM employees

-- ✓ Select only needed columns
SELECT name, salary FROM employees

-- ❌ Function on indexed column
WHERE YEAR(hire_date) = 2024

-- ✓ Range comparison
WHERE hire_date >= '2024-01-01' AND hire_date < '2025-01-01'

-- ❌ Leading wildcard
WHERE email LIKE '%@gmail.com'

-- ✓ Trailing wildcard (can use index)
WHERE email LIKE 'john%'

-- ❌ OR can prevent index use
WHERE department_id = 1 OR salary > 100000

-- ✓ UNION may be faster
SELECT * FROM emp WHERE department_id = 1
UNION ALL
SELECT * FROM emp WHERE salary > 100000 AND department_id <> 1
```

### Reading EXPLAIN

```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 1;
```

**Key things to look for:**
- **Seq Scan** - Full table scan (often bad)
- **Index Scan** - Using index (good)
- **Index Only Scan** - Data from index only (best)
- **Nested Loop** - For each row in A, scan B
- **Hash Join** - Build hash table, then probe
- **Merge Join** - Both inputs sorted, merge

---

## 12. Data Modeling

### Normal Forms (Detailed)

| Form | Rule | Example |
|------|------|---------|
| **1NF** | Atomic values, no repeating groups | `Phone1, Phone2` → Separate rows |
| **2NF** | 1NF + All non-key cols depend on FULL primary key | No partial dependencies in composite keys |
| **3NF** | 2NF + No transitive dependencies | No non-key col depends on another non-key col |
| **BCNF** | 3NF + Every determinant is a candidate key | Stricter version of 3NF for overlapping keys |

**Normalization vs Denormalization:**
- **Normalization:** Reduces redundancy, improves integrity, slower reads (more joins).
- **Denormalization:** Improves read speed, redundant data, risks integrity issues.

### Views

**Purpose:** A virtual table based on the result-set of an SQL statement.

```sql
-- Create a view
CREATE VIEW active_engineering_staff AS
SELECT name, email, hire_date
FROM employees
WHERE department_id = 1 AND status = 'active';

-- Use like a table
SELECT * FROM active_engineering_staff WHERE hire_date > '2022-01-01';

-- Update/Replace view
CREATE OR REPLACE VIEW active_engineering_staff AS ...;

-- Drop view
DROP VIEW active_engineering_staff;
```

**Benefits:**
- **Security:** Hide sensitive columns (like salary) from users.
- **Simplicity:** Simplify complex multi-table joins into a single "table".
- **Consistency:** Centralize logic (e.g., standard formula for "Total Revenue").

**Materialized Views (PostgreSQL/Oracle):**
- Physically stores the data.
- Faster reads but must be refreshed.
- `REFRESH MATERIALIZED VIEW view_name;`

### Star Schema (Data Warehouse)

```
           ┌─────────────┐
           │  dim_date   │
           └──────┬──────┘
                  │
┌──────────┐     │     ┌──────────────┐
│dim_product├────┼─────┤  FACT_SALES  │
└──────────┘     │     └──────────────┘
                  │            │
           ┌──────┴──────┐     │
           │dim_customer │     │
           └─────────────┘     │
                               │
                        ┌──────┴──────┐
                        │ dim_store   │
                        └─────────────┘
```

**Characteristics:**
- Central fact table with metrics
- Surrounding dimension tables
- Denormalized for query speed
- Simple star-like structure

### Snowflake Schema

Same as star, but dimensions are normalized:
```
dim_product → dim_category → dim_brand
```

**Trade-offs:**
| Star Schema | Snowflake Schema |
|-------------|------------------|
| Faster queries | Slower queries |
| More storage | Less storage |
| Simpler joins | More complex joins |
| Redundant data | Normalized data |

---

## 📚 Quick Reference Card

### Most Common Patterns

```sql
-- Top N per group
WITH ranked AS (
    SELECT *, DENSE_RANK() OVER (
        PARTITION BY group_col ORDER BY value_col DESC
    ) AS rn
    FROM table
)
SELECT * FROM ranked WHERE rn <= 3;

-- Running total
SELECT *, SUM(amount) OVER (
    ORDER BY date ROWS UNBOUNDED PRECEDING
) AS running_total
FROM orders;

-- YoY comparison
SELECT *,
    LAG(value, 12) OVER (ORDER BY month) AS prev_year,
    (value - LAG(value, 12) OVER (ORDER BY month)) / 
        LAG(value, 12) OVER (ORDER BY month) * 100 AS yoy_pct
FROM monthly_data;

-- Gaps and islands
SELECT *, 
    date - ROW_NUMBER() OVER (ORDER BY date) * INTERVAL '1 day' AS grp
FROM consecutive_dates;
```

---

*Use this reference alongside the practice problems in each daily file!*
