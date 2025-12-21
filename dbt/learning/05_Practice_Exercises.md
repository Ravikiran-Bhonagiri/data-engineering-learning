# Practice Exercises (End-to-End)

**Goal:** Build complete dbt projects from scratch. No solutions provided - test your skills!

---

## Exercise 1: Employee Performance Analytics

**Domain:** HR Analytics  
**Difficulty:** Medium  
**Estimated Time:** 2-3 hours

### Scenario

You're building an HR analytics platform. Your company has:
- Employees with departments and managers
- Projects that employees work on
- Time tracking (hours logged per project)
- Performance reviews (quarterly ratings)

### Raw Tables

```sql
-- raw.employees
id, full_name, email, department, manager_id, hire_date, salary

-- raw.projects  
id, project_name, client_name, budget, start_date, end_date, status

-- raw.time_entries
id, employee_id, project_id, date, hours_worked

-- raw.performance_reviews
id, employee_id, review_date, rating, reviewer_id
```

### Your Tasks

Build a complete dbt project with:

1. **Staging Models**
   - Clean and standardize all raw tables
   - Add calculated fields where appropriate

2. **Intermediate Models**
   - `int_employee_time_summary`: Hours per employee per project
   - `int_project_team`: Who worked on which projects

3. **Mart Models**
   - `dim_employees`: Employee dimension with manager name, tenure, avg rating
   - `fct_employee_performance`: 
     - Employee ID
     - Total hours worked (all time)
     - Number of projects
     - Average performance rating
     - Billable utilization % (assume 160 hours/month standard)
   - `fct_project_metrics`:
     - Project ID
     - Total hours consumed
     - Number of employees who worked on it
     - Budget vs actual (hours * avg hourly rate)
     - Project ROI

4. **Tests**
   - All primary keys are unique and not null
   - No employee is their own manager
   - Project hours are non-negative
   - Performance ratings are between 1-5

5. **Custom Test**
   - Ensure no employee has >60 hours logged in a single day

6. **Snapshot**
   - Track employee department changes over time

### Deliverables

- Source definitions in YAML
- 4 staging models
- 2 intermediate models
- 3 mart models
- Schema tests
- 1 custom test
- 1 snapshot
- Documentation descriptions

### Success Criteria

- `dbt run` completes without errors
- `dbt test` passes all tests
- `dbt docs generate` creates full lineage
- Models follow naming conventions (`stg_`, `int_`, `fct_`, `dim_`)

---

## Exercise 2: SaaS Subscription Analytics

**Domain:** Subscription Business  
**Difficulty:** Hard  
**Estimated Time:** 3-4 hours

### Scenario

You're building analytics for a SaaS company. Track:
- Customer subscriptions (monthly/annual plans)
- Usage metrics (API calls, active users)
- Upgrades, downgrades, churns
- Revenue recognition (MRR, ARR)

### Raw Tables

```sql
-- raw.accounts
id, company_name, industry, created_at, account_status

-- raw.subscriptions
id, account_id, plan_type, mrr, billing_period, start_date, end_date, status

-- raw.subscription_events
id, subscription_id, event_type, event_date, old_plan, new_plan, old_mrr, new_mrr
-- event_type: 'new', 'upgrade', 'downgrade', 'cancel', 'reactivate'

-- raw.usage_data
id, account_id, date, api_calls, active_users, data_storage_gb
```

### Your Tasks

Build a complete dbt project with:

1. **Staging Models**
   - Clean all raw tables
   - Calculate useful derived fields

2. **Intermediate Models**
   - `int_subscription_history`: Full subscription lifecycle per account
   - `int_monthly_usage`: Aggregated usage per account per month
   - `int_mrr_movements`: MRR changes (new, expansion, contraction, churn)

3. **Mart Models**
   - `dim_accounts`: Account dimension with:
     - Current plan
     - Total lifetime MRR
     - Customer segment (based on MRR: <$100, $100-500, $500+)
     - Tenure (months since signup)
   
   - `fct_monthly_mrr`: Monthly recurring revenue facts:
     - Month
     - Account ID
     - MRR (current)
     - MRR change from last month
     - Churn flag
     - Customer cohort (signup month)
   
   - `fct_usage_metrics`: Usage patterns:
     - Account ID
     - Month
     - API calls per $ of MRR (efficiency metric)
     - Active users per $ of MRR
     - Usage tier (light/medium/heavy based on API calls)

4. **Incremental Model**
   - `fct_daily_usage_trends` (incremental on date)
   - Only process new dates to optimize performance

