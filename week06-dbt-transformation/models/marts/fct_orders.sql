SELECT
    o.order_id,
    c.customer_id,
    p.product_id,
    o.quantity,
    o.total_amount,
    o.order_date
FROM {{ ref('int_orders_cleaned') }} o
LEFT JOIN {{ ref('dim_customers') }} c ON o.customer_name = c.customer_name
LEFT JOIN {{ ref('dim_products') }} p ON o.product_name = p.product_name
