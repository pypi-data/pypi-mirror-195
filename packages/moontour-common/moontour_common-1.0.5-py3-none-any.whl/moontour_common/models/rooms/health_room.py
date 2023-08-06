from moontour_common.models.guess import Guess
from moontour_common.models.phase import HealthPhase
from moontour_common.models.rooms.room import BaseRoom


START_HEALTH = 5000


class HealthRoom(BaseRoom):
    start_health = START_HEALTH
    phase_count: int = 5
    phases: list[HealthPhase] = []
    guesses: list[dict[str, Guess]] = []  # user ID to guess
