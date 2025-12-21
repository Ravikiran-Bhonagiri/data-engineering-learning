# 🚀 SQL Course - Day 0: Setup

## Database Setup

Use PostgreSQL, MySQL, or SQLite. Run these commands to set up your practice environment.

---

## 📊 Create Tables

```sql
-- DEPARTMENTS TABLE
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100)
);

-- EMPLOYEES TABLE  
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    department_id INT REFERENCES departments(id),
    manager_id INT REFERENCES employees(id),
    salary DECIMAL(10,2) CHECK (salary > 0),
    hire_date DATE NOT NULL
);

-- CUSTOMERS TABLE
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    city VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

-- PRODUCTS TABLE
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2) CHECK (price >= 0)
);

-- ORDERS TABLE
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    order_date DATE NOT NULL,
    amount DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'pending'
);

-- ORDER_ITEMS TABLE
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id),
    product_id INT REFERENCES products(id),
    quantity INT CHECK (quantity > 0),
    unit_price DECIMAL(10,2)
);
```

---

## 📥 Insert Sample Data

```sql
-- Departments
INSERT INTO departments (name, location) VALUES
('Engineering', 'San Francisco'),
('Sales', 'New York'),
('Marketing', 'Chicago'),
('HR', 'Boston'),
('Finance', 'New York');

-- Employees (12 rows)
INSERT INTO employees (name, email, department_id, manager_id, salary, hire_date) VALUES
('John Smith', 'john@company.com', 1, NULL, 150000, '2019-03-15'),
('Sarah Johnson', 'sarah@company.com', 1, 1, 120000, '2020-06-01'),
('Mike Brown', 'mike@company.com', 1, 1, 95000, '2021-01-10'),
('Emily Davis', 'emily@company.com', 2, NULL, 130000, '2018-09-20'),
('David Wilson', 'david@company.com', 2, 4, 85000, '2020-11-05'),
('Lisa Anderson', 'lisa@company.com', 2, 4, 90000, '2021-03-15'),
('James Taylor', 'james@company.com', 3, NULL, 110000, '2019-07-01'),
('Anna Martinez', 'anna@company.com', 3, 7, 75000, '2022-01-20'),
('Robert Garcia', 'robert@company.com', 4, NULL, 95000, '2020-02-14'),
('Jennifer Lee', 'jennifer@company.com', 5, NULL, 140000, '2017-11-30'),
('Chris Thomas', 'chris@company.com', 1, 2, 80000, '2022-06-01'),
('Amanda White', 'amanda@company.com', 2, 4, 72000, '2023-01-15');

-- Customers (8 rows)
INSERT INTO customers (name, email, city) VALUES
('Acme Corp', 'contact@acme.com', 'New York'),
('Tech Solutions', 'info@techsol.com', 'San Francisco'),
('Global Trade', 'sales@globaltrade.com', 'Chicago'),
('StartUp Inc', 'hello@startup.com', 'Austin'),
('Big Enterprise', 'procurement@bigent.com', 'Seattle'),
('Local Shop', 'owner@localshop.com', 'Boston'),
('Digital Agency', 'team@digitalagency.com', 'Los Angeles'),
('Manufacturing Co', 'orders@mfgco.com', 'Detroit');

-- Products (8 rows)
INSERT INTO products (name, category, price) VALUES
('Laptop Pro', 'Electronics', 1299.99),
('Wireless Mouse', 'Electronics', 49.99),
('Office Chair', 'Furniture', 299.99),
('Standing Desk', 'Furniture', 599.99),
('Monitor 27"', 'Electronics', 399.99),
('Keyboard', 'Electronics', 79.99),
('Webcam HD', 'Electronics', 89.99),
('Desk Lamp', 'Furniture', 45.99);

-- Orders (12 rows)
INSERT INTO orders (customer_id, order_date, amount, status) VALUES
(1, '2024-01-15', 1649.98, 'completed'),
(1, '2024-02-20', 599.99, 'completed'),
(2, '2024-01-20', 2599.98, 'completed'),
(2, '2024-03-10', 129.98, 'completed'),
(3, '2024-02-01', 899.98, 'completed'),
(4, '2024-02-15', 1299.99, 'pending'),
(5, '2024-03-01', 3299.97, 'completed'),
(5, '2024-03-15', 169.98, 'shipped'),
(6, '2024-01-10', 345.98, 'completed'),
(7, '2024-03-20', 1699.98, 'pending'),
(1, '2024-03-25', 479.98, 'pending'),
(3, '2024-04-01', 1299.99, 'pending');

-- Order Items (23 rows)
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 1299.99), (1, 2, 1, 49.99), (1, 6, 4, 79.99),
(2, 4, 1, 599.99),
(3, 1, 2, 1299.99),
(4, 2, 1, 49.99), (4, 6, 1, 79.99),
(5, 3, 1, 299.99), (5, 4, 1, 599.99),
(6, 1, 1, 1299.99),
(7, 1, 2, 1299.99), (7, 5, 1, 399.99), (7, 7, 1, 89.99), (7, 2, 2, 49.99),
(8, 6, 1, 79.99), (8, 7, 1, 89.99),
(9, 3, 1, 299.99), (9, 8, 1, 45.99),
(10, 1, 1, 1299.99), (10, 5, 1, 399.99),
(11, 2, 2, 49.99), (11, 5, 1, 399.99),
(12, 1, 1, 1299.99);
```

---

## ✅ Verify Setup

```sql
-- Check row counts
SELECT 'departments' as table_name, COUNT(*) as rows FROM departments
UNION ALL SELECT 'employees', COUNT(*) FROM employees
UNION ALL SELECT 'customers', COUNT(*) FROM customers
UNION ALL SELECT 'products', COUNT(*) FROM products
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'order_items', COUNT(*) FROM order_items;
```

Expected output:
| table_name | rows |
|------------|------|
| departments | 5 |
| employees | 12 |
| customers | 8 |
| products | 8 |
| orders | 12 |
| order_items | 23 |

---

## 📁 Course Structure

- **Day 1-2**: Basics & CRUD Operations
- **Day 3**: Aggregations & GROUP BY
- **Day 4**: Joins
- **Day 5**: Subqueries & CTEs
- **Day 6**: Window Functions
- **Day 7**: Advanced CTEs & Hierarchies
- **Day 8**: Stored Procedures & Triggers
- **Day 9**: Transactions
- **Day 10**: Performance & Indexing
- **Bonus**: [**100 Advanced Practice Problems**](practice.md)
- **Bonus**: [**Complete Solutions Bank**](solutions.md)

> **Start with Day 1 after running the setup!**
