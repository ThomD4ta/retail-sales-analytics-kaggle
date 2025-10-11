-- ===========================================
-- 08_dqcheck_repeated_customers.sql
-- Purpose: Key metric check, data quality/Business Intelligence
-- ===========================================

-- Audit customer_id column, find repeated customers
SELECT customer_id, COUNT(*) AS cnt
FROM public.retail_sales
GROUP BY customer_id
HAVING COUNT(*) > 1 -- to find Duplicates
ORDER BY cnt DESC
LIMIT 100;

