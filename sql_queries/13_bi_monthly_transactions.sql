-- ===========================================
-- 13_bi_monthly_transactions.sql
-- Purpose: Business data check
-- ===========================================

-- Dates Group by Month, no duplicate transactions
SELECT
  date_trunc('month', date)       AS month,
  COUNT(*)                       AS transactions_per_month
FROM public.retail_sales
GROUP BY month
ORDER BY month;



