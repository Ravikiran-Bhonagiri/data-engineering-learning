# Sample Data Setup Guide

**Problem Solved:** You need raw data to practice with dbt.

This file provides complete SQL scripts to create sample databases for all examples and exercises.

---

## Option 1: E-Commerce Database (For Examples 1-2 and Days 1-7)

### Step 1: Create Schema

```sql
-- PostgreSQL / Redshift / Snowflake
CREATE SCHEMA IF NOT EXISTS raw;

-- BigQuery
CREATE SCHEMA IF NOT EXISTS `your_project.raw`;
```

### Step 2: Create Tables

```sql
-- Customers table
CREATE TABLE raw.customers (
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(2),
    customer_segment VARCHAR(20),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Products table
CREATE TABLE raw.products (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2),
    cost DECIMAL(10,2),
    created_at TIMESTAMP
);

-- Orders table
CREATE TABLE raw.orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    status VARCHAR(20),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Order Items table
CREATE TABLE raw.order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    created_at TIMESTAMP
);
```

### Step 3: Insert Sample Data

```sql
-- Insert Customers (8 records)
INSERT INTO raw.customers VALUES
(1, 'John', 'Doe', 'john.doe@email.com', 'New York', 'NY', 'VIP', '2023-01-15 10:00:00', '2024-01-15 10:00:00'),
(2, 'Jane', 'Smith', 'jane.smith@email.com', 'Los Angeles', 'CA', 'Regular', '2023-02-20 11:30:00', '2024-02-20 11:30:00'),
(3, 'Bob', 'Johnson', 'bob.j@email.com', 'Chicago', 'IL', 'New', '2023-03-10 09:15:00', '2024-03-10 09:15:00'),
(4, 'Alice', 'Williams', 'alice.w@email.com', 'Houston', 'TX', 'VIP', '2023-01-25 14:20:00', '2024-01-25 14:20:00'),
(5, 'Charlie', 'Brown', 'charlie.b@email.com', 'Phoenix', 'AZ', 'Regular', '2023-04-05 16:45:00', '2024-04-05 16:45:00'),
(6, 'Diana', 'Davis', 'diana.d@email.com', 'San Francisco', 'CA', 'VIP', '2023-02-14 08:30:00', '2024-02-14 08:30:00'),
(7, 'Eve', 'Miller', 'eve.m@email.com', 'Seattle', 'WA', 'Regular', '2023-05-18 12:00:00', '2024-05-18 12:00:00'),
(8, 'Frank', 'Wilson', 'frank.w@email.com', 'Boston', 'MA', 'New', '2023-06-22 15:30:00', '2024-06-22 15:30:00');

-- Insert Products (8 records)
INSERT INTO raw.products VALUES
(1, 'Laptop Pro', 'Electronics', 1299.99, 800.00, '2023-01-01 00:00:00'),
(2, 'Wireless Mouse', 'Electronics', 29.99, 12.00, '2023-01-01 00:00:00'),
(3, 'Office Desk', 'Furniture', 349.99, 180.00, '2023-01-01 00:00:00'),
(4, 'Ergonomic Chair', 'Furniture', 249.99, 120.00, '2023-01-01 00:00:00'),
(5, 'USB-C Cable', 'Electronics', 19.99, 5.00, '2023-01-01 00:00:00'),
(6, 'Monitor 27"', 'Electronics', 399.99, 220.00, '2023-01-01 00:00:00'),
(7, 'Desk Lamp', 'Furniture', 49.99, 20.00, '2023-01-01 00:00:00'),
(8, 'Notebook Set', 'Office', 14.99, 6.00, '2023-01-01 00:00:00');

-- Insert Orders (12 records)
INSERT INTO raw.orders VALUES
(1, 1, '2024-01-05', 'delivered', '2024-01-05 10:00:00', '2024-01-05 10:00:00'),
(2, 2, '2024-01-08', 'delivered', '2024-01-08 11:00:00', '2024-01-08 11:00:00'),
(3, 1, '2024-01-15', 'delivered', '2024-01-15 14:00:00', '2024-01-15 14:00:00'),
(4, 3, '2024-01-20', 'shipped', '2024-01-20 09:00:00', '2024-01-20 09:00:00'),
(5, 4, '2024-02-01', 'delivered', '2024-02-01 16:00:00', '2024-02-01 16:00:00'),
(6, 2, '2024-02-10', 'delivered', '2024-02-10 12:00:00', '2024-02-10 12:00:00'),
(7, 5, '2024-02-15', 'pending', '2024-02-15 10:30:00', '2024-02-15 10:30:00'),
(8, 6, '2024-03-01', 'delivered', '2024-03-01 13:00:00', '2024-03-01 13:00:00'),
(9, 1, '2024-03-10', 'delivered', '2024-03-10 15:00:00', '2024-03-10 15:00:00'),
(10, 7, '2024-03-20', 'cancelled', '2024-03-20 11:00:00', '2024-03-20 11:00:00'),
(11, 4, '2024-04-05', 'delivered', '2024-04-05 14:00:00', '2024-04-05 14:00:00'),
(12, 8, '2024-04-15', 'delivered', '2024-04-15 16:00:00', '2024-04-15 16:00:00');

-- Insert Order Items (19 records)
INSERT INTO raw.order_items VALUES
(1, 1, 1, 1, 1299.99, '2024-01-05 10:00:00'),
(2, 1, 2, 2, 29.99, '2024-01-05 10:00:00'),
(3, 2, 3, 1, 349.99, '2024-01-08 11:00:00'),
(4, 2, 4, 1, 249.99, '2024-01-08 11:00:00'),
(5, 3, 6, 1, 399.99, '2024-01-15 14:00:00'),
(6, 3, 5, 3, 19.99, '2024-01-15 14:00:00'),
(7, 4, 8, 5, 14.99, '2024-01-20 09:00:00'),
(8, 5, 1, 1, 1299.99, '2024-02-01 16:00:00'),
(9, 5, 6, 1, 399.99, '2024-02-01 16:00:00'),
(10, 6, 2, 1, 29.99, '2024-02-10 12:00:00'),
(11, 6, 5, 2, 19.99, '2024-02-10 12:00:00'),
(12, 7, 7, 1, 49.99, '2024-02-15 10:30:00'),
(13, 8, 1, 2, 1299.99, '2024-03-01 13:00:00'),
(14, 8, 4, 1, 249.99, '2024-03-01 13:00:00'),
(15, 9, 3, 1, 349.99, '2024-03-10 15:00:00'),
(16, 9, 7, 1, 49.99, '2024-03-10 15:00:00'),
(17, 11, 6, 1, 399.99, '2024-04-05 14:00:00'),
(18, 12, 8, 10, 14.99, '2024-04-15 16:00:00'),
(19, 12, 5, 5, 19.99, '2024-04-15 16:00:00');
```

