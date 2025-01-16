Define L2 metrics for focus and L1 metric below.

Focus metric : avg timespend per player
L1 : DAU, no of sessions per player, avg session length per player

Segment of user you have to define L2 metrics are : PvP players (kills > 3)

Here's data you are collecting in csv:
{sql_schema}
Types of events :
{event_types}

You can only use this data to create metrics.

Here's game's gdd :
{GDD}

Here's some context dump for defining good L2 metrics :
{metric_guide}

# Task : Define L2 metric that can be derived from data. NOTE THAT DATA TABLE IS SAVED IN POSTGRESSQL. ENSURE METRICS CAN BE CALCULATED USING QUERRY. SUGESST NO MORE THAN 4 METRICS. METRICS CAN BE USED TO DISPLAY LINE, PIE, METRIC OR HISTOGRAM.

# Response format for each metric :

- name : metric name
- description : metric description. this include what metric is about and how it can be calculated. What are the parameters and what is the formula.
- chartType : type of chart that can be used to display metric.
- chartOptions : options that can be used to display chart.

# Response format for chartOptions :

- chartOptions :
  - title : title of chart
  - xAxis : x-axis label
  - yAxis : y-axis label
