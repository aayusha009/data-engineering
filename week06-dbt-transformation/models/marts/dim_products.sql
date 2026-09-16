SELECT ROW_NUMBER() OVER (ORDER BY product_name) AS product_id, product_name
FROM (SELECT DISTINCT product_name FROM {{ ref('int_orders_cleaned') }})
