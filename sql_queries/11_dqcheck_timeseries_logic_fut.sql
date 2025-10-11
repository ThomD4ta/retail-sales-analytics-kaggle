-- ===========================================
-- 11_dqcheck_timeseries_logic_fut.sql
-- Purpose: Time/date dataset logic data quality
-- ===========================================

-- Future dates transactions
SELECT * FROM public.retail_sales WHERE date > current_date LIMIT 50;


