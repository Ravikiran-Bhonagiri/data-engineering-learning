# 🎯 SQL Advanced Practice Bank (100 Problems)

This file contains 100 medium and hard SQL problems designed for Senior Data Engineer interview preparation. 

---

## 🏗️ Schema Reference
Use the tables created in `Day_00_Setup.md`:
- `departments`, `employees`, `customers`, `products`, `orders`, `order_items`

---

## 🗺️ Table of Contents
1. [Part 1: Complex Joins & Aggregations (1-25)](#-part-1-complex-joins--aggregations-problems-1-25)
2. [Part 2: Window Functions Deep Dive (26-50)](#-part-2-window-functions-deep-dive-problems-26-50)
3. [Part 3: Advanced CTEs & Recursion (51-70)](#-part-3-advanced-ctes--recursion-problems-51-70)
4. [Part 4: Data Analysis & Business Logic (71-85)](#-part-4-data-analysis--business-logic-problems-71-85)
5. [Part 5: Query Optimization & Performance (86-100)](#-part-5-query-optimization--performance-problems-86-100)

---

## 🔗 Part 1: Complex Joins & Aggregations (Problems 1-25)

---

### 🎯 Problem 1: Self-Join Growth
**Difficulty: Medium** | **Concept: Self-JOIN + Subquery**

Find employees earning more than their manager AND more than the average salary of their own department.

```sql
-- Write your solution here
```

---

### 🎯 Problem 2: Missing Dimensions
**Difficulty: Hard** | **Concept: CROSS JOIN + LEFT JOIN**

List all departments and products. For each pair, show the total quantity sold. Include pairs with 0 sales.

```sql
-- Write your solution here
```

---

### 🎯 Problem 3: Customer Value Gap
**Difficulty: Medium** | **Concept: Window AVG**

Find the difference between a customer's total spend and the average spend of all customers in their city.

```sql
-- Write your solution here
```

---

### 🎯 Problem 4: Product Cannibalization
**Difficulty: Hard** | **Concept: NOT IN / NOT EXISTS**

Find customers who bought 'Laptop Pro' but never bought any accessories (category = 'Electronics' where price < 100).

```sql
-- Write your solution here
```

---

### 🎯 Problem 5: Department Diversity
**Difficulty: Medium** | **Concept: COUNT(DISTINCT)**

Find departments that have employees from at least 3 different cities (based on customer cities).

```sql
-- Write your solution here
```

---

### 🎯 Problem 6: Multi-hop Hierarchy
**Difficulty: Hard** | **Concept: Self-JOIN chain**

Find all employees who report directly to a manager who themselves report to John Smith.

```sql
-- Write your solution here
```

---

### 🎯 Problem 7: Cross-Category Heavy Hitters
**Difficulty: Medium** | **Concept: INTERSECT / Multiple Joins**

List customers who have spent more than $500 in BOTH 'Electronics' and 'Furniture' categories.

```sql
-- Write your solution here
```

---

### 🎯 Problem 8: Incomplete Orders
**Difficulty: Medium** | **Concept: SUM vs Table Total**

Find orders where total amount in `orders` table does not match the sum of `unit_price * quantity` in `order_items`.

```sql
-- Write your solution here
```

---

### 🎯 Problem 9: Manager Performance
**Difficulty: Medium** | **Concept: Aggregation + Division**

For each manager, calculate the total salary of their direct reports as a percentage of the manager's own salary.

```sql
-- Write your solution here
```

---

### 🎯 Problem 10: Product Affinity
**Difficulty: Hard** | **Concept: Self-JOIN on OrderItems**

For every product, find the most common product bought in the same order.

```sql
-- Write your solution here
```

---

### 🎯 Problem 11: Recent High Spenders
**Difficulty: Medium** | **Concept: Window AVG vs Lifetime**

Find customers whose total spend in the last 3 orders is greater than their lifetime average order value.

```sql
-- Write your solution here
```

---

### 🎯 Problem 12: Payroll Concentration
**Difficulty: Hard** | **Concept: Window SUM + Percentage**

Find departments where the top 2 earners take home more than 40% of the total department payroll.

```sql
-- Write your solution here
```

---

### 🎯 Problem 13: City Loyalty
**Difficulty: Medium** | **Concept: Filter on different attributes**

List customers who only place orders from cities other than their own registered city.

```sql
-- Write your solution here
```

---

### 🎯 Problem 14: Dead-End Categories
**Difficulty: Medium** | **Concept: Date filtering + Aggregation**

Find product categories where no product has been ordered in the last 90 days.

```sql
-- Write your solution here
```

---

### 🎯 Problem 15: Overlapping Roles
**Difficulty: Easy** | **Concept: JOIN on same table**

Find employees who share the same name but work in different departments.

```sql
-- Write your solution here
```

---

### 🎯 Problem 16: Sales Velocity
**Difficulty: Hard** | **Concept: Date Diff + Windowing**

Find the average time (in days) between first and second order for each customer.

```sql
-- Write your solution here
```

---

### 🎯 Problem 17: Top-Heavy Depts
**Difficulty: Medium** | **Concept: AVG comparison**

List departments where the average salary of employees is higher than the average salary of managers.

```sql
-- Write your solution here
```

---

### 🎯 Problem 18: Product Replacement
**Difficulty: Medium** | **Concept: Comparative dates**

Find products that were ordered more frequently after a specific product went out of stock.

```sql
-- Write your solution here
```

---

### 🎯 Problem 19: LTV Tiering
**Difficulty: Medium** | **Concept: NTILE(10)**

Categorize customers into Deciles (1-10) based on total lifetime spend.

```sql
-- Write your solution here
```

---

### 🎯 Problem 20: Aggregated Status
**Difficulty: Medium** | **Concept: Conditional COUNT/HAVING**

Find customers with at least 5 'completed' orders and 0 'cancelled' or 'pending' orders.

```sql
-- Write your solution here
```

---

### 🎯 Problem 21: Non-Sales Season
**Difficulty: Medium** | **Concept: MIN aggregation per group**

For each product, find the month with the lowest sales volume in 2024.

```sql
-- Write your solution here
```

---

### 🎯 Problem 22: Retention Risk
**Difficulty: Medium** | **Concept: Date logic**

Find employees who have been with the company for > 3 years but have the lowest salary in their department.

```sql
-- Write your solution here
```

---

### 🎯 Problem 23: Revenue Attribution
**Difficulty: Hard** | **Concept: Multi-level Aggregation**

Calculate product revenue share percentage per customer city.

```sql
-- Write your solution here
```

---

### 🎯 Problem 24: Small Order King
**Difficulty: Medium** | **Concept: COUNT + LIMIT**

Find the customer who has the highest number of orders below $50.

```sql
-- Write your solution here
```

---

### 🎯 Problem 25: Join Inequalities
**Difficulty: Hard** | **Concept: Multi-condition JOIN**

Find all pairs of employees (A, B) where A was hired before B and A earns less than B.

```sql
-- Write your solution here
```

---

## 🪟 Part 2: Window Functions Deep Dive (Problems 26-50)

---

### 🎯 Problem 26: Running Total with Cap
**Difficulty: Hard** | **Concept: Window SUM + Conditional Logic**

Calculate running total of order amounts by date, but reset the total whenever it exceeds $5000.

```sql
-- Write your solution here
```

---

### 🎯 Problem 27: Z-Score Calculation
**Difficulty: Hard** | **Concept: AVG() and STDDEV() OVER**

Calculate the Z-Score of salaries for each employee within their department. Formula: `(Salary - Avg) / StdDev`.

```sql
-- Write your solution here
```

---

### 🎯 Problem 28: Gap Detection
**Difficulty: Hard** | **Concept: LAG() or Recursive CTE**

Find the first date in 2024 where no orders were placed (requires generating a date series).

```sql
-- Write your solution here
```

---

### 🎯 Problem 29: Consecutive Days
**Difficulty: Hard** | **Concept: ROW_NUMBER() - Date grouping**

List customers who placed orders on at least 3 consecutive days.

```sql
-- Write your solution here
```

---

### 🎯 Problem 30: N-Tile Analysis
**Difficulty: Medium** | **Concept: NTILE(5)**

Divide orders into 5 buckets based on amount and show the min/max for each bucket.

```sql
-- Write your solution here
```

---

### 🎯 Problem 31: Lead/Lag Comparison
**Difficulty: Hard** | **Concept: LAG(offset, 3)**

Show each order's amount and the percentage change relative to the average of the *previous 3* orders from the same customer.

```sql
-- Write your solution here
```

---

### 🎯 Problem 32: Ranking Ties
**Difficulty: Medium** | **Concept: DENSE_RANK()**

Show the 3rd and 4th highest salaries in the company, ensuring no ranks are skipped even if people share salaries.

```sql
-- Write your solution here
```

---

### 🎯 Problem 33: Window Frame Mastery
**Difficulty: Hard** | **Concept: ROWS BETWEEN**

For each product, calculate the total quantity sold in the 7 days following its first-ever order.

```sql
-- Write your solution here
```

---

### 🎯 Problem 34: Active Customer Streaks
**Difficulty: Hard** | **Concept: Windowing Streaks**

Find the longest continuous streak of months that each customer placed at least one order.

```sql
-- Write your solution here
```

---

### 🎯 Problem 35: Salary Percentile
**Difficulty: Medium** | **Concept: PERCENT_RANK() / CUME_DIST()**

Find employees who are in the top 5% of earners in their respective departments.

```sql
-- Write your solution here
```

---

### 🎯 Problem 36: Peak Sales Period
**Difficulty: Hard** | **Concept: Rolling 3-day window**

For each month, find the 3-day window that generated the highest total revenue.

```sql
-- Write your solution here
```

---

### 🎯 Problem 37: First/Last Interaction
**Difficulty: Medium** | **Concept: FIRST_VALUE / LAST_VALUE**

For each customer, show the product name of their first and most recent purchase in a single row.

```sql
-- Write your solution here
```

---

### 🎯 Problem 38: Running Average (Exclusion)
**Difficulty: Hard** | **Concept: Window Frame Tuning**

Calculate the average salary of all *other* employees in the same department (excluding the current employee's row).

```sql
-- Write your solution here
```

---

### 🎯 Problem 39: Rank within Category
**Difficulty: Medium** | **Concept: RANK() + PARTITION BY**

For each product category, find the top 2 sold products by unique quantity.

```sql
-- Write your solution here
```

---

### 🎯 Problem 40: Difference from Prev Product
**Difficulty: Medium** | **Concept: LAG on ordered set**

List products ordered by price. Show the price difference between the current product and the previous one in the same category.

```sql
-- Write your solution here
```

---

### 🎯 Problem 41: CUM_DIST Analysis
**Difficulty: Medium** | **Concept: CUME_DIST()**

Show the cumulative distribution of customer spending (percentage of customers spending less than or equal to the current customer).

```sql
-- Write your solution here
```

---

### 🎯 Problem 42: Moving Median
**Difficulty: Hard** | **Concept: PERCENTILE_CONT simulation**

Calculate the 5-order moving median order amount per customer.

```sql
-- Write your solution here
```

---

### 🎯 Problem 43: Row Between Dates
**Difficulty: Hard** | **Concept: RANGE BETWEEN**

Calculate the running sum of orders for exactly the last 30 days for each order date.

```sql
-- Write your solution here
```

---

### 🎯 Problem 44: Rank Change
**Difficulty: Hard** | **Concept: Rank Comparison**

Find employees whose salary rank within their department has improved compared to a theoretical previous rank (use hire_date as proxy for seniority rank).

```sql
-- Write your solution here
```

---

### 🎯 Problem 45: Department Breadth
**Difficulty: Medium** | **Concept: COUNT(DISTINCT) OVER**

Rank departments by the number of unique product categories purchased for their employees.

```sql
-- Write your solution here
```

---

### 🎯 Problem 46: Running Count Distinct
**Difficulty: Hard** | **Concept: Simulated Running Count Distinct**

Calculate a running count of unique customers who have made purchases up to each date in the year.

```sql
-- Write your solution here
```

---

### 🎯 Problem 47: Windowing on Strings
**Difficulty: Medium** | **Concept: FIRST_VALUE with String order**

For each city, find the alphabetically first and last customer name using window functions.

```sql
-- Write your solution here
```

---

### 🎯 Problem 48: Percent of Total
**Difficulty: Medium** | **Concept: SUM() OVER / Total**

Calculate each order's amount as a percentage of the total revenue in its corresponding month.

```sql
-- Write your solution here
```

---

### 🎯 Problem 49: Date Gaps with LEAD
**Difficulty: Medium** | **Concept: LEAD() date subtraction**

Find orders that were placed more than 30 days after the customer's previous order.

```sql
-- Write your solution here
```

---

### 🎯 Problem 50: Weighted Average
**Difficulty: Hard** | **Concept: Product Sum / Count**

Calculate the weighted average price of products sold in each category (where weight = quantity sold per order).

```sql
-- Write your solution here
```

---

## 🌲 Part 3: Advanced CTEs & Recursion (Problems 51-70)

---

### 🎯 Problem 51: Chained CTE Aggregation
**Difficulty: Medium** | **Concept: Multiple CTEs**

Use CTEs to find customers whose average items per order is higher than their category's global average.

```sql
-- Write your solution here
```

---

### 🎯 Problem 52: Recursive Fibonacci
**Difficulty: hard** | **Concept: Recursive CTE (Math)**

Generate the first 20 Fibonacci numbers using a recursive CTE.

```sql
-- Write your solution here
```

---

### 🎯 Problem 53: Menu Hierarchy
**Difficulty: Hard** | **Concept: Recursive CTE (Trees)**

Create a recursive CTE to represent a 3-level website menu: Category -> Subcategory -> Product.

```sql
-- Write your solution here
```

---

### 🎯 Problem 54: Path Finder
**Difficulty: Hard** | **Concept: Recursive Pathing**

For a given employee, use recursion to show the management path from them up to the CEO, including the total salary of everyone in that path.

```sql
-- Write your solution here
```

---

### 🎯 Problem 55: Recursive Date Gaps
**Difficulty: Medium** | **Concept: Recursive Series**

Generate a series of dates for the next 52 Mondays starting from '2024-01-01'.

```sql
-- Write your solution here
```

---

### 🎯 Problem 56: Tree Breadth
**Difficulty: Hard** | **Concept: Level Tracking**

Count how many direct reports each manager has at each level of the hierarchy using a recursive CTE.

```sql
-- Write your solution here
```

---

### 🎯 Problem 57: Cycle Detection
**Difficulty: Hard** | **Concept: Cycle Check in Recursion**

Write a query that detects if there is a circular dependency in the `employees.manager_id` column (e.g., A manages B, B manages A).

```sql
-- Write your solution here
```

---

### 🎯 Problem 58: Running Inventory
**Difficulty: Medium** | **Concept: CTE State Tracking**

Use a CTE to calculate the current stock of each product by subtracting `order_items.quantity` from a starting inventory constant.

```sql
-- Write your solution here
```

---

### 🎯 Problem 59: CTE for Deduplication
**Difficulty: Medium** | **Concept: ROW_NUMBER inside CTE**

Write a query using a CTE and `ROW_NUMBER` to select only the most recent order for each customer, including all order details.

```sql
-- Write your solution here
```

---

### 🎯 Problem 60: Flattening Data
**Difficulty: Medium** | **Concept: Aggregation inside CTE**

Use a CTE to transform a multi-row order list into a single row per customer with a comma-separated list of order IDs.

```sql
-- Write your solution here
```

---

### 🎯 Problem 61: Multi-level Commission
**Difficulty: Hard** | **Concept: Hierarchical Aggregation**

Calculate salesperson commission where they get 5% of their own sales and 2% of the sales of everyone they manage.

```sql
-- Write your solution here
```

---

### 🎯 Problem 62: Recursive String Splitting
**Difficulty: Hard** | **Concept: String Manipulation Recursion**

Use a recursive CTE to split a comma-separated string of IDs into individual rows.

```sql
-- Write your solution here
```

---

### 🎯 Problem 63: Cohort Base
**Difficulty: Medium** | **Concept: Categorical filtering in CTE**

Create a CTE that defines "New Customers" (first order in Q1) and then join it to find their total Q2 spend.

```sql
-- Write your solution here
```

---

### 🎯 Problem 64: Recursive Factorial
**Difficulty: Medium** | **Concept: Recursive Math**

Calculate the factorial of 10 using a recursive CTE.

```sql
-- Write your solution here
```

---

### 🎯 Problem 65: Employee Siblings
**Difficulty: Easy** | **Concept: Self-pointing logic**

For each employee, find how many other employees report to the same manager.

```sql
-- Write your solution here
```

---

### 🎯 Problem 66: CTE Ranking
**Difficulty: Medium** | **Concept: Multi-factor scoring**

Calculate a custom score: `(OrderCount * 2) + AverageOrderAmount`. Rank customers by this score using CTEs.

```sql
-- Write your solution here
```

---

### 🎯 Problem 67: Hierarchical Path
**Difficulty: Hard** | **Concept: String Aggregation in Path**

Show the full path for all products in the hierarchy as `MainCategory > SubCategory > Product`.

```sql
-- Write your solution here
```

---

### 🎯 Problem 68: Filling Missing Months
**Difficulty: Hard** | **Concept: LEFT JOIN on Generated Series**

Use a recursive CTE to generate all months in 2024 and LEFT JOIN it with sales data to show $0 for months with no sales.

```sql
-- Write your solution here
```

---

### 🎯 Problem 69: Longest Chain
**Difficulty: Hard** | **Concept: Depth Tracking**

Find the employee who has the most levels of management above them (the deepest leaf in the tree).

```sql
-- Write your solution here
```

---

### 🎯 Problem 70: CTE Pivot
**Difficulty: Hard** | **Concept: Pivoting with CTE**

Use CTEs to pivot the `orders` table to show months as columns and total sales as rows for each customer.

```sql
-- Write your solution here
```

---

## 📈 Part 4: Data Analysis & Business Logic (Problems 71-85)

---

### 🎯 Problem 71: MoM Growth
**Difficulty: Medium** | **Concept: Percentage Change over Window**

Calculate the percentage change in revenue from one month to the next for the entire year 2024.

```sql
-- Write your solution here
```

---

### 🎯 Problem 72: Customer Retention
**Difficulty: Medium** | **Concept: Intersection / Semi-JOIN**

Find customers who placed an order in January 2024 and *also* placed an order in February 2024.

```sql
-- Write your solution here
```

---

### 🎯 Problem 73: Churn Analysis
**Difficulty: Medium** | **Concept: EXCEPT / NOT EXISTS**

Find customers who placed an order in Q1 2024 but have zero orders in Q2 2024.

```sql
-- Write your solution here
```

---

### 🎯 Problem 74: Pareto Principle (80/20)
**Difficulty: Hard** | **Concept: Cumulative Share**

Identify the top 20% of products (by count) that generate 80% of the total revenue.

```sql
-- Write your solution here
```

---

### 🎯 Problem 75: Repeat Buyer Rate
**Difficulty: Medium** | **Concept: Ratio calculation**

Calculate the percentage of customers who have placed more than one order lifetime.

```sql
-- Write your solution here
```

---

### 🎯 Problem 76: AOV Trend
**Difficulty: Medium** | **Concept: Rolling AOV**

Show the 3-month rolling average of the "Average Order Value" (AOV).

```sql
-- Write your solution here
```

---

### 🎯 Problem 77: New vs Returning Revenue
**Difficulty: Hard** | **Concept: First-order tagging**

For each month, show the total revenue from First-time customers vs Returning customers.

```sql
-- Write your solution here
```

---

### 🎯 Problem 78: Order Item Density
**Difficulty: Easy** | **Concept: COUNT(DISTINCT) per group**

Find orders that contain more than 5 different types of products.

```sql
-- Write your solution here
```

---

### 🎯 Problem 79: City Revenue Concentration
**Difficulty: Hard** | **Concept: Contribution Share**

Identify cities where a single customer accounts for more than 50% of the city's total revenue.

```sql
-- Write your solution here
```

---

### 🎯 Problem 80: Basket Analysis
**Difficulty: Hard** | **Concept: Self-JOIN combinations**

Find the pair of products that are most frequently bought together in the same order.

```sql
-- Write your solution here
```

---

### 🎯 Problem 81: Revenue Leakage
**Difficulty: Medium** | **Concept: Price Variance Analysis**

Find products that have a `unit_price` in `order_items` that is 20% lower than the standard `price` in the `products` table.

```sql
-- Write your solution here
```

---

### 🎯 Problem 82: Customer Tier Migration
**Difficulty: Hard** | **Concept: State Transition Analysis**

Identify customers who moved from the 'Bronze' tier (spend < 1000) to 'Gold' tier (spend > 5000) within exactly a 6-month period.

```sql
-- Write your solution here
```

---

### 🎯 Problem 83: Weekday vs Weekend
**Difficulty: Medium** | **Concept: EXTRACT(DOW)**

Calculate the total revenue and average order value for Weekdays vs Weekends.

```sql
-- Write your solution here
```

---

### 🎯 Problem 84: Abandoned Product
**Difficulty: Medium** | **Concept: Ratio filtering**

Find products that have been added to at least 5 orders but have a status of 'cancelled' in 100% of those orders.

```sql
-- Write your solution here
```

---

### 🎯 Problem 85: Inventory Turnover
**Difficulty: Hard** | **Concept: Financial Business Logic**

Calculate how many times the average inventory was sold over the year (Inventory Turnover Ratio).

```sql
-- Write your solution here
```

---

## ⚡ Part 5: Query Optimization & Performance (Problems 86-100)

---

### 🎯 Problem 86: Refactor Scalar Subquery
**Difficulty: Medium** | **Concept: JOIN optimization**

Convert a slow scalar subquery in the SELECT clause (e.g., fetching department name for every employee) into a more efficient JOIN.

```sql
-- Write your solution here
```

---

### 🎯 Problem 87: Avoiding OR
**Difficulty: Medium** | **Concept: UNION vs OR for indexing**

Refactor a query with multiple `OR` conditions in `WHERE` into a `UNION` or `IN` clause to ensure the database can utilize indexes.

```sql
-- Write your solution here
```

---

### 🎯 Problem 88: Index-Friendly Filtering
**Difficulty: Easy** | **Concept: Sargability**

Rewrite `WHERE YEAR(hire_date) = 2024` to be index-friendly (sargable).

```sql
-- Write your solution here
```

---

### 🎯 Problem 89: Exists vs Count
**Difficulty: Medium** | **Concept: EXISTS Semi-JOIN**

Rewrite a query that uses `COUNT(*) > 0` in a subquery to use the more efficient `EXISTS` keyword.

```sql
-- Write your solution here
```

---

### 🎯 Problem 90: Sargability Check
**Difficulty: Medium** | **Concept: Arithmetic in WHERE**

Identify why `WHERE price * 1.1 > 100` might lead to a full table scan and rewrite it more efficiently.

```sql
-- Write your solution here
```

---

### 🎯 Problem 91: Data Type Mismatch
**Difficulty: Medium** | **Concept: Implicit Casting overhead**

(Conceptual/Code) Write a query that shows how to correctly join a table where the ID is stored as `VARCHAR` to a table where it is `INT` without losing index performance.

```sql
-- Write your solution here
```

---

### 🎯 Problem 92: Partial Index Advantage
**Difficulty: Hard** | **Concept: Partial Index Utilization**

Write a query that explicitly targets an existing partial index (e.g., where `status = 'pending'`) to avoid scanning the entire orders table.

```sql
-- Write your solution here
```

---

### 🎯 Problem 93: CTE Materialization
**Difficulty: Hard** | **Concept: MATERIALIZED vs INLINE**

Explain or demonstrate using a CTE hint (PostgreSQL) to force materialization of a complex subquery that is reused multiple times.

```sql
-- Write your solution here
```

---

### 🎯 Problem 94: Refactor NOT IN
**Difficulty: Medium** | **Concept: NOT EXISTS vs NOT IN**

Rewrite a query using `NOT IN` (which can be slow and bug-prone with NULLs) to use `NOT EXISTS`.

```sql
-- Write your solution here
```

---

### 🎯 Problem 95: Eliminating DISTINCT
**Difficulty: Hard** | **Concept: Semi-JOIN vs DISTINCT**

Refactor a query where a `DISTINCT` is used to uniquely identify customers who have orders. Use `EXISTS` to achieve the same result potentially faster.

```sql
-- Write your solution here
```

---

### 🎯 Problem 96: Joining on Functions
**Difficulty: Hard** | **Concept: Functional Indexes**

Explain why `JOIN table ON LOWER(email)` is slow and suggest a better approach involving a functional index.

```sql
-- Write your solution here
```

---

### 🎯 Problem 97: Query Plan Analysis
**Difficulty: Hard** | **Concept: EXPLAIN ANALYZE**

Given a hypothetical query plan with a "Parallel Seq Scan" on a large table, write the `CREATE INDEX` statement that would most likely switch it to an "Index Only Scan".

```sql
-- Write your solution here
```

---

### 🎯 Problem 98: Window vs Self-Join
**Difficulty: Medium** | **Concept: LAG() vs Self-JOIN**

Rewrite a query that uses a self-join for "Previous Day Sales" calculation to use the `LAG()` window function for better performance.

```sql
-- Write your solution here
```

---

### 🎯 Problem 99: Limit & Sort
**Difficulty: Medium** | **Concept: Index-backed MIN/MAX**

Explain the performance difference between `SELECT amount FROM orders ORDER BY amount LIMIT 1` and `SELECT MIN(amount) FROM orders` when an index exists.

```sql
-- Write your solution here
```

---

### 🎯 Problem 100: The "Big Table" Strategy
**Difficulty: Hard** | **Concept: Partitioning / Indexing Strategy**

(Conceptual) Propose a high-performance strategy for querying a 1-Billion row sensor data table where you only ever need the last 2 hours of data.

```sql
-- Write your solution here
```

---

## ✅ Practice Checklist
- [ ] Attempted 1-25 (Joins)
- [ ] Attempted 26-50 (Window)
- [ ] Attempted 51-70 (CTEs)
- [ ] Attempted 71-85 (Analysis)
- [ ] Attempted 86-100 (Optimization)

**Start solving and check your progress in `solutions.md`!**
