from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, func
from megabot.database.db import Base, async_session
from sqlalchemy.future import select

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    question = Column(String)
    answer = Column(String, nullable=True)
    is_closed = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

async def create_ticket(user_id: int, question: str) -> int:
    async with async_session() as session:
        ticket = Ticket(user_id=user_id, question=question)
        session.add(ticket)
        await session.commit()
        return ticket.id

async def get_all_open_tickets():
    async with async_session() as session:
        result = await session.execute(select(Ticket).where(Ticket.is_closed == False))
        return result.scalars().all()

async def answer_ticket(ticket_id: int, answer: str):
    async with async_session() as session:
        await session.execute(
            Ticket.__table__.update()
            .where(Ticket.id == ticket_id)
            .values(answer=answer, is_closed=True)
        )
        await session.commit()

async def get_ticket_by_id(ticket_id: int):
    async with async_session() as session:
        result = await session.execute(select(Ticket).where(Ticket.id == ticket_id))
        return result.scalar_one_or_none()
