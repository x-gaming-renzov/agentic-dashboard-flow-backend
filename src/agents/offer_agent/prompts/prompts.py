from langchain.prompts import PromptTemplate

offer_prompt = PromptTemplate(
    template="""
You are a liveOps director of a game. You are given task to personalise in-app purchase bundles for your game for segments : 
{segment_names}

Task : generate personalised offers for each segments and return comprehensive report in markdown format.

Here's human's remark : {human_remark} 

Here's what you must include in your response:
- Bundle name
- Bundle price
- Bundle items
- Bundle description
- segments
- Bundle recommendation
- Product Experiment Instructions

You have to explore following idea : 
{idea}

Here's details of segments : 
{segments}

Here's game's gdd : 
{GDD}

Here are the items available in the game. These are the only available items, effects and enchantments:
{items}

RULES : 
- Be accurate with facts and make use of metrics visualisations provided
- You will suggest bundles only and ONLY from the provided list of items. No items are allowed outside of the list
- You can be as detailed as you want
- Golden apples are NOT allowed

Do not include suggestions that require:
- Game design changes
- Level modifications
- Developer implementation
- New asset creation
- Game balance adjustments

""", input_variables=["segment_names", "idea", "segments", "GDD", "human_remark","items"]
)

generate_offer_strategy_prompt = PromptTemplate(
    template="""
You are in-app purchase strategist of a game. You are given task to personalise in-app purchase bundles for your game for segments :
{segment_names}

Here's Details of segments :
{segments}

Here's human's remark : {human_remark}

You have to explore following idea :
{idea}

But to do that, you need to generate a strategy for in-app purchase bundles for each segment.

A good strategy should include:
- Theory behind the offer
- Justification for the offer
- content of the offer

Since you are a strategist, you do not know the exact content of the offer. You need to create list of possible types of items that will appeal to the segment.

Content of the offer should include:
- What type of items should be included in the offer
- What are perks that can be included in the offer

Here's learning from data :
{learning_from_data}
""", input_variables=["segment_names", "idea", "segments", "human_remark", "learning_from_data"]
)