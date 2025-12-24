-- models/marts/dim_users.sql

WITH staging AS (
    SELECT * FROM {{ ref('stg_users') }}
)

SELECT
    user_id,
    full_name,
    joined_at,
    -- Simple Business Logic: Cohort calculation
    DATE_TRUNC('month', joined_at) as signup_cohort
FROM staging
WHERE is_active_flag = true
