from langchain.prompts import PromptTemplate

get_item_details_prompt = PromptTemplate(
    template="""

#TASK
Your task is to come up with an item in minecraft to be given to a player based on the following offer description
{offer_description}

The item must be in one of the following categories. Properties to be provided should only include the instruction given for that item type
{item_types}

You will provide
- An interesting name for the item
- Intresting lore for the item within 20 words
- A reasonable amount of item to be given
- properties of the item (like which armor? which enchantment? what level?) in 20 words


""", input_variables=["offer_description","item_types"])
# Generate seperate description for the item