# 📋 SQL Interview Cheatsheet

Quick reference for interviews - print this!

---

## 🔑 Query Execution Order
```
FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```

---

## 📊 Aggregate Functions

| Function | NULL Handling |
|----------|---------------|
| COUNT(*) | Counts NULLs |
| COUNT(col) | Ignores NULLs |
| SUM/AVG/MIN/MAX | Ignore NULLs |

---

## 🔗 Joins

| Type | Result |
|------|--------|
| INNER | Only matches |
| LEFT | All left + matches |
| RIGHT | All right + matches |
| FULL | All from both |
| CROSS | Cartesian product |

---

## 🏆 Ranking Functions

| Function | With Ties (2 people tie for 2nd) |
|----------|----------------------------------|
| ROW_NUMBER | 1, 2, 3, 4 (always unique) |
| RANK | 1, 2, 2, 4 (skip after tie) |
| DENSE_RANK | 1, 2, 2, 3 (no skip) |

---

## 🪟 Window Function Syntax

```sql
function() OVER (
    PARTITION BY col  -- Groups
    ORDER BY col      -- Order within group
    ROWS BETWEEN x AND y  -- Frame
)
```

**Common frames:**
- `ROWS UNBOUNDED PRECEDING` - Running total
- `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` - Moving avg (3)

---

## 🔄 CTE Syntax

```sql
WITH cte_name AS (
    SELECT ... FROM ...
)
SELECT * FROM cte_name;
```

**Recursive:**
```sql
WITH RECURSIVE cte AS (
    SELECT ... WHERE start_condition  -- Base
    UNION ALL
    SELECT ... FROM cte WHERE continue_condition  -- Recurse
)
```

---

## 📈 Index Tips

**Create when:**
- Column in WHERE/JOIN often
- High cardinality

**Avoid when:**
- Small tables
- Frequently updated columns
- Low cardinality

**Composite index (A, B, C) helps:**
- ✅ WHERE A = ?
- ✅ WHERE A = ? AND B = ?
- ❌ WHERE B = ? (needs A first)

---

## ⚡ Query Anti-Patterns

```sql
-- ❌ Avoid
SELECT * FROM table
WHERE YEAR(date) = 2024
WHERE col LIKE '%value'

-- ✅ Better
SELECT col1, col2 FROM table
WHERE date >= '2024-01-01' AND date < '2025-01-01'
WHERE col LIKE 'value%'
```

---

## 🔐 Isolation Levels

| Level | Dirty Read | Phantom |
|-------|------------|---------|
| READ UNCOMMITTED | Yes | Yes |
| READ COMMITTED | No | Yes |
| REPEATABLE READ | No | Yes |
| SERIALIZABLE | No | No |

---

## 🧩 Common Patterns

**Top N per group:**
```sql
WITH ranked AS (
    SELECT *, DENSE_RANK() OVER (
        PARTITION BY group_col ORDER BY value DESC
    ) AS rn FROM table
)
SELECT * FROM ranked WHERE rn <= 3;
```

**Running total:**
```sql
SUM(amount) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING)
```

**Year-over-year:**
```sql
LAG(value, 12) OVER (ORDER BY month) AS prev_year
```

---

*Good luck! 🎯*
