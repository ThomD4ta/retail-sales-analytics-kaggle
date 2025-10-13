-- ===========================================
-- 26_view_monthly_transactions.sql
-- Purpose: Business data insights
-- ===========================================

-- Total transactions by month

CREATE VIEW monthly_transactions AS
SELECT
    DATE_TRUNC('month', date)::date AS month_start,
    EXTRACT(YEAR FROM date) AS year,
    EXTRACT(MONTH FROM date) AS month,
    SUM(total_amount) AS total_revenue,
    SUM(quantity) AS total_units,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM public.retail_sales
GROUP BY 1, 2, 3
ORDER BY month_start;
