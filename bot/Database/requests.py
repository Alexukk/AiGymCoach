from .models import async_session
from .models import User
from sqlalchemy import select, Update


async def set_user(tg_id: int, data: dict):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            new_user = User(tg_id=tg_id, **data)
            session.add(new_user)
            await session.commit()


async def check_user_exists(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return True

        return False


async def get_user_data(tg_id: int) -> User | None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return user

        return None


async def update_user_field(tg_id: int, field_name: str, value: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            setattr(user, field_name, value)
            await session.commit()
