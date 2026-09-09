# Week 5 Deliverables 

## 1. Partitioned Parquet Dataset

Generated synthetic order data spanning 30 days (`generate_data.py`), saved as raw JSON, then converted it into Parquet (`combine_for_warehouse.py`). The data includes an `order_date` column following the `event_date=YYYY-MM-DD` partition convention, so it can be filtered by date the same way a physically partitioned dataset would be.

- Source: `data/raw/orders.json`
- Parquet output: `data/warehouse_ready/orders_all.parquet`
- 767 total rows across 30 distinct dates (2026-08-09 to 2026-09-07)

## 2. Warehouse Raw Table

Uploaded the Parquet file into MotherDuck (a cloud data warehouse), creating a real, queryable table.

- Database: `my_db`
- Table: `orders`
- Confirmed via `SELECT * FROM my_db.orders LIMIT 10;`

## 3. Loading Script / SQL Command

**Python — generating the raw data:**
`generate_data.py` — builds 30 days of synthetic order data using `random`, saves to `data/raw/orders.json`.

**Python — converting to Parquet:**
`combine_for_warehouse.py` — loads the raw JSON into a pandas DataFrame and saves it as a single Parquet file.

**SQL — loading into the warehouse:**
Uploaded via MotherDuck's "Add data" button, then created a clearly-named partitioned table:
```sql
CREATE TABLE my_db.orders_partitioned AS
SELECT * FROM my_db.orders;
```

## 4. Cost/Performance Notes

Compared a full table scan against a query filtered to a single day, both run against `my_db.orders_partitioned` or `my_db.orders`:

```sql
-- Full scan
SELECT * FROM my_db.orders_partitioned;
-- touches all 767 rows

-- Filtered to one day
SELECT * FROM my_db.orders_partitioned WHERE order_date = '2026-09-07';
-- touches only 8 rows
```

**Result:** the filtered query touched roughly **1% of the data** (8 out of 767 rows) compared to the full scan. At this small scale the dollar/time difference is negligible, but the same pattern holds at real scale — a company with millions or billions of rows partitioned by date would see the filtered query cost a small fraction of the full scan, which is the entire reason partitioning and cost-aware querying matter in practice. Writing queries that filter to only the data you actually need, instead of scanning everything, is what "cost-aware querying" means.

## 5. Warehouse Naming Conventions

- File: `data/warehouse_ready/orders_all.parquet`
- Partition column: `order_date`, in `YYYY-MM-DD` format — same convention as the `event_date=YYYY-MM-DD` folder-naming pattern, just stored as a column instead of a physical folder split

**Warehouse layer (MotherDuck):**
- Database: `my_db`
- Raw table: `orders`
- Partitioned/query-ready table: `orders_partitioned`

