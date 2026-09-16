SELECT
    order_id,
    customer_name,
    product_name,
    unit_price,
    quantity,
    total_amount,
    order_date
FROM {{ source('raw', 'orders') }}

