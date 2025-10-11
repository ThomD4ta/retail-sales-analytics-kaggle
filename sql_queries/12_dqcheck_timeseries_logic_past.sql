-- ===========================================
-- 12_dqcheck_timeseries_logic_past.sql
-- Purpose: Time/date dataset logic data quality
-- ===========================================

-- Old / suspicious dates (example: before 2000-01-01)
SELECT * FROM public.retail_sales WHERE date < '2000-01-01' LIMIT 50;


