-- ===========================================
-- 23_bi_total_count_distinct_categories.sql
-- Purpose: Business data insights
-- ===========================================

-- Count Total product_categories by unique product_category
SELECT product_category, COUNT(*) AS cnt 
FROM public.retail_sales 
GROUP BY product_category 
ORDER BY cnt 
DESC LIMIT 200;






