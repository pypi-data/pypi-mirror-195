from moontour_common.models.guess import Guess
from moontour_common.models.phase import Phase
from moontour_common.models.rooms.room import BaseRoom, RoomMode
from moontour_common.models.user import User


class StreakRoom(BaseRoom):
    mode = RoomMode.streak
    streak: int = 0
    phases: list[Phase] = []
    guesses: list[Guess] = []
    player: User | None
