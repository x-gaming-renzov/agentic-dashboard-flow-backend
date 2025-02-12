from langchain.prompts import PromptTemplate

get_multi_item_details_prompt = PromptTemplate(
    template="""

#TASK
Your task is to come up with items in minecraft to be given to a player based on the following bundle description
{offer_description}

Each item must be in one of the following categories and follow the instruction for that category 
(For example in case of food, only food item is given, while in case of sword, as per incstructions, enchantments can be listed)
{item_types}

The item selection should be reasonable, it should not be generous

You will provide, for each item
- An interesting name for the item
- Intresting lore for the item within 20 words
- A reasonable amount of item to be given
- properties of the item (like which armor? which enchantment? what level?) in 20 words
- Item category (from the category list, name should be exact)

""", input_variables=["offer_description","item_types"])
# Generate seperate description for the item