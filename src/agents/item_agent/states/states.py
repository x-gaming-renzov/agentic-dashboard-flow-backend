from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ItemDetails(BaseModel):
    name : str = Field(..., description="Interesting name of item")
    description : str = Field(..., description="Intresting lore of the item")
    amount : int = Field(..., description="Amount of item")
    properties : str = Field(..., description="Properties of the item")
    category : str = Field(..., description="Category of the item")

class Items(BaseModel):
    items: List[ItemDetails] = Field(..., description="List of items")