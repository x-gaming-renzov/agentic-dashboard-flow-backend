import json

def format_armor_enchantments(json_data):
    # Initialize an empty list for the output
    output = []
    
    # Assuming we want to print the first category ("armor_enchantment") as the main header
    categories = list(json_data.keys())  # Extract the category name (e.g. "armor_enchantment")
    
    for category in categories:
    # Add the category title to the output
        output.append(f"{category.replace('_', ' ').capitalize()}")  # E.g., "Armor enchantments"
        
        # Iterate through the enchantments of that category
        enchantments = json_data[category]
        
        for enchantment, details in enchantments.items():
            name = enchantment
            description = details['description']
            output.append(f"{name} - {description}")
    
    return "\n".join(output)

if __name__ == "__main__":
    # read a file
    path = "/Users/pranaypandit/Documents/mystuff/x/extrarepos/agentic-dashboard-flow-backend/functions/kb/categorized_data.json"
    with open(path, 'r') as f:
        json_data = json.load(f)
        formatted_output = format_armor_enchantments(json_data)
    print(formatted_output)
