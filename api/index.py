import os
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

app = FastAPI()

# الرابط من Vercel
MONGODB_URI = os.getenv("MONGODB_URI")

@app.get("/")
async def test_connection():
    try:
        # بنعرف العميل جوه الدالة عشان نضمن إنه يلقط التغييرات
        client = AsyncIOMotorClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=5000,
            tls=True,
            tlsAllowInvalidCertificates=True
        )
        
        # محاولة فحص الاتصال
        await asyncio.wait_for(client.admin.command('ping'), timeout=4.0)
        
        return {
            "status": "success",
            "message": "فل الفففففف يا محمود! السيستم نطق أخيراً.",
            "info": "Connected to Ingenious Database"
        }
    except Exception as e:
        return {
            "status": "waiting",
            "message": "السيرفر لسه بيفكر، اعمل ريفريش كمان دقيقة",
            "error_detail": str(e)
        }
