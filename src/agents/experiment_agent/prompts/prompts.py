from langchain.prompts import PromptTemplate

get_experiment_offer_prompt = PromptTemplate(
    template="""
You are liveOps director at minecraft server. You had a conversation with human and now you have to create an offer for A/B testing. 

# Task : from below chat with user, return final offer details for given segments.

# RULES : 
- Only include items/perks/commands that are mentioned in chat.
- Do not include items/perks/commands that are not part of offering for target segment.
- ONLY INCLUDE items/perks/commands that are mentioned in chat.

# Here's segment details :
{segments}

# Here's the chat history :
{chat}
""",
input_variables=["chat", "segments"])

get_item_details_prompt = PromptTemplate(
    template="""
You are tasked to create a structured format of items/perks/commands to be provided to user in minecraft server.

But to give that, you need to create a correct item detials format which has all the detailes and minecraft command that can be used to provide that item to user.

# Task : Create a structured format of items/perks/commands to be provided to user in minecraft server. To create accurate format, use items context from the server's GDD

# RULES :
- You need to provide item details as per context of minecraft server.
- You need to provide item details in structured format.
- You need to provide minecraft command to provide that item to user.
- Keep player name as {{player}} in command str.
- in case item is in-game currency, _set_command will be /give cash {{player}} {{amount}}
- ONLY ADD COMMAND THAT CAN BE SUCCESSFULLY RUN USING SPIGOT PLUGIN. 
- USE MINECRAFT COMMAND TO PROVIDE CUSTOMISE ITEM TO USER.
- MAKE SURE TO ADD NAME AND LORE TO ITEM.

# Here's the item to be provided : {item}
# Here's the context of offer this item is part of : {offer_context}

# Here's the context of item : 
# {context}
""", input_variables=["item", "context", "offer_context"])

get_bundle_prompt = PromptTemplate(
    template="""
You will be given a chat history between human and ai with details about launching an expreiment in a minecraft game by offering bundles to players
In this chat, the messages may involve talk about changing the bundle in some way, you need to focus on that.
There are two bundles in this chat
{chat_history}

#TASK
read the chat history, identify the bundles in the first ai message, and record any changes in the bundles throughout the chat.

#OUTPUT FORMAT
You will return, for both bundles:
1. Bundle name
2. Original items in the bundle from the first ai message
3. Final bundle items after all changes from the chat. It is possible to have no change at all in the items

""",
input_variables=["chat_history"])