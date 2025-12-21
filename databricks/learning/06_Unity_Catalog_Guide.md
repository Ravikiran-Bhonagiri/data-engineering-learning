# Supplemental: Unity Catalog Guide

**The comprehensive guide to Databricks' unified governance layer.**

---

## 1. Concepts Deep Dive

**Identity Federation:**
Users and Groups are managed at the **Account Level**, not the workspace level.
- **Benefits:** Add a user once, give them access to 10 workspaces.

**Metastore Assignment:**
One Metastore is assigned to multiple workspaces in the same region.
- **Implication:** All those workspaces share the same view of data (Catalog/Schema/Table) without needing complex grants.

---

## 2. External Locations vs Storage Credentials

This is the most confusing part for beginners.

1. **Storage Credential:** Converting an IAM Role / Service Principal into a Databricks object.
   - *Example:* `aws_role_finance_read`

2. **External Location:** Combining a Credential with a specific S3 path.
   - *Example:* `s3://finance-data/` using `aws_role_finance_read`.

**Why separate them?**
You might have one role (`aws_role_full_access`) but you only want to allow Databricks to read from `s3://my-bucket/public`. You create an External Location for that specific subpath.

---

## 3. Row Filtering & Column Masking

**Row Filter (SQL UDF):**
Apply logic to filter rows based on user identity.
```sql
CREATE FUNCTION us_only_filter(region STRING)
RETURN IF(is_account_group_member('us_users'), true, region = 'US');

ALTER TABLE sales SET ROW FILTER us_only_filter ON (region);
```

**Dynamic View (Column Masking):**
See `04_Complete_Examples.md`.

---

## 4. Lineage API

You can access lineage programmatically via REST API (great for custom governance tools).

```bash
GET /api/2.0/lineage-tracking/table-lineage \
    ?table_name=main.default.users \
    ?include_entity_lineage=true
```

---

## 5. Best Practices Checklist

- [ ] **One Metastore per Region.** Don't slice metastores by department.
- [ ] **Catalog per Environment.** (`prod`, `dev`, `stage`).
- [ ] **Schema per Domain.** (`prod.finance`, `prod.marketing`).
- [ ] **Managed Tables** for internal data (let Databricks manage storage).
- [ ] **External Tables** only for data shared with other tools (e.g., direct S3 access from an external app) or legacy migrations.
- [ ] **Groups, not Users.** Always GRANT permissions to Groups.

---

**Interview Tip:**
If asked "How do you secure PII?", mention that Unity Catalog solves this at the *platform* level, so it applies to SQL, Python, and even files (via Volumes), whereas legacy ACLs were often language-specific or easily bypassed.
