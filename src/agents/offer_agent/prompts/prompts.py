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

RULES : 
- When creating bundle recommendations, follow these rules:
- Be accurate with facts and make use of metrics visualisations provided
- Only suggest bundles using existing in-game items and currencies
- You can be as detailed as you want

Do not include suggestions that require:
- Game design changes
- Level modifications
- Developer implementation
- New asset creation
- Game balance adjustments

You have to explore following idea : 
{idea}

Here's details of segments : 
{segments}

Here's game's gdd : 
{GDD}

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

RULES : 
- When creating bundle recommendations, follow these rules:
- Be accurate with facts and make use of metrics visualisations provided
- Only suggest bundles using existing in-game items and currencies
- You can be as detailed as you want

Do not include suggestions that require:
- Game design changes
- Level modifications
- Developer implementation
- New asset creation
- Game balance adjustments
""", input_variables=["segment_names", "idea", "segments", "GDD", "human_remark"]
)
