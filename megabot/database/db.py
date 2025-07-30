# database/db.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from megabot.config import DATABASE_URL

Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    from megabot.database.models import User
    from megabot.database.warnings import Warning
    from megabot.database.messages import Message
    from megabot.database.products import Product
    from megabot.database.orders import Order
    from megabot.database.tickets import Ticket

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
