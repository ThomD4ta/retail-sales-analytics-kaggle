-- ===========================================
-- 26_bi_view_monthly_transactions.sql
-- Purpose: Business data insights
-- ===========================================

-- Total transactions by month

CREATE VIEW monthly_transactions AS
SELECT 
  date_trunc('month', date)::date AS month,
  COUNT(transaction_id) as total_transactions,
  SUM(total_amount) as total_sales,
  SUM(quantity) as total_qty_sold
FROM retail_sales
GROUP BY month
ORDER BY month;