### Step 4: Verify Data

```sql
SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM raw.customers
UNION ALL
SELECT 'products', COUNT(*) FROM raw.products
UNION ALL
SELECT 'orders', COUNT(*) FROM raw.orders
UNION ALL
SELECT 'order_items', COUNT(*) FROM raw.order_items;
```

Expected output:
```
table_name   | row_count
-------------|----------
customers    | 8
products     | 8
orders       | 12
order_items  | 19
```

---

## Option 2: HR Analytics Database (For Practice Exercise 1)

```sql
-- Create tables
CREATE TABLE raw.employees (
    id INTEGER PRIMARY KEY,
    full_name VARCHAR(100),
    email VARCHAR(100),
    department VARCHAR(50),
    manager_id INTEGER,
    hire_date DATE,
    salary DECIMAL(10,2)
);

CREATE TABLE raw.projects (
    id INTEGER PRIMARY KEY,
    project_name VARCHAR(100),
    client_name VARCHAR(100),
    budget DECIMAL(12,2),
    start_date DATE,
    end_date DATE,
    status VARCHAR(20)
);

CREATE TABLE raw.time_entries (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    project_id INTEGER,
    date DATE,
    hours_worked DECIMAL(4,2)
);

CREATE TABLE raw.performance_reviews (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    review_date DATE,
    rating INTEGER,
    reviewer_id INTEGER
);

-- Insert sample data
INSERT INTO raw.employees VALUES
(1, 'Sarah Connor', 'sarah.c@company.com', 'Engineering', NULL, '2020-01-15', 120000),
(2, 'John Smith', 'john.s@company.com', 'Engineering', 1, '2021-03-20', 95000),
(3, 'Emily Davis', 'emily.d@company.com', 'Marketing', NULL, '2020-06-10', 85000),
(4, 'Michael Brown', 'michael.b@company.com', 'Marketing', 3, '2022-01-05', 70000),
(5, 'Lisa Anderson', 'lisa.a@company.com', 'Sales', NULL, '2019-11-01', 110000);

INSERT INTO raw.projects VALUES
(1, 'Website Redesign', 'Acme Corp', 50000, '2024-01-01', '2024-03-31', 'completed'),
(2, 'Mobile App', 'Tech Inc', 80000, '2024-02-01', '2024-06-30', 'active'),
(3, 'Marketing Campaign', 'Retail Co', 30000, '2024-01-15', '2024-02-28', 'completed');

INSERT INTO raw.time_entries VALUES
(1, 2, 1, '2024-01-05', 8.0),
(2, 2, 1, '2024-01-06', 7.5),
(3, 4, 3, '2024-01-15', 6.0),
(4, 2, 2, '2024-02-01', 8.0);

INSERT INTO raw.performance_reviews VALUES
(1, 2, '2024-01-31', 4, 1),
(2, 4, '2024-01-31', 5, 3);
```

---

## Option 3: Quick Start with dbt Seed

Alternatively, use dbt's built-in CSV loader:

### Step 1: Create CSV files in `seeds/` directory

**seeds/raw_customers.csv:**
```csv
id,first_name,last_name,email,city,state,customer_segment,created_at
1,John,Doe,john.doe@email.com,New York,NY,VIP,2023-01-15
2,Jane,Smith,jane.smith@email.com,Los Angeles,CA,Regular,2023-02-20
```

### Step 2: Load seeds

```bash
dbt seed
```

### Step 3: Use in models

```sql
SELECT * FROM {{ ref('raw_customers') }}
```

---

## Quick Test Query

After loading data, verify everything works:

```sql
SELECT 
    c.first_name,
    c.last_name,
    COUNT(o.id) AS total_orders,
    SUM(oi.quantity * oi.unit_price) AS total_spent
FROM raw.customers c
LEFT JOIN raw.orders o ON c.id = o.customer_id
LEFT JOIN raw.order_items oi ON o.id = oi.order_id
WHERE o.status != 'cancelled' OR o.status IS NULL
GROUP BY 1, 2
ORDER BY total_spent DESC;
```

---

**You're ready to start learning dbt!** 🚀
