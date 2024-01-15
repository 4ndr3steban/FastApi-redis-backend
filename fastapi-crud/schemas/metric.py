from pydantic import BaseModel


class Metric(BaseModel):
    id: int | None = None
    device_id: str
    metric_type: str
    metric_value: float
    timestamp: str
    