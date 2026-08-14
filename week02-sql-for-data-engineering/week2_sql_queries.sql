-- =====================================================================
-- Week 2 — SQL for Data Engineering
-- Solved practice queries: joins, CTEs, subqueries, set operations,
-- window functions, deduplication, CASE WHEN, date analysis, sessionization
-- Database: dvdrental (PostgreSQL sample database)
-- =====================================================================


-- =====================================================================
-- SECTION 1: CTEs
-- =====================================================================

-- Show all active customers
WITH active_cus AS (
    SELECT first_name, last_name FROM customer WHERE active = 1
)
SELECT * FROM active_cus;

-- Show all films longer than 120 minutes
WITH film_time AS (
    SELECT title FROM film WHERE length > 120
)
SELECT * FROM film_time;

-- Total amount paid, per customer
WITH payment_each_customer AS (
    SELECT customer_id, SUM(amount) AS total_payment
    FROM payment
    GROUP BY customer_id
)
SELECT * FROM payment_each_customer;


-- =====================================================================
-- SECTION 2: JOINS (1-hop through 3-hop chains)
-- =====================================================================

-- Rentals with customer name (1 join)
SELECT r.rental_id, r.rental_date, c.first_name, c.last_name
FROM rental r
JOIN customer c ON r.customer_id = c.customer_id;

-- Films with category name (2 joins via bridge table)
SELECT f.title, c.name
FROM film f
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category c ON fc.category_id = c.category_id;

-- Rentals with film title (2-hop join via inventory)
SELECT r.rental_id, f.title
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON f.film_id = i.film_id;

-- Payments with customer name and email (1 join)
SELECT p.amount, c.first_name, c.email
FROM payment p
JOIN customer c ON p.customer_id = c.customer_id;

-- Store's city (3-hop join: store -> address -> city)
SELECT s.store_id, c.city
FROM store s
JOIN address a ON s.address_id = a.address_id
JOIN city c ON a.city_id = c.city_id;

-- Rental with customer name and film title (3-table combined join)
SELECT r.rental_id, c.first_name, f.title
FROM rental r
JOIN customer c ON r.customer_id = c.customer_id
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id;


-- =====================================================================
-- SECTION 3: CTE + JOIN COMBINED, GROUP BY / HAVING
-- =====================================================================

-- Popular films: total rentals per title, only films rented more than 25 times
WITH film_rental_counts AS (
    SELECT f.title, COUNT(*) AS total_rentals
    FROM rental r
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film f ON i.film_id = f.film_id
    GROUP BY f.title
)
SELECT * FROM film_rental_counts
WHERE total_rentals > 25;

-- Total rentals per customer, only customers with more than 40 rentals
WITH total_rental AS (
    SELECT COUNT(*) AS number_of_rental, customer_id FROM rental
    GROUP BY customer_id
)
SELECT * FROM total_rental WHERE number_of_rental > 40;


-- =====================================================================
-- SECTION 4: SUBQUERIES (IN, NOT IN, EXISTS)
-- =====================================================================

-- Films that have never been rented (NOT IN)
SELECT * FROM film
WHERE film_id NOT IN (
    SELECT film_id FROM inventory i
    JOIN rental r ON i.inventory_id = r.inventory_id
);

-- Customers who have made at least one payment over $10 (EXISTS)
SELECT * FROM customer c
WHERE EXISTS (
    SELECT * FROM payment p
    WHERE p.customer_id = c.customer_id
    AND amount > 10
);


-- =====================================================================
-- SECTION 5: SET OPERATIONS
-- =====================================================================

-- Customer IDs that appear in BOTH rental and payment (INTERSECT)
SELECT customer_id FROM rental
INTERSECT
SELECT customer_id FROM payment;

-- Customers who exist in customer table but never rented (EXCEPT)
-- (Returns 0 rows in dvdrental -- confirms every customer has rented at least once)
SELECT customer_id FROM customer
EXCEPT
SELECT customer_id FROM rental;


-- =====================================================================
-- SECTION 6: WINDOW FUNCTIONS -- RANKING
-- =====================================================================

-- Number each customer's rentals, oldest first (ROW_NUMBER)
SELECT rental_id, customer_id, rental_date,
       ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY rental_date ASC) AS rn
FROM rental
ORDER BY customer_id, rn;

-- Number each customer's payments, oldest first (ROW_NUMBER)
SELECT payment_id, payment_date, customer_id,
       ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY payment_date ASC) AS payment_customer_made
FROM payment
ORDER BY customer_id, payment_customer_made;

