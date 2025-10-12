-- ===========================================
-- 07_dqcheck_duplicated_transactions.sql
-- Purpose: Key metric Duplicate check, data quality checks
-- ===========================================

-- Audit transaction ID column, find duplicates
SELECT transaction_id, COUNT(*) AS cnt
FROM public.retail_sales
GROUP BY transaction_id
HAVING COUNT(*) > 1 -- to find Duplicates
ORDER BY cnt DESC
LIMIT 100;

