# magabot
مگابات تلگرام
 بیا خط به خط فایل `main.py` رو با هم بررسی کنیم. این فایل حکم مغز اصلی پروژه رو داره، مثل وقتی که تلویزیونو روشن می‌کنی، اینجا هم ما ربات رو روشن می‌کنیم!

---

## 🔹 خط اول:

```python
import asyncio
```

این کتابخونه مخصوص کارهای **همزمان (asynchronous)** هست. مثل اینه که به جای اینکه صبر کنیم یک کار تموم شه، چندتا کارو با هم انجام بدیم.

---

## 🔹 خط دوم تا هشتم: ماژول‌ها رو وارد می‌کنیم:

```python
from megabot.bot import bot, dp
```

ما اینجا ربات و dispatcher (مدیر پخش پیام‌ها) رو وارد می‌کنیم. `bot` همون ماشینیه که به تلگرام وصل می‌شه و پیام‌ها رو می‌فرسته. `dp` هم کسیه که پیام‌ها رو مدیریت می‌کنه.

```python
from megabot.database.db import init_db
```

تابع `init_db` دیتابیس رو راه میندازه. یعنی مثل اینکه بگیم "دفتر یادداشت‌مون رو باز کن!"

```python
from megabot.handlers import start, help
from megabot.handlers import shop, ticket, ai_handler
from megabot.handlers import quiz_handler, admin_dashboard_handler
```

اینا همه‌اشون فایل‌هایی هستن که دستورات مختلفی رو مدیریت می‌کنن. مثلاً:

* `/start` و `/help`
* فروشگاه (`shop`)
* پشتیبانی (`ticket`)
* چت‌بات هوشمند (`ai_handler`)
* آزمون و سرگرمی (`quiz_handler`)
* آمار و گزارش ادمین (`admin_dashboard_handler`)

---

## 🔹 خط:

```python
from megabot.utils.logger import setup_logger
```

اینجا یه سیستمی برای لاگ‌گرفتن داریم؛ یعنی مثل جعبه سیاه هواپیما، هر اتفاقی می‌افته، توی فایل لاگ ثبت می‌کنه.

---

## 🔹 خط:

```python
from megabot.middlewares.message_logger import MessageLoggerMiddleware
from megabot.middlewares.anti_spam import AntiSpamMiddleware
```

اینا مثل "نگهبان‌ها" هستن که وسط راه پیام رو می‌گیرن:

* اولی پیام‌ها رو ثبت می‌کنه (کی چی گفت)
* دومی جلوی اسپم رو می‌گیره (اگه کسی زیاد پیام بده یا حرف بد بزنه، اخطار یا بنش می‌کنه)

---

## ✅ حالا بریم سراغ تابع اصلی برنامه:

```python
async def main():
```

یه تابع غیرهمزمانه، یعنی می‌تونه چند کارو با هم انجام بده.

### داخلش چه خبره؟ ببین:

```python
    setup_logger()
```

جعبه سیاه رو روشن می‌کنیم.

```python
    await init_db()
```

دیتابیس رو راه‌اندازی می‌کنیم.

---

### بعدش نگهبان‌ها رو می‌ذاریم سر جاشون:

```python
    dp.update.middleware.register(MessageLoggerMiddleware())
    dp.update.middleware.register(AntiSpamMiddleware())
```

---

### بعد همه‌ی مدیرای بخش‌ها رو صدا می‌زنیم:

```python
    dp.include_router(start.router)
    dp.include_router(help.router)
    ...
```

هر کدوم از اینا مسئول یه بخش هستن، مثلا:

* `start.router`: وقتی یکی `/start` می‌زنه
* `shop.router`: وقتی کاربر می‌ره فروشگاه
* `ai_handler.router`: وقتی ربات قراره هوشمند جواب بده
  و...

---

### در نهایت:

```python
    print("✅ Bot is running...")
    await dp.start_polling(bot)
```

این یعنی: برو رباتو روشن کن و هرکی هرچی گفت، گوش بده و جواب بده.

---

### و در انتها:

```python
if __name__ == "__main__":
    asyncio.run(main())
```

این یعنی وقتی فایل مستقیماً اجرا شد، برنامه‌ی ما از `main()` شروع می‌شه.

===============================================================================================================================
bot.py



```python
from aiogram import Bot, Dispatcher
```

ماژول اصلی `aiogram` رو وارد کردیم که دو چیز مهم داره:

* `Bot`: برای ارتباط با تلگرام
* `Dispatcher`: برای مدیریت پیام‌هایی که دریافت می‌شه (مثل منشی یا مدیر پخش)

