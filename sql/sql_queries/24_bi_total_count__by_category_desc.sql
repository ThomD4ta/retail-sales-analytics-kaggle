-- ===========================================
-- 24_bi_total_count__by_category_desc.sql
-- Purpose: Business data insights
-- ===========================================

-- Total Count by Category DESC, total values and unique category count
WITH per_cat AS (
  SELECT
    product_category,
    COUNT(*) AS cnt
  FROM retail_sales
  WHERE product_category IS NOT NULL
  GROUP BY product_category
),
totals AS (
  SELECT
    SUM(cnt)           AS rows_with_category,
    COUNT(*)           AS distinct_categories
  FROM per_cat
)
SELECT
  per_cat.product_category,
  per_cat.cnt,
  totals.rows_with_category,
  totals.distinct_categories
FROM per_cat
CROSS JOIN totals
ORDER BY per_cat.cnt DESC
LIMIT 30;






