from sqlalchemy import update, select
from megabot.database.db import async_session
from megabot.database.models import User

async def update_user_score(user_id: int, delta: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == user_id))
        user = result.scalar()
        if user:
            user.score += delta
            await session.commit()

async def get_user_score(user_id: int) -> int:
    async with async_session() as session:
        result = await session.execute(select(User.score).where(User.telegram_id == user_id))
        score = result.scalar()
        return score or 0