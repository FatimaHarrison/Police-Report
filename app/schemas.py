from pydantic import BaseModel


# Pydantic Schemas
class ReportBase(BaseModel):
    type: str
    location: str
    description: str | None = None

class ReportCreate(ReportBase):
    pass

class Report(ReportBase):
    id: int
class Report(BaseModel):
    id: int
    type: str
    location: str
    description: str | None = None
    created_at: str
