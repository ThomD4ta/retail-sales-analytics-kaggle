-- ===========================================
-- 31_view_sales_and_customers_mom_ytd.sql
-- Purpose: Business data insights
-- ===========================================

-- YTD total_amount/revenue, unique customers and units sold performance

CREATE OR REPLACE VIEW sales_and_customers_mom_ytd AS
SELECT
    s.month_start,
    s.year,
    s.month,
    s.total_revenue,
    s.total_units,
    s.unique_customers,
    m.mom_revenue_growth_pct,
    y.ytd_revenue,
    y.ytd_units
FROM monthly_transactions s
LEFT JOIN monthly_mom m USING (month_start, year, month, total_revenue)
LEFT JOIN monthly_ytd_performance y USING (month_start, year, month, total_revenue)
ORDER BY s.month_start;