import os
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "success", "message": "فل الفففففف يا محمود!"}
