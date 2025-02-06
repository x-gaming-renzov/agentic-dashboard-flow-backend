import os
import sys

def read_json(path:str) -> dict:
    """
    Reads a JSON file and returns its contents as a dictionary.

    Args:
        path (str): The path to the JSON file.

    Returns:
        dict: The contents of the JSON file as a dictionary.
    """
    import json
    with open(path, 'r') as f:
        return json.load(f)

def get_option_paths(flow_json: dict) -> list:
    """
    Traverses the flow_json and returns all possible paths from the root down to the leaves.
    Each path is represented as a list of node names (excluding the root node).
    """
    paths = []
    
    def traverse(node, current_path):
        # If the node has children, traverse each one.
        if "children" in node and node["children"]:
            for child in node["children"]:
                traverse(child, current_path + [child["id"]])
        else:
            # Leaf node reached, add the current path.
            paths.append(current_path)
    
    # Start traversing from the root node's children (if any)
    if "children" in flow_json and flow_json["children"]:
        for child in flow_json["children"]:
            traverse(child, [child["id"]])
    else:
        # If no children, then the root itself is the only node.
        paths.append([flow_json.get("id", "root")])
    
    return paths

def list_subroot_instructions(flow_json: dict) -> dict:
    """
    Given a flow JSON in the defined schema, this function returns a dictionary
    mapping each sub-root node's id to its instruction.
    
    For example:
      {
        "food": "A food item available in minecraft.",
        "swords": "A sword in minecraft which may include enchantments.",
         ... etc.
      }
    """
    instructions = {}
    
    # Check if the root has children
    if "children" in flow_json and flow_json["children"]:
        for child in flow_json["children"]:
            # Extract the instruction if it exists; if not, use an empty string
            instructions[child.get("id", "")] = child.get("instruction", "")
    
    return instructions

def get_propmt_list(path_list: list) -> str:
    """
    Takes a list of paths (each a list of node names) and returns a numbered string
    representation where each path is joined with a comma.
    Example:
        1. Food
        2. Sword, Sword Enchantment
    """
    lines = []
    for idx, path in enumerate(path_list, start=1):
        # Capitalize each word in the path for display purposes.
        display_path = ", ".join(name.capitalize() for name in path)
        lines.append(f"{idx}. {display_path}")
    return "\n".join(lines)

if __name__ == "__main__":
    # Get the path to the JSON file from command line arguments.
    path = "../flow.json"
    # Read the JSON file.
    flow_json = read_json(path)
    # Get the paths from the JSON file.
    paths = get_option_paths(flow_json)
    # Print the paths.
    print(list_subroot_instructions(flow_json=flow_json))
    print(get_propmt_list(paths))
