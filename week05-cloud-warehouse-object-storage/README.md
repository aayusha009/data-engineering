# Week 5 — Cloud Warehouse + Object Storage

To understand how modern data platforms store, load, and query analytical data — partitioning, cost-aware querying, and the separation of storage from compute.

## What's in this folder

- generate_data.py — generates synthetic order data across 30 days
- combine_for_warehouse.py — converts raw JSON into a partitioned Parquet file
- data/raw/orders.json — raw extracted data
- data/warehouse_ready/orders_all.parquet — Parquet output, partitioned by `order_date`

## 1. Partitioned Parquet dataset

Converted raw JSON order data into Parquet, using an `order_date` column (`YYYY-MM-DD` format) as the partition key by following the same `event_date=YYYY-MM-DD` order.

- Source: `data/raw/orders.json`
- Output: `data/warehouse_ready/orders_all.parquet`

## 2. Warehouse tables

Loaded the Parquet file into MotherDuck (cloud data warehouse).

- Database: `[my_db]`
- Raw table: `[orders]`
- Partitioned table: `[orders_partitioned]`

Confirmed load with:
```sql
SELECT * FROM my_db.orders LIMIT 10;
```

## 3. Loading script / SQL

**Generate raw data:**
```bash
python3 generate_data.py
```

**Convert to Parquet:**
```bash
python3 combine_for_warehouse.py
```

**Load into warehouse** (via MotherDuck's "Add data," then):
```sql
CREATE TABLE my_db.orders_partitioned AS
SELECT * FROM my_db.orders;
```

## 4. Cost/performance notes

Compared a full table scan against a query filtered to one partition:

```sql
-- Full scan
SELECT * FROM [my_db].[orders_partitioned];

-- Filtered to one day
SELECT * FROM [my_db].[orders_partitioned] WHERE order_date = '[2026-09-07]';

```
