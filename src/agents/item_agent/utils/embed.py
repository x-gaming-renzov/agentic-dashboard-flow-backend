import os
import sys
import dotenv
import numpy as np
import json
from openai import OpenAI

dotenv.load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def embed(message):
    embd = client.embeddings.create(
        input=message,
        model="text-embedding-3-small"
    ).data[0].embedding
    return embd

def get_top_k(category, description, k=5):
    # Generate embedding for the provided description.
    query_embd = np.array(embed(description))
    
    # Load the knowledge base (item data)
    with open('kb/categorized_data.json') as f:
        data = json.load(f)
    
    # Check if the category exists in the knowledge base.
    if category not in data:
        return []
    
    scores = []
    # Iterate over each item in the category.
    for item_id, item_info in data[category].items():
        item_embd = np.array(item_info.get("embd", []))
        # Compute the dot product between query embedding and item's embedding.
        score = np.dot(query_embd, item_embd)
        scores.append((score, item_id, item_info))
    
    # Sort by descending score.
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Select top k items (or all if less than k)
    top_items = []
    for score, item_id, item_info in scores[:k]:
        # Remove the "embd" field from the returned item info.
        item_copy = {key: value for key, value in item_info.items() if key != "embd"}
        item_copy["name"] = item_id
        item_copy["score"] = score
        item_copy["category"] = category
        top_items.append(item_copy)
    
    return top_items

# Example usage:
if __name__ == "__main__":
    category = "armour_enchantment"
    description = "Enchantment that reduces damage taken in battle"
    top_items = get_top_k(category, description, k=5)
    print(json.dumps(top_items, indent=2))
