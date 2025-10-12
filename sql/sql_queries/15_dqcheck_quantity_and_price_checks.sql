-- ===========================================
-- 15_dq_quantity_and_price_checks.sql
-- Purpose: Business data check
-- ===========================================

-- Negative quantity or price
SELECT * FROM public.retail_sales
WHERE quantity < 0 OR price_per_unit < 0
LIMIT 50;



