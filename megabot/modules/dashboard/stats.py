from sqlalchemy import select, func
from megabot.database.models import User
from megabot.database.orders import Order

from megabot.database.messages import Message


async def gather_stats(session):
    total_users = await session.scalar(select(func.count(User.id)))
    total_messages = await session.scalar(select(func.count(Message.id)))
    total_orders = await session.scalar(select(func.count(Order.id)))

    return {
        "users": total_users,
        "messages": total_messages,
        "orders": total_orders
    }