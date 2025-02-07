import os, pathlib, json, dotenv
from termcolor import colored

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from ..prompts.prompts import *
from ..states.states import *
from ..utils.embed import get_top_k
from ..utils.flowutils import get_propmt_list, get_option_paths, read_json, list_subroot_instructions
from ...data_agent.agent import get_metrics_dicts, generate_metric_plot
from ..utils.commands import generate_armor_command,generate_bow_command,generate_potions_command,generate_tool_command

dotenv.load_dotenv()
JSON_PATH = pathlib.Path(__file__).parent.parent / "flow.json"
#db_uri = postgresql://xgaming:Xgaming123$@34.131.81.20:5432/mixpanel

print(colored(f"Status: ", "yellow"), colored(f"Initialising nodes", "white")) 
print(colored(f"Status: ", "yellow"), colored(f"Initialising ChatOpenAI", "white"))
model_large = ChatOpenAI(model="o1-preview")
model = ChatOpenAI(model="gpt-4o-mini")
print(colored(f"Status: ", "green"), colored(f"ChatOpenAI initialised", "white"))
    
def get_multi_item_details_node(offer_description : str = None) -> Items:
    generator_model = model.with_structured_output(Items)
    generator = get_multi_item_details_prompt | generator_model
    flow_json = read_json(JSON_PATH)
    item_instructions = list_subroot_instructions(flow_json)

    response = generator.invoke({
        "offer_description": offer_description,
        "item_types": item_instructions
        # "offer_context": offer_description
    })

    if isinstance(response, Items):
        return response
    else:
        return None

def generate_command(item_json):
    if item_json["category"] == "potions":
        return generate_potions_command(item_json)
    elif item_json["category"] == "bow":
        return generate_bow_command(item_json)
    elif item_json["category"] == "armor":
        return generate_armor_command(item_json)
    elif item_json["category"] == "tools":
        return generate_tool_command(item_json)
    else:
        return None
# -> List[Dict[str,str]]
def get_multi_item_commands(Items: Items):
    """
    For each item in Items, retrieves the option path (from the flow JSON)
    corresponding to its category. Then for each node in that path, it selects 
    the top item (using embedding dot product) based on the item's properties.
    
    Returns a list of commands where each command is a dict with:
        - 'item': the original item details
        - 'selection': a list of top selections for each category in the option path
    """
    commands = []
    # Read the flow JSON from the known JSON_PATH (assumed to be defined)
    flow_json = read_json(JSON_PATH)
    # Get all option paths from the flow (each path is a list of node IDs)
    option_paths = get_option_paths(flow_json)

    for item in Items.items:
        # Prepare the item details as a dictionary.
        item_dict = {
            "name": item.name,
            "description": item.description,
            "amount": item.amount,
            "properties": item.properties,
            "category": item.category
        }

        # Find the option path that starts with the item's category.
        # (Assuming that item.category matches the first node's id in lowercase.)
        selected_path = None
        for path in option_paths:
            if path and path[0].lower() == item.category.lower():
                selected_path = path
                break
        # Fallback: if no matching path is found, use the category itself.
        if not selected_path:
            selected_path = [item.category]

        # For each node in the option path, get the top item (k=1)
        selection = []
        for node_id in selected_path:
            top_items = get_top_k(node_id, item.properties, k=1)
            if top_items:
                # We take the first (and only) top item.
                selection.append(top_items[0])
        item_dict["top_k"] = selection
        command = generate_command(item_dict)
        item_dict["set_command"] = command

        # Append the item details and its selection chain to the commands list.
        commands.append(item_dict)

    return commands

if __name__ == "__main__":
    description = "designed for the competitive player, this bundle provides crucial boosts for PvP battles, enhancing both offense and defense strategies. With upgrades tailored to skills and gear, players are positioned for success in their PvP endeavors."