---

### 2.

```python
from aiogram.enums import ParseMode
```

می‌خوایم تعیین کنیم که پیام‌ها با چه فرمتی فرستاده بشن. مثلاً با HTML یا Markdown. این به ربات اجازه می‌ده متن‌های قشنگ (بولد، لینک‌دار، رنگی و...) ارسال کنه.

---

### 3.

```python
from aiogram.client.default import DefaultBotProperties
```

با این خط، ویژگی‌های پیش‌فرض ربات رو تنظیم می‌کنیم. مثل اینکه بگیم: "همیشه با فونت HTML بنویس."

---

### 4.

```python
from megabot.config import BOT_TOKEN
```

توکن ربات رو از فایل تنظیمات (config) می‌گیریم. ما توکن رو تو `.env` ذخیره کردیم که امن باشه و مستقیم توی کد ننویسیم.

---

## ✅ حالا دو خط اصلی:

### 5. ساختن ربات:

```python
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
```

ما اینجا ربات‌مون رو "می‌سازیم" و می‌گیم:

* از این توکن استفاده کن
* و همه پیام‌هاتو با HTML بفرست

---

### 6. ساختن Dispatcher:

```python
dp = Dispatcher()
```

اینجا هم یک **dispatcher** می‌سازیم که قراره همه پیام‌ها رو بررسی کنه و بفرسته به هندلرهای مربوطه.

---

💡 پس خلاصه:

* `bot`: ارتباط با تلگرام
* `dp`: مدیریت پیام‌ها
* هر دو ساخته شدن تا در `main.py` ازشون استفاده کنیم

=======================================================================================================================
config.py

## 🧠 خط به خط بریم جلو:

### 1.

```python
import os
from dotenv import load_dotenv
```

اینجا ما از کتابخونه‌ی `dotenv` استفاده می‌کنیم تا بتونیم متغیرهایی که داخل فایل `.env` نوشتیم رو به صورت امن بخونیم.
فایده‌اش چیه؟ اینکه توکن‌ها و رمزها رو داخل کد اصلی نمی‌نویسیم!

---

### 2.

```python
load_dotenv()
```

این خط فایل `.env` رو بارگذاری می‌کنه و آماده‌ش می‌کنه برای اینکه بتونیم ازش متغیر بخونیم.

---

### 3.

```python
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
```

اینجا دو تا متغیر مهم رو از `.env` می‌خونیم:

* `BOT_TOKEN`: رمز ربات تلگرام
* `DATABASE_URL`: آدرس دیتابیس PostgreSQL

---

### 4.

```python
ADMINS = [int(x) for x in os.getenv("ADMINS", "").split(",") if x]
```

یک لیست از آیدی‌های ادمین‌ها. مثلاً اگه تو `.env` اینو نوشته باشیم:

```
ADMINS=12345678,987654321
```

این خط تبدیلش می‌کنه به:

```python
ADMINS = [12345678, 987654321]
```

---

## 🧠 پارت دوم فایل:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str = "your-key-here"
    # سایر تنظیمات

settings = Settings()
```

### این چیه؟

اینجا از پکیج [pydantic](https://docs.pydantic.dev/) استفاده کردیم تا تنظیمات رو حرفه‌ای‌تر مدیریت کنیم.

این `Settings`:

* می‌تونه خودش از `.env` پر بشه
* و همه‌ی تنظیمات مثل `openai_api_key` رو به صورت یک آبجکت تمیز به ما بده.

---

### 🔐 پس به طور خلاصه:

* از `.env` متغیرها رو می‌خونیم (توکن، دیتابیس، ادمین‌ها)
* با `pydantic` تنظیمات پیچیده‌تر (مثل OpenAI API key) رو نگه می‌داریم
==============================================================================================================================
 `.env` 


## 🔐 تنظیمات امنیتی و اتصال:

### ✅ توکن ربات:

```env
BOT_TOKEN=
```

این رمز اصلی ربات تلگرامه. اگه لو بره، هر کسی می‌تونه کنترل رباتتو بگیره!

---

### ✅ اطلاعات دیتابیس:

```

اینا برای اتصال به دیتابیس PostgreSQL هستن:

* روی هم می‌گن: "برو به دیتابیس محلی به نام `megabot` با یوزر `mega_user` و پسوردش `4202elnaz` وصل شو."

### ✅ لیست ادمین‌ها:

```env
ADMINS=123456789
```

