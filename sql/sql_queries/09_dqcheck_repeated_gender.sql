-- ===========================================
-- 09_dqcheck_repeated_gender.sql
-- Purpose: Key metric check, data quality/Business Intelligence
-- ===========================================

-- Audit gender column, find repeated gender
SELECT gender, COUNT(*) AS cnt
FROM public.retail_sales
GROUP BY gender
HAVING COUNT(*) > 1 -- to find Duplicates
ORDER BY cnt DESC
LIMIT 100;

