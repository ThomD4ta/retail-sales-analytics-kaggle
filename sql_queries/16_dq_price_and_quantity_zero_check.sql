-- ===========================================
-- 16_dq_price_and_quantity_zero_check.sql
-- Purpose: Business data check
-- ===========================================

-- Zero price or quantity (maybe suspicious)
SELECT * FROM public.retail_sales
WHERE quantity = 0 OR price_per_unit = 0
LIMIT 50;


