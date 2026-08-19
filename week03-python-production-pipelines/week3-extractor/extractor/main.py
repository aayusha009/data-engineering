

#the "conductor" file that ties everything together: 
# creates the client, fetches, validates, and saves the data, in order.

import logging
import json
import csv
import os
from extractor.api_client import APIClient # class imported from api_client.py
from extractor.models import validate_users

# logging setup (to see how it actually looks like with timestamp )
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def save_as_json(data: list, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)   # folder create garna
    with open(path, "w") as f:
        json.dump(data, f, indent=2)    # writes data into json file with indentation for readability

def save_as_csv(data: list, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "email", "phone"])
        writer.writeheader()             # writes header line of the column name
        for user in data:                # each line for each user
            writer.writerow({"id": user["id"], "name": user["name"], "email": user["email"], "phone": user["phone"]})

#only once you run the file directly, this block will execute
if __name__ == "__main__":
    client = APIClient("https://jsonplaceholder.typicode.com")   # APIClient made
    raw_users = client.get_users()
    save_as_json(raw_users, "data/raw/users.json")

    users = validate_users(raw_users)
    save_as_json(users, "data/processed/users.json")
    save_as_csv(users, "data/processed/users.csv")





