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
    qa_status : Optional[bool] = Field(None, description="QA Status")
    human_query : Optional[str] = Field(None, description="Human query")

class QaResponse(BaseModel):
    ok : bool = Field(None, description="true if everything is ok")
    remarks: Optional[str] = Field(None, description="Remarks on what is wrong")

class QuerryResponse(BaseModel):
    querry: Optional[str] = Field(None, description="Querry string for script")