5. **Macro**
   - `calculate_ltv(mrr, months)`: Customer lifetime value calculator
   - Usage: `{{ calculate_ltv('current_mrr', 'customer_tenure_months') }}`

6. **Tests**
   - All subscription IDs unique
   - MRR is non-negative
   - Event dates are not in future
   - Accounts have valid subscription status
   - Usage data exists for all active accounts

7. **Custom Tests**
   - Ensure MRR movements sum to current MRR
   - No overlapping active subscriptions for same account

8. **Exposure**
   - Define a dashboard exposure that depends on your models

### Deliverables

- Source definitions with freshness checks
- 4 staging models
- 3 intermediate models  
- 3 mart models
- 1 incremental model
- 1 macro
- Comprehensive tests (schema + custom)
- 1 exposure definition
- Full documentation

### Advanced Challenges

- Calculate cohort retention by signup month
- Identify accounts at risk of churn (usage declining)
- Revenue waterfall (new, expansion, contraction, churn)

---

## Exercise 3: Social Media Analytics Platform

**Domain:** Social Media  
**Difficulty:** Medium-Hard  
**Estimated Time:** 3 hours

### Scenario

Build analytics for a social platform tracking:
- Users and their profiles
- Posts (images, videos, text)
- Engagement (likes, comments, shares)
- Follower relationships

### Raw Tables

```sql
-- raw.users
id, username, email, bio, follower_count, following_count, created_at, is_verified

-- raw.posts
id, user_id, post_type, content_url, caption, posted_at, is_deleted

-- raw.post_engagement
id, post_id, user_id, engagement_type, created_at
-- engagement_type: 'like', 'comment', 'share', 'save'

-- raw.follows
id, follower_user_id, followed_user_id, followed_at, unfollowed_at
```

### Your Tasks

Build a complete dbt project with:

1. **Staging Models**
   - Clean and validate all tables
   - Calculate engagement metrics per post

2. **Intermediate Models**
   - `int_post_metrics`: Post-level engagement summary
   - `int_user_network`: User follower/following stats
   - `int_engagement_velocity`: Engagement rate over time

3. **Mart Models**
   - `dim_users`: User profiles with:
     - Total posts
     - Average engagement per post
     - Follower-to-following ratio
     - Growth rate (new followers last 30 days)
     - Influence score (custom formula)
   
   - `fct_posts`: Post facts with:
     - Post ID
     - User ID
     - Post type
     - Total likes, comments, shares
     - Engagement rate (engagements / follower_count)
     - Viral score (shares / views)
     - Posted date
   
   - `fct_daily_platform_metrics`: Daily aggregates:
     - Date
     - New users
     - Total posts
     - Total engagement actions
     - DAU (daily active users)
     - Engagement rate

4. **Window Functions Model**
   - `fct_user_growth_trends`: User growth over time
   - Include: running total followers, 7-day moving average engagement

5. **Snapshot**
   - Track follower_count changes for all users

6. **Tests**
   - Users cannot follow themselves
   - Post timestamps not in future
   - Engagement types are valid
   - No duplicate engagements (user can't like same post twice)

7. **Macro**
   - `engagement_score(likes, comments, shares, saves)`: Weighted engagement calculator
   - Weights: like=1, comment=3, share=5, save=2

### Deliverables

- Full dbt project structure
- Source definitions
- 4 staging models
- 3 intermediate models
- 3 mart models
- Window functions usage
- 1 snapshot
- 1 macro
- Comprehensive tests
- Documentation

### Bonus Challenges

- Identify trending posts (rapid engagement growth)
- Calculate user engagement clusters (high/medium/low)
- Build influencer network analysis (who influences whom)

---

## How to Submit Your Solution

For each exercise:

1. Create a new dbt project folder
2. Build all required models
3. Run `dbt run` and verify success
4. Run `dbt test` and ensure all tests pass
5. Generate docs: `dbt docs generate`
6. Take screenshots of:
   - DAG lineage
   - Test results
   - Sample query results

---

## Evaluation Criteria

Your solutions will be evaluated on:

✅ **Correctness** - Do models produce accurate results?  
✅ **Structure** - Proper staging → intermediate → marts layers?  
✅ **Testing** - Comprehensive data quality checks?  
✅ **Documentation** - Clear descriptions and lineage?  
✅ **Best Practices** - Naming conventions, DRY, performance?  
✅ **Complexity** - Proper use of CTEs, window functions, macros?  

---

**Good luck! These exercises will solidify your dbt skills.** 💪
