# This script creates a list of on https://warframe.market selleable items 
# seperated into categories according to the given CATEGORY_RULES using the warframe.market API.
# The script was created by 1Xanaton4You on 20.07.2026
# This is an open source script under GNU GENERAL PUBLIC LICENSE Version 3.
try:
	import requests
except ModuleNotFoundError:
	print("Failed to load the python 'requests' package. Make sure it is installed on your system!\n")

from datetime import datetime

ITEM_DATABASE_API = "https://api.warframe.market/v2/items"

headers = {
    "User-Agent": "WarframeMarketDatabaseGenerator/1.0",
    "Accept": "application/json"
}

useTestRules = 0    # Set this 1 to use the test rules (default=0)
# ==================================
# Your category definitions
# ==================================
# Note: You can use the TagFinder.py scrit to check what tags for the item selection are provided by the ITEM_DATABASE_API
if useTestRules:
    CATEGORY_RULES = {
            "test": {
            "include_and": ["syndicate"],
            "include_or": ["weapon"],
            "exclude": ["mod","blueprint","prime"]
        }
    }
else:
    CATEGORY_RULES = {
# All mods (excluding Riven mods)
        "mods": {
            "include_and": ["mod"],
            "include_or": [],
            "exclude": ["riven_mod"]
        },
# All prime warframe sets
        "warframes": {
            "include_and": [
                "set"],
            "include_or": [
                "warframe"],
            "exclude": [
                "mod",
                "augment"]
        },
# All non-prime weapons (excluding syndicate weapons)
        "weapons": {
            "include_and": [],
            "include_or": [
                "weapon"],
            "exclude": [
                "mod",
                "blueprint",
                "prime",
                "syndicate"]
        },
# All prime weapon sets
        "prime_weapons": {
            "include_and": [
                "prime",
                "set"],
            "include_or": [
                "weapon"],
            "exclude": [
                "mod",
                "blueprint",
                "syndicate"]
        },
# All syndicate weapon sets
        "syndicate_weapons": {
            "include_and": [
                "syndicate"],
            "include_or": [
                "weapon"],
            "exclude": [
                "mod",
                "blueprint",
                "prime"]
        },
# All companions and archwings
        "companions": {
            "include_and": [
                "prime",
                "set"
            ],
            "include_or": [],
            "exclude": [
                "mod",
                "blueprint",
                "weapon",
                "warframe",
            ]
        },
# All arcanes
        "arcanes": {
            "include_and": [],
            "include_or": [
                "arcane_enhancement"],
            "exclude": [
                "mod"]
        },
# All relics
        "relics": {
            "include_and": [],
            "include_or": ["relic"],
            "exclude": []
        },
# Veiled Riven mods
        "riven_mods": {
            "include_and": [],
            "include_or": ["riven_mod"],
            "exclude": []
        }

    }

def update_database():

	# ==================================
	# Download API data
	# ==================================
	try:
		response = requests.get(ITEM_DATABASE_API, headers=headers)
		response.raise_for_status()
		data = response.json()
		items = data["data"]
	except Exception as e:
		print("Failed to download Warframe Market data:")
		print(e)
		return False

	print("Downloading Warframe Market data...")
	print(f"Loaded {len(items)} items.")

	# ==================================
	# Build categories
	# ==================================

	categories = {}
	for category, rules in CATEGORY_RULES.items():
		categories[category] = []
        # Check required tags
		for item in items:
			tags = item.get("tags", [])
			# All required tags must exist
			if not all(tag in tags for tag in rules["include_and"]):
				continue
			# At least one OR tag must exist (if defined)
			include_or = rules.get("include_or", [])
			if include_or:
				if not any(tag in tags for tag in include_or):
					continue
			# No excluded tags may exist
			if any(tag in tags for tag in rules["exclude"]):
				continue

			categories[category].append(item["slug"])

	# Remove duplicates and sort
	for category in categories:
		categories[category] = sorted(set(categories[category]))

	# ==================================
	# Write database file
	# ==================================
	with open(
		"warframe_market_database.py",
		"w",
		encoding="utf-8"
	) as f:
		today = datetime.now().strftime("%Y-%m-%d")
		f.write(f"# Generated from Warframe Market API on {today}\n\n")
		f.write("categories = {\n")

		for category, items in categories.items():
			f.write(f'    "{category}": [\n')
			# Write 5 items per line
			for i in range(0, len(items), 5):
				chunk = items[i:i+5]
				line = ", ".join(f'"{item}"' for item in chunk)
				f.write(f"        {line},\n")
			f.write("    ],\n\n")
		f.write("}\n")

	# ==================================
	# Summary
	# ==================================
	print("\nCreated warframe_market_database.py\n")

#	for category, values in categories.items():
#		print(f"{category:25} {len(values):5} items")
	return True
    
if __name__ == "__main__":
	update_database()