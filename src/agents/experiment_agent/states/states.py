from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class SegmentOfferItemsResponse(BaseModel):
    items: List[str] = Field(..., description="Description of items/perks/commands to be offered")
    segment_id : str = Field(..., description="Segment ID. DO NOT INCLUDE NAME JUST ID IN STR")
    offer_name : str = Field(..., description="Offer name")
    offer_description : str = Field(..., description="Offer description")

class ExperimentState(BaseModel):
    chat_id: str = Field(..., description="Chat ID")
    segment_id: Optional[List[str]] = Field("", description="Segment ID")
    offers : Optional[List[SegmentOfferItemsResponse]] = Field([], description="Offers")
    offer_dict : Optional[Dict[str, Any]] = Field({}, description="Offer dict")

class ItemDetailsResponse(BaseModel):
    name : str = Field(..., description="Name of item")
    description : str = Field(..., description="Description of item")
    amount : int = Field(..., description="Amount of item")
    material : Optional[str] = Field(..., description="Material of item")
    set_command : str = Field(..., description="Minecraft command to provide item to user")