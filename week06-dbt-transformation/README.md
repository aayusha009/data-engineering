# Week 6 – dbt Transformation Project

A dbt project that cleans and organizes order data from MotherDuck.

- **Staging** – `stg_orders`: pulls raw columns from the source table
- **Intermediate** – `int_orders_cleaned`: cleans up text formatting and removes bad rows
- **Marts** – `dim_customers`, `dim_products`, `fct_orders`: the final tables ready for querying

## Tests
26 tests across all models, covering uniqueness, required fields, valid product names, and correct links between the fact and dimension tables. All passing.

## How to run

```bash
source venv/bin/activate
export motherduck_token=token
dbt run
dbt test
dbt docs generate
dbt docs serve --port 8081
```
