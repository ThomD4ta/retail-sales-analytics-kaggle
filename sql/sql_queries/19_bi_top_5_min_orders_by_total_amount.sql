-- ===========================================
-- 19_bi_top_5_min_orders_by_total_amount.sql
-- Purpose: Min orders data insights
-- ===========================================

-- Counting top N total_amount values, showing outliers count under $60 (p25)
SELECT
  total_amount as top_orders_min_amount,
  COUNT(*) AS total_orders_same_amount
FROM public.retail_sales
WHERE total_amount < 60
GROUP BY total_amount
ORDER BY total_amount ASC
LIMIT 5;




