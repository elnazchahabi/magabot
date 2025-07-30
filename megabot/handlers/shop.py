from aiogram import Router, types, F
from aiogram.filters import Command
from megabot.database.products import get_all_products, get_product
from megabot.database.orders import create_order
from megabot.keyboards.shop import product_buttons

router = Router()

@router.message(Command("shop"))
async def show_shop(message: types.Message):
    products = await get_all_products()
    if not products:
        await message.answer("فعلاً محصولی وجود ندارد.")
        return
    await message.answer("🛍 محصولات موجود:", reply_markup=product_buttons(products))

@router.callback_query(F.data.startswith("buy_"))
async def buy_product(callback: types.CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    product = await get_product(product_id)
    if not product:
        await callback.message.answer("محصول یافت نشد.")
        return

    order_id = await create_order(callback.from_user.id, product_id)
    await callback.message.answer(
        f"شما <b>{product.title}</b> را انتخاب کردید.\n"
        f"💵 قیمت: {product.price} تومان\n"
        f"برای تست پرداخت، این پیام فقط شبیه‌سازی است.\n"
        f"✅ پرداخت فرضی انجام شد، فایل محصول ارسال می‌شود..."
    )
    await callback.message.answer_document(product.file_id)
