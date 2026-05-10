import os
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

app = FastAPI()

# جلب الرابط من إعدادات Vercel
MONGODB_URI = os.getenv("MONGODB_URI")

@app.get("/")
async def test_connection():
    try:
        # إعداد العميل مع مهلة زمنية 5 ثواني
        client = AsyncIOMotorClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        
        # محاولة فحص الاتصال فعلياً بطلب 'ping'
        await asyncio.wait_for(client.admin.command('ping'), timeout=5.0)
        
        return {
            "status": "success",
            "message": "فل الفففففف يا محمود! السيستم نطق والربط شغال 100%.",
            "database": "Connected to MongoDB Atlas"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": "السيرفر شغال بس في مشكلة في الوصول للداتا بيز",
            "details": str(e)
        }
