-- ===========================================
-- 14_dq_total_amount_tolerance.sql
-- Purpose: Business data check
-- ===========================================

-- Tolerance: total_amount ≈ quantity * price_per_unit
SELECT *
FROM public.retail_sales
WHERE
  (quantity IS NOT NULL AND price_per_unit IS NOT NULL AND total_amount IS NOT NULL)
  AND abs(total_amount - (quantity * price_per_unit)) > 0.01  -- tolerance
LIMIT 100;



