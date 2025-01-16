from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class DataQuerryState(BaseModel):
    data: Optional[Any] = Field(None, description="Data from the querry")
    db_type: Optional[str] = Field(None, description="Type of database")
    event_data: Optional[str] = Field(None, description="Events in the table")
    table_name: Optional[str] = Field(None, description="Table name")
    query: Optional[str] = Field(None, description="Query")
    instruction: Optional[str] = Field(None, description="Instruction")
    dialect: Optional[str] = Field(None, description="Dialect")
    db_schema: Optional[str] = Field(None, description="Database schema")
    should_retry: Optional[bool] = Field(None, description="Should retry")

class QuerryResponse(BaseModel):
    querry: Optional[str] = Field(None, description="Querry string for script")