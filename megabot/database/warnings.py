from sqlalchemy import Column, BigInteger, Integer
from sqlalchemy.future import select
from megabot.database.db import Base, async_session

class Warning(Base):
    __tablename__ = "warnings"
    user_id = Column(BigInteger, primary_key=True)
    count = Column(Integer, default=0)

async def increase_warning(user_id: int) -> int:
    async with async_session() as session:
        result = await session.execute(select(Warning).where(Warning.user_id == user_id))
        row = result.scalar_one_or_none()

        if not row:
            row = Warning(user_id=user_id, count=1)
            session.add(row)
        else:
            row.count += 1

        await session.commit()
        return row.count
