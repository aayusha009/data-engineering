-- Intermediate cleanup layer: standardizes text fields coming out of staging
-- and filters out rows that shouldn't reach the marts (nulls, bad quantities).

SELECT
    order_id,
    UPPER(TRIM(customer_name)) AS customer_name,
    UPPER(TRIM(product_name))  AS product_name,
    unit_price,
    quantity,
    total_amount,
    order_date
FROM {{ ref('stg_orders') }}
WHERE order_id IS NOT NULL
  AND quantity > 0
  AND total_amount IS NOT NULL
