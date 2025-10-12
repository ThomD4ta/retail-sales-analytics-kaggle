-- ===========================================
-- 06_dqcheck_missingness_total_nulls.sql
-- Purpose: Find missing/null values, data quality checks
-- ===========================================

-- Count total rows, and find missing/null values
SELECT
  COUNT(*) AS total_rows,
  COUNT(*) FILTER (WHERE transaction_id IS NULL) AS transaction_id_nulls,
  COUNT(*) FILTER (WHERE date IS NULL) AS date_nulls,
  COUNT(*) FILTER (WHERE quantity IS NULL) AS quantity_nulls,
  COUNT(*) FILTER (WHERE price_per_unit IS NULL) AS price_nulls,
  COUNT(*) FILTER (WHERE total_amount IS NULL) AS total_amount_nulls
FROM public.retail_sales;
