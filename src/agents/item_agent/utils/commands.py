import pymongo
from psycopg2 import connect
import pathlib
import os, dotenv
import string

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
        lore = item_json["description"]
        effect = item_json["top_k"][0]["name"].lower()
        amount = item_json["amount"]
        effect = effect.replace("potion of ", "")
        
        command_str = command_str.replace("{name}", name).replace("{lore}", lore).replace("{effect}", effect).replace("{amount}", str(amount))  
        return command_str

def generate_bow_command(item_json):
    with open(BOW_COMMAND_FILE, "r") as f:
        command_str = f.read()
        name = item_json["name"]
        lore = item_json["description"]
        enchantment = item_json["top_k"][0]["name"].lower()
        enchantment = enchantment.replace(" ","_")

        command_str = command_str.replace("{name}", name).replace("{lore}", lore).replace("{effect}", effect).replace("{amount}", str(amount))
        return command_str
    
def generate_armor_command(item_json):
    with open(ARMOR_COMMAND_FILE, "r") as f:
        command_str = f.read()
        name = item_json["name"]
        lore = item_json["description"]
        enchantment = item_json["top_k"][0]["name"].lower()
        enchantment = enchantment.replace(" ", "_")

        command_str = command_str.replace("{name}", name).replace("{lore}", lore).replace("{effect}", effect).replace("{amount}", str(amount))
        return command_str
    


        

    
    

