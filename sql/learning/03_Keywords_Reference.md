# 📚 Complete SQL Keywords Reference

Every SQL keyword explained with syntax, examples, and tips.

---

## 📋 Table of Contents

1. [SELECT Statement Keywords](#1-select-statement-keywords)
2. [Filtering Keywords](#2-filtering-keywords)
3. [Sorting & Limiting](#3-sorting--limiting)
4. [Aggregation Keywords](#4-aggregation-keywords)
5. [Join Keywords](#5-join-keywords)
6. [Subquery Keywords](#6-subquery-keywords)
7. [Set Operation Keywords](#7-set-operation-keywords)
8. [Data Modification Keywords](#8-data-modification-keywords)
9. [Table Definition Keywords](#9-table-definition-keywords)
10. [Constraint Keywords](#10-constraint-keywords)
11. [Transaction Keywords](#11-transaction-keywords)
12. [Conditional Keywords](#12-conditional-keywords)
13. [Null Handling Keywords](#13-null-handling-keywords)
14. [Date/Time Keywords](#14-datetime-keywords)
15. [String Keywords](#15-string-keywords)
16. [Window Function Keywords](#16-window-function-keywords)
17. [View Keywords](#17-view-keywords)

---

## 1. SELECT Statement Keywords

### SELECT
**Purpose:** Retrieve data from database tables.

```sql
-- Basic syntax
SELECT column1, column2 FROM table_name;

-- Select all columns
SELECT * FROM employees;

-- Select with alias
SELECT name AS employee_name, salary AS annual_salary FROM employees;

-- Select with expression
SELECT name, salary, salary * 12 AS annual_salary FROM employees;

-- Select with concatenation
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM employees;
```

**Tips:**
- Avoid `SELECT *` in production - specify needed columns only
- Use meaningful aliases for calculated columns
- Column order in SELECT determines output order

---

### FROM
**Purpose:** Specify the table(s) to query.

```sql
-- Single table
SELECT * FROM employees;

-- Multiple tables (implicit join - avoid this)
SELECT * FROM employees, departments;

-- With table alias
SELECT e.name, d.name 
FROM employees e, departments d
WHERE e.department_id = d.id;

-- Subquery as table
SELECT * FROM (SELECT * FROM employees WHERE salary > 50000) AS high_earners;
```

---

### AS (Alias)
**Purpose:** Rename columns or tables temporarily in query.

```sql
-- Column alias
SELECT name AS employee_name FROM employees;
SELECT name employee_name FROM employees;  -- AS is optional

-- Table alias
SELECT e.name, d.name
FROM employees AS e
JOIN departments AS d ON e.department_id = d.id;

-- Expression alias
SELECT salary * 12 AS annual_income FROM employees;
```

**When aliases are required:**
- Subqueries in FROM clause
- Self-joins
- When column names conflict

---

### DISTINCT
**Purpose:** Return only unique rows.

```sql
-- Unique values in one column
SELECT DISTINCT city FROM customers;

-- Unique combinations
SELECT DISTINCT city, status FROM orders;

-- Count distinct values
SELECT COUNT(DISTINCT city) AS unique_cities FROM customers;

-- DISTINCT ON (PostgreSQL only) - first row per group
SELECT DISTINCT ON (department_id) * 
FROM employees 
ORDER BY department_id, salary DESC;
```

**Performance tip:** DISTINCT can be slow on large datasets - consider if you really need it.

---

## 2. Filtering Keywords

### WHERE
**Purpose:** Filter rows based on conditions.

```sql
-- Basic comparison
SELECT * FROM employees WHERE salary > 50000;

-- Multiple conditions with AND
SELECT * FROM employees WHERE salary > 50000 AND department_id = 1;

-- OR condition
SELECT * FROM employees WHERE department_id = 1 OR department_id = 2;

-- Using parentheses for complex logic
SELECT * FROM employees 
WHERE (department_id = 1 OR department_id = 2) AND salary > 50000;
```

**Cannot use:** Aggregate functions, window functions, or SELECT aliases in WHERE.

---

### AND / OR / NOT
**Purpose:** Combine multiple conditions.

```sql
-- AND: Both conditions must be true
SELECT * FROM employees WHERE salary > 50000 AND hire_date > '2020-01-01';

-- OR: At least one condition must be true
SELECT * FROM employees WHERE department_id = 1 OR department_id = 2;

-- NOT: Negate a condition
SELECT * FROM employees WHERE NOT department_id = 1;
SELECT * FROM employees WHERE department_id != 1;  -- Same result

-- Complex combinations
SELECT * FROM employees 
WHERE NOT (salary < 50000 OR hire_date < '2020-01-01');
```

**Precedence:** NOT > AND > OR. Use parentheses to be explicit.

---

### IN / NOT IN
**Purpose:** Check if value is in a list.

```sql
-- List of values
SELECT * FROM employees WHERE department_id IN (1, 2, 3);

-- Equivalent to
SELECT * FROM employees 
WHERE department_id = 1 OR department_id = 2 OR department_id = 3;

-- NOT IN
SELECT * FROM employees WHERE department_id NOT IN (1, 2);

-- Subquery
SELECT * FROM employees 
WHERE department_id IN (SELECT id FROM departments WHERE location = 'NYC');
```

**Warning:** If subquery returns NULL, NOT IN returns no rows! Use NOT EXISTS instead.

---

### BETWEEN
**Purpose:** Check if value is within a range (inclusive).

```sql
-- Numeric range
SELECT * FROM products WHERE price BETWEEN 100 AND 500;

-- Equivalent to
SELECT * FROM products WHERE price >= 100 AND price <= 500;

-- Date range
SELECT * FROM orders WHERE order_date BETWEEN '2024-01-01' AND '2024-03-31';

-- NOT BETWEEN
SELECT * FROM products WHERE price NOT BETWEEN 100 AND 500;
```

**Note:** BETWEEN is inclusive on both ends.

---

### LIKE / ILIKE
**Purpose:** Pattern matching in strings.

```sql
-- % matches any sequence of characters
SELECT * FROM customers WHERE name LIKE 'John%';      -- Starts with John
SELECT * FROM customers WHERE name LIKE '%Smith';     -- Ends with Smith
SELECT * FROM customers WHERE name LIKE '%Corp%';     -- Contains Corp

-- _ matches exactly one character
SELECT * FROM products WHERE code LIKE 'A_B';         -- A followed by any char, then B
SELECT * FROM employees WHERE phone LIKE '555-___-____';

-- ILIKE for case-insensitive (PostgreSQL)
SELECT * FROM customers WHERE name ILIKE 'john%';

-- MySQL case-insensitive
SELECT * FROM customers WHERE LOWER(name) LIKE 'john%';

-- Escape special characters
SELECT * FROM products WHERE name LIKE '%50\%%' ESCAPE '\';  -- Contains 50%
```

**Performance:** Leading wildcard `LIKE '%value'` cannot use indexes - avoid if possible.

---

### IS NULL / IS NOT NULL
**Purpose:** Check for NULL values.

```sql
-- Find NULL values
SELECT * FROM employees WHERE manager_id IS NULL;

-- Find non-NULL values
SELECT * FROM employees WHERE manager_id IS NOT NULL;

-- WRONG: This doesn't work!
SELECT * FROM employees WHERE manager_id = NULL;      -- Returns nothing
SELECT * FROM employees WHERE manager_id != NULL;     -- Returns nothing
```

**Why = NULL fails:** NULL represents unknown. Comparing anything to unknown is unknown.

---

### EXISTS / NOT EXISTS
**Purpose:** Check if subquery returns any rows.

```sql
-- Customers who have orders
SELECT * FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.id
);

-- Customers who never ordered
SELECT * FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.id
);

-- Employees with subordinates
SELECT * FROM employees e
WHERE EXISTS (
    SELECT 1 FROM employees sub WHERE sub.manager_id = e.id
);
```

**EXISTS vs IN:**
- EXISTS: Better for large subquery results
- EXISTS: Handles NULLs correctly
- IN: Better for small, static value lists

---

### ANY / SOME / ALL
**Purpose:** Compare value to set of values.

```sql
-- ANY: True if comparison is true for at least one value
SELECT * FROM employees 
WHERE salary > ANY (SELECT salary FROM employees WHERE department_id = 1);

-- SOME: Same as ANY
SELECT * FROM products WHERE price = SOME (SELECT price FROM featured_products);

-- ALL: True if comparison is true for all values
SELECT * FROM employees 
WHERE salary > ALL (SELECT salary FROM employees WHERE department_id = 2);
-- Returns employees earning more than EVERYONE in dept 2
```

---

## 3. Sorting & Limiting

### ORDER BY
**Purpose:** Sort query results.

```sql
-- Ascending (default)
SELECT * FROM employees ORDER BY salary;
SELECT * FROM employees ORDER BY salary ASC;

-- Descending
SELECT * FROM employees ORDER BY salary DESC;

-- Multiple columns
SELECT * FROM employees ORDER BY department_id ASC, salary DESC;

-- By column position (not recommended)
SELECT name, salary FROM employees ORDER BY 2 DESC;

-- By expression
SELECT name, salary FROM employees ORDER BY salary * 12 DESC;

-- NULL handling
SELECT * FROM employees ORDER BY manager_id NULLS FIRST;  -- PostgreSQL
SELECT * FROM employees ORDER BY manager_id NULLS LAST;   -- PostgreSQL
SELECT * FROM employees ORDER BY COALESCE(manager_id, 0); -- Standard
```

**Note:** ORDER BY runs after SELECT, so aliases work here.

---

### LIMIT
**Purpose:** Restrict number of rows returned.

```sql
-- First N rows
SELECT * FROM employees ORDER BY salary DESC LIMIT 10;

-- MySQL/PostgreSQL syntax
SELECT * FROM employees LIMIT 10;

-- SQL Server syntax (TOP)
SELECT TOP 10 * FROM employees ORDER BY salary DESC;

-- Oracle syntax (FETCH)
SELECT * FROM employees ORDER BY salary DESC FETCH FIRST 10 ROWS ONLY;
```

---

### OFFSET
**Purpose:** Skip rows before returning results (pagination).

```sql
-- Skip first 20, return next 10
SELECT * FROM employees ORDER BY id LIMIT 10 OFFSET 20;

-- SQL Server
SELECT * FROM employees ORDER BY id OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY;

-- Pagination formula: Page N, Size S
-- LIMIT S OFFSET (N-1)*S
-- Page 3, 10 per page: LIMIT 10 OFFSET 20
```

**Performance warning:** Large OFFSET values are slow. Consider keyset pagination instead.

---

## 4. Aggregation Keywords

### GROUP BY
**Purpose:** Group rows for aggregation.

```sql
-- Count per department
SELECT department_id, COUNT(*) AS count
FROM employees
GROUP BY department_id;

-- Multiple grouping columns
SELECT department_id, EXTRACT(YEAR FROM hire_date) AS year, COUNT(*)
FROM employees
GROUP BY department_id, EXTRACT(YEAR FROM hire_date);

-- GROUP BY with expression
SELECT DATE_TRUNC('month', order_date) AS month, SUM(amount)
FROM orders
GROUP BY DATE_TRUNC('month', order_date);
```

**Rule:** Every non-aggregated column in SELECT must be in GROUP BY.

---

### HAVING
**Purpose:** Filter groups after aggregation.

```sql
-- Departments with more than 5 employees
SELECT department_id, COUNT(*) AS count
FROM employees
GROUP BY department_id
HAVING COUNT(*) > 5;

-- Multiple conditions
SELECT department_id, AVG(salary) AS avg_sal
FROM employees
GROUP BY department_id
HAVING COUNT(*) > 3 AND AVG(salary) > 50000;

-- Using alias in HAVING (MySQL allows, others don't)
SELECT department_id, COUNT(*) AS cnt
FROM employees
GROUP BY department_id
HAVING cnt > 5;  -- May not work in PostgreSQL
```

**WHERE vs HAVING:**
- WHERE: Filters rows BEFORE grouping
- HAVING: Filters groups AFTER aggregation
- WHERE cannot use aggregate functions
- HAVING can use aggregate functions

---

### COUNT
**Purpose:** Count rows.

```sql
-- Count all rows
SELECT COUNT(*) FROM employees;

-- Count non-NULL values in column
SELECT COUNT(manager_id) FROM employees;  -- Excludes NULLs

-- Count distinct values
SELECT COUNT(DISTINCT department_id) FROM employees;

-- Count with condition
SELECT COUNT(CASE WHEN salary > 50000 THEN 1 END) AS high_earners
FROM employees;
```

---

### SUM / AVG / MIN / MAX
**Purpose:** Aggregate numeric calculations.

```sql
SELECT 
    SUM(salary) AS total_payroll,
    AVG(salary) AS avg_salary,
    MIN(salary) AS min_salary,
    MAX(salary) AS max_salary
FROM employees;

-- With GROUP BY
SELECT 
    department_id,
    SUM(salary) AS dept_total,
    ROUND(AVG(salary), 2) AS dept_avg
FROM employees
GROUP BY department_id;

-- MIN/MAX on dates and strings
SELECT MIN(hire_date) AS first_hire, MAX(hire_date) AS last_hire FROM employees;
SELECT MIN(name) AS first_alphabetically FROM employees;
```

**Note:** All aggregate functions ignore NULL values (except COUNT(*)).

---

## 5. Join Keywords

### INNER JOIN / JOIN
**Purpose:** Return matching rows from both tables.

```sql
-- Explicit INNER JOIN
SELECT e.name, d.name AS department
FROM employees e
INNER JOIN departments d ON e.department_id = d.id;

-- JOIN is short for INNER JOIN
SELECT e.name, d.name AS department
FROM employees e
JOIN departments d ON e.department_id = d.id;

-- Multiple join conditions
SELECT *
FROM orders o
JOIN order_items oi ON o.id = oi.order_id AND o.status = 'active';
```

---

### LEFT JOIN / LEFT OUTER JOIN
**Purpose:** Return all rows from left table, matched rows from right.

```sql
-- All employees, even those without department
SELECT e.name, d.name AS department
FROM employees e
LEFT JOIN departments d ON e.department_id = d.id;

-- Find unmatched (employees without department)
SELECT e.name
FROM employees e
LEFT JOIN departments d ON e.department_id = d.id
WHERE d.id IS NULL;
```

---

### RIGHT JOIN / RIGHT OUTER JOIN
**Purpose:** Return all rows from right table, matched rows from left.

```sql
-- All departments, even empty ones
SELECT e.name, d.name AS department
FROM employees e
RIGHT JOIN departments d ON e.department_id = d.id;
```

**Tip:** RIGHT JOIN can always be rewritten as LEFT JOIN by swapping tables.

---

### FULL OUTER JOIN
**Purpose:** Return all rows from both tables.

```sql
SELECT e.name, d.name
FROM employees e
FULL OUTER JOIN departments d ON e.department_id = d.id;

-- MySQL doesn't support FULL OUTER JOIN - use UNION
SELECT e.name, d.name FROM employees e LEFT JOIN departments d ON e.department_id = d.id
UNION
SELECT e.name, d.name FROM employees e RIGHT JOIN departments d ON e.department_id = d.id;
```

---

### CROSS JOIN
**Purpose:** Cartesian product - every row with every row.

```sql
-- All combinations
SELECT e.name, p.name AS project
FROM employees e
CROSS JOIN projects p;

-- Implicit cross join
SELECT e.name, p.name FROM employees e, projects p;

-- Useful for generating combinations
SELECT dates.d, statuses.s
FROM (SELECT generate_series('2024-01-01'::date, '2024-01-07', '1 day') AS d) dates
CROSS JOIN (VALUES ('pending'), ('completed'), ('shipped')) AS statuses(s);
```

---

### SELF JOIN
**Purpose:** Join table to itself.

```sql
-- Employee with manager
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;

-- Find colleagues (same department)
SELECT e1.name, e2.name AS colleague
FROM employees e1
JOIN employees e2 ON e1.department_id = e2.department_id
WHERE e1.id < e2.id;  -- Avoid duplicates
```

---

### NATURAL JOIN
**Purpose:** Join on columns with same name (avoid this).

```sql
-- Joins on all matching column names
SELECT * FROM employees NATURAL JOIN departments;

-- Equivalent to (assuming common column is department_id)
SELECT * FROM employees e JOIN departments d ON e.department_id = d.department_id;
```

**Warning:** NATURAL JOIN is dangerous - column changes can break queries silently.

---

### USING
**Purpose:** Simplified join when columns have same name.

```sql
-- Instead of ON e.department_id = d.department_id
SELECT * FROM employees e JOIN departments d USING (department_id);

-- Multiple columns
SELECT * FROM orders o JOIN order_items oi USING (order_id, product_id);
```

---

## 6. Subquery Keywords

### WITH (CTE - Common Table Expression)
**Purpose:** Define named temporary result sets.

```sql
-- Single CTE
WITH high_earners AS (
    SELECT * FROM employees WHERE salary > 100000
)
SELECT * FROM high_earners;

-- Multiple CTEs
WITH 
    dept_counts AS (
        SELECT department_id, COUNT(*) AS cnt FROM employees GROUP BY department_id
    ),
    large_depts AS (
        SELECT department_id FROM dept_counts WHERE cnt > 5
    )
SELECT e.* FROM employees e WHERE e.department_id IN (SELECT department_id FROM large_depts);

-- CTE referencing previous CTE
WITH 
    step1 AS (SELECT * FROM orders WHERE status = 'completed'),
    step2 AS (SELECT customer_id, SUM(amount) AS total FROM step1 GROUP BY customer_id)
SELECT * FROM step2 WHERE total > 1000;
```

---

### WITH RECURSIVE
**Purpose:** Self-referencing CTE for hierarchies and series.

```sql
-- Generate number series
WITH RECURSIVE nums AS (
    SELECT 1 AS n              -- Base case
    UNION ALL
    SELECT n + 1 FROM nums WHERE n < 10  -- Recursive case
)
SELECT * FROM nums;

-- Organization hierarchy
WITH RECURSIVE org_chart AS (
    -- Base: top-level (no manager)
    SELECT id, name, manager_id, 1 AS level
    FROM employees WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive: employees reporting to previous level
    SELECT e.id, e.name, e.manager_id, oc.level + 1
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.id
)
SELECT * FROM org_chart ORDER BY level, name;
```

---

## 7. Set Operation Keywords

### UNION
**Purpose:** Combine results, remove duplicates.

```sql
SELECT name FROM employees
UNION
SELECT name FROM customers;
```

### UNION ALL
**Purpose:** Combine results, keep duplicates.

```sql
SELECT name, 'Employee' AS type FROM employees
UNION ALL
SELECT name, 'Customer' AS type FROM customers;
```

**UNION ALL is faster** - no deduplication overhead.

---

### INTERSECT
**Purpose:** Rows that exist in both queries.

```sql
-- Customers who are also employees
SELECT name FROM customers
INTERSECT
SELECT name FROM employees;
```

---

### EXCEPT / MINUS
**Purpose:** Rows in first query but not in second.

```sql
-- Customers who are not employees
SELECT name FROM customers
EXCEPT
SELECT name FROM employees;

-- Oracle uses MINUS instead of EXCEPT
SELECT name FROM customers
MINUS
SELECT name FROM employees;
```

---

## 8. Data Modification Keywords

### INSERT
**Purpose:** Add new rows.

```sql
-- Insert single row
INSERT INTO employees (name, email, salary) VALUES ('John', 'john@co.com', 50000);

-- Insert multiple rows
INSERT INTO employees (name, email, salary) VALUES 
    ('Alice', 'alice@co.com', 55000),
    ('Bob', 'bob@co.com', 60000);

-- Insert from SELECT
INSERT INTO employee_archive SELECT * FROM employees WHERE status = 'inactive';

-- Insert with RETURNING (PostgreSQL)
INSERT INTO employees (name, salary) VALUES ('Jane', 70000) RETURNING id;
```

---

### UPDATE
**Purpose:** Modify existing rows.

```sql
-- Update single column
UPDATE employees SET salary = 55000 WHERE id = 1;

-- Update multiple columns
UPDATE employees SET salary = 55000, department_id = 2 WHERE id = 1;

-- Update with calculation
UPDATE employees SET salary = salary * 1.10 WHERE department_id = 1;

-- Update with subquery
UPDATE employees SET salary = (
    SELECT AVG(salary) FROM employees
) WHERE department_id = 2;

-- Update with JOIN (PostgreSQL)
UPDATE employees e
SET salary = e.salary * 1.05
FROM departments d
WHERE e.department_id = d.id AND d.name = 'Engineering';
```

**Safety tip:** Always use WHERE clause! Run SELECT first to verify affected rows.

---

### DELETE
**Purpose:** Remove rows.

```sql
-- Delete specific rows
DELETE FROM employees WHERE id = 1;

-- Delete with condition
DELETE FROM orders WHERE order_date < '2020-01-01';

-- Delete with subquery
DELETE FROM employees WHERE department_id IN (
    SELECT id FROM departments WHERE location = 'Closed Office'
);

-- Delete all rows (but keep table structure)
DELETE FROM temp_data;
```

**Safety tip:** Always use WHERE clause! Consider using transaction for safety.

---

### TRUNCATE
**Purpose:** Remove all rows quickly.

```sql
-- Fast delete all rows
TRUNCATE TABLE temp_data;

-- Reset identity/serial counter
TRUNCATE TABLE temp_data RESTART IDENTITY;

-- Multiple tables
TRUNCATE TABLE table1, table2;
```

**DELETE vs TRUNCATE:**
| Feature | DELETE | TRUNCATE |
|---------|--------|----------|
| WHERE clause | Yes | No |
| Can rollback | Yes (logged) | Depends on DB |
| Speed | Slow (row by row) | Fast |
| Triggers | Fires | Usually not |
| Reset identity | No | Yes |

---

### MERGE / UPSERT
**Purpose:** Insert or update based on condition.

```sql
-- PostgreSQL: INSERT ON CONFLICT
INSERT INTO employees (id, name, salary) VALUES (1, 'John', 50000)
ON CONFLICT (id) DO UPDATE SET salary = EXCLUDED.salary;

-- SQL Server: MERGE
MERGE INTO employees AS target
USING new_employees AS source
ON target.id = source.id
WHEN MATCHED THEN UPDATE SET salary = source.salary
WHEN NOT MATCHED THEN INSERT (id, name, salary) VALUES (source.id, source.name, source.salary);

-- MySQL: INSERT ON DUPLICATE KEY
INSERT INTO employees (id, name, salary) VALUES (1, 'John', 50000)
ON DUPLICATE KEY UPDATE salary = VALUES(salary);
```

---

## 9. Table Definition Keywords

### CREATE TABLE
**Purpose:** Define new table structure.

```sql
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    department_id INT REFERENCES departments(id),
    salary DECIMAL(10,2) CHECK (salary > 0),
    hire_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'active'
);
```

---

### ALTER TABLE
**Purpose:** Modify table structure.

```sql
-- Add column
ALTER TABLE employees ADD COLUMN phone VARCHAR(20);

-- Drop column
ALTER TABLE employees DROP COLUMN phone;

-- Rename column
ALTER TABLE employees RENAME COLUMN name TO full_name;

-- Change data type
ALTER TABLE employees ALTER COLUMN salary TYPE NUMERIC(12,2);

-- Add constraint
ALTER TABLE employees ADD CONSTRAINT chk_salary CHECK (salary > 0);

-- Drop constraint
ALTER TABLE employees DROP CONSTRAINT chk_salary;

-- Rename table
ALTER TABLE employees RENAME TO staff;
```

---

### DROP TABLE
**Purpose:** Delete table entirely.

```sql
-- Delete table (error if doesn't exist)
DROP TABLE temp_data;

-- Delete if exists (no error)
DROP TABLE IF EXISTS temp_data;

-- Delete with dependent objects
DROP TABLE departments CASCADE;  -- Drops related foreign keys too
```

---

## 10. Constraint Keywords

### PRIMARY KEY
**Purpose:** Unique identifier for rows.

```sql
-- Inline definition
CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100));

-- Named constraint
CREATE TABLE users (
    id INT,
    name VARCHAR(100),
    CONSTRAINT pk_users PRIMARY KEY (id)
);

-- Composite primary key
CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    PRIMARY KEY (order_id, product_id)
);
```

---

### FOREIGN KEY / REFERENCES
**Purpose:** Enforce referential integrity.

```sql
-- Inline
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(id)
);

-- Named with actions
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT,
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) 
        REFERENCES customers(id) ON DELETE CASCADE ON UPDATE CASCADE
);
```

---

### UNIQUE
**Purpose:** Prevent duplicate values.

```sql
-- Single column
CREATE TABLE users (email VARCHAR(255) UNIQUE);

-- Multiple columns (composite unique)
CREATE TABLE assignments (
    employee_id INT,
    project_id INT,
    UNIQUE (employee_id, project_id)
);
```

---

### CHECK
**Purpose:** Validate data with custom rules.

```sql
CREATE TABLE products (
    id INT PRIMARY KEY,
    price DECIMAL(10,2) CHECK (price > 0),
    quantity INT CHECK (quantity >= 0),
    discount DECIMAL(3,2) CHECK (discount BETWEEN 0 AND 1)
);
```

---

### DEFAULT
**Purpose:** Auto-fill value when not provided.

```sql
CREATE TABLE orders (
    id INT PRIMARY KEY,
    order_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

### NOT NULL
**Purpose:** Require a value (no NULLs).

```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);
```

---

## 11. Transaction Keywords

### BEGIN / START TRANSACTION
**Purpose:** Start a transaction block.

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

---

### COMMIT
**Purpose:** Make all changes permanent.

```sql
BEGIN;
INSERT INTO orders (customer_id, amount) VALUES (1, 100);
COMMIT;  -- Changes are now permanent
```

---

### ROLLBACK
**Purpose:** Undo all changes since BEGIN.

```sql
BEGIN;
DELETE FROM employees;  -- Oops!
ROLLBACK;  -- Phew, nothing deleted
```

---

### SAVEPOINT
**Purpose:** Create restore point within transaction.

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
SAVEPOINT after_debit;

UPDATE accounts SET balance = balance + 100 WHERE id = 999;  -- This might fail
ROLLBACK TO SAVEPOINT after_debit;  -- Undo only the second update

UPDATE accounts SET balance = balance + 100 WHERE id = 2;  -- Try different account
COMMIT;
```

---

### SET TRANSACTION
**Purpose:** Configure transaction properties.

```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SET TRANSACTION READ ONLY;
```

---

## 12. Conditional Keywords

### CASE
**Purpose:** Conditional logic in SQL.

```sql
-- Simple CASE
SELECT name,
    CASE department_id
        WHEN 1 THEN 'Engineering'
        WHEN 2 THEN 'Sales'
        ELSE 'Other'
    END AS department
FROM employees;

-- Searched CASE
SELECT name, salary,
    CASE 
        WHEN salary < 50000 THEN 'Low'
        WHEN salary < 100000 THEN 'Medium'
        ELSE 'High'
    END AS salary_band
FROM employees;

-- CASE in ORDER BY
SELECT * FROM orders
ORDER BY CASE status
    WHEN 'urgent' THEN 1
    WHEN 'pending' THEN 2
    ELSE 3
END;
```

---

### COALESCE
**Purpose:** Return first non-NULL value.

```sql
-- Use default when NULL
SELECT COALESCE(phone, email, 'No contact') AS contact FROM customers;

-- Use in calculations
SELECT name, COALESCE(bonus, 0) + salary AS total_comp FROM employees;
```

---

### NULLIF
**Purpose:** Return NULL if values are equal.

```sql
-- Avoid division by zero
SELECT revenue / NULLIF(units, 0) AS price_per_unit FROM products;

-- Returns NULL instead of error when units = 0
```

---

### IIF (SQL Server) / IF (MySQL)
**Purpose:** Simple if-else.

```sql
-- SQL Server
SELECT name, IIF(salary > 50000, 'High', 'Low') AS level FROM employees;

-- MySQL
SELECT name, IF(salary > 50000, 'High', 'Low') AS level FROM employees;
```

---

## 13. Null Handling Keywords

### IS NULL
```sql
SELECT * FROM employees WHERE manager_id IS NULL;
```

### IS NOT NULL
```sql
SELECT * FROM employees WHERE manager_id IS NOT NULL;
```

### COALESCE
```sql
SELECT COALESCE(nickname, first_name) AS display_name FROM users;
```

### NULLIF
```sql
SELECT amount / NULLIF(quantity, 0) AS unit_price FROM items;
```

### IFNULL (MySQL) / ISNULL (SQL Server)
```sql
-- MySQL
SELECT IFNULL(phone, 'N/A') FROM customers;

-- SQL Server
SELECT ISNULL(phone, 'N/A') FROM customers;
```

---

## 14. Date/Time Keywords

### CURRENT_DATE / CURRENT_TIME / CURRENT_TIMESTAMP
```sql
SELECT CURRENT_DATE;                -- 2024-01-15
SELECT CURRENT_TIME;                -- 14:30:00
SELECT CURRENT_TIMESTAMP;           -- 2024-01-15 14:30:00
SELECT NOW();                       -- Same as CURRENT_TIMESTAMP
```

### EXTRACT
```sql
SELECT EXTRACT(YEAR FROM order_date) AS year,
       EXTRACT(MONTH FROM order_date) AS month,
       EXTRACT(DAY FROM order_date) AS day,
       EXTRACT(DOW FROM order_date) AS day_of_week,
       EXTRACT(QUARTER FROM order_date) AS quarter
FROM orders;
```

### DATE_TRUNC (PostgreSQL)
```sql
SELECT DATE_TRUNC('month', order_date) AS month_start FROM orders;
SELECT DATE_TRUNC('year', order_date) AS year_start FROM orders;
```

### DATE_ADD / DATE_SUB (MySQL)
```sql
SELECT DATE_ADD(order_date, INTERVAL 7 DAY) FROM orders;
SELECT DATE_SUB(order_date, INTERVAL 1 MONTH) FROM orders;
```

### DATEDIFF
```sql
-- MySQL: Returns days
SELECT DATEDIFF(end_date, start_date) FROM projects;

-- SQL Server: Specify unit
SELECT DATEDIFF(day, start_date, end_date) FROM projects;
SELECT DATEDIFF(month, start_date, end_date) FROM projects;
```

### TO_CHAR / DATE_FORMAT
```sql
-- PostgreSQL
SELECT TO_CHAR(order_date, 'YYYY-MM-DD') FROM orders;
SELECT TO_CHAR(order_date, 'Month DD, YYYY') FROM orders;

-- MySQL
SELECT DATE_FORMAT(order_date, '%Y-%m-%d') FROM orders;
```

### INTERVAL
```sql
-- PostgreSQL
SELECT order_date + INTERVAL '7 days' FROM orders;
SELECT order_date - INTERVAL '1 month' FROM orders;

-- MySQL
SELECT order_date + INTERVAL 7 DAY FROM orders;
```

---

## 15. String Keywords

### CONCAT / ||
```sql
SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM employees;
SELECT first_name || ' ' || last_name AS full_name FROM employees;  -- PostgreSQL
```

### SUBSTRING / SUBSTR
```sql
SELECT SUBSTRING(name FROM 1 FOR 3) FROM employees;  -- PostgreSQL
SELECT SUBSTRING(name, 1, 3) FROM employees;         -- MySQL
SELECT SUBSTR(name, 1, 3) FROM employees;            -- Oracle
```

### LENGTH / LEN
```sql
SELECT LENGTH(name) FROM employees;  -- PostgreSQL, MySQL
SELECT LEN(name) FROM employees;     -- SQL Server
```

### UPPER / LOWER / INITCAP
```sql
SELECT UPPER(name), LOWER(name), INITCAP(name) FROM employees;
```

### TRIM / LTRIM / RTRIM
```sql
SELECT TRIM('  hello  ');     -- 'hello'
SELECT LTRIM('  hello');      -- 'hello'
SELECT RTRIM('hello  ');      -- 'hello'
SELECT TRIM(BOTH 'x' FROM 'xxxhelloxxx');  -- 'hello'
```

### REPLACE
```sql
SELECT REPLACE(email, '@old.com', '@new.com') FROM employees;
```

### POSITION / INSTR / CHARINDEX
```sql
SELECT POSITION('@' IN email) FROM employees;   -- PostgreSQL
SELECT INSTR(email, '@') FROM employees;        -- MySQL
SELECT CHARINDEX('@', email) FROM employees;    -- SQL Server
```

### SPLIT_PART (PostgreSQL)
```sql
SELECT SPLIT_PART(email, '@', 2) AS domain FROM employees;  -- Gets domain
```

### REVERSE
```sql
SELECT REVERSE('hello');  -- 'olleh'
```

### LEFT / RIGHT
```sql
SELECT LEFT(name, 3) FROM employees;   -- First 3 chars
SELECT RIGHT(name, 3) FROM employees;  -- Last 3 chars
```

### LPAD / RPAD
```sql
SELECT LPAD(id::text, 5, '0') FROM employees;  -- '00001', '00002'
SELECT RPAD(name, 20, '.') FROM employees;     -- 'John................'
```

---

## 16. Window Function Keywords

### OVER
```sql
SELECT name, salary,
    AVG(salary) OVER () AS overall_avg,
    AVG(salary) OVER (PARTITION BY department_id) AS dept_avg
FROM employees;
```

### PARTITION BY
```sql
SELECT name, department_id, salary,
    RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dept_rank
FROM employees;
```

### ROW_NUMBER
```sql
SELECT ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num, name, salary
FROM employees;
```

### RANK / DENSE_RANK
```sql
SELECT name, salary,
    RANK() OVER (ORDER BY salary DESC) AS rank,        -- 1,2,2,4
    DENSE_RANK() OVER (ORDER BY salary DESC) AS dense  -- 1,2,2,3
FROM employees;
```

### NTILE
```sql
SELECT name, salary,
    NTILE(4) OVER (ORDER BY salary) AS quartile
FROM employees;
```

### LAG / LEAD
```sql
SELECT name, salary,
    LAG(salary) OVER (ORDER BY hire_date) AS prev_salary,
    LEAD(salary) OVER (ORDER BY hire_date) AS next_salary
FROM employees;
```

### FIRST_VALUE / LAST_VALUE
```sql
SELECT name, salary,
    FIRST_VALUE(salary) OVER (PARTITION BY department_id ORDER BY salary) AS min_salary,
    LAST_VALUE(salary) OVER (
        PARTITION BY department_id ORDER BY salary 
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS max_salary
FROM employees;
```

### ROWS BETWEEN / RANGE BETWEEN
```sql
-- Running total
SUM(amount) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING)

-- Moving average (last 3 rows)
AVG(amount) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)

-- Surrounding rows
AVG(amount) OVER (ORDER BY date ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)
```

---

## 17. View Keywords

### CREATE VIEW
**Purpose:** Create a virtual table based on a query.

```sql
CREATE VIEW high_salary_employees AS
SELECT name, department_id, salary
FROM employees
WHERE salary > 100000;

-- Query the view
SELECT * FROM high_salary_employees;
```

### CREATE OR REPLACE VIEW
**Purpose:** Update an existing view definition.

```sql
CREATE OR REPLACE VIEW high_salary_employees AS
SELECT name, department_id, salary, email
FROM employees
WHERE salary > 100000;
```

### DROP VIEW
**Purpose:** Remove a view.

```sql
DROP VIEW IF EXISTS high_salary_employees;
```

### MATERIALIZED VIEW (PostgreSQL/Oracle)
**Purpose:** Create a physical copy of view data for performance.

```sql
-- Create
CREATE MATERIALIZED VIEW sales_summary AS
SELECT product_id, SUM(amount) AS total_revenue
FROM order_items
GROUP BY product_id;

-- Refresh (required to see data changes)
REFRESH MATERIALIZED VIEW sales_summary;
```

---

*This reference covers all major SQL keywords with practical examples!*
