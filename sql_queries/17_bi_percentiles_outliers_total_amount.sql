-- ===========================================
-- 17_bi_percentiles_outliers_total_amount.sql
-- Purpose: Total amount outliers data insights
-- ===========================================


-- CTEs stats to track total_amount percentiles and show "outliers"
WITH stats AS (
  SELECT
    COUNT(*) FILTER (WHERE total_amount IS NOT NULL) AS non_null_count,
    percentile_cont(0.25) WITHIN GROUP (ORDER BY total_amount) AS p25,
    percentile_cont(0.75) WITHIN GROUP (ORDER BY total_amount) AS p75
  FROM public.retail_sales
)
SELECT
  s.non_null_count,
  s.p25,
  s.p75,
  SUM(CASE WHEN r.total_amount < s.p25 THEN 1 ELSE 0 END) AS below_p25,
  SUM(CASE WHEN r.total_amount >= s.p25 AND r.total_amount <= s.p75 THEN 1 ELSE 0 END) AS between_p25_p75,
  SUM(CASE WHEN r.total_amount > s.p75 THEN 1 ELSE 0 END) AS above_p75
FROM public.retail_sales r
CROSS JOIN stats s
WHERE r.total_amount IS NOT NULL
  AND s.p25 IS NOT NULL
GROUP BY s.non_null_count, s.p25, s.p75;