اینجا آی‌دی تلگرام ادمین‌هاست. مثلاً فقط کاربر `123456789` دسترسی ادمینی داره.

---

## ✅ نتیجه‌گیری:

* این فایل یکی از ستون‌های اصلی پروژه‌ست.
* همه چی رو امن و تمیز از محیط می‌گیره.
* با ترکیب `config.py` و `.env`، پروژه کاملاً **ماژولار و امن** طراحی شده.

===============================================================================================
حالا اومدیم سراغ اولین برخورد کاربر با ربات:
فایل `start.py` توی پوشه‌ی `handlers` قرار داره و دقیقاً همون چیزی رو انجام می‌ده که اسمش می‌گه: هندل کردن دستور `/start`

---

## 🎯 هدف:

وقتی یه کاربر جدید `/start` می‌فرسته:

1. اطلاعاتش ذخیره می‌شه (اگه قبلاً نبود)
2. پیام خوش‌آمد دریافت می‌کنه

---

## 🧠 خط به خط توضیح:

### 1.

```python
from aiogram import Router, types
```

* `Router`: مثل صفحۀ جداگانه‌ای برای مدیریت یه سری دستور خاصه.
* `types`: برای استفاده از کلاس‌هایی مثل `Message`, `User` و...

---

### 2.

```python
from aiogram.filters import CommandStart
```

این یه فیلتره که می‌گه: "اگه پیامی شامل `/start` بود، این تابع رو اجرا کن!"

---

### 3.

```python
from megabot.database.models import add_user_if_not_exists
```

این تابع از دیتابیس میاد و مسئول ثبت کاربر جدید توی جدول `users` هست (در ادامه کدش رو هم می‌بینیم).

---

### 4.

```python
router = Router()
```

اینجا یک router مخصوص این فایل ساخته می‌شه. بعداً توی `main.py` این Router به dispatcher وصل می‌شه.

---

### 5.

```python
@router.message(CommandStart())
async def start_handler(message: types.Message):
```

هر وقت کاربر دستور `/start` داد، این تابع اجرا می‌شه.
همیشه `message` همون پیامی هست که کاربر فرستاده.

---

### 6.

```python
    user = message.from_user
```

کاربر ارسال‌کننده پیام رو می‌گیریم: آی‌دی، نام کامل، یوزرنیم و...

---

### 7.

```python
    await add_user_if_not_exists(user.id, user.full_name, user.username)
```

کاربر رو توی دیتابیس ذخیره می‌کنیم. اگه از قبل ثبت شده باشه، کاری نمی‌کنه. (کد کاملش رو بررسی می‌کنیم الان)

---

### 8.

```python
    await message.answer(f"سلام {user.full_name} 👋\nبه Mega Bot خوش اومدی!")
```

و در نهایت، به کاربر یه پیام خوش‌آمد نمایش می‌ده.
===============================================================================================================


## 🔸 اول کلاس `User`

```python
class User(Base):
    __tablename__ = "users"
```

اینجا داریم یک جدول به نام `users` تعریف می‌کنیم با استفاده از SQLAlchemy.

---

### 📦 ستون‌های جدول:

```python
telegram_id = Column(BigInteger, primary_key=True)
```

* آیدی تلگرام که نقش "شناسه یکتا" رو داره (Primary Key)

```python
full_name = Column(String)
username = Column(String)
```

* اسم کامل و یوزرنیم کاربر

```python
is_banned = Column(Boolean, default=False)
```

* وضعیت بن‌شدن کاربر (برای اسپم‌زن‌ها به درد می‌خوره)

```python
created_at = Column(DateTime, server_default=func.now())
```

* زمان عضویت (خودکار پر می‌شه با زمان فعلی)

---

## 🔸 حالا تابع اصلی: `add_user_if_not_exists`

```python
async def add_user_if_not_exists(telegram_id, full_name, username):
```

این تابع می‌گه:

1. اگر کاربری با این آیدی توی دیتابیس نبود...
2. اون رو اضافه کن

---

### داخلش:

```python
async with async_session() as session:
```

با `async_session` یه اتصال جدید به دیتابیس باز می‌کنیم.

---

```python
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()
```

اینجا بررسی می‌کنیم: "آیا این کاربر توی جدول `users` وجود داره یا نه؟"

---

```python
if not user:
    new_user = User(
        telegram_id=telegram_id,
        full_name=full_name,
        username=username
    )
    session.add(new_user)
    await session.commit()
```

اگر کاربر وجود نداشت:

