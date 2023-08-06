import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class RoomMode(str, Enum):
    streak = 'streak'
    duel = 'duel'
    teams = 'teams'


class RoomStatus(str, Enum):
    waiting = 'waiting'
    running = 'running'


class BaseRoom(BaseModel):
    id: str = Field(alias='id_', default_factory=lambda: str(uuid.uuid4()))
    mode: RoomMode
    map: str = 'world'
    status: RoomStatus = RoomStatus.waiting
    create_time: datetime = Field(default_factory=datetime.now)
    start_time: datetime | None = None
