from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from langchain_core.messages import AnyMessage

class OfferState(BaseModel):
    segments_ids : List[str] = Field(description="Segments")
    metric_ids : List[str] = Field(description="Metrics")
    human_remark : str = Field(description="Human Remark")
    idea : Optional[List[str]] = Field('', description="Idea")
    offers : Optional[str] = Field('', description="Offers")
    chat_history: Optional[List[AnyMessage]] = Field([], description="Chat History")