* یه شیء جدید از کلاس `User` می‌سازیم
* اون رو به دیتابیس اضافه می‌کنیم
* و `commit` می‌کنیم تا ذخیره بشه
================================================================================================================================
 حالا رسیدیم به مغز دیتابیس ربات یعنی فایل `db.py` 🧠
این فایل مسئول اتصال به دیتابیس PostgreSQL و ساختن جدول‌هاست.


## 🧱 ۱. ایمپورت کتابخونه‌ها:

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from megabot.config import DATABASE_URL
```

* `create_async_engine`: موتور اتصال Async به PostgreSQL
* `AsyncSession`: سشن برای کار async با دیتابیس
* `sessionmaker`: ساخت سشن‌های متعدد
* `declarative_base`: پایه‌ای برای تعریف مدل‌ها (`Base`)
* `DATABASE_URL`: مسیر اتصال از `.env`

---

## 🏗️ ۲. تعریف ابزارهای اصلی:

```python
Base = declarative_base()
```

پایه‌ای برای ساختن مدل‌ها مثل `User`, `Order`, ...

```python
engine = create_async_engine(DATABASE_URL, echo=True)
```

اینجا به PostgreSQL وصل می‌شیم. `echo=True` یعنی دستورات SQL هم توی لاگ نشون داده می‌شن (برای دیباگ خوبه).

```python
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```

این خط سازنده‌ی sessionهاست. با `expire_on_commit=False`، داده‌ها بعد از ذخیره از حافظه پاک نمی‌شن.

---

## 🔄 ۳. تابع `init_db()`:

```python
async def init_db():
```

وقتی پروژه بالا میاد، این تابع صدا زده می‌شه تا اگر جدول‌ها هنوز ساخته نشدن، ساخته بشن.

---

### ایمپورت مدل‌ها:

```python
from megabot.database.models import User
from megabot.database.warnings import Warning
from megabot.database.messages import Message
from megabot.database.products import Product
from megabot.database.orders import Order
from megabot.database.tickets import Ticket
```

اینجا همه‌ی مدل‌های دیتابیس رو وارد می‌کنیم چون اگر وارد نکنیم، SQLAlchemy متوجه وجودشون نمی‌شه!

---

### ساخت جدول‌ها:

```python
async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
```

با این خط، همه‌ی جدول‌هایی که با `Base` ساخته شده‌ن رو داخل دیتابیس ایجاد می‌کنه.
یعنی اگر `users`, `orders`, `products`, ... وجود نداشتن، اون‌ها رو می‌سازه.

---

## ✅ جمع‌بندی:

| جزء             | نقش                      |
| --------------- | ------------------------ |
| `Base`          | پایه‌ی تعریف مدل‌ها      |
| `engine`        | اتصال به PostgreSQL      |
| `async_session` | مدیریت سشن برای کوئری‌ها |
| `init_db()`     | ساخت جدول‌های دیتابیس    |
=========================================================================================================
 `products.py`

## 📦 کلاس `Product`

```python
class Product(Base):
    __tablename__ = "products"
```

تعریف یک جدول به اسم `products` در دیتابیس.

### ستون‌ها:

```python
id = Column(Integer, primary_key=True)
```

شناسه یکتا برای هر محصول (توسط دیتابیس خودکار پر می‌شه)

```python
title = Column(String)
description = Column(String)
```

عنوان محصول و توضیحش

```python
price = Column(Integer)  # قیمت به تومان
```

قیمت محصول (توضیح خوب داده: قیمت به "تومان")

```python
file_id = Column(String)  # شناسه فایل یا لینک
```

این می‌تونه:

* شناسه فایل تلگرام باشه (برای ارسال فایل خودکار)
* یا لینک دانلود

---

## 🔍 توابع مربوط به دیتابیس:

### 1. دریافت همه‌ی محصولات:

```python
async def get_all_products():
    async with async_session() as session:
        result = await session.execute(Product.__table__.select())
        return result.fetchall()
```

این تابع برای نمایش لیست محصولات توی فروشگاه استفاده می‌شه.
همه محصولات جدول رو می‌خونه و به‌صورت لیست برمی‌گردونه.

---

### 2. دریافت یک محصول خاص:

```python
async def get_product(product_id: int):
    async with async_session() as session:
        result = await session.execute(
            Product.__table__.select().where(Product.id == product_id)
        )
        return result.first()
