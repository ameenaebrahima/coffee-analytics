"""
Coffee Shop Customer Analytics — Data Generator
Generates realistic transaction data for a Bahrain coffee shop ("Qahwa & Co")
Simulates 18 months of real-world customer behavior.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

# ─── CONFIG ───────────────────────────────────────────────────────────────────
START_DATE = datetime(2023, 7, 1)
END_DATE = datetime(2024, 12, 31)
N_CUSTOMERS = 800

# Menu — realistic Bahrain coffee shop (prices in BHD)
MENU = {
    "Espresso": 1.200, "Americano": 1.400, "Latte": 1.800, "Cappuccino": 1.800,
    "Flat White": 1.900, "Spanish Latte": 2.100, "Cortado": 1.600,
    "Iced Latte": 2.000, "Cold Brew": 2.200, "Matcha Latte": 2.500,
    "Croissant": 1.500, "Cheesecake": 2.800, "Date Cake": 2.200,
    "Avocado Toast": 3.500, "Halloumi Sandwich": 3.200, "Karak Tea": 0.800,
}
DRINKS = list(MENU.keys())[:10]
FOOD = list(MENU.keys())[10:]

PAYMENT = ["Benefit Pay", "Apple Pay", "Card", "Cash"]
PAYMENT_W = [0.40, 0.25, 0.25, 0.10]
CHANNELS = ["Dine-in", "Takeaway", "Talabat", "Jahez"]
CHANNEL_W = [0.45, 0.30, 0.15, 0.10]
BRANCHES = ["Seef", "Adliya", "Riffa", "Muharraq"]

# Customer personas → drive realistic behavior
PERSONAS = {
    "Daily Regular":   {"n": 120, "visits": (180, 400), "basket": (1, 2)},
    "Frequent":        {"n": 180, "visits": (40, 120),  "basket": (1, 3)},
    "Weekend Visitor": {"n": 200, "visits": (15, 50),   "basket": (2, 4)},
    "Occasional":      {"n": 200, "visits": (3, 12),    "basket": (1, 3)},
    "One-Timer":       {"n": 100, "visits": (1, 2),     "basket": (1, 2)},
}

rows = []
txn_id = 100000
customer_id = 1

for persona, cfg in PERSONAS.items():
    for _ in range(cfg["n"]):
        cust = f"CUST{customer_id:04d}"
        n_visits = random.randint(*cfg["visits"])
        # signup date
        signup = START_DATE + timedelta(days=random.randint(0, 400))
        fav_branch = random.choice(BRANCHES)
        loyalty_member = random.random() < (0.8 if persona in ["Daily Regular","Frequent"] else 0.3)

        for _ in range(n_visits):
            days_after = random.randint(0, max(1, (END_DATE - signup).days))
            txn_date = signup + timedelta(days=days_after)
            if txn_date > END_DATE:
                continue
            hour = random.choices(
                population=[7,8,9,10,11,12,13,14,15,16,17,18,19,20,21],
                weights=[8,14,12,9,7,8,7,6,7,9,8,6,4,3,2],
                k=1
            )[0]
            basket_size = random.randint(*cfg["basket"])

            items, total = [], 0.0
            # at least one drink
            for i in range(basket_size):
                if i == 0 or random.random() < 0.7:
                    item = random.choice(DRINKS)
                else:
                    item = random.choice(FOOD)
                items.append(item)
                total += MENU[item]

            channel = random.choices(CHANNELS, CHANNEL_W)[0]
            rows.append({
                "transaction_id": f"TXN{txn_id}",
                "customer_id": cust,
                "persona": persona,
                "date": txn_date.strftime("%Y-%m-%d"),
                "hour": hour,
                "branch": fav_branch if random.random() < 0.8 else random.choice(BRANCHES),
                "channel": channel,
                "items": " + ".join(items),
                "num_items": len(items),
                "amount_bhd": round(total, 3),
                "payment_method": random.choices(PAYMENT, PAYMENT_W)[0],
                "loyalty_member": loyalty_member,
            })
            txn_id += 1
        customer_id += 1

df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
df.to_csv("data/transactions.csv", index=False)

print(f"✅ Generated {len(df):,} transactions")
print(f"   {df['customer_id'].nunique()} unique customers")
print(f"   Date range: {df['date'].min()} → {df['date'].max()}")
print(f"   Total revenue: BD {df['amount_bhd'].sum():,.2f}")
print(f"   Avg transaction: BD {df['amount_bhd'].mean():.3f}")
