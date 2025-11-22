-- E-commerce Product Sales Analysis SQL Queries
-- Database: SQLite, MySQL, PostgreSQL compatible

-- ============================================
-- 1. OVERALL SALES METRICS
-- ============================================

-- Total sales summary
SELECT
    COUNT(*) AS total_products,
    COUNT(DISTINCT category) AS total_categories,
    SUM(sales_month_1 + sales_month_2 + sales_month_3 + sales_month_4 +
        sales_month_5 + sales_month_6 + sales_month_7 + sales_month_8 +
        sales_month_9 + sales_month_10 + sales_month_11 + sales_month_12) AS total_units_sold,
    SUM((sales_month_1 + sales_month_2 + sales_month_3 + sales_month_4 +
        sales_month_5 + sales_month_6 + sales_month_7 + sales_month_8 +
        sales_month_9 + sales_month_10 + sales_month_11 + sales_month_12) * price) AS total_revenue,
    AVG(price) AS avg_product_price
FROM products;


-- ============================================
-- 2. CATEGORY PERFORMANCE
-- ============================================

-- Sales and revenue by category
SELECT
    category,
    COUNT(*) AS num_products,
    SUM(sales_month_1 + sales_month_2 + sales_month_3 + sales_month_4 +
        sales_month_5 + sales_month_6 + sales_month_7 + sales_month_8 +
        sales_month_9 + sales_month_10 + sales_month_11 + sales_month_12) AS total_units,
    SUM((sales_month_1 + sales_month_2 + sales_month_3 + sales_month_4 +
        sales_month_5 + sales_month_6 + sales_month_7 + sales_month_8 +
        sales_month_9 + sales_month_10 + sales_month_11 + sales_month_12) * price) AS total_revenue,
    AVG(price) AS avg_price,
    AVG(review_score) AS avg_review_score
FROM products
GROUP BY category
ORDER BY total_revenue DESC;


-- ============================================
-- 3. TOP PERFORMING PRODUCTS
-- ============================================

-- Top 20 products by revenue
SELECT
    product_name,
    category,
    price,
    (sales_month_1 + sales_month_2 + sales_month_3 + sales_month_4 +
     sales_month_5 + sales_month_6 + sales_month_7 + sales_month_8 +
     sales_month_9 + sales_month_10 + sales_month_11 + sales_month_12) AS total_sales,
    (sales_month_1 + sales_month_2 + sales_month_3 + sales_month_4 +
     sales_month_5 + sales_month_6 + sales_month_7 + sales_month_8 +
     sales_month_9 + sales_month_10 + sales_month_11 + sales_month_12) * price AS revenue,
    review_score,
    review_count
FROM products
ORDER BY revenue DESC
LIMIT 20;


-- ============================================
-- 4. REVIEW SCORE ANALYSIS
-- ============================================

-- Average sales by review score range
SELECT
    CASE
        WHEN review_score < 2 THEN 'Poor (0-2)'
        WHEN review_score < 3 THEN 'Fair (2-3)'
        WHEN review_score < 4 THEN 'Good (3-4)'
        ELSE 'Excellent (4-5)'
    END AS review_category,
    COUNT(*) AS num_products,
    AVG(sales_month_1 + sales_month_2 + sales_month_3 + sales_month_4 +
        sales_month_5 + sales_month_6 + sales_month_7 + sales_month_8 +
        sales_month_9 + sales_month_10 + sales_month_11 + sales_month_12) AS avg_total_sales,
    AVG(price) AS avg_price
FROM products
GROUP BY review_category
ORDER BY review_category;


-- ============================================
-- 5. PRICE ANALYSIS
-- ============================================

-- Products by price range
SELECT
    CASE
        WHEN price < 100 THEN '$0-$100'
        WHEN price < 200 THEN '$100-$200'
        WHEN price < 300 THEN '$200-$300'
        WHEN price < 500 THEN '$300-$500'
        ELSE '$500+'
    END AS price_range,
    COUNT(*) AS num_products,
    AVG(sales_month_1 + sales_month_2 + sales_month_3 + sales_month_4 +
        sales_month_5 + sales_month_6 + sales_month_7 + sales_month_8 +
        sales_month_9 + sales_month_10 + sales_month_11 + sales_month_12) AS avg_sales
FROM products
GROUP BY price_range
ORDER BY price_range;


-- ============================================
-- 6. MONTHLY TRENDS
-- ============================================

-- Total sales per month
SELECT
    'Month 1' AS month, SUM(sales_month_1) AS total_sales, SUM(sales_month_1 * price) AS revenue FROM products
UNION ALL SELECT 'Month 2', SUM(sales_month_2), SUM(sales_month_2 * price) FROM products
UNION ALL SELECT 'Month 3', SUM(sales_month_3), SUM(sales_month_3 * price) FROM products
UNION ALL SELECT 'Month 4', SUM(sales_month_4), SUM(sales_month_4 * price) FROM products
UNION ALL SELECT 'Month 5', SUM(sales_month_5), SUM(sales_month_5 * price) FROM products
UNION ALL SELECT 'Month 6', SUM(sales_month_6), SUM(sales_month_6 * price) FROM products
UNION ALL SELECT 'Month 7', SUM(sales_month_7), SUM(sales_month_7 * price) FROM products
UNION ALL SELECT 'Month 8', SUM(sales_month_8), SUM(sales_month_8 * price) FROM products
UNION ALL SELECT 'Month 9', SUM(sales_month_9), SUM(sales_month_9 * price) FROM products
UNION ALL SELECT 'Month 10', SUM(sales_month_10), SUM(sales_month_10 * price) FROM products
UNION ALL SELECT 'Month 11', SUM(sales_month_11), SUM(sales_month_11 * price) FROM products
UNION ALL SELECT 'Month 12', SUM(sales_month_12), SUM(sales_month_12 * price) FROM products;


-- ============================================
-- 7. UNDERPERFORMING PRODUCTS
-- ============================================

-- Products with low sales despite good reviews
SELECT
    product_name,
    category,
    price,
    review_score,
    (sales_month_1 + sales_month_2 + sales_month_3 + sales_month_4 +
     sales_month_5 + sales_month_6 + sales_month_7 + sales_month_8 +
     sales_month_9 + sales_month_10 + sales_month_11 + sales_month_12) AS total_sales
FROM products
WHERE review_score >= 4
  AND (sales_month_1 + sales_month_2 + sales_month_3 + sales_month_4 +
       sales_month_5 + sales_month_6 + sales_month_7 + sales_month_8 +
       sales_month_9 + sales_month_10 + sales_month_11 + sales_month_12) < (
       SELECT AVG(sales_month_1 + sales_month_2 + sales_month_3 + sales_month_4 +
                  sales_month_5 + sales_month_6 + sales_month_7 + sales_month_8 +
                  sales_month_9 + sales_month_10 + sales_month_11 + sales_month_12)
       FROM products
   )
ORDER BY total_sales ASC
LIMIT 20;


-- ============================================
-- 8. CATEGORY INSIGHTS
-- ============================================

-- Category with highest average review score
SELECT
    category,
    AVG(review_score) AS avg_review,
    COUNT(*) AS num_products,
    SUM((sales_month_1 + sales_month_2 + sales_month_3 + sales_month_4 +
        sales_month_5 + sales_month_6 + sales_month_7 + sales_month_8 +
        sales_month_9 + sales_month_10 + sales_month_11 + sales_month_12) * price) AS revenue
FROM products
GROUP BY category
ORDER BY avg_review DESC;
