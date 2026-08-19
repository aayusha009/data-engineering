# Import the libraries needed for HTTP requests, JSON handling, and CSV writing.
#original single-file script from Day 1/2 that fetches API data and saves it as JSON/CSV; 
# now mostly superseded by the extractor/ package.

import requests
import json
import csv

# This function gets a list of users from the JSONPlaceholder API.
def get_users():
    # Send a GET request to the users endpoint.
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    # Convert the API response (JSON text) into a Python list/dictionary.
    return response.json()

# This function saves the data into a JSON file.
def save_as_json(data, path):
    # Open the file in write mode ("w").
    with open(path, "w") as f:
        # Write the Python data as JSON text with formatting.
        json.dump(data, f, indent=2)

# This function saves selected user information into a CSV file.
def save_as_csv(data, path):
    # Open the file for writing, and newline="" helps avoid blank lines on Windows.
    with open(path, "w", newline="") as f:
        # Create a CSV writer with only these columns: id, name, email and phone.
        writer = csv.DictWriter(f, fieldnames=["id", "name", "email", "phone"])
        # Write the header row.
        writer.writeheader()
        # Loop through each user in the list.
        for user in data:
            # Write one row for each user with only the needed fields.
            writer.writerow({"id": user["id"], "name": user["name"], "email": user["email"], "phone": user["phone"]})

# This block runs only when the file is executed directly.
if __name__ == "__main__":
    # Fetch the user list from the API.
    users = get_users()
    # Save the full data as a JSON file.
    save_as_json(users, "data/raw/users.json")
    # Save a smaller version as a CSV file.
    save_as_csv(users, "data/raw/users.csv")
    # Show a message in the terminal to confirm the files were saved.
    print("Saved raw data to data/raw/")