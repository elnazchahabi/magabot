from sqlalchemy import Column, Integer, BigInteger, ForeignKey, Boolean, DateTime, func
from megabot.database.db import Base, async_session

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    product_id = Column(Integer, ForeignKey("products.id"))
    is_paid = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

async def create_order(user_id: int, product_id: int):
    async with async_session() as session:
        order = Order(user_id=user_id, product_id=product_id)
        session.add(order)
        await session.commit()
        return order.id

async def mark_order_paid(order_id: int):
    async with async_session() as session:
        await session.execute(
            Order.__table__.update().where(Order.id == order_id).values(is_paid=True)
        )
        await session.commit()
