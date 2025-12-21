# End-to-End dbt Examples (With Solutions)

Complete, production-ready dbt project examples from start to finish.

---

## Example 1: E-Commerce Revenue Analytics

**Scenario:** Build a complete analytics pipeline to track product revenue, customer segments, and order trends.

### Setup: Raw Data

Assume you have these raw tables:

```sql
-- raw.customers
CREATE TABLE raw.customers (
    id INT,
    email VARCHAR,
    first_name VARCHAR,
    last_name VARCHAR,
    city VARCHAR,
    state VARCHAR,
    customer_segment VARCHAR, -- 'VIP', 'Regular', 'New'
    created_at TIMESTAMP
);

-- raw.products
CREATE TABLE raw.products (
    id INT,
    name VARCHAR,
    category VARCHAR,
    price DECIMAL(10,2),
    cost DECIMAL(10,2)
);

-- raw.orders
CREATE TABLE raw.orders (
    id INT,
    customer_id INT,
    order_date DATE,
    status VARCHAR, -- 'pending', 'shipped', 'delivered', 'cancelled'
    created_at TIMESTAMP
);

-- raw.order_items
CREATE TABLE raw.order_items (
    id INT,
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2)
);
```

---

### Step 1: Define Sources

**File:** `models/staging/ecommerce/sources.yml`
```yaml
version: 2

sources:
  - name: ecommerce
    database: raw
    schema: raw
    tables:
      - name: customers
        columns:
          - name: id
            tests:
              - unique
              - not_null
      
      - name: products
        columns:
          - name: id
            tests:
              - unique
              - not_null
      
      - name: orders
        loaded_at_field: created_at
        freshness:
          warn_after: {count: 24, period: hour}
      
      - name: order_items
```

---

### Step 2: Staging Models

**File:** `models/staging/ecommerce/stg_ecommerce__customers.sql`
```sql
WITH source AS (
    SELECT * FROM {{ source('ecommerce', 'customers') }}
),

cleaned AS (
    SELECT
        id AS customer_id,
        LOWER(TRIM(email)) AS email,
        INITCAP(first_name) AS first_name,
        INITCAP(last_name) AS last_name,
        UPPER(state) AS state,
        city,
        customer_segment,
        created_at,
        CURRENT_TIMESTAMP AS _loaded_at
    FROM source
    WHERE email IS NOT NULL
)

SELECT * FROM cleaned
```

**File:** `models/staging/ecommerce/stg_ecommerce__products.sql`
```sql
SELECT
    id AS product_id,
    name AS product_name,
    category,
    price,
    cost,
    ROUND(price - cost, 2) AS profit_per_unit,
    ROUND((price - cost) / NULLIF(price, 0) * 100, 2) AS margin_pct
FROM {{ source('ecommerce', 'products') }}
```

**File:** `models/staging/ecommerce/stg_ecommerce__orders.sql`
```sql
SELECT
    id AS order_id,
    customer_id,
    order_date,
    status,
    created_at,
    CASE 
        WHEN status = 'delivered' THEN TRUE
        ELSE FALSE
    END AS is_completed
FROM {{ source('ecommerce', 'orders') }}
WHERE status != 'cancelled'
```

**File:** `models/staging/ecommerce/stg_ecommerce__order_items.sql`
```sql
SELECT
    id AS order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    ROUND(quantity * unit_price, 2) AS line_total
FROM {{ source('ecommerce', 'order_items') }}
WHERE quantity > 0
```

---

### Step 3: Intermediate Models

**File:** `models/intermediate/int_order_details.sql`
```sql
WITH orders AS (
    SELECT * FROM {{ ref('stg_ecommerce__orders') }}
),

order_items AS (
    SELECT * FROM {{ ref('stg_ecommerce__order_items') }}
),

products AS (
    SELECT * FROM {{ ref('stg_ecommerce__products') }}
),

order_item_details AS (
    SELECT
        oi.order_item_id,
        oi.order_id,
        o.customer_id,
        o.order_date,
        o.status,
        o.is_completed,
        oi.product_id,
        p.product_name,
        p.category,
        oi.quantity,
        oi.unit_price,
        oi.line_total,
        p.cost * oi.quantity AS line_cost,
        oi.line_total - (p.cost * oi.quantity) AS line_profit
    FROM order_items oi
    INNER JOIN orders o ON oi.order_id = o.order_id
    INNER JOIN products p ON oi.product_id = p.product_id
)

SELECT * FROM order_item_details
```

