from langchain.prompts import PromptTemplate

factor_prompt = PromptTemplate(
    template="""
Give list of factors effecting my focus metrics : {focus_metrics} for the segment : {segment_name}

Here's Humans remark : {human_remark}

Details of segment : {segment_details}

Factors are based on data given to you. Make use of metrics and visualizations to suggest factors that are affecting the focus metrics.
RULES :
1. DO NOT HALLUCINATE
2. BE ACCURATE IN YOU FACTS
3. NEVER SUGGEST ANYTHING THAT IS NOT TRUE
4. NEVER SUGGEST FACTORS THAT REQUIRE DEVELOPER/GAME DESGIN INTERVENTION

Here's description of metrics images attached represent : 
{metrics}

Here's game's GDD : 
{gdd}
""",
input_variables=["focus_metrics", "segment_name", "segment_details", "metrics", "gdd", "human_remark"],)

ideas_prompt = PromptTemplate(
    template="""
    You are liveops director of a game.
Generate {num_ideas} ideas for the segment : {segment_name} to improve the focus metrics : {focus_metrics}.
Here's Humans remark : {human_remark}

Details of segment : {segment_details}

Here's factors that are affecting the focus metrics : {factors}

Ideas are based on data given to you. Make use of factors and visualizations to suggest ideas that are affecting the focus metrics.
RULES :
1. DO NOT HALLUCINATE
2. BE ACCURATE IN YOU FACTS
3. NEVER SUGGEST ANYTHING THAT IS NOT TRUE
4. NEVER SUGGEST IDEAS THAT REQUIRE DEVELOPER/GAME DESGIN INTERVENTION

Here's description of metrics images attached represent :
{metrics}

Here's game's GDD :
{gdd}
""",
input_variables=["num_ideas", "focus_metrics", "segment_name", "segment_details", "metrics", "gdd", "human_remark", "factors"],)