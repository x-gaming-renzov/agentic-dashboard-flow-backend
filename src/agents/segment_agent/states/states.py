from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class SegmentInfo(BaseModel):
    name : str = Field(..., title="Name of segment")
    description : str = Field(..., title="Description of segment")
    insights : str = Field(..., title="Insights gained from data")
    criteria : str = Field(..., title="Criteria used for segmentation")
    remarks : str = Field(..., title="Remarks")

class SegmentsResponse(BaseModel):
    segments: List[SegmentInfo]

# defining agent state
class SegmentState(BaseModel):
   human_remark: str
   metrics : List[str]
   num_segments: int
   segments : Optional[List[SegmentInfo]] = None
   plots: Optional[List[str]] = None