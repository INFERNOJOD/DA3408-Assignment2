import csv
import os
import re

shard_index = os.environ["SHARD_INDEX"]
node_name = os.environ["NODE_NAME"]

shard_file = f"shards/shard-{shard_index}.csv"
invalid_count = 0

with open(shard_file, newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        email = row["email"]
        name = row["name"]

        valid_email = re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email)
        valid_name = bool(name.strip())

        if not valid_email or not valid_name:
            invalid_count += 1

print(f"Shard: {shard_index}")
print(f"Node: {node_name}")
print(f"Invalid rows: {invalid_count}")
