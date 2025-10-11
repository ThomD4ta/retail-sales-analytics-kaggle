-- ===========================================
-- 21_bi_count_distinct_product_category.sql
-- Purpose: Business data insights
-- ===========================================

-- Count unique product_category
SELECT product_category, COUNT(*) AS cnt
FROM public.retail_sales
GROUP BY product_category
ORDER BY cnt DESC
LIMIT 200;