---

### Step 4: Mart Models (Final Analytics Tables)

**File:** `models/marts/fct_orders.sql`
```sql
{{ config(materialized='table') }}

WITH order_details AS (
    SELECT * FROM {{ ref('int_order_details') }}
),

order_aggregates AS (
    SELECT
        order_id,
        customer_id,
        order_date,
        status,
        is_completed,
        COUNT(DISTINCT product_id) AS product_count,
        SUM(quantity) AS total_items,
        SUM(line_total) AS order_revenue,
        SUM(line_cost) AS order_cost,
        SUM(line_profit) AS order_profit,
        ROUND(SUM(line_profit) / NULLIF(SUM(line_total), 0) * 100, 2) AS profit_margin_pct
    FROM order_details
    GROUP BY 1, 2, 3, 4, 5
)

SELECT * FROM order_aggregates
```

**File:** `models/marts/dim_customers.sql`
```sql
{{ config(materialized='table') }}

WITH customers AS (
    SELECT * FROM {{ ref('stg_ecommerce__customers') }}
),

orders AS (
    SELECT * FROM {{ ref('fct_orders') }}
),

customer_metrics AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(CASE WHEN is_completed THEN 1 ELSE 0 END) AS completed_orders,
        SUM(order_revenue) AS lifetime_revenue,
        SUM(order_profit) AS lifetime_profit,
        AVG(order_revenue) AS avg_order_value,
        MIN(order_date) AS first_order_date,
        MAX(order_date) AS last_order_date,
        MAX(order_date) - MIN(order_date) AS customer_tenure_days
    FROM orders
    GROUP BY 1
),

final AS (
    SELECT
        c.customer_id,
        c.first_name || ' ' || c.last_name AS full_name,
        c.email,
        c.state,
        c.city,
        c.customer_segment,
        c.created_at AS customer_since,
        COALESCE(cm.total_orders, 0) AS total_orders,
        COALESCE(cm.completed_orders, 0) AS completed_orders,
        COALESCE(cm.lifetime_revenue, 0) AS lifetime_revenue,
        COALESCE(cm.lifetime_profit, 0) AS lifetime_profit,
        COALESCE(cm.avg_order_value, 0) AS avg_order_value,
        cm.first_order_date,
        cm.last_order_date,
        cm.customer_tenure_days,
        CASE
            WHEN cm.total_orders >= 10 THEN 'High Value'
            WHEN cm.total_orders >= 5 THEN 'Medium Value'
            WHEN cm.total_orders >= 1 THEN 'Low Value'
            ELSE 'No Orders'
        END AS value_tier
    FROM customers c
    LEFT JOIN customer_metrics cm ON c.customer_id = cm.customer_id
)

SELECT * FROM final
```

**File:** `models/marts/fct_product_performance.sql`
```sql
{{ config(materialized='table') }}

WITH order_details AS (
    SELECT * FROM {{ ref('int_order_details') }}
),

product_metrics AS (
    SELECT
        product_id,
        product_name,
        category,
        COUNT(DISTINCT order_id) AS times_ordered,
        COUNT(DISTINCT customer_id) AS unique_customers,
        SUM(quantity) AS total_units_sold,
        SUM(line_total) AS total_revenue,
        SUM(line_profit) AS total_profit,
        ROUND(AVG(line_profit / NULLIF(quantity, 0)), 2) AS avg_profit_per_unit,
        MIN(order_date) AS first_sale_date,
        MAX(order_date) AS last_sale_date
    FROM order_details
    WHERE is_completed = TRUE
    GROUP BY 1, 2, 3
),

ranked AS (
    SELECT
        *,
        RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank,
        RANK() OVER (ORDER BY total_profit DESC) AS profit_rank,
        RANK() OVER (PARTITION BY category ORDER BY total_revenue DESC) AS category_revenue_rank
    FROM product_metrics
)

SELECT * FROM ranked
```

