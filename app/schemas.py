from pydantic import BaseModel, Field
from typing import Optional

class TicketCreate(BaseModel):
    id: str = Field(..., description="Unique ticket identifier, e.g., t-1001")
    subject: str = Field(..., description="Subject of the ticket")
    body: str = Field(..., description="Detailed body of the ticket")

class TicketResponse(BaseModel):
    id: str
    subject: str
    body: str
    status: str
    category: Optional[str] = None
    priority: Optional[str] = None
    summary: Optional[str] = None
    retry_count: int

    class Config:
        from_attributes = True