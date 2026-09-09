import pandas as pd
import json

with open("data/raw/orders.json") as f:
    data = json.load(f)

df = pd.DataFrame(data)
df.to_parquet("data/warehouse_ready/orders_all.parquet")
print(f"Saved {len(df)} rows to data/warehouse_ready/orders_all.parquet")




