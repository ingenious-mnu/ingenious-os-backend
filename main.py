from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

app = FastAPI()

# السطر ده هو السر
@app.get("/")
async def root():
    return {"message": "فل الفففففف يا هندسة! السيستم نطق أخيراً."}

# وبقية الكود بتاع test_connection سيبه زي ما هو تحت
import os
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

app = FastAPI()

MONGODB_URI = os.getenv("MONGODB_URI")

@app.get("/")
async def test_connection():
    try:
        # إعداد العميل مع مهلة زمنية قصيرة عشان ميعلقش
        client = AsyncIOMotorClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        
        # محاولة فحص الاتصال
        await asyncio.wait_for(client.admin.command('ping'), timeout=5.0)
        
        return {
            "status": "success",
            "message": "فل الفففففف يا محمود! السيستم نطق أخيراً.",
            "database": "Connected"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": "لسه في مشكلة، بس ده السبب بالظبط:",
            "details": str(e)
        }
