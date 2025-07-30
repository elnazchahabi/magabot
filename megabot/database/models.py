# database/models.py
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, func
from megabot.database.db import Base

class User(Base):
    __tablename__ = "users"
    telegram_id = Column(BigInteger, primary_key=True)
    full_name = Column(String)
    username = Column(String)
    is_banned = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())




from megabot.database.db import async_session
from sqlalchemy.future import select

async def add_user_if_not_exists(telegram_id, full_name, username):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        if not user:
            new_user = User(
                telegram_id=telegram_id,
                full_name=full_name,
                username=username
            )
            session.add(new_user)
            await session.commit()



