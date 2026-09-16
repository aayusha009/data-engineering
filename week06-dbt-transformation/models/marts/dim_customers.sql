SELECT ROW_NUMBER() OVER (ORDER BY customer_name) AS customer_id,
    customer_name
FROM (SELECT DISTINCT customer_name FROM {{ ref('int_orders_cleaned') }})
