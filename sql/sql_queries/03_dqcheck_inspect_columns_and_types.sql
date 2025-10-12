-- ===========================================
-- 03_inspect_columns_and_types.sql
-- Purpose: Table and types understanding
-- ===========================================

-- Inspect Column names and types
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = 'retail_sales'
ORDER BY ordinal_position;