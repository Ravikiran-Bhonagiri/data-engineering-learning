# 🗝️ Solutions: Advanced Practice Bank (100 Problems)

This file contains optimized SQL solutions for the 100 advanced practice problems.

---

## 🗺️ Table of Contents
1. [Part 1: Complex Joins & Aggregations (1-25)](#-solutions-part-1-problems-1-25-joins--aggregations)
2. [Part 2: Window Functions Deep Dive (26-50)](#-solutions-part-2-problems-26-50-window-functions)
3. [Part 3: Advanced CTEs & Recursion (51-70)](#-solutions-part-3-problems-51-70-ctes--recursion)
4. [Part 4: Data Analysis & Business Logic (71-85)](#-solutions-part-4-problems-71-85-data-analysis)
5. [Part 5: Query Optimization & Performance (86-100)](#-solutions-part-5-problems-86-100-optimization)

---

## 🔗 Solutions: Part 1 (Problems 1-25: Joins & Aggregations)

### 1. Self-Join Growth
```sql
SELECT e.name, e.salary, d.name AS department
FROM employees e
JOIN employees m ON e.manager_id = m.id
JOIN departments d ON e.department_id = d.id
WHERE e.salary > m.salary
  AND e.salary > (
      SELECT AVG(salary) 
      FROM employees 
      WHERE department_id = e.department_id
  );
```

### 2. Missing Dimensions
```sql
SELECT d.name AS department, p.name AS product, COALESCE(SUM(oi.quantity), 0) AS total_sold
FROM departments d
CROSS JOIN products p
LEFT JOIN employees e ON e.department_id = d.id
LEFT JOIN orders o ON o.customer_id IS NOT NULL -- This is complex due to schema
-- Correct approach for sales:
SELECT d.name, p.name, COALESCE(SUM(oi.quantity), 0)
FROM departments d
CROSS JOIN products p
LEFT JOIN employees e ON d.id = e.department_id
LEFT JOIN orders o ON 1=1 -- Logic depends on specific business goal
-- Simplified:
SELECT d.name, p.name, COALESCE(SUM(oi.quantity), 0)
FROM departments d
CROSS JOIN products p
LEFT JOIN order_items oi ON oi.product_id = p.id
-- Note: Requires a bridge to departments via customers/orders if needed.
```

### 3. Customer Value Gap
```sql
SELECT c.name, c.city, 
       SUM(o.amount) AS total_spend,
       AVG(SUM(o.amount)) OVER (PARTITION BY c.city) AS city_avg,
       SUM(o.amount) - AVG(SUM(o.amount)) OVER (PARTITION BY c.city) AS gap
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name, c.city;
```

### 4. Product Cannibalization
```sql
SELECT DISTINCT c.name
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE p.name = 'Laptop Pro'
  AND c.id NOT IN (
      SELECT DISTINCT o2.customer_id
      FROM orders o2
      JOIN order_items oi2 ON o2.id = oi2.order_id
      JOIN products p2 ON oi2.product_id = p2.id
      WHERE p2.category = 'Electronics' AND p2.price < 100
  );
```

### 5. Department Diversity
```sql
SELECT d.name
FROM departments d
JOIN employees e ON d.id = e.department_id
JOIN customers c ON e.name = c.name -- Assuming names link to city data
GROUP BY d.name
HAVING COUNT(DISTINCT c.city) >= 3;
```

### 6. Multi-hop Hierarchy
```sql
SELECT e1.name AS employee, e2.name AS manager
FROM employees e1
JOIN employees e2 ON e1.manager_id = e2.id
JOIN employees e3 ON e2.manager_id = e3.id
WHERE e3.name = 'John Smith';
```

### 7. Cross-Category Heavy Hitters
```sql
SELECT customer_id FROM (
    SELECT o.customer_id
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    JOIN products p ON oi.product_id = p.id
    WHERE p.category = 'Electronics'
    GROUP BY o.customer_id HAVING SUM(o.amount) > 500
) t1
INTERSECT
SELECT customer_id FROM (
    SELECT o.customer_id
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    JOIN products p ON oi.product_id = p.id
    WHERE p.category = 'Furniture'
    GROUP BY o.customer_id HAVING SUM(o.amount) > 500
) t2;
```

### 8. Incomplete Orders
```sql
SELECT o.id, o.amount AS recorded_total, SUM(oi.quantity * oi.unit_price) AS item_total
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
GROUP BY o.id, o.amount
HAVING o.amount <> SUM(oi.quantity * oi.unit_price);
```

### 9. Manager Performance
```sql
SELECT m.name AS manager, 
       (SUM(e.salary) / m.salary) * 100 AS report_pay_pct
FROM employees e
JOIN employees m ON e.manager_id = m.id
GROUP BY m.id, m.name, m.salary;
```

### 10. Product Affinity
```sql
WITH pairs AS (
    SELECT oi1.product_id AS p1, oi2.product_id AS p2, COUNT(*) as frequency
    FROM order_items oi1
    JOIN order_items oi2 ON oi1.order_id = oi2.order_id AND oi1.product_id <> oi2.product_id
    GROUP BY 1, 2
)
SELECT p1, p2, frequency
FROM (
    SELECT p1, p2, frequency, RANK() OVER (PARTITION BY p1 ORDER BY frequency DESC) as rn
    FROM pairs
) t WHERE rn = 1;
```

### 11. Recent High Spenders
```sql
WITH last_3 AS (
    SELECT customer_id, amount,
           AVG(amount) OVER(PARTITION BY customer_id ORDER BY order_date DESC ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING) as recent_avg
    FROM orders
)
SELECT DISTINCT customer_id FROM (
    SELECT l.customer_id, l.recent_avg, 
           AVG(o.amount) OVER(PARTITION BY o.customer_id) as lifetime_avg
    FROM last_3 l
    JOIN orders o ON l.customer_id = o.customer_id
) t WHERE recent_avg > lifetime_avg;
```

### 12. Payroll Concentration
```sql
WITH ranked AS (
    SELECT department_id, salary, 
           SUM(salary) OVER (PARTITION BY department_id) as total_dept_pay,
           ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) as rn
    FROM employees
)
SELECT department_id, SUM(salary) / MAX(total_dept_pay) as top_2_share
FROM ranked
WHERE rn <= 2
GROUP BY department_id
HAVING SUM(salary) / MAX(total_dept_pay) > 0.4;
```

### 13. City Loyalty
```sql
SELECT DISTINCT c.name
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE c.city <> 'Target City' -- Hypothetical logic check
-- Actual query would check if any single order matches customer city
GROUP BY c.id, c.name, c.city
HAVING COUNT(*) = SUM(CASE WHEN o.status IS NOT NULL THEN 1 ELSE 0 END); -- Logic depends on available 'order_city'
```

### 14. Dead-End Categories
```sql
SELECT DISTINCT category FROM products
WHERE category NOT IN (
    SELECT p.category
    FROM products p
    JOIN order_items oi ON p.id = oi.product_id
    JOIN orders o ON oi.order_id = o.id
    WHERE o.order_date >= CURRENT_DATE - INTERVAL '90 days'
);
```

### 15. Overlapping Roles
```sql
SELECT e1.name, e1.department_id as dept1, e2.department_id as dept2
FROM employees e1
JOIN employees e2 ON e1.name = e2.name AND e1.department_id <> e2.department_id;
```

### 16. Sales Velocity
```sql
WITH ordered AS (
    SELECT customer_id, order_date,
           ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY order_date) as rn
    FROM orders
)
SELECT AVG(o2.order_date - o1.order_date) AS avg_velocity_days
FROM ordered o1
JOIN ordered o2 ON o1.customer_id = o2.customer_id AND o1.rn = 1 AND o2.rn = 2;
```

### 17. Top-Heavy Depts
```sql
SELECT d.name
FROM departments d
JOIN employees e ON d.id = e.department_id
GROUP BY d.name
HAVING AVG(e.salary) > (
    SELECT AVG(salary) FROM employees 
    WHERE id IN (SELECT DISTINCT manager_id FROM employees)
);
```

### 18. Product Replacement
```sql
-- Comparing frequency before and after a date/event
WITH stock_out AS (
    SELECT order_date FROM orders WHERE status = 'cancelled' LIMIT 1
)
SELECT p.name, COUNT(o.id) as freq
FROM products p
JOIN order_items oi ON p.id = oi.product_id
JOIN orders o ON oi.order_id = o.id
WHERE o.order_date > (SELECT order_date FROM stock_out)
GROUP BY p.name;
```

### 19. LTV Tiering
```sql
SELECT name, total_spend, NTILE(10) OVER(ORDER BY total_spend DESC) as tier
FROM (
    SELECT c.name, SUM(o.amount) as total_spend
    FROM customers c
    JOIN orders o ON c.id = o.customer_id
    GROUP BY c.id, c.name
) t;
```

### 20. Aggregated Status
```sql
SELECT c.name
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name
HAVING COUNT(CASE WHEN o.status = 'completed' THEN 1 END) >= 5
   AND COUNT(CASE WHEN o.status IN ('cancelled', 'pending') THEN 1 END) = 0;
```

### 21. Non-Sales Season
```sql
WITH monthly_sales AS (
    SELECT product_id, DATE_TRUNC('month', o.order_date) as month, SUM(oi.quantity) as qty
    FROM orders o JOIN order_items oi ON o.id = oi.order_id
    WHERE EXTRACT(YEAR FROM o.order_date) = 2024
    GROUP BY 1, 2
)
SELECT product_id, month, qty
FROM (
    SELECT *, RANK() OVER(PARTITION BY product_id ORDER BY qty ASC) as rn
    FROM monthly_sales
) t WHERE rn = 1;
```

### 22. Retention Risk
```sql
SELECT name, salary, hire_date
FROM employees e
WHERE hire_date < CURRENT_DATE - INTERVAL '3 years'
  AND salary = (
      SELECT MIN(salary) FROM employees WHERE department_id = e.department_id
  );
```

### 23. Revenue Attribution
```sql
SELECT c.city, p.name, 
       SUM(oi.quantity * oi.unit_price) / SUM(SUM(oi.quantity * oi.unit_price)) OVER(PARTITION BY c.city) * 100 as city_share_pct
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
GROUP BY c.city, p.name;
```

### 24. Small Order King
```sql
SELECT c.name, COUNT(*) as small_order_count
FROM customers c
JOIN orders o ON c.id = o.customer_id
WHERE o.amount < 50
GROUP BY c.id, c.name
ORDER BY small_order_count DESC LIMIT 1;
```

### 25. Join Inequalities
```sql
SELECT e1.name as junior_senior, e2.name as mentor_equivalent
FROM employees e1
JOIN employees e2 ON e1.salary < e2.salary AND e1.hire_date < e2.hire_date;
```

---

## 🪟 Solutions: Part 2 (Problems 26-50: Window Functions)

### 26. Running Total with Cap
```sql
WITH RECURSIVE capped_total AS (
    SELECT id, order_date, amount, amount as running_total
    FROM (SELECT *, ROW_NUMBER() OVER(ORDER BY order_date, id) as rn FROM orders) t
    WHERE rn = 1
    
    UNION ALL
    
    SELECT t.id, t.order_date, t.amount,
           CASE WHEN ct.running_total + t.amount > 5000 THEN t.amount 
                ELSE ct.running_total + t.amount END
    FROM (SELECT *, ROW_NUMBER() OVER(ORDER BY order_date, id) as rn FROM orders) t
    JOIN capped_total ct ON t.rn = (SELECT rn FROM (SELECT *, ROW_NUMBER() OVER(ORDER BY order_date, id) as rn FROM orders) t2 WHERE t2.id = ct.id) + 1
WITH RECURSIVE running_totals AS (
    SELECT id, order_date, amount, amount as current_sum, 1 as sort_key
    FROM orders WHERE id = (SELECT MIN(id) FROM orders)
    UNION ALL
    SELECT o.id, o.order_date, o.amount,
           CASE WHEN rt.current_sum + o.amount > 5000 THEN o.amount ELSE rt.current_sum + o.amount END,
           rt.sort_key + 1
    FROM orders o
    JOIN running_totals rt ON rt.sort_key + 1 = o.id -- Simplified logic for demo
)
SELECT * FROM running_totals;
```

### 27. Z-Score Calculation
```sql
SELECT name, salary, department_id,
       (salary - AVG(salary) OVER(PARTITION BY department_id)) / 
       STDDEV(salary) OVER(PARTITION BY department_id) as z_score
FROM employees;
```

### 28. Gap Detection
```sql
WITH RECURSIVE dates AS (
    SELECT DATE '2024-01-01' as d
    UNION ALL
    SELECT d + 1 FROM dates WHERE d < '2024-12-31'
)
SELECT d FROM dates
WHERE d NOT IN (SELECT order_date FROM orders)
LIMIT 1;
```

### 29. Consecutive Days
```sql
WITH groupings AS (
    SELECT customer_id, order_date,
           order_date - CAST(ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY order_date) AS INT) as grp
    FROM orders
)
SELECT customer_id, COUNT(*) as consecutive_days
FROM groupings
GROUP BY customer_id, grp
HAVING COUNT(*) >= 3;
```

### 30. N-Tile Analysis
```sql
SELECT bucket, MIN(amount), MAX(amount)
FROM (
    SELECT amount, NTILE(5) OVER(ORDER BY amount) as bucket
    FROM orders
) t
GROUP BY bucket;
```

### 31. Lead/Lag Comparison
```sql
SELECT id, customer_id, amount,
       LAG(amount, 1) OVER(PARTITION BY customer_id ORDER BY order_date) as prev_1,
       AVG(amount) OVER(PARTITION BY customer_id ORDER BY order_date ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING) as prev_3_avg,
       (amount - AVG(amount) OVER(PARTITION BY customer_id ORDER BY order_date ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING)) / 
       NULLIF(AVG(amount) OVER(PARTITION BY customer_id ORDER BY order_date ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING), 0) * 100 as pct_change
FROM orders;
```

### 32. Ranking Ties
```sql
SELECT * FROM (
    SELECT name, salary, DENSE_RANK() OVER(ORDER BY salary DESC) as r
    FROM employees
) t WHERE r IN (3, 4);
```

### 33. Window Frame Mastery
```sql
WITH first_sales AS (
    SELECT product_id, MIN(order_date) as first_date
    FROM orders o JOIN order_items oi ON o.id = oi.order_id
    GROUP BY 1
)
SELECT fs.product_id, SUM(oi.quantity)
FROM first_sales fs
JOIN orders o ON o.order_date BETWEEN fs.first_date AND fs.first_date + 7
JOIN order_items oi ON o.id = oi.order_id AND oi.product_id = fs.product_id
GROUP BY 1;
```

### 34. Active Customer Streaks
```sql
WITH monthly_active AS (
    SELECT DISTINCT customer_id, DATE_TRUNC('month', order_date) as active_month
    FROM orders
),
streaks AS (
    SELECT customer_id, active_month,
           active_month - (INTERVAL '1 month' * ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY active_month)) as grp
    FROM monthly_active
)
SELECT customer_id, COUNT(*) as longest_streak
FROM streaks
GROUP BY customer_id, grp
ORDER BY longest_streak DESC;
```

### 35. Percentile Rank
```sql
SELECT name, salary, 
       CUME_DIST() OVER(ORDER BY salary) as percentile
FROM employees;
```

### 36. Row to Row Calculations
```sql
SELECT order_date, amount,
       amount - LAG(amount) OVER(ORDER BY order_date) as diff_from_prev
FROM orders;
```

### 37. First/Last Interaction
```sql
SELECT DISTINCT customer_id,
       FIRST_VALUE(p.name) OVER(PARTITION BY o.customer_id ORDER BY o.order_date) as first_prod,
       LAST_VALUE(p.name) OVER(PARTITION BY o.customer_id ORDER BY o.order_date 
                                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as last_prod
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id;
```

### 38. Moving Average (7-Day)
```sql
SELECT order_date, SUM(amount) as daily_total,
       AVG(SUM(amount)) OVER(ORDER BY order_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7d
FROM orders
GROUP BY 1;
```

### 39. Quarterly Performance
```sql
SELECT EXTRACT(QUARTER FROM order_date) as qtr,
       SUM(amount) as revenue,
       RANK() OVER(ORDER BY SUM(amount) DESC) as qtr_rank
FROM orders
GROUP BY 1;
```

### 40. Top N per Group
```sql
SELECT * FROM (
    SELECT d.name as dept, e.name, e.salary,
           ROW_NUMBER() OVER(PARTITION BY department_id ORDER BY salary DESC) as rn
    FROM employees e
    JOIN departments d ON e.department_id = d.id
) t WHERE rn <= 3;
```

### 41. Cumulative Revenue Share
```sql
WITH daily_rev AS (
    SELECT order_date, SUM(amount) as rev
    FROM orders GROUP BY 1
)
SELECT order_date, rev,
       SUM(rev) OVER(ORDER BY order_date) / SUM(rev) OVER() * 100 as cum_share_pct
FROM daily_rev;
```

### 42. Moving Median (Simulation)
```sql
SELECT customer_id, order_date, amount,
       PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount) OVER(PARTITION BY customer_id) as median_spend
FROM orders;
```

### 43. Peak Hour Analysis
```sql
SELECT EXTRACT(HOUR FROM created_at) as hr, COUNT(*) as volume
FROM customers -- Or any table with timestamp
GROUP BY 1 ORDER BY 2 DESC;
```

### 44. Retention Cohorts
```sql
-- Logic: Group by first order month
WITH first_orders AS (
    SELECT customer_id, MIN(DATE_TRUNC('month', order_date)) as cohort
    FROM orders GROUP BY 1
)
SELECT cohort, DATE_TRUNC('month', order_date) as active_month, COUNT(DISTINCT customer_id)
FROM first_orders f
JOIN orders o USING(customer_id)
GROUP BY 1, 2;
```

### 45. Standard Deviation Outliers
```sql
WITH stats AS (
    SELECT AVG(amount) as mean, STDDEV(amount) as sd FROM orders
)
SELECT * FROM orders, stats
WHERE amount > mean + (2 * sd) OR amount < mean - (2 * sd);
```

### 46. Year-over-Year Growth
```sql
WITH yearly AS (
    SELECT EXTRACT(YEAR FROM order_date) as yr, SUM(amount) as rev
    FROM orders GROUP BY 1
)
SELECT yr, rev,
       (rev - LAG(rev) OVER(ORDER BY yr)) / LAG(rev) OVER(ORDER BY yr) * 100 as yoy_growth
FROM yearly;
```

### 47. Customer Ranking by Tenure
```sql
SELECT name, created_at,
       RANK() OVER(ORDER BY created_at) as loyalty_rank
FROM customers;
```

### 48. Department Salary Variance
```sql
SELECT d.name, VARIANCE(salary) OVER(PARTITION BY d.id) as sal_var
FROM employees e JOIN departments d ON e.department_id = d.id;
```

### 49. Lead Time Calculation
```sql
SELECT o.id, o.order_date, c.created_at,
       o.order_date - CAST(c.created_at AS DATE) as lead_days
FROM orders o JOIN customers c ON o.customer_id = c.id;
```

### 50. Weighted Average
```sql
SELECT category,
       SUM(price * quantity) OVER(PARTITION BY category) / 
       SUM(quantity) OVER(PARTITION BY category) as weighted_avg_price
FROM products p
JOIN order_items oi ON p.id = oi.product_id;
```

---

## 🌲 Solutions: Part 3 (Problems 51-70: CTEs & Recursion)

### 51. Chained CTE Aggregation
```sql
WITH order_stats AS (
    SELECT order_id, COUNT(*) as items_per_order
    FROM order_items
    GROUP BY order_id
),
category_avg AS (
    SELECT p.category, AVG(t.items_per_order) as cat_avg_items
    FROM products p
    JOIN order_items oi ON p.id = oi.product_id
    JOIN order_stats t ON oi.order_id = t.order_id
    GROUP BY p.category
)
SELECT o.customer_id, AVG(os.items_per_order)
FROM orders o
JOIN order_stats os ON o.id = os.order_id
GROUP BY o.customer_id;
```

### 52. Recursive Fibonacci
```sql
WITH RECURSIVE fib AS (
    SELECT 1 as n, 0::bigint as val, 1::bigint as next_val
    UNION ALL
    SELECT n + 1, next_val, val + next_val
    FROM fib WHERE n < 20
)
SELECT val FROM fib;
```

### 53. Menu Hierarchy
```sql
WITH RECURSIVE menu AS (
    SELECT id, name, CAST(name AS VARCHAR(255)) as path, 1 as level
    FROM departments
    UNION ALL
    SELECT p.id, p.name, CAST(m.path || ' > ' || p.name AS VARCHAR(255)), m.level + 1
    FROM products p
    JOIN menu m ON m.id = p.id -- Simplified hierarchy link
    WHERE m.level < 3
)
SELECT * FROM menu;
```

### 54. Path Finder
```sql
WITH RECURSIVE mgmt_path AS (
    SELECT id, name, manager_id, salary, CAST(name AS VARCHAR(500)) as path
    FROM employees WHERE name = 'Target Employee'
    UNION ALL
    SELECT e.id, e.name, e.manager_id, e.salary, CAST(mp.path || ' -> ' || e.name AS VARCHAR(500))
    FROM employees e
    JOIN mgmt_path mp ON e.id = mp.manager_id
)
SELECT *, (SELECT SUM(salary) FROM mgmt_path) as total_path_salary FROM mgmt_path;
```

### 55. Recursive Date Gaps
```sql
WITH RECURSIVE mondays AS (
    SELECT DATE '2024-01-01' as d
    UNION ALL
    SELECT d + 7 FROM mondays WHERE d < '2024-12-25'
)
SELECT d FROM mondays;
```

### 56. Tree Breadth
```sql
WITH RECURSIVE tree AS (
    SELECT id, manager_id, 1 as level
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.manager_id, t.level + 1
    FROM employees e
    JOIN tree t ON e.manager_id = t.id
)
SELECT manager_id, level, COUNT(*) as reports_at_level
FROM tree
WHERE manager_id IS NOT NULL
GROUP BY 1, 2;
```

### 57. Cycle Detection
```sql
WITH RECURSIVE search_graph AS (
    SELECT id, manager_id, ARRAY[id] as path, false as is_cycle
    FROM employees
    UNION ALL
    SELECT e.id, e.manager_id, sg.path || e.id, e.id = ANY(sg.path)
    FROM employees e
    JOIN search_graph sg ON e.manager_id = sg.id
    WHERE NOT sg.is_cycle
)
SELECT * FROM search_graph WHERE is_cycle;
```

### 58. Running Inventory
```sql
WITH starting_inv AS (
    SELECT id as product_id, 1000 as start_qty FROM products
),
sales AS (
    SELECT product_id, SUM(quantity) as sold
    FROM order_items GROUP BY 1
)
SELECT p.name, si.start_qty - COALESCE(s.sold, 0) as current_stock
FROM products p
JOIN starting_inv si ON p.id = si.product_id
LEFT JOIN sales s ON p.id = s.product_id;
```

### 59. CTE for Deduplication
```sql
WITH ranked_orders AS (
    SELECT *, ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY order_date DESC) as rn
    FROM orders
)
SELECT * FROM ranked_orders WHERE rn = 1;
```

### 60. Flattening Data (STRING_AGG)
```sql
SELECT customer_id, 
       STRING_AGG(id::text, ', ' ORDER BY order_date) as order_ids
FROM orders
GROUP BY customer_id;
```

### 61. Multi-level Commission
```sql
WITH sales_totals AS (
    SELECT e.id as emp_id, COALESCE(SUM(o.amount), 0) as personal_sales
    FROM employees e
    LEFT JOIN orders o ON e.id = o.customer_id
    GROUP BY 1
)
SELECT e.name, 
       (st.personal_sales * 0.05) + 
       (SELECT SUM(st2.personal_sales) FROM employees e2 JOIN sales_totals st2 ON e2.id = st2.emp_id WHERE e2.manager_id = e.id) * 0.02 as commission
FROM employees e
JOIN sales_totals st ON e.id = st.emp_id;
```

### 62. Recursive String Splitting
```sql
WITH RECURSIVE split(id, rest) AS (
    SELECT 
        SUBSTR('1,2,3,4', 1, INSTR('1,2,3,4' || ',', ',') - 1),
        SUBSTR('1,2,3,4' || ',', INSTR('1,2,3,4' || ',', ',') + 1)
    UNION ALL
    SELECT 
        SUBSTR(rest, 1, INSTR(rest, ',') - 1),
        SUBSTR(rest, INSTR(rest, ',') + 1)
    FROM split WHERE rest <> ''
)
SELECT id FROM split;
```

### 63. Cohort Base
```sql
WITH q1_new AS (
    SELECT customer_id FROM orders 
    WHERE order_date BETWEEN '2024-01-01' AND '2024-03-31'
    GROUP BY 1
    HAVING MIN(order_date) >= '2024-01-01'
)
SELECT SUM(o.amount)
FROM orders o
JOIN q1_new q ON o.customer_id = q.customer_id
WHERE o.order_date BETWEEN '2024-04-01' AND '2024-06-30';
```

### 64. Recursive Factorial
```sql
WITH RECURSIVE fact(n, val) AS (
    SELECT 1, 1::bigint
    UNION ALL
    SELECT n + 1, val * (n + 1)
    FROM fact WHERE n < 10
)
SELECT val FROM fact WHERE n = 10;
```

### 65. Employee Siblings
```sql
SELECT name, manager_id,
       COUNT(*) OVER(PARTITION BY manager_id) - 1 as siblings
FROM employees;
```

### 66. CTE Ranking
```sql
WITH scores AS (
    SELECT customer_id, 
           (COUNT(*) * 2) + AVG(amount) as score
    FROM orders
    GROUP BY customer_id
)
SELECT c.name, s.score,
       RANK() OVER(ORDER BY score DESC) as rank
FROM customers c
JOIN scores s ON c.id = s.customer_id;
```

### 67. Hierarchical Path
```sql
WITH RECURSIVE paths AS (
    SELECT id, name, manager_id, CAST(name AS VARCHAR(500)) as path
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, CAST(p.path || ' > ' || e.name AS VARCHAR(500))
    FROM employees e
    JOIN paths p ON e.manager_id = p.id
)
SELECT * FROM paths;
```

### 68. Filling Missing Months
```sql
WITH RECURSIVE months AS (
    SELECT DATE_TRUNC('month', DATE '2024-01-01') as month
    UNION ALL
    SELECT month + INTERVAL '1 month'
    FROM months WHERE month < DATE '2024-12-01'
),
monthly_sales AS (
    SELECT DATE_TRUNC('month', order_date) as m, SUM(amount) as revenue
    FROM orders GROUP BY 1
)
SELECT m.month, COALESCE(ms.revenue, 0)
FROM months m
LEFT JOIN monthly_sales ms ON m.month = ms.m;
```

### 69. Longest Chain
```sql
WITH RECURSIVE depth AS (
    SELECT id, 1 as d FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, d + 1 FROM employees e JOIN depth dt ON e.manager_id = dt.id
)
SELECT * FROM depth ORDER BY d DESC LIMIT 1;
```

### 70. CTE Pivot
```sql
WITH monthly_rev AS (
    SELECT customer_id, 
           EXTRACT(MONTH FROM order_date) as m,
           SUM(amount) as rev
    FROM orders GROUP BY 1, 2
)
SELECT customer_id,
       SUM(CASE WHEN m = 1 THEN rev ELSE 0 END) as Jan,
       SUM(CASE WHEN m = 2 THEN rev ELSE 0 END) as Feb,
       SUM(CASE WHEN m = 12 THEN rev ELSE 0 END) as Dec
FROM monthly_rev
GROUP BY customer_id;
```

---

## 📈 Solutions: Part 4 (Problems 71-85: Data Analysis)

### 71. MoM Growth
```sql
WITH monthly AS (
    SELECT DATE_TRUNC('month', order_date) as month, SUM(amount) as rev
    FROM orders GROUP BY 1
)
SELECT month, rev,
       (rev - LAG(rev) OVER(ORDER BY month)) / LAG(rev) OVER(ORDER BY month) * 100 as growth_pct
FROM monthly;
```

### 72. Customer Retention
```sql
SELECT DISTINCT c.id, c.name
FROM customers c
JOIN orders o1 ON c.id = o1.customer_id AND o1.order_date BETWEEN '2024-01-01' AND '2024-01-31'
JOIN orders o2 ON c.id = o2.customer_id AND o2.order_date BETWEEN '2024-02-01' AND '2024-02-29';
```

### 73. Churn Analysis
```sql
SELECT DISTINCT customer_id FROM orders 
WHERE order_date BETWEEN '2024-01-01' AND '2024-03-31'
EXCEPT
SELECT DISTINCT customer_id FROM orders 
WHERE order_date BETWEEN '2024-04-01' AND '2024-06-30';
```

### 74. Pareto Principle (80/20)
```sql
WITH product_rev AS (
    SELECT product_id, SUM(quantity * unit_price) as rev
    FROM order_items GROUP BY 1
),
running_rev AS (
    SELECT product_id, rev,
           SUM(rev) OVER(ORDER BY rev DESC) / SUM(rev) OVER() as cum_pct
    FROM product_rev
)
SELECT * FROM running_rev WHERE cum_pct <= 0.8;
```

### 75. High Value Acquisition
```sql
WITH first_order AS (
    SELECT customer_id, id as order_id, amount,
           ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY order_date) as rn
    FROM orders
)
SELECT * FROM first_order WHERE rn = 1 AND amount > 500;
```

### 76. Average Order Gap
```sql
WITH gaps AS (
    SELECT customer_id, 
           order_date - LAG(order_date) OVER(PARTITION BY customer_id ORDER BY order_date) as gap
    FROM orders
)
SELECT customer_id, AVG(gap) as avg_days_between
FROM gaps
WHERE gap IS NOT NULL
GROUP BY 1;
```

### 77. Return Rate by Category
```sql
SELECT p.category,
       COUNT(CASE WHEN o.status = 'cancelled' THEN 1 END)::float / COUNT(*) * 100 as return_rate
FROM products p
JOIN order_items oi ON p.id = oi.product_id
JOIN orders o ON oi.order_id = o.id
GROUP BY 1;
```

### 78. User Session Simulation
```sql
-- Activity within 30 mins
WITH sessions AS (
    SELECT customer_id, created_at,
           CASE WHEN created_at - LAG(created_at) OVER(PARTITION BY customer_id ORDER BY created_at) > INTERVAL '30 minutes' 
                THEN 1 ELSE 0 END as is_new_session
    FROM customers -- Proxy for activity log
)
SELECT customer_id, SUM(is_new_session) + 1 as total_sessions
FROM sessions
GROUP BY 1;
```

### 79. Weekend vs Weekday Sales
```sql
SELECT CASE WHEN EXTRACT(DOW FROM order_date) IN (0, 6) THEN 'Weekend' ELSE 'Weekday' END as day_type,
       AVG(amount) as avg_rev
FROM orders
GROUP BY 1;
```

### 80. Basket Analysis
```sql
SELECT oi1.product_id, oi2.product_id, COUNT(*) as frequency
FROM order_items oi1
JOIN order_items oi2 ON oi1.order_id = oi2.order_id AND oi1.product_id < oi2.product_id
GROUP BY 1, 2
ORDER BY frequency DESC LIMIT 1;
```

### 81. RFM Scoring (Recency)
```sql
SELECT customer_id,
       MAX(order_date) as last_order,
       CURRENT_DATE - MAX(order_date) as recency_days
FROM orders GROUP BY 1;
```

### 82. RFM Scoring (Frequency)
```sql
SELECT customer_id, COUNT(*) as frequency
FROM orders GROUP BY 1;
```

### 83. RFM Scoring (Monetary)
```sql
SELECT customer_id, SUM(amount) as monetary
FROM orders GROUP BY 1;
```

### 84. Top City per Category
```sql
SELECT * FROM (
    SELECT c.city, p.category, SUM(o.amount) as rev,
           RANK() OVER(PARTITION BY p.category ORDER BY SUM(o.amount) DESC) as r
    FROM customers c
    JOIN orders o ON c.id = o.customer_id
    JOIN order_items oi ON o.id = oi.order_id
    JOIN products p ON oi.product_id = p.id
    GROUP BY 1, 2
) t WHERE r = 1;
```

### 85. Underperforming Products
```sql
SELECT p.name, p.category
FROM products p
WHERE NOT EXISTS (
    SELECT 1 FROM order_items oi
    JOIN orders o ON oi.order_id = o.id
    WHERE oi.product_id = p.id 
      AND o.order_date >= CURRENT_DATE - INTERVAL '6 months'
);
```

---

## ⚡ Solutions: Part 5 (Problems 86-100: Optimization)

### 86. Refactor Scalar Subquery
```sql
-- SLOW:
SELECT name, (SELECT name FROM departments WHERE id = e.department_id) as dept
FROM employees e;

-- FAST:
SELECT e.name, d.name as dept
FROM employees e
JOIN departments d ON e.department_id = d.id;
```

### 87. Avoiding OR
```sql
-- SLOW:
SELECT * FROM products WHERE category = 'Electronics' OR price < 10;

-- FAST (using index on both):
SELECT * FROM products WHERE category = 'Electronics'
UNION
SELECT * FROM products WHERE price < 10;
```

### 88. Index-Friendly Filtering
```sql
-- SLOW (Non-sargable):
SELECT * FROM employees WHERE YEAR(hire_date) = 2024;

-- FAST (Sargable):
SELECT * FROM employees 
WHERE hire_date >= '2024-01-01' AND hire_date < '2025-01-01';
```

### 89. Exists vs Count
```sql
-- SLOW:
SELECT * FROM customers c WHERE (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.id) > 0;

-- FAST:
SELECT * FROM customers c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
```

### 90. Unnecessary Joins
```sql
-- SLOW:
SELECT o.id, c.name FROM orders o JOIN customers c ON o.customer_id = c.id;

-- FAST (if you only need ID/FK):
SELECT id, customer_id FROM orders;
```

### 91. Materialized View Logic
```sql
-- Simulation: Refreshing a summary table
CREATE TABLE sales_summary AS 
SELECT product_id, SUM(quantity) as total 
FROM order_items GROUP BY 1;

-- Optimized:
REFRESH MATERIALIZED VIEW concurr_sales_summary;
```

### 92. Over-indexing Check
```sql
-- Scenario: Find indexes rarely used
-- PostgreSQL specific:
SELECT relname, indexrelname, idx_scan 
FROM pg_stat_user_indexes 
WHERE idx_scan = 0;
```

### 93. CTE vs Temp Table
```sql
-- USE CTE if small/referenced once.
-- USE Temp Table if large/referenced multiple times (to add indexes).
CREATE TEMP TABLE large_subset AS 
SELECT * FROM orders WHERE amount > 10000;
CREATE INDEX idx_subset_cust ON large_subset(customer_id);
```

### 94. Refactor NOT IN
```sql
-- RISKY (Returns nothing if any order_id is NULL):
SELECT * FROM order_items WHERE order_id NOT IN (SELECT id FROM orders);

-- SAFE & FAST:
SELECT * FROM order_items oi 
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.id = oi.order_id);
```

### 95. Partition Pruning
```sql
-- Logic: Ensure query uses partition key
SELECT * FROM large_log_table 
WHERE log_date >= '2024-12-01' AND log_date < '2024-12-02';
```

### 96. Limit and Sort
```sql
-- Ensure index on (department_id, salary) for:
SELECT * FROM employees 
WHERE department_id = 5 
ORDER BY salary DESC LIMIT 10;
```

### 97. Partial Indexing
```sql
-- Create:
CREATE INDEX idx_active_orders ON orders(customer_id) WHERE status = 'pending';

-- Use:
SELECT * FROM orders WHERE status = 'pending' AND customer_id = 123;
```

### 98. Window vs Self-Join
```sql
-- SELF JOIN:
SELECT o1.order_date, o1.amount, o2.amount as prev_day_amount
FROM orders o1
JOIN orders o2 ON o1.order_date = o2.order_date + INTERVAL '1 day';

-- WINDOW (Much faster):
SELECT order_date, amount,
       LAG(amount) OVER(ORDER BY order_date) as prev_day_amount
FROM orders;
```

### 99. Covering Index
```sql
-- Create:
CREATE INDEX idx_covering ON employees(department_id) INCLUDE (name, salary);

-- Query avoids reading table heap:
SELECT name, salary FROM employees WHERE department_id = 2;
```

### 100. The "Big Table" Strategy
**Strategy:**
1.  **Partitioning**: Use table partitioning by `timestamp` column.
2.  **Indexing**: Create a BRIN index (Block Range Index) or B-Tree index on the timestamp.
3.  **Materialized Views**: Maintain a sliding window materialized view for the last 2 hours.

---

**Congratulations! You've completed the 100 Advanced Problems!**
