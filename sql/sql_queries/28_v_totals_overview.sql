-- ===========================================
-- 28_bi_view_totals_overview.sql
-- Purpose: Business data insights
-- ===========================================

-- Total dataset overview

CREATE VIEW dataset_totals as (
SELECT 
count(transaction_id) as total_transactions,
count(customer_id) as total_customers,
SUM(total_amount) as total_sales,
SUM(quantity) as total_items_sold,
AVG(age) as avg_customer_age,
AVG(total_amount) as avg_order_amount
FROM retail_sales
);