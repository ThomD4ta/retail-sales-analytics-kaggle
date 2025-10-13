-- ===========================================
-- 30_view_monthly_ytd_performance.sql
-- Purpose: Business data insights
-- ===========================================

-- YTD total_amount/revenue and units sold performance

CREATE VIEW monthly_ytd_performance AS
SELECT
    year,
    month,
    month_start,
    total_revenue,
    SUM(total_revenue) OVER (
        PARTITION BY year
        ORDER BY month_start
    ) AS ytd_revenue,
    total_units,
    SUM(total_units) OVER (
        PARTITION BY year
        ORDER BY month_start
    ) AS ytd_units
FROM monthly_transactions
ORDER BY month_start;