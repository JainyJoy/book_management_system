from database import session_obj, User
from sqlalchemy.future import select

class UserRepository:
    def __init__(self):
        pass

    async def create_user(self, payload):
        """Create a user"""
        async with session_obj() as session:
            async with session.begin():
                user = User(**payload)
                session.add(user)
                session.commit()
                session.refresh(user)
        return True

    async def get_user_by_email(self, email):
        """Get user by email"""
        async with session_obj() as session:
            async with session.begin():
                stmt = select(User).filter_by(email=email)
                result = await session.execute(stmt)
                user = result.scalars().first()
        return user

