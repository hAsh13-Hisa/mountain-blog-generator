#!/usr/bin/env python3
"""
Debug script to check mountain data structure
"""
import json

with open('data/mountains_japan_expanded.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

mountains = data['mountains']
print(f"Total mountains: {len(mountains)}")

for i, mountain in enumerate(mountains):
    if 'prefecture' not in mountain:
        print(f"❌ Mountain {i}: Missing 'prefecture' field")
        print(f"   ID: {mountain.get('id', 'N/A')}")
        print(f"   Name: {mountain.get('name', 'N/A')}")
        print(f"   Keys: {list(mountain.keys())}")
        print()
    elif i < 5:  # Show first 5 for verification
        print(f"✅ Mountain {i}: {mountain['name']} - {mountain['prefecture']}")

print("✅ Debug complete")