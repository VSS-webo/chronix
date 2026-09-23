print("JAI SHRIRAM")

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DatasetResponse(BaseModel):
    id: int
    repository_id: int
    name: str
    object_hash: str
    file_size: int
    row_count: int
    column_count: int
    schema: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class DatasetVersionResponse(BaseModel):
    id: int
    version_number: int
    object_hash: str
    file_size: int
    row_count: int
    column_count: int
    schema: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DatasetVersionHistoryResponse(BaseModel):
    dataset_id: int
    dataset_name: str
    versions: list[DatasetVersionResponse]
    