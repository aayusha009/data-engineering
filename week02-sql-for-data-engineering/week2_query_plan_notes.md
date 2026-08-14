# Week 2 Notes — Query Plan (EXPLAIN)

## What EXPLAIN does

EXPLAIN shows how Postgres plans to find your data, before it
actually runs the query.

## My query

```sql
EXPLAIN SELECT * FROM payment WHERE customer_id = 5;
```

## What Postgres said

```
Bitmap Heap Scan on payment  (cost=4.56..79.17 rows=35 width=26)
  Recheck Cond: (customer_id = 5)
  ->  Bitmap Index Scan on idx_fk_customer_id  (cost=0.00..4.55 rows=35 width=0)
        Index Cond: (customer_id = 5)
```

## What it means, simply

- Postgres did **not** check every row in the table.
- It used an **index** (a shortcut) to find the right rows fast.
- First it found *where* the matching rows are (cheap: cost 4.55).
- Then it went and got the actual row data (more expensive: cost 79.17).
- So the **second step (getting the row data) is the expensive part.**

## The one thing to remember

- If Postgres says **Seq Scan** → it checked every row (slow).
- If Postgres says **Index Scan** or **Bitmap Scan** → it used a
  shortcut (fast).
- The bigger the `cost` number, the more work that step takes.

## Partitioning & Clustering (concept only, practical work in Week 5)

- **Partitioning** = splitting one big table into smaller physical
  pieces (e.g. by year), so a query can skip pieces it doesn't need.
- **Clustering** = physically reordering rows on disk to match an
  index, so related rows sit next to each other and are faster to
  fetch together.