```

وقتی کاربر یک محصول خاص رو انتخاب کنه، این تابع فقط اون محصول رو از دیتابیس می‌گیره.

---

## ✅ خلاصه:

| تابع / کلاس          | کاربرد                                |
| -------------------- | ------------------------------------- |
| `Product`            | تعریف مدل محصول                       |
| `get_all_products()` | گرفتن لیست همه‌ی محصولات برای فروشگاه |
| `get_product(id)`    | گرفتن یک محصول خاص برای نمایش یا خرید |
============================================================================================================================

`orders.py` 🧾

## 📦 کلاس `Order`

```python
class Order(Base):
    __tablename__ = "orders"
```

جدولی به نام `orders` تعریف می‌کنیم که هر سطرش نماینده‌ی یک سفارشه.

### ستون‌ها:

```python
id = Column(Integer, primary_key=True)
```

شناسه سفارش (خودکار توسط دیتابیس پر می‌شه)

```python
user_id = Column(BigInteger)
```

آی‌دی تلگرام کاربر سفارش‌دهنده

```python
product_id = Column(Integer, ForeignKey("products.id"))
```

محصولی که کاربر خریده (با کلید خارجی به جدول `products` متصل می‌شه)

```python
is_paid = Column(Boolean, default=False)
```

آیا پرداخت موفق بوده؟ (پیش‌فرض: False)

```python
created_at = Column(DateTime, server_default=func.now())
```

زمان ثبت سفارش

---

## 🔁 توابع عملیاتی:

### 1. ساخت سفارش جدید:

```python
async def create_order(user_id: int, product_id: int):
    ...
```

* یک سفارش جدید با `user_id` و `product_id` ایجاد می‌کنه.
* وضعیت پرداخت `False` می‌مونه تا بعداً تأیید بشه.
* پس از `commit`، `id` سفارش رو برمی‌گردونه.

📦 این معمولاً وقتی اجرا می‌شه که کاربر محصولی رو انتخاب کرده، ولی هنوز پرداخت نکرده.

---

### 2. علامت‌گذاری پرداخت موفق:

```python
async def mark_order_paid(order_id: int):
    ...
```

* سفارش با `order_id` رو پیدا می‌کنه.
* `is_paid` رو برابر `True` می‌ذاره.
* و در دیتابیس ذخیره می‌کنه.

🧾 این وقتی اجرا می‌شه که کاربر از درگاه پرداخت برمی‌گرده و موفق بوده.

---

## ✅ خلاصه عملکرد:

| تابع / کلاس                         | نقش                               |
| ----------------------------------- | --------------------------------- |
| `Order`                             | مدل جدول سفارشات                  |
| `create_order(user_id, product_id)` | ثبت یک سفارش جدید (پرداخت‌نشده)   |
| `mark_order_paid(order_id)`         | تأیید پرداخت موفق برای سفارش مشخص |
============================================================================================================================

فایل `shop.py` توی پوشه‌ی `handlers/` جاییه که تعامل واقعی کاربر با محصولات و خرید انجام می‌شه.


## 📦 واردات‌ها:

```python
from aiogram import Router, types, F
from aiogram.filters import Command
```

ابزارهای اصلی برای مدیریت پیام‌ها و دستورها (`/shop` و دکمه‌ها)

```python
from megabot.database.products import get_all_products, get_product
from megabot.database.orders import create_order
```

دسترسی به لیست محصولات و ثبت سفارش جدید

```python
from megabot.keyboards.shop import product_buttons
```

ایجاد کیبورد با دکمه‌های محصولات

---

## 🔸 تعریف Router:

```python
router = Router()
```

یک مسیر جدا برای مدیریت فروشگاه

---

## 🛍 بخش اول: نمایش لیست محصولات

```python
@router.message(Command("shop"))
async def show_shop(message: types.Message):
```

### این تابع اجرا می‌شه وقتی کاربر `/shop` بفرسته:

```python
products = await get_all_products()
if not products:
    await message.answer("فعلاً محصولی وجود ندارد.")
    return
```

* از دیتابیس لیست محصولات رو می‌گیریم
* اگر لیست خالی بود، پیام "محصولی نیست" می‌دیم

```python
await message.answer("🛍 محصولات موجود:", reply_markup=product_buttons(products))
```

* دکمه‌های مربوط به هر محصول رو با `product_buttons` می‌سازیم
* و به کاربر نمایش می‌دیم

---

## 🧾 بخش دوم: خرید محصول (کلیک روی دکمه)

```python
@router.callback_query(F.data.startswith("buy_"))
async def buy_product(callback: types.CallbackQuery):
```

اگر کاربر روی یکی از دکمه‌ها کلیک کنه که دیتای اون دکمه با `"buy_"` شروع بشه، این تابع اجرا می‌شه.

### داخلش:

```python
product_id = int(callback.data.split("_")[1])
product = await get_product(product_id)
```

* آیدی محصول رو از متن دکمه جدا می‌کنیم
* محصول رو از دیتابیس می‌گیریم

```python
if not product:
    await callback.message.answer("محصول یافت نشد.")
    return
