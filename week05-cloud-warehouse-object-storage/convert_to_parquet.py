# My raw data (orders.json) is one big file with all 5 days mixed together.
import pandas as pd   #  work with data as a table (rows and columns)
import json            # read json files
import os               # create folders

# Open the raw file and load its contents into a Python variable called "data"
with open("data/raw/orders.json") as f:
    data = json.load(f)
df = pd.DataFrame(data) # raw list of orders into a table 

# Look at the "order_date" column and pull out every DIFFERENT date that
# appears in it, with no duplicates. Since my data spans 5 days,
# this gives me a list of exactly those 5 dates.
unique_dates = df["order_date"].unique()

# Loop once for EACH of those 5 dates, this line runs 5 times total,
# once per date, with "order_date" holding a different date each time
for order_date in unique_dates:

    # This is "filtering": df["order_date"] == order_date checks EVERY row
    # and marks it True or False depending on whether it matches this date.
    day_df = df[df["order_date"] == order_date]
    partition_path = f"data/warehouse_ready/event_date={order_date}/orders.parquet"
    os.makedirs(os.path.dirname(partition_path), exist_ok=True)  # Create that folder if it doesn't exist yet.
    
    # Save just this one day's rows (day_df) as a Parquet file,
    # inside the folder we just made
    day_df.to_parquet(partition_path, index=False)

    # Print a confirmation so you can see it worked, one line per day
    print(f"Saved {len(day_df)} rows to {partition_path}")