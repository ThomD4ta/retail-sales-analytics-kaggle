-- ===========================================
-- 20_dq_product_category_standarized_strings.sql
-- Purpose: Standarize strings
-- ===========================================

-- Standarize strings: product_category
UPDATE public.retail_sales
SET product_category = lower(trim(product_category))
WHERE product_category IS NOT NULL;





