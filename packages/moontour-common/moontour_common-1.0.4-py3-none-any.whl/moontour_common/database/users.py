from pymongo.errors import DuplicateKeyError

from moontour_common.database.clients.mongo import mongo_client
from moontour_common.models.user import InternalUser

users_collection = mongo_client.get_collection('users')


class UserExistsException(Exception):
    pass


def get_user(username: str) -> InternalUser | None:
    user_dict = users_collection.find_one({'username': username})
    return InternalUser(**user_dict) if user_dict else None


def create_user(user: InternalUser):
    try:
        users_collection.insert_one(user.json())
    except DuplicateKeyError:
        raise UserExistsException(f'User "{user.username}" already exists')
