from redis.client import Pipeline
from redis.commands.json.path import Path
from redis.commands.search.query import Query

from moontour_common.database.clients.redis import redis_client
from moontour_common.models.phase import Phase
from moontour_common.models.room import Room

ROOMS_INDEX = 'rooms_idx'
ROOM_KEY_PREFIX = 'room:'


class RoomJoiningException(Exception):
    pass


def _get_room_key(room_id: str):
    return f'{ROOM_KEY_PREFIX}{room_id}'


def create_room(room: Room):
    redis_client.json().set(_get_room_key(room.id), Path.root_path(), room.json(exclude={'id'}))


def get_room(room_id: str) -> Room:
    room_dict = redis_client.json().get(_get_room_key(room_id), Path.root_path())
    return Room(**room_dict)


def join_room(room_id: str, user_id: str):
    room_key = _get_room_key(room_id)

    def transaction(pipe: Pipeline):
        if pipe.json().arrlen(room_key, Path('.players')) >= pipe.json().get(room_key, Path('.max_player_count')):
            raise RoomJoiningException('Room is full')

        if pipe.json().get(room_key, Path('.start_time')) is not None:
            raise RoomJoiningException('Room is already running')

        pipe.json().arrappend(room_key, Path('.players'), user_id)

    redis_client.transaction(transaction, room_key)


def find_waiting_room() -> Room | None:
    result = redis_client.ft(ROOMS_INDEX).search(Query('@status:{waiting}'))
    if len(result.docs) == 0:
        return None
    room = Room(**result.docs[0])
    return room


def add_phase(room_id: str, phase: Phase):
    redis_client.json().arrappend(_get_room_key(room_id), Path('.phases'), phase)
