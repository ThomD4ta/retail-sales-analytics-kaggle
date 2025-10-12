-- ===========================================
-- 18_bi_top_5_max_orders_by_total_amount.sql
-- Purpose: Max orders data insights
-- ===========================================

-- Counting top N total_amount values, showing outliers count over $900 (p75)
SELECT
  total_amount as top_orders_max_amount,
  COUNT(*) AS total_orders_same_amount
FROM public.retail_sales
WHERE total_amount > 900
GROUP BY total_amount
ORDER BY total_amount DESC
LIMIT 5;




