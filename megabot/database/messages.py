from sqlalchemy import Column, Integer, BigInteger, Text, DateTime, func
from megabot.database.db import Base, async_session
from sqlalchemy.future import select

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    text = Column(Text)
    date = Column(DateTime, server_default=func.now())

async def save_message(user_id: int, text: str):
    async with async_session() as session:
        msg = Message(user_id=user_id, text=text)
        session.add(msg)
        await session.commit()
