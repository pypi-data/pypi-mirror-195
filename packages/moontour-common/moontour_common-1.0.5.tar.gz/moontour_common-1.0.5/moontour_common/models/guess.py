from datetime import datetime

from pydantic import BaseModel, Field

from moontour_common.models import Coordinates


class Guess(BaseModel):
    time: datetime = Field(default_factory=datetime.now)
    coordinates: Coordinates