-- Compare ROW_NUMBER, RANK, and DENSE_RANK side by side on the same data
-- (highlights how each function handles tied amount values differently)
WITH numbered_payment AS (
    SELECT payment_id, customer_id, payment_date, amount,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY amount DESC) AS rn,
    RANK() OVER (PARTITION BY customer_id ORDER BY amount DESC) AS r,
    DENSE_RANK() OVER (PARTITION BY customer_id ORDER BY amount DESC) AS dr
    FROM payment
)
SELECT * FROM numbered_payment
ORDER BY customer_id, rn;


-- =====================================================================
-- SECTION 7: WINDOW FUNCTIONS -- LATEST/FIRST RECORD PER KEY (DEDUPLICATION)
-- =====================================================================
-- The core dedup pattern: number rows per group, then filter to rn = 1
-- to keep only one representative row (latest or first) per key.

-- Each customer's very first-ever rental
WITH numbered_rentals AS (
    SELECT rental_id, customer_id, rental_date,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY rental_date ASC) AS rn
    FROM rental
)
SELECT * FROM numbered_rentals
WHERE rn = 1;

-- Each customer's most recent payment
WITH numbered_payments AS (
    SELECT payment_id, customer_id, payment_date,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY payment_date DESC) AS rn
    FROM payment
)
SELECT * FROM numbered_payments
WHERE rn = 1;

-- Check for true exact-duplicate rows (same title + release_year inserted more than once)
-- (Returns 0 rows in dvdrental -- confirms no duplicate film records)
SELECT title, release_year, COUNT(*)
FROM film
GROUP BY title, release_year
HAVING COUNT(*) > 1;


-- =====================================================================
-- SECTION 8: WINDOW FUNCTIONS -- RUNNING TOTALS
-- =====================================================================

-- Running total of each customer's payments over time
SELECT payment_id, customer_id, payment_date, amount,
       SUM(amount) OVER (PARTITION BY customer_id ORDER BY payment_date) AS running_total
FROM payment;


-- =====================================================================
-- SECTION 9: CASE WHEN + CONDITIONAL AGGREGATION
-- =====================================================================

-- Label each payment by size
SELECT payment_id, amount,
    CASE
        WHEN amount < 3 THEN 'Small'
        WHEN amount BETWEEN 3 AND 7 THEN 'Medium'
        ELSE 'Large'
    END AS payment_size
FROM payment
ORDER BY amount DESC;

-- Conditional aggregation: count payments per size category, one row, three columns
SELECT
    COUNT(CASE WHEN amount < 3 THEN 1 END) AS small_count,
    COUNT(CASE WHEN amount BETWEEN 3 AND 7 THEN 1 END) AS medium_count,
    COUNT(CASE WHEN amount > 7 THEN 1 END) AS large_count
FROM payment;


-- =====================================================================
-- SECTION 10: DATE-BASED ANALYSIS / TIME FILTERING
-- =====================================================================

-- Total rentals per month (across all years)
SELECT EXTRACT(MONTH FROM rental_date) AS rental_month, COUNT(*) AS total_rentals
FROM rental
GROUP BY rental_month
ORDER BY rental_month;

-- Total rentals per year AND month (the real "monthly revenue"-style pattern)
SELECT
    EXTRACT(YEAR FROM rental_date) AS rental_year,
    EXTRACT(MONTH FROM rental_date) AS rental_month,
    COUNT(*) AS total_rentals
FROM rental
GROUP BY rental_year, rental_month
ORDER BY rental_year, rental_month;


-- =====================================================================
-- SECTION 11: SESSIONIZATION (GAPS AND ISLANDS)
-- =====================================================================
-- Goal: group each customer's rentals into separate "sessions" (visits),
-- where a new session starts whenever the gap since their last rental
-- exceeds 7 days.

WITH gaps AS (
    -- Step 1: calculate the time gap since each customer's previous rental
    SELECT customer_id, rental_date,
           rental_date - LAG(rental_date) OVER (
               PARTITION BY customer_id ORDER BY rental_date
           ) AS gap
    FROM rental
),
flagged AS (
    -- Step 2: flag rows where a new session starts (big gap, or first-ever rental)
    SELECT *,
        CASE
            WHEN gap IS NULL OR gap > INTERVAL '7 days' THEN 1
            ELSE 0
        END AS new_session_flag
    FROM gaps
)
-- Step 3: running total of the flag turns 1/0 markers into actual session numbers
SELECT *,
    SUM(new_session_flag) OVER (
        PARTITION BY customer_id ORDER BY rental_date
    ) AS session_id
FROM flagged
ORDER BY customer_id, rental_date;
