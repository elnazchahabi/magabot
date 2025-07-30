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

---


