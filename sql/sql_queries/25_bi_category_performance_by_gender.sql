-- ===========================================
-- 25_bi_category_performance_by_gender.sql
-- Purpose: Business data insights
-- ===========================================

-- Distinct Categories total_amount by gender
WITH sales_by_cat AS (
  SELECT
    product_category,
    SUM(total_amount) AS category_total,
	SUM(quantity) AS quantity_sold
  FROM public.retail_sales
  GROUP BY product_category
)
SELECT
  public.retail_sales.product_category,
  public.retail_sales.gender,
  SUM(public.retail_sales.total_amount) AS total_sales_by_gender,
  COUNT(*) AS transactions_count,
  sales_by_cat.category_total,
  sales_by_cat.quantity_sold,
  SUM(public.retail_sales.total_amount) * 100 / NULLIF(sales_by_cat.category_total, 0) AS pct_of_category
FROM public.retail_sales
LEFT JOIN sales_by_cat
  ON public.retail_sales.product_category = sales_by_cat.product_category
GROUP BY
  public.retail_sales.product_category,
  public.retail_sales.gender,
  sales_by_cat.category_total,
  sales_by_cat.quantity_sold
ORDER BY
  public.retail_sales.product_category,
  total_sales_by_gender DESC;