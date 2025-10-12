-- ===========================================
-- 22_bi_category_total_count_and_distinct_categories.sql
-- Purpose: Business data insights
-- ===========================================

-- Count Total product_categories no null, and unique product_category
SELECT 
  COUNT (*) FILTER(WHERE product_category IS NOT NULL) AS rows_with_category,
  COUNT (DISTINCT product_category) AS distinct_categories
FROM retail_sales;






