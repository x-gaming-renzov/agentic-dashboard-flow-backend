from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ChartOptionState(BaseModel):
    title: str = Field(None, description="Chart Title")
    xAxis: str = Field(None, description="X axis Label Name. ")
    yAxis: str = Field(None, description="Y axis Label Name.")

class MetricState(BaseModel):
    name: str = Field(None, description="Metric Name")
    description: str = Field(None, description="Metric Description. Description should be clear, and what are x and y columns needed to display chart and how it is useful.")
    chartType: str = Field(None, description="Chart Type. Possible values: line, pie, metric, histogram")
    chartOptions: ChartOptionState = Field(None, description="Chart Options")
    how_to_calculate: str = Field(None, description="How to calculate the metric. This should include the formula, parameters and how the metric can be calculated.")

class L2MetricStructuredResponse(BaseModel):
    metrics: List[MetricState] = Field(None, description="Metrics")

class L2MetricsState(BaseModel):
    l2_metrics: Optional[List[MetricState]] = Field(None, description="Metrics")
    remarks: Optional[str] = Field('', description="Remarks")
    l1_metrics: List[str] = Field(None, description="L1 Metrics")
    focus_metric: str = Field(None, description="Focus Metric")
    l2_instructions: Optional[str] = Field(None, description="Instructions for L2 Metrics")

