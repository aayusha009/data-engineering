# Week 5 Practice Queries

Table used: `my_db.orders` (also copied to `my_db.orders_partitioned` for the cost-aware comparison).

## 1. How many total orders are there for 2026-09-01?

```sql
SELECT COUNT(*) AS TOTAL_ORDERS 
FROM my_db.orders_partitioned 
where order_date = '2026-09-01';
```

## 2. What is the total revenue (total_amount) for the most recent day in your data?
```sql
SELECT sum(total_amount) as total 
from my_db.orders 
where order_date = '2026-09-07';
```

## 3. Which product appears most often across all orders?
```sql
SELECT count(*) 
as total_times_bought, product_name 
from my_db.orders 
group by product_name 
ORDER BY product_name DESC 
LIMIT 1;
```

## 4. What is the average total_amount per order, across the whole table?
```sql
SELECT AVG(unit_price) 
FROM my_db.orders;
```

## 5. Which customer has spent the most money in total?
```sql
select customer_name, sum(unit_price) 
from my_db.orders 
group by customer_name 
order by sum(unit_price) desc 
limit 1;
```

## 6. How many orders had a quantity of 3 or more?
```sql
select count(*) 
as count_order_quantity 
from my_db.orders 
where quantity >= 3;
```

## 7. What is the total revenue for just the last 7 days of data?
```sql
select sum(total_amount) 
from my_db.orders 
where order_date::TIMESTAMP >= NOW() - interval '7 days';
```

## 8. Which single day had the highest number of orders?
```sql
select count(*) from my_db.orders 
group by order_date 
order by count(*) desc 
limit 1;
```

## 9. Cost-aware comparison: full scan vs. filtered
Same question ("total revenue for Mechanical Keyboard"), answered two ways to compare rows touched.

**Version A — no date restriction (scans every Mechanical Keyboard row, any date):**
```sql
select sum(total_amount) 
as mechanical_keyboard_total_revenue 
from my_db.orders 
where product_name = 'Mechanical Keyboard';
```

**Version B — restricted to the last 3 days (scans far fewer rows):**
```sql
select sum(total_amount) as mechanical_keyboard_total_revenue 
from my_db.orders 
where product_name = 'Mechanical Keyboard'
and order_date:: TIMESTAMP >= NOW() - interval '3 days';
```

## 10. Which product generated the most total revenue (not just most orders)?
```sql
select product_name, sum(total_amount) 
from my_db.orders 
group by product_name 
order by sum(total_amount) desc limit 1;
```


## Cost-aware querying demo 

**Full scan (touches all 767 rows):**
```sql
SELECT * FROM my_db.orders_partitioned;
```

**Filtered to one day (touches only 8 rows):**
```sql
SELECT * FROM my_db.orders_partitioned
WHERE order_date = '2026-09-07';
```
