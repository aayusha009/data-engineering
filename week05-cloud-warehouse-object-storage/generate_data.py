import json
import random
from datetime import date, timedelta
import os
os.makedirs("data/raw", exist_ok=True)

customers = [
    "Arav Shah",
    "Priya Nair",
    "Rohan Mehta",
    "Ananya Kapoor",
    "Vikram Singh",
    "Sanya Malhotra",
    "Karan Johar",
    "Aisha Sharma",
    "Rahul Verma",
    "Neha Gupta",
    "Aditya Rao",
    "Isha Patel",
    "Kabir Khan",
    "Meera Joshi",
    "Riya Desai",
    "Aarav Choudhury",
    "Siddharth Iyer",
    "Tara Menon",
    "Devansh Bhatia",
    "Naina Reddy",  
]

products = [
    {"name": "Wireless Mouse", "price": 799},
    {"name": "Mechanical Keyboard", "price": 3499},
    {"name": "USB-C Hub", "price": 1299},
    {"name": "Laptop Stand", "price": 1599},
    {"name": "Webcam", "price": 2199},
    {"name": "Desk Lamp", "price": 899},
    {"name": "Noise-Cancelling Headphones", "price": 4999},
    {"name": "Portable SSD", "price": 6999},
    {"name": "Smartwatch", "price": 9999},
    {"name": "Bluetooth Speaker", "price": 2499},
]

orders = []
order_id = 1

for days_ago in range(30):
    order_date = (date.today() - timedelta(days=days_ago)).isoformat()
    num_orders_today = random.randint(8, 60)

    for _ in range(num_orders_today):
        product = random.choice(products)
        quantity = random.randint(1, 3)
        orders.append({
            "order_id": order_id,
            "customer_name": random.choice(customers),
            "product_name": product["name"],
            "unit_price": product["price"],
            "quantity": quantity,
            "total_amount": product["price"] * quantity,
            "order_date": order_date,
        })
        order_id += 1

with open("data/raw/orders.json", "w") as f:
    json.dump(orders, f, indent=2)

print(f"Generated {len(orders)} orders across 30 days")