---

### Step 5: Tests

**File:** `models/marts/schema.yml`
```yaml
version: 2

models:
  - name: fct_orders
    description: "Fact table with order-level metrics"
    columns:
      - name: order_id
        description: "Unique order identifier"
        tests:
          - unique
          - not_null
      - name: order_revenue
        tests:
          - dbt_utils.expression_is_true:
              expression: ">= 0"

  - name: dim_customers
    description: "Customer dimension with lifetime metrics"
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
      - name: email
        tests:
          - unique
          - not_null
      - name: total_orders
        tests:
          - dbt_utils.expression_is_true:
              expression: ">= 0"
```

**File:** `tests/data_quality/orders_have_items.sql`
```sql
-- Every order should have at least one order item
SELECT o.order_id
FROM {{ ref('fct_orders') }} o
LEFT JOIN {{ ref('int_order_details') }} oi 
    ON o.order_id = oi.order_id
WHERE oi.order_id IS NULL
```

---

### Step 6: Run Everything

```bash
# Install dependencies (if using dbt_utils)
dbt deps

# Run all models
dbt run

# Run tests
dbt test

# Generate docs
dbt docs generate
dbt docs serve
```

---

## Example 2: Customer Cohort Analysis

**Scenario:** Track customer retention by signup cohort.

### Mart Model

**File:** `models/marts/fct_customer_cohorts.sql`
```sql
{{ config(materialized='table') }}

WITH customers AS (
    SELECT * FROM {{ ref('dim_customers') }}
),

orders AS (
    SELECT * FROM {{ ref('fct_orders') }}
    WHERE is_completed = TRUE
),

customer_cohorts AS (
    SELECT
        c.customer_id,
        DATE_TRUNC('month', c.customer_since) AS cohort_month,
        o.order_date,
        DATE_TRUNC('month', o.order_date) AS order_month,
        DATEDIFF('month', 
            DATE_TRUNC('month', c.customer_since),
            DATE_TRUNC('month', o.order_date)
        ) AS months_since_signup,
        o.order_revenue
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
),

cohort_metrics AS (
    SELECT
        cohort_month,
        months_since_signup,
        COUNT(DISTINCT customer_id) AS active_customers,
        SUM(order_revenue) AS cohort_revenue,
        AVG(order_revenue) AS avg_order_value
    FROM customer_cohorts
    GROUP BY 1, 2
),

cohort_sizes AS (
    SELECT
        cohort_month,
        COUNT(DISTINCT customer_id) AS cohort_size
    FROM customers
    GROUP BY 1
),

final AS (
    SELECT
        cm.cohort_month,
        cs.cohort_size,
        cm.months_since_signup,
        cm.active_customers,
        ROUND(cm.active_customers::DECIMAL / cs.cohort_size * 100, 2) AS retention_pct,
        cm.cohort_revenue,
        cm.avg_order_value
    FROM cohort_metrics cm
    INNER JOIN cohort_sizes cs ON cm.cohort_month = cs.cohort_month
)

SELECT * FROM final
ORDER BY cohort_month, months_since_signup
```

### Macro for Reusable Logic

**File:** `macros/cohort_analysis.sql`
```sql
{% macro months_between(start_date, end_date) %}
    DATEDIFF('month',
        DATE_TRUNC('month', {{ start_date }}),
        DATE_TRUNC('month', {{ end_date }})
    )
{% endmacro %}
```

**Usage:**
```sql
{{ months_between('customer_since', 'order_date') }} AS months_since_signup
```

---

## Running Both Examples

```bash
# Build everything
dbt build

# Run specific models
dbt run --select fct_orders
dbt run --select dim_customers+  # dim_customers and downstream

# Test specific models
dbt test --select fct_orders

# Run models and their children
dbt run --select fct_orders+
```

---

## Key Takeaways

✅ **Staging → Intermediate → Marts** (proper layering)  
✅ **ref() for dependencies** (automatic DAG)  
✅ **Tests on every fact/dimension** (data quality)  
✅ **Macros for reusable logic** (DRY principle)  
✅ **Materialization configs** (table for marts)  

**You now have 2 complete, production-ready dbt projects!** 🚀
