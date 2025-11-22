-- E-commerce Sales Analysis SQL Queries
-- These queries can be run on any SQL database after importing the CSV data

-- ============================================
-- 1. SALES OVERVIEW
-- ============================================

-- Total revenue, orders, and average order value
SELECT
    COUNT(DISTINCT transaction_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_order_value,
    SUM(quantity) AS total_items_sold
FROM transactions;


-- ============================================
-- 2. SALES TRENDS OVER TIME
-- ============================================

-- Monthly sales trend
SELECT
    strftime('%Y-%m', date) AS month,
    COUNT(transaction_id) AS num_orders,
    SUM(total_amount) AS revenue,
    AVG(total_amount) AS avg_order_value
FROM transactions
GROUP BY month
ORDER BY month;


-- Daily sales for last 30 days
SELECT
    date,
    COUNT(transaction_id) AS num_orders,
    SUM(total_amount) AS revenue
FROM transactions
WHERE date >= date('now', '-30 days')
GROUP BY date
ORDER BY date DESC;


-- ============================================
-- 3. PRODUCT ANALYSIS
-- ============================================

-- Top 10 products by revenue
SELECT
    product_name,
    category,
    COUNT(transaction_id) AS num_orders,
    SUM(quantity) AS total_quantity_sold,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_order_value
FROM transactions
GROUP BY product_name, category
ORDER BY total_revenue DESC
LIMIT 10;


-- Category performance
SELECT
    category,
    COUNT(transaction_id) AS num_orders,
    SUM(total_amount) AS revenue,
    AVG(total_amount) AS avg_order_value,
    SUM(quantity) AS items_sold,
    ROUND(SUM(total_amount) * 100.0 / (SELECT SUM(total_amount) FROM transactions), 2) AS revenue_percentage
FROM transactions
GROUP BY category
ORDER BY revenue DESC;


-- ============================================
-- 4. CUSTOMER ANALYSIS
-- ============================================

-- Customer segment performance
SELECT
    customer_segment,
    COUNT(DISTINCT customer_id) AS num_customers,
    COUNT(transaction_id) AS num_orders,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_order_value
FROM transactions
GROUP BY customer_segment
ORDER BY total_revenue DESC;


-- Top 20 customers by revenue
SELECT
    customer_id,
    customer_segment,
    COUNT(transaction_id) AS num_purchases,
    SUM(total_amount) AS lifetime_value,
    AVG(total_amount) AS avg_order_value,
    MAX(date) AS last_purchase_date
FROM transactions
GROUP BY customer_id, customer_segment
ORDER BY lifetime_value DESC
LIMIT 20;


-- Customer purchase frequency
SELECT
    purchase_count,
    COUNT(*) AS num_customers
FROM (
    SELECT
        customer_id,
        COUNT(transaction_id) AS purchase_count
    FROM transactions
    GROUP BY customer_id
)
GROUP BY purchase_count
ORDER BY purchase_count;


-- ============================================
-- 5. GEOGRAPHIC ANALYSIS
-- ============================================

-- Revenue by country
SELECT
    country,
    COUNT(transaction_id) AS num_orders,
    SUM(total_amount) AS revenue,
    AVG(total_amount) AS avg_order_value
FROM transactions
GROUP BY country
ORDER BY revenue DESC;


-- ============================================
-- 6. PAYMENT & SHIPPING ANALYSIS
-- ============================================

-- Payment method preferences
SELECT
    payment_method,
    COUNT(transaction_id) AS num_transactions,
    SUM(total_amount) AS revenue,
    ROUND(COUNT(transaction_id) * 100.0 / (SELECT COUNT(*) FROM transactions), 2) AS percentage
FROM transactions
GROUP BY payment_method
ORDER BY num_transactions DESC;


-- Shipping method analysis
SELECT
    shipping_method,
    COUNT(transaction_id) AS num_orders,
    AVG(total_amount) AS avg_order_value
FROM transactions
GROUP BY shipping_method
ORDER BY num_orders DESC;


-- ============================================
-- 7. DISCOUNT ANALYSIS
-- ============================================

-- Discount impact on sales
SELECT
    CASE
        WHEN discount_percent = 0 THEN 'No Discount'
        WHEN discount_percent <= 10 THEN '1-10%'
        WHEN discount_percent <= 20 THEN '11-20%'
        WHEN discount_percent <= 30 THEN '21-30%'
        ELSE '31%+'
    END AS discount_range,
    COUNT(transaction_id) AS num_orders,
    SUM(total_amount) AS revenue,
    AVG(total_amount) AS avg_order_value
FROM transactions
GROUP BY discount_range
ORDER BY
    CASE discount_range
        WHEN 'No Discount' THEN 1
        WHEN '1-10%' THEN 2
        WHEN '11-20%' THEN 3
        WHEN '21-30%' THEN 4
        ELSE 5
    END;


-- ============================================
-- 8. COHORT ANALYSIS (Monthly)
-- ============================================

-- First purchase month for each customer
WITH customer_cohorts AS (
    SELECT
        customer_id,
        MIN(strftime('%Y-%m', date)) AS cohort_month
    FROM transactions
    GROUP BY customer_id
)

-- Cohort size and revenue
SELECT
    cc.cohort_month,
    COUNT(DISTINCT cc.customer_id) AS cohort_size,
    SUM(t.total_amount) AS total_revenue,
    AVG(t.total_amount) AS avg_order_value
FROM customer_cohorts cc
JOIN transactions t ON cc.customer_id = t.customer_id
WHERE strftime('%Y-%m', t.date) = cc.cohort_month
GROUP BY cc.cohort_month
ORDER BY cc.cohort_month;


-- ============================================
-- 9. YEAR-OVER-YEAR COMPARISON
-- ============================================

-- YoY monthly comparison
SELECT
    strftime('%m', date) AS month,
    strftime('%Y', date) AS year,
    SUM(total_amount) AS revenue,
    COUNT(transaction_id) AS num_orders
FROM transactions
GROUP BY year, month
ORDER BY month, year;