```

اگر محصول وجود نداشت، پیام خطا

---

### ثبت سفارش فرضی:

```python
order_id = await create_order(callback.from_user.id, product_id)
```

سفارش ثبت می‌شه (پرداخت‌نشده فعلاً)

---

### شبیه‌سازی پرداخت موفق:

```python
await callback.message.answer(
    f"شما <b>{product.title}</b> را انتخاب کردید.\n"
    f"💵 قیمت: {product.price} تومان\n"
    f"برای تست پرداخت، این پیام فقط شبیه‌سازی است.\n"
    f"✅ پرداخت فرضی انجام شد، فایل محصول ارسال می‌شود..."
)
await callback.message.answer_document(product.file_id)
```

* به کاربر می‌گه که خرید فرضی موفق بود
* فایل محصول (از `file_id`) رو براش می‌فرسته

---

## ✅ نتیجه‌گیری:

| مرحله             | عملکرد                         |
| ----------------- | ------------------------------ |
| `/shop`           | نمایش لیست محصولات             |
| کلیک روی دکمه     | ثبت سفارش                      |
| ارسال پیام و فایل | پرداخت فرضی موفق و تحویل محصول |

---

نکته مهم: این نسخه برای تسته و هنوز به درگاه پرداخت واقعی مثل **زرین‌پال یا کریپتو** وصل نشده.
در آینده فقط کافیه جای اون قسمت پیام فرضی، لینک درگاه و تأیید پرداخت واقعی رو بذاریم.

============================================================================================
رسیدیم به بخش پشتیبانی! 🎟
تو فایل `tickets.py` زیرساختی برای ثبت و مدیریت تیکت‌های کاربران تعریف شده — یعنی وقتی کسی مشکلی داره یا سوالی می‌پرسه، اینجا ذخیره و پیگیری می‌شه.

---

## 🏛 کلاس `Ticket`

```python
class Ticket(Base):
    __tablename__ = "tickets"
```

مدل جدول `tickets` برای نگهداری تیکت‌های ارسالی کاربران.

### ستون‌ها:

```python
id = Column(Integer, primary_key=True)
user_id = Column(BigInteger)
question = Column(String)
answer = Column(String, nullable=True)
is_closed = Column(Boolean, default=False)
created_at = Column(DateTime, server_default=func.now())
```

| ستون         | توضیح                         |
| ------------ | ----------------------------- |
| `id`         | شماره تیکت                    |
| `user_id`    | آیدی تلگرام کاربر ارسال‌کننده |
| `question`   | متن سوال یا مشکل              |
| `answer`     | پاسخ ادمین (ممکنه خالی باشه)  |
| `is_closed`  | تیکت بسته شده یا نه           |
| `created_at` | زمان ارسال تیکت               |

---

## 📬 توابع اصلی

### 1. ثبت تیکت جدید:

```python
async def create_ticket(user_id: int, question: str) -> int:
```

تیکت جدید می‌سازه و `id` اون رو برمی‌گردونه.

---

### 2. گرفتن لیست تیکت‌های باز:

```python
async def get_all_open_tickets():
```

همه‌ی تیکت‌هایی که هنوز بسته نشده‌اند رو از دیتابیس می‌خونه. برای استفاده در پنل ادمین خیلی مهمه.

---

### 3. پاسخ دادن به یک تیکت:

```python
async def answer_ticket(ticket_id: int, answer: str):
```

تیکت رو با `answer` پر می‌کنه و `is_closed=True` می‌ذاره (یعنی بسته می‌شه).

---

### 4. گرفتن یک تیکت خاص:

```python
async def get_ticket_by_id(ticket_id: int):
```

برای نمایش جزئیات یک تیکت خاص (مثلاً در پنل ادمین)

---

## ✅ جمع‌بندی:

| تابع                   | عملکرد                |
| ---------------------- | --------------------- |
| `create_ticket`        | ثبت تیکت جدید         |
| `get_all_open_tickets` | دریافت تیکت‌های باز   |
| `answer_ticket`        | پاسخ دادن و بستن تیکت |
| `get_ticket_by_id`     | نمایش یک تیکت خاص     |
==============================================================================================================
عالــیه! 👏 الان کامل سیستم **پشتیبانی ربات** رو داریم:
در این فایل `ticket.py`، نحوه ثبت تیکت توسط کاربر و پاسخ‌دهی ادمین رو بررسی می‌کنیم.
بیایم با هم مثل یک استاد دقیق بریم جلو:

---

## 🎯 هدف کلی:

* کاربر `/ticket` می‌زنه و سوالش رو می‌فرسته
* ربات تیکت رو ذخیره می‌کنه
* به ادمین اطلاع می‌ده
* ادمین جواب می‌ده
* ربات جواب رو برای کاربر می‌فرسته

---

## 📦 ساختار فایل:

### ایمپورت‌ها:

```python
from aiogram.fsm.state import State, StatesGroup
```

برای مدیریت وضعیت گفتگو (FSM)

```python
from megabot.database.tickets import create_ticket, get_all_open_tickets, ...
```

توابع مرتبط با دیتابیس تیکت‌ها

```python
from megabot.keyboards.ticket import ticket_admin_buttons
```

کیبورد مخصوص ادمین برای پاسخ دادن

---

## 🧠 وضعیت‌ها (State)

```python
class TicketState(StatesGroup):
    waiting_for_question = State()
    waiting_for_answer = State()
