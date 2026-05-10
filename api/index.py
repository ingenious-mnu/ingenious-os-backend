import os
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

app = FastAPI()

# جلب الرابط من Vercel
MONGODB_URI = os.getenv("MONGODB_URI")

# إضافة إعدادات الأمان والاتصال مباشرة في الكود
client = AsyncIOMotorClient(
    MONGODB_URI,
    tls=True,
    tlsAllowInvalidCertificates=True, # دي عشان نتخطى مشاكل الشهادات لو موجودة
    serverSelectionTimeoutMS=5000
)

db = client.ingenious_db

@app.get("/")
async def test_connection():
    try:
        # بنحاول نكلم القاعدة ونشوفها هترد في خلال 3 ثواني ولا لأ
        await asyncio.wait_for(client.admin.command('ping'), timeout=3.0)
        return {
            "status": "success",
            "message": "تم الربط بنجاح يا محمود! إحنا كدة أونلاين فعلياً.",
            "database": "Connected to MongoDB Atlas"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": "لسه في خناقة مع الداتا بيز",
            "details": str(e)
        }
