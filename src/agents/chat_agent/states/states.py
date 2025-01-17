from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from langchain_core.messages import AnyMessage

class AskAgentInstructions(BaseModel):
    agent_instructions: str = Field(description="""Natural language instructions """)
    agent_name: Literal["ask_db_agent", "ask_metric_agent_to_display_chart", "ask_idea_agent_to_generate_idea"] = Field(description="Tool name")

class AIRepsonse(BaseModel):
    reply: str = Field(description="Reply to human message. Incase of tool call, ask human to verify.")
    agent_instructions: Optional[AskAgentInstructions] = Field(description="Tool Params in case of tool call")
    is_asking_sub_agent: Optional[bool] = Field(description="True if want to call tool before replying to human")

class ChatState(BaseModel):
    metric_ids: List[str] = Field(..., description="Metric IDs")
    segment_ids: List[str] = Field(..., description="Segment IDs")
    idea_ids: List[str] = Field(..., description="Idea IDs")
    offer : Optional[str] = Field(None, description="Offer")
    human_message : Optional[str] = Field(None, description="Human Remark")
    reply : Optional[str] = Field(None, description="Reply")
    agent_instructions : Optional[AskAgentInstructions] = Field(None, description="Tool Params")
    is_asking_sub_agent : Optional[bool] = Field(None, description="Is calling tool")
    chat_history : List[AnyMessage] = Field([], description="Chat History")

