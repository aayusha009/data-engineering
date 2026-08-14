# Week 2 Notes — Query Plan Observations (EXPLAIN)

## What EXPLAIN does

`EXPLAIN` shows Postgres's execution plan for a query instead of
actually running it — it reveals the strategy Postgres will use to
find the data (checking every row one by one, or using a shortcut via
an index), along with an estimated "cost" for each step.

## Observation 1

**Query:**
```sql
EXPLAIN SELECT * FROM payment WHERE customer_id = 5;
```

**Plan returned:**
```
Bitmap Heap Scan on payment  (cost=4.56..79.17 rows=35 width=26)
  Recheck Cond: (customer_id = 5)
  ->  Bitmap Index Scan on idx_fk_customer_id  (cost=0.00..4.55 rows=35 width=0)
        Index Cond: (customer_id = 5)
```

**What this shows:** `payment.customer_id` already has an index
(`idx_fk_customer_id`), since it's a foreign key. Postgres used a
two-step bitmap approach: first the **Bitmap Index Scan** cheaply
found the locations of all 35 matching rows (cost up to 4.55), then
the **Bitmap Heap Scan** fetched the actual row data from those
locations (cost up to 79.17).

**Expensive step:** the Bitmap Heap Scan (cost 4.56..79.17) is the
more expensive of the two steps — it has to go fetch the real row
data from disk, unlike the index scan which only locates row
positions.

## Observation 2

**Query:**
```sql
EXPLAIN SELECT r.rental_id, f.title
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id;
```

**What to look for:** this is a 2-hop join across three tables, so
the plan has multiple steps — one scan per table, plus one or more
join steps combining them (e.g. Hash Join or Nested Loop). The
expensive step is whichever line in the plan has the highest total
cost number — usually the scan on the largest table involved (in this
case, `rental`, since it has the most rows of the three).

## General takeaways

- **Seq Scan** = checks every row in the table one by one. Fine for
  small tables, slow on large ones.
- **Index Scan / Bitmap Index Scan** = uses a pre-built index to jump
  almost straight to matching rows, instead of checking everything.
- The **cost=start..total** numbers are an arbitrary unit for
  comparing strategies, not real seconds. The step with the highest
  total cost in a plan is the "expensive step" — the part most likely
  to slow a query down on a larger dataset.
- Foreign key columns (like `payment.customer_id`) are often already
  indexed, which is why filtering on them tends to be fast even
  without manually creating an index yourself.
