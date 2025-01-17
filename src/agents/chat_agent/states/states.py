from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from langchain_core.messages import AnyMessage

class ToolPrams(BaseModel):
    query: str = Field(description="""Natural language query to be send to tools. In case of get_db_query, it will be SQL description, expected output, 
                       incase of display_metric, it will be metric description of which chart to be displayed and how to calculate it, in case of generate_ideas, what type/topic you want to generate ideas""")
    tool_name: Literal["get_db_query", "display_metric", "generate_ideas"] = Field(description="Tool name")

class AIRepsonse(BaseModel):
    reply: str = Field(description="Reply to human message. Incase of tool call, ask human to verify.")
    tool_params: Optional[ToolPrams] = Field(description="Tool Params in case of tool call")
    is_calling_tool: Optional[bool] = Field(description="True if want to call tool before replying to human")

class ChatState(BaseModel):
    metric_ids: List[str] = Field(..., description="Metric IDs")
    segment_ids: List[str] = Field(..., description="Segment IDs")
    idea_ids: List[str] = Field(..., description="Idea IDs")
    offer : Optional[str] = Field(None, description="Offer")
    human_message : Optional[str] = Field(None, description="Human Remark")
    reply : Optional[str] = Field(None, description="Reply")
    tool_params : Optional[ToolPrams] = Field(None, description="Tool Params")
    is_calling_tool : Optional[bool] = Field(None, description="Is calling tool")
    chat_history : List[AnyMessage] = Field([], description="Chat History")

