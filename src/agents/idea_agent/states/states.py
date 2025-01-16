from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class IdeasDetails(BaseModel):
    name: str = Field(description="The name of the idea.")
    one_liner: str = Field(description="The one liner of the idea. Must be punchy and intriuging.")
    detailed_description: str = Field(description="The detailed and comprehensive description of the idea.")
    idea_type: Optional[str] = Field(description="Type of the idea. Can be 'offer', 'event', 'promotion', 'monetization', 'marketing', 'other'.")

class IdeaDetailResponse(BaseModel):
    ideas_details: List[IdeasDetails] = Field(description="List of ideas details")

class IdeaState(BaseModel):
    metrics: Optional[List[str]] = Field([],description="Metrics")
    human_remark: Optional[str] = Field('',description="Metrics")
    num_ideas: Optional[int] = Field(None,description="Metrics")
    segments: Optional[List[int]] = Field([],description="Metrics")
    factors: Optional[str] = Field('',description="Metrics")
    plots : Optional[List[str]] = Field([],description="Metrics")
    ideas_details: Optional[List[IdeasDetails]] = Field([],description="Metrics")