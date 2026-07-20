# Simple scritp to collect all used tags in the WarframeMarket database, 
# whch can be used in the ItemFinder.py for the CATEGORY_RULES
# The script was created by 1Xanaton4You on 20.07.2026
# This is an open source script under GNU GENERAL PUBLIC LICENSE Version 3.
import requests
from collections import Counter

API_URL = "https://api.warframe.market/v2/items"

headers = {
    "User-Agent": "WarframeMarketTagInspector/1.0",
    "Accept": "application/json"
}


print("Downloading Warframe Market data...")

response = requests.get(API_URL, headers=headers)
response.raise_for_status()

data = response.json()

items = data["data"]

print(f"Loaded {len(items)} items\n")


tag_counter = Counter()


for item in items:

    # Only read the tags array
    tags = item.get("tags", [])

    for tag in tags:
        tag_counter[tag] += 1


print(f"Found {len(tag_counter)} unique tags:\n")


for tag, count in sorted(tag_counter.items()):
    print(f"{tag:25} {count:5}")