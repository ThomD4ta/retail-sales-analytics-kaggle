-- ===========================================
-- 02_create_retail_sales_raw.sql
-- Purpose: Table Version that can be restored if needed
-- ===========================================

-- Make a point-in-time copy of the raw table
CREATE TABLE IF NOT EXISTS public.retail_sales_raw AS
SELECT *, now() AS _snapshot_ts
FROM public.retail_sales;