from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class OfferState(BaseModel):
    segments_ids : List[str] = Field(description="Segments")
    metric_ids : List[str] = Field(description="Metrics")
    human_remark : str = Field(description="Human Remark")
    idea : Optional[str] = Field('', description="Idea")
    offers : Optional[str] = Field('', description="Offers")