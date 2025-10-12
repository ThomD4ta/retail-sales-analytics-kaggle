-- ===========================================
-- 10_dqcheck_dulicated_rows.sql
-- Purpose: data quality entire duplicated rows
-- ===========================================

-- Show how many full-row duplicates exist
SELECT COUNT(*) - COUNT(DISTINCT (transaction_id, date, customer_id, product_category, quantity, price_per_unit, total_amount, ds)) AS full_row_duplicate_count
FROM public.retail_sales;