```

ما دو وضعیت داریم:

1. کاربر داره سوالشو می‌فرسته
2. ادمین داره پاسخ می‌ده

---

## 📨 مرحله ۱: ثبت تیکت

```python
@router.message(Command("ticket"))
async def ask_ticket(message, state):
```

کاربر `/ticket` بزنه، وارد حالت پرسش می‌شه:

```python
await state.set_state(TicketState.waiting_for_question)
```

---

```python
@router.message(TicketState.waiting_for_question)
async def save_ticket(message, state):
```

توی این مرحله:

* تیکت در دیتابیس ذخیره می‌شه
* پیام موفقیت برای کاربر فرستاده می‌شه
* وضعیت گفتگو پاک می‌شه
* و مهم‌تر: پیام به ادمین‌ها هم فرستاده می‌شه با دکمه پاسخ!

```python
await message.bot.send_message(
    admin,
    f"📩 تیکت جدید #{ticket_id}:\\n{message.text}",
    reply_markup=ticket_admin_buttons(ticket_id)
)
```

---

## 📝 مرحله ۲: پاسخ ادمین

```python
@router.callback_query(F.data.startswith("reply_"))
```

اگر ادمین روی دکمه پاسخ کلیک کنه:

* آیدی تیکت رو از دکمه درمیاریم
* وارد وضعیت `waiting_for_answer` می‌شیم

---

```python
@router.message(TicketState.waiting_for_answer)
```

ادمین پاسخ می‌نویسه:

* تیکت رو از دیتابیس می‌خونیم
* متن پاسخ رو ذخیره می‌کنیم
* وضعیت تیکت بسته می‌شه (`is_closed = True`)
* پاسخ برای کاربر ارسال می‌شه:

```python
await message.bot.send_message(
    ticket.user_id,
    f"🟢 پاسخ به تیکت شما:\n{message.text}"
)
```

---

## ✅ نتیجه کلی:

| نقش   | عملکرد                                        |
| ----- | --------------------------------------------- |
| کاربر | `/ticket` می‌زنه → سؤالش رو می‌نویسه          |
| ربات  | تیکت رو ذخیره می‌کنه و به ادمین خبر می‌ده     |
| ادمین | روی دکمه کلیک می‌کنه و پاسخ می‌ده             |
| ربات  | پاسخ رو برای کاربر می‌فرسته و تیکت رو می‌بنده |

---=====================================================================================================
وایسا که رسیدیم به یکی از خفن‌ترین بخش‌های ربات: **ماژول هوش مصنوعی** 🤖🧠
فایل `ai_handler.py` توی `handlers/`، مغز چت‌باته که کارهای هوشمند انجام می‌ده. بیایم دقیق بررسیش کنیم.

---

## 📦 کارهایی که این ماژول انجام می‌ده:

| دستور            | عملکرد                       |
| ---------------- | ---------------------------- |
| `/ask سوال`      | استفاده از ChatGPT برای پاسخ |
| `/translate متن` | ترجمه به انگلیسی             |
| `/summarize متن` | خلاصه‌سازی متن               |
| ارسال عکس        | OCR (تشخیص متن در عکس)       |
| ارسال ویس        | تبدیل ویس به متن             |

---

## 🧠 بخش اول: ChatGPT

```python
@router.message(F.text.startswith('/ask'))
async def handle_chatgpt(message: Message):
```

اگر کاربر `/ask` بزنه:

* باقی متن جدا می‌شه:

```python
prompt = message.text.replace('/ask', '').strip()
```

* اگه خالی بود، هشدار می‌ده:

```python
if not prompt:
    await message.answer("✏️ لطفا سوال خود را وارد کنید.")
