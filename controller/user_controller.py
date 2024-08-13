from repository import UserRepository
from database import User
from utils.status import *
from utils.user_util import *


class UserController:
    def __init__(self):
        self.__user_repo = UserRepository()

    async def register_user(self, payload: dict):
        check_user = await self.__user_repo.get_user_by_email(payload["email"])
        if check_user:
            return "User already exists with the same enail", HTTP_400_BAD_REQUEST
        payload["password"] = get_hashed_password(payload["password"])
        await self.__user_repo.create_user(payload)
        return "User registration successful", HTTP_201_CREATED

    async def login_user(self, payload):
        db_record = await self.__user_repo.get_user_by_email(payload["email"])
        if not db_record or not check_password(payload["password"], db_record.password):
            return "Invalid credentials", HTTP_401_UNAUTHORIZED
        return "credential validated", HTTP_200_OK

    def fetch_user_profile(self, email=None):
        user_record = self.__user_repo.get_user_by_email(email)
        if not isinstance(user_record, User) or not user_record:
            return NOT_FOUND_MSG, HTTP_404_NOT_FOUND
        user_record = {"user_id": user_record.id,
                       "email": user_record.email,
                       "first_name": user_record.first_name,
                       "middle_name": user_record.middle_name,
                       "last_name": user_record.last_name,
                       "created_at": user_record.created_at}
        return user_record, HTTP_200_OK
