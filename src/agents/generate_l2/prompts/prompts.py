from langchain.prompts import PromptTemplate

l2_prompt = PromptTemplate(
    template="""
Define L2 metrics for focus and L1 metric below.

Focus metric : {focus_metric}
L1 Metrics: 
{l1_metrics}

Here's data you are collecting in csv:
{sql_schema}
Types of events :
{event_types}

You can only use this data to create metrics.

Here's game's gdd :
{GDD}

Here's some context dump for defining good L2 metrics :
{metric_guide}

# Task : Define L2 metric that can be derived from data. NOTE THAT DATA TABLE IS SAVED IN POSTGRESSQL. ENSURE METRICS CAN BE CALCULATED USING QUERRY. SUGESST NO MORE THAN 4 METRICS. METRICS CAN BE USED TO DISPLAY LINE, PIE, METRIC OR BAR.

# Remark from team leader : {remarks}

# Response format for each metric :

- name : metric name
- description : metric description. this include what metric is about and how it can be calculated. What are the parameters and what is the formula.
- chartType : type of chart that can be used to display metric.
- chartOptions : options that can be used to display chart.

# Response format for chartOptions :
  - title : title of chart
  - xAxis : x-axis label
  - yAxis : y-axis label

# Guidelines :
1. Metric should be clear and easy to understand.
2. Metric should be useful and should help in making decisions.
3. Metric should be calculated using data provided.
4. Metric should be calculated using SQL query.
5. Metric should be calculated using simple formula.
""", input_variables=["sql_schema", "event_types", "GDD", "metric_guide", "focus_metric", "l1_metrics", "remarks"]
)

l2_out_prompt = PromptTemplate(
    template="""
Define L2 metrics for focus and L1 metric below.

Focus metric : {focus_metric}
L1 Metrics: 
{l1_metrics}

Here's data you are collecting in csv:
{sql_schema}
Types of events :
{event_types}

You can only use this data to create metrics.

Here's game's gdd :
{GDD}

# Task : Define L2 metric that can be derived from data. NOTE THAT DATA TABLE IS SAVED IN POSTGRESSQL. ENSURE METRICS CAN BE CALCULATED USING QUERRY. SUGESST NO MORE THAN 4 METRICS. METRICS CAN BE USED TO DISPLAY LINE, PIE, METRIC OR BAR.

# Remark from team leader : {remarks}

# Response format for each metric :

- name : metric name
- description : metric description. this include what metric is about and how it can be calculated. What are the parameters and what is the formula.
- chartType : type of chart that can be used to display metric.
- chartOptions : options that can be used to display chart.

# Response format for chartOptions :
  - title : title of chart
  - xAxis : x-axis label
  - yAxis : y-axis label

# Guidelines :
1. Metric should be clear and easy to understand.
2. Metric should be useful and should help in making decisions.
3. Metric should be calculated using data provided.
4. Metric should be calculated using SQL query.
5. Metric should be calculated using simple formula.

# L2 Metrics : 
{l2_metrics}
""", input_variables=["sql_schema", "event_types", "GDD", "focus_metric", "l1_metrics", "remarks", "l2_metrics"]
)

display_metric_prompt = PromptTemplate(
    template="""
User has given you instructions to display metrics. Here are the instructions :
{instructions}

# Task : create new metric based on instructions provided. 


# Response format for each metric :

- name : metric name
- description : metric description. this include what metric is about and how it can be calculated. What are the parameters and what is the formula.
- chartType : type of chart that can be used to display metric.
- chartOptions : options that can be used to display chart.

# Response format for chartOptions :
  - title : title of chart
  - xAxis : x-axis label
  - yAxis : y-axis label

# Guidelines to decide if new metric is required :
1. No existing metric is displaying the required data.

# Guidelines :
1. Metric should be clear and easy to understand.
2. Metric should be useful and should help in making decisions.
3. Metric should be calculated using data provided.
4. Metric should be calculated using SQL query.
5. Metric should be calculated using simple formula.""",
    input_variables=["instructions"]
)

should_generate_new_metric_prompt = PromptTemplate(
    template="""
You are given task to display following metric : 
{metric_details}

# Task : Check available metrics and return metric that is identical to the metric details provided above. If no metric is found, generate new metric. 

Here's the list of metrics available :
{existing_metrics}""",
    input_variables=["metric_details", "existing_metrics"]
)