-- ===========================================
-- 29_view_monthly_mom.sql
-- Purpose: Business data insights
-- ===========================================

-- MoM total_amount/revenue performance

CREATE VIEW monthly_mom AS
SELECT
    month_start,
    year,
    month,
    total_revenue,
    total_units,
    unique_customers,
    LAG(total_revenue) OVER (ORDER BY month_start) AS prev_month_revenue,
    ROUND(
        (total_revenue - LAG(total_revenue) OVER (ORDER BY month_start))
        / NULLIF(LAG(total_revenue) OVER (ORDER BY month_start), 0) * 100,
        2
    ) AS mom_revenue_growth_pct
FROM monthly_transactions
ORDER BY month_start;
