print("JAI SHRIRAM")

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class RepositoryCreate(BaseModel):
    name: str


class RepositoryResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)