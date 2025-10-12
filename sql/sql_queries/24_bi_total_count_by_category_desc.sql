-- Total Count by Category DESC, total values and unique category count
WITH per_cat AS (
  SELECT
    product_category,
    COUNT(*) AS order_cnt_by_cat
  FROM retail_sales
  WHERE product_category IS NOT NULL
  GROUP BY product_category
),
totals AS (
  SELECT
    SUM(order_cnt_by_cat)           AS orders_by_category,
    COUNT(*)           AS distinct_categories
  FROM per_cat
)
SELECT
  per_cat.product_category,
  per_cat.order_cnt_by_cat,
  totals.orders_by_category,
  totals.distinct_categories
FROM per_cat
CROSS JOIN totals
ORDER BY per_cat.order_cnt_by_cat DESC
LIMIT 30;