import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from moontour_common.models.phase import Phase


class RoomStatus(str, Enum):
    waiting = 'waiting'
    running = 'running'
    closed = 'closed'


class Player(BaseModel):
    user_id: str
    score: int = 0


class Room(BaseModel):
    id: str = Field(alias='id_', default_factory=lambda: str(uuid.uuid4()))
    status: RoomStatus = RoomStatus.waiting
    create_time: datetime = Field(default_factory=datetime.now)
    start_time: datetime | None = None
    phase_count: int = 5
    phases: list[Phase] = []
    max_player_count: int = 4
    players: set[Player] = []
