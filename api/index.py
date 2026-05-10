import os
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# جلب رابط الاتصال من إعدادات Vercel
MONGODB_URI = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient(MONGODB_URI)
db = client.ingenious_db # ده اسم قاعدة البيانات بتاعتنا

@app.get("/")
async def test_connection():
    try:
        # محاولة الاتصال للتأكد إن كل شيء تمام
        await client.admin.command('ping')
        return {
            "message": "تم الربط بقاعدة البيانات بنجاح! السيستم الآن متصل وجاهز يا هندسة.",
            "database": "MongoDB Atlas connected"
        }
    except Exception as e:
        return {"error": f"فشل الاتصال: {str(e)}"}
