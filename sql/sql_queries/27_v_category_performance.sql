-- ===========================================
-- 27_bi_view_category_performance.sql
-- Purpose: Business data insights
-- ===========================================

-- Product Category Performance

CREATE VIEW product_category_performance AS (
WITH total_agg_g AS (
  SELECT
    product_category,
    SUM(total_amount) AS total_sales,
    SUM(quantity) AS total_qty_sold,	
    COUNT(*) FILTER (WHERE lower(trim(gender)) = 'male') AS transactions_male,
    SUM(quantity) FILTER (WHERE lower(trim(gender)) = 'male') AS t_quantity_male,
    SUM(total_amount) FILTER (WHERE lower(trim(gender)) = 'male') AS t_amount_male,
    COUNT(*) FILTER (WHERE lower(trim(gender)) = 'female') AS transactions_female,
    SUM(total_amount) FILTER (WHERE lower(trim(gender)) = 'female') AS t_amount_female,
    SUM(quantity) FILTER (WHERE lower(trim(gender)) = 'female') AS t_quantity_female
  FROM public.retail_sales
  GROUP BY product_category
)
SELECT
  product_category,
  total_sales,
  total_qty_sold,
  transactions_male,
  t_quantity_male,
  t_amount_male,
  100.0 * COALESCE(t_amount_male, 0) / NULLIF(total_sales, 0) AS pct_t_male,
  transactions_female,
  t_quantity_female,
  t_amount_female,
  100.0 * COALESCE(t_amount_female, 0) / NULLIF(total_sales, 0) AS pct_t_female
FROM total_agg_g
ORDER BY total_sales DESC
);