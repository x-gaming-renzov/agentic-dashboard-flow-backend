import pathlib
import os, dotenv
import string
import random

dotenv.load_dotenv()

POTIONS_COMMAND_FILE = pathlib.Path(__file__).parent.parent / "commands/potions.txt"
ARMOR_COMMAND_FILE = pathlib.Path(__file__).parent.parent / "commands/armor.txt"
BOW_COMMAND_FILE = pathlib.Path(__file__).parent.parent / "commands/bow.txt"
TOOLS_COMMAND_FILE = pathlib.Path(__file__).parent.parent / "commands/tools.txt"

COMMANDS_FORMAT = [
    "tools",
    "bow",
    "potions",
    "armor",
]

def generate_potions_command(item_json):
    with open(POTIONS_COMMAND_FILE, "r") as f:
        command_str = f.read()
        name = item_json["name"]
        name = name.replace("'", "")
        lore = item_json["description"]
        lore = lore.replace("'", "")
        effect = item_json["top_k"][0]["name"].lower()
        amount = item_json["amount"]
        effect = effect.replace("potion of ", "")
        
        command_str = command_str.replace("{name}", name).replace("{lore}", lore).replace("{effect}", effect).replace("{amount}", str(amount))  
        return command_str

def generate_bow_command(item_json):
    with open(BOW_COMMAND_FILE, "r") as f:
        command_str = f.read()
        name = item_json["name"]
        name = name.replace("'", "")
        lore = item_json["description"]
        lore = lore.replace("'", "")
        enchantment = item_json["top_k"][0]["name"].lower()
        enchantment = enchantment.replace(" ","_")
        level = random.randint(1, 3)

        command_str = command_str.replace("{name}", name).replace("{lore}", lore).replace("{enchantment}", enchantment).replace("{level}", str(level))
        return command_str
    
def generate_armor_command(item_json):
    with open(ARMOR_COMMAND_FILE, "r") as f:
        command_str = f.read()
        name = item_json["name"]
        name = name.replace("'", "")
        lore = item_json["description"]
        lore = lore.replace("'", "")
        item_name = item_json["top_k"][0]["name"].lower()
        item_name = item_name.replace(" ", "_")
        enchantment = item_json["top_k"][1]["name"].lower()
        enchantment = enchantment.replace(" ", "_")
        level = random.randint(1, 3)

        command_str = command_str.replace("{name}", name).replace("{lore}", lore).replace("{item_name}",item_name).replace("{enchantment}", enchantment).replace("{level}", str(level))
        return command_str

def generate_tool_command(item_json):
    with open(TOOLS_COMMAND_FILE, "r") as f:
        command_str = f.read()
        name = item_json["name"]
        name = name.replace("'", "")
        lore = item_json["description"]
        lore = lore.replace("'", "")
        item_name = item_json["top_k"][0]["name"].lower()
        item_name = item_name.replace(" ", "_")
        enchantment = item_json["top_k"][1]["name"].lower()
        enchantment = enchantment.replace(" ", "_")
        level = random.randint(1, 3)

        command_str = command_str.replace("{name}", name).replace("{lore}", lore).replace("{tool_name}", item_name).replace("{enchantment}", enchantment).replace("{level}", str(level))
        return command_str
