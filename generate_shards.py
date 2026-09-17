import csv
import random
import os

random.seed(42)

os.makedirs("shards", exist_ok=True)

for shard_id in range(8):
    rows = []

    for i in range(20):
        user_id = shard_id * 20 + i + 1
        email = f"user{user_id}@example.com"
        name = f"User {user_id}"

        rows.append([user_id, email, name])

    # 3 deliberately invalid rows per shard
    invalid_indices = random.sample(range(20), 3)

    for idx in invalid_indices:
        if idx % 2 == 0:
            rows[idx][1] = "invalid-email"
        else:
            rows[idx][2] = ""

    path = f"shards/shard-{shard_id}.csv"

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "email", "name"])
        writer.writerows(rows)

    print(f"Created {path}: 3 invalid rows")


print("Created 8 shards.")
