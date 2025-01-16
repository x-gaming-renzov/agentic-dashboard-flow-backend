from langchain.prompts import PromptTemplate

segmentation_prompt = PromptTemplate(
    template="""
You are segmentation expert at gaming company. Divide players into {num_segments} segments based on data available.

You can use images provided to help you with segmentation.

# Here's remark fro human : {human_remark}

Metrics based on which you can segment players are:
{metrics}

Here's schema of data available:
{data_schema}

Here's types of events data is gathered from:
{events}

# Task : 
- Divide players into {num_segments} segments based on data available.
- Provide a brief description of each segment.
- Provide a insights gained from data available.
- Provide criteria used for segmentation.
- Provide any remarks you feel are important and not covered in above points.

Good criteria for segmentation is one which can be computed dirctly in a single sql query.

Here's game's GDD for your reference:
{gdd}
""",
input_variables=["num_segments", "human_remark", "metrics", "data_schema", "events", "gdd"])