```

* در غیر این صورت، می‌فرسته به تابع `ask_chatgpt`:

```python
reply = await ask_chatgpt(prompt)
await message.answer(reply)
```

---

## 🌍 ترجمه:

```python
@router.message(F.text.startswith('/translate'))
async def handle_translate(message: Message):
```

* متن بعد از `/translate` جدا می‌شه
* فرستاده می‌شه به تابع `translate_text`
* خروجی نمایش داده می‌شه

---

## 📚 خلاصه‌سازی:

```python
@router.message(F.text.startswith('/summarize'))
```

دقیقاً مشابه ترجمه، فقط با تابع `summarize_text`

---

## 🖼 OCR از عکس:

```python
@router.message(F.photo)
async def handle_ocr(message: Message):
```

اگر کاربر عکس بفرسته:

1. عکس ذخیره می‌شه در مسیر `temp/`
2. با `extract_text_from_image()` متن داخل عکس خونده می‌شه
3. فایل حذف می‌شه و نتیجه به کاربر نمایش داده می‌شه

---

## 🎤 تبدیل ویس به متن:

```python
@router.message(F.voice)
async def handle_voice(message: Message):
```

دقیقاً مشابه OCR:

* فایل ویس دانلود می‌شه
* با `convert_voice_to_text()` متن استخراج می‌شه
* فایل پاک می‌شه
* متن برای کاربر ارسال می‌شه

---

## ✅ جمع‌بندی:

| قابلیت     | ماژول پشتش                |
| ---------- | ------------------------- |
| چت هوشمند  | `chatgpt.py`              |
| ترجمه      | `translate.py`            |
| خلاصه‌سازی | `summarizer.py`           |
| OCR عکس    | `vision/ocr.py`           |
| تبدیل ویس  | `vision/voice_to_text.py` |

طراحی بسیار تمیز و قابل توسعه‌ایه!

---

مرحله بعدی می‌تونه باشه:

* نگاهی به یکی از ماژول‌های `modules/ai/` یا `vision/`
* یا بررسی سیستم ضد اسپم (anti\_spam)

نظرت چیه بریم سراغ `anti_spam.py` تا امنیت و مدیریت گروه رو هم یاد بگیری؟ 😎
==================================================================================================================
عالــی! حالا وارد شدیم به قلب سیستم ضداسپم یعنی فایل `warnings.py` ⚠️
این ماژول وظیفه داره اخطارهای کاربران رو پیگیری کنه — مثلاً اگه یکی زیاد پیام بده یا فحش بده، براش اخطار ثبت می‌کنه.

---

## 🔸 جدول `warnings`

```python
class Warning(Base):
    __tablename__ = "warnings"
```

این جدول نگه می‌داره که هر کاربر چندبار اخطار گرفته.

### ستون‌ها:

```python
user_id = Column(BigInteger, primary_key=True)
```

آی‌دی تلگرام کاربر

```python
count = Column(Integer, default=0)
```

تعداد اخطارها

---

## 🧠 تابع `increase_warning`

```python
async def increase_warning(user_id: int) -> int:
```

این تابع:

* بررسی می‌کنه آیا کاربر تو جدول هست یا نه
* اگه نیست، می‌سازه و `count=1` می‌ذاره
* اگه هست، تعداد اخطار رو یکی زیاد می‌کنه
* تغییرات رو `commit` می‌کنه
* و در نهایت مقدار نهایی `count` رو برمی‌گردونه

---

## 🎯 هدفش چیه؟

ما معمولاً توی middleware ضداسپم از این تابع استفاده می‌کنیم:

* هر وقت کاربر تخلف کرد (مثلاً فحش داد یا اسپم کرد)
* این تابع صدا زده می‌شه
* اگر اخطار زیاد شد → بن یا سکوت

---

## ✅ آماده‌ایم برای مرحله بعد:

* بررسی فایل `anti_spam.py` که از همین تابع برای تشخیص و مقابله با کاربر خاطی استفاده می‌کنه.

بریم ببینیم چطوری جلوی اسپم و فحاشی گرفته می‌شه؟ 😎
=============================================================================================


