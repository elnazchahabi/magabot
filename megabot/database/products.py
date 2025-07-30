from sqlalchemy import Column, Integer, String, BigInteger
from megabot.database.db import Base, async_session

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    price = Column(Integer)  # قیمت به تومان
    file_id = Column(String)  # شناسه فایل یا لینک

async def get_all_products():
    async with async_session() as session:
        result = await session.execute(Product.__table__.select())
        return result.fetchall()

async def get_product(product_id: int):
    async with async_session() as session:
        result = await session.execute(Product.__table__.select().where(Product.id == product_id))
        return result.first()
