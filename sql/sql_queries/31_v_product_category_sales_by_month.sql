-- ===========================================
-- 31_view_product_category_sales_by_month.sql
-- Purpose: Business data insights
-- ===========================================

-- Product category sales by Month

CREATE VIEW product_category_sales_by_month as (
WITH monthly AS (
  SELECT
    product_category,
    DATE_TRUNC('month', date)::date AS month_start,
    SUM(total_amount)   AS month_total_amount,
    SUM(quantity)       AS month_total_quantity,
    COUNT(*)            AS transactions_count
  FROM public.retail_sales
  WHERE product_category IS NOT NULL
  GROUP BY 1, 2
)
SELECT
  product_category,
  month_start,
  transactions_count,
  month_total_amount,
  month_total_quantity,
  -- share of this category across all months (category total = denominator)
  ROUND(month_total_amount::numeric / NULLIF(SUM(month_total_amount) OVER (PARTITION BY product_category), 0), 4) AS pct_of_category_amount,
  ROUND(month_total_quantity::numeric / NULLIF(SUM(month_total_quantity) OVER (PARTITION BY product_category), 0), 4) AS pct_of_category_quantity,
  -- optional: share of this category within the same month across categories
  ROUND(month_total_amount::numeric / NULLIF(SUM(month_total_amount) OVER (PARTITION BY month_start), 0), 4) AS pct_of_month_amount,
  ROUND(month_total_quantity::numeric / NULLIF(SUM(month_total_quantity) OVER (PARTITION BY month_start), 0), 4) AS pct_of_month_quantity
FROM monthly
ORDER BY product_category, month_start
);
