WITH customer_sales AS (

    SELECT

        ct.customer_id,
        ct.product_id,
        p.product_category,
        c.region,
        c.customer_segment,
        ct.transaction_date,

        ct.quantity,
        ct.total_sales,
        ct.discount,
        ct.profit

    FROM customer_transactions ct

    INNER JOIN products p
        ON ct.product_id = p.product_id

    INNER JOIN customers c
        ON ct.customer_id = c.customer_id

    WHERE
        ct.transaction_status = 'Completed'
        AND ct.transaction_date >= DATE('2024-01-01')
),

regional_sales AS (

    SELECT

        product_category,

        region,

        customer_segment,

        SUM(total_sales) AS revenue,

        SUM(profit) AS total_profit,

        SUM(quantity) AS units_sold,

        COUNT(DISTINCT customer_id) AS active_customers,

        AVG(total_sales) AS avg_order_value

    FROM customer_sales

    GROUP BY

        product_category,
        region,
        customer_segment

)

SELECT *

FROM regional_sales

ORDER BY revenue DESC;