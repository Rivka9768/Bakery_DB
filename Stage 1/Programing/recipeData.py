import csv
import random

# Define baked goods and raw materials
baked_goods_ids = list(range(1, 101))  # Assuming 100 baked goods
raw_materials_ids = list(range(1, 41))  # Assuming 40 raw materials

# Generate unique recipe data
recipe_data = set()
unique_pairs = set()

while len(recipe_data) < 400:
    bake_goods_id = random.choice(baked_goods_ids)
    raw_material_id = random.choice(raw_materials_ids)

    # Ensure unique (bakeGoodsId, rawMaterialsId) pairs
    if (bake_goods_id, raw_material_id) in unique_pairs:
        continue

    unique_pairs.add((bake_goods_id, raw_material_id))
    material_quantity = random.randint(1, 10)  # Random quantity between 1-10
    recipe_data.add((bake_goods_id, raw_material_id, material_quantity))

# Write to CSV file
csv_filename = "recipe_data.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["bakeGoodsId", "rawMaterialsId", "materialQuantity"])
    writer.writerows(recipe_data)

print(f"CSV file '{csv_filename}' has been created successfully!")
