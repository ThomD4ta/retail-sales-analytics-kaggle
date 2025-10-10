-- ===========================================
-- 01_create_or_truncate_retail_sales.sql
-- Purpose: Update retail_sales table
-- ===========================================

-- Ensure schema exists
CREATE SCHEMA IF NOT EXISTS public;

-- Switch to schema (optional but good habit)
SET search_path TO public;

-- Create or truncate the table for new data
	-- Clear old data before loading new CSV
TRUNCATE TABLE retail_sales;

-- Create table if it doesn't exist
CREATE TABLE IF NOT EXISTS retail_sales (
    sale_id TEXT PRIMARY KEY,
    sale_date TIMESTAMP,
    store_id TEXT,
    customer_id TEXT,
    product_id TEXT,
    category TEXT,
    quantity INTEGER,
    price NUMERIC,
    amount NUMERIC,
    payment_type TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
