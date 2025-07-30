# utils/test.py
import psycopg2
from config import BOT_TOKEN, DB_CONFIG

def check_system_status():
    print("🔍 در حال بررسی وضعیت سیستم...")

    # بررسی توکن
    if not BOT_TOKEN or not BOT_TOKEN.startswith(""):
        print("❌ توکن ربات تنظیم نشده!")
        return

    # بررسی اتصال دیتابیس
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        conn.close()
        print("✅ اتصال به دیتابیس برقرار است.")
    except Exception as e:
        print("❌ اتصال به دیتابیس شکست خورد:")
        print(e)
        return

    print("✅ سیستم سالم و آماده اجراست.")

if __name__ == "__main__":
    check_system_status()
