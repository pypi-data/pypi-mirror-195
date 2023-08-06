from datetime import datetime, timedelta
from enum import Enum

from pydantic import BaseModel, Field


class PhaseStatus(str, Enum):
    waiting = 'waiting'
    running = 'running'
    closed = 'closed'


class Guess(BaseModel):
    time: datetime
    coordinates: str


class Phase(BaseModel):
    start_time: datetime = Field(default_factory=datetime.now)
    duration: timedelta
    guesses: dict[str, Guess] = {}  # user ID to guess
