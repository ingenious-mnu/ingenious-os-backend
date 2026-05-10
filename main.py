import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List

app = FastAPI()

# الربط بقاعدة بيانات مانجو (بياخد الرابط من Vercel)
MONGODB_URI = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient(MONGODB_URI)
db = client.ingenious_database

class Member(BaseModel):
    name: str
    committee: str
    position: str

# --- واجهة الموقع (HTML & CSS) تظهر عند فتح الرابط ---
@app.get("/", response_class=HTMLResponse)
async def get_index():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ingenious Portal</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
        <style>body { font-family: 'Cairo', sans-serif; }</style>
    </head>
    <body class="bg-slate-50">
        <nav class="bg-[#002147] text-white p-5 shadow-2xl flex justify-between items-center">
            <div class="flex items-center gap-3">
                <div class="bg-yellow-500 text-blue-900 w-10 h-10 flex items-center justify-center rounded-lg font-bold">I</div>
                <h1 class="text-2xl font-bold tracking-tighter text-white">INGENIOUS</h1>
            </div>
            <span class="bg-yellow-500 text-blue-900 px-3 py-1 rounded-full text-xs font-bold">لوحة تحكم محمود</span>
        </nav>

        <main class="container mx-auto p-6 grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div class="bg-white p-6 rounded-2xl shadow-lg border-t-4 border-yellow-500">
                <h2 class="text-xl font-bold mb-6 text-blue-900"><i class="fa-solid fa-user-plus ml-2"></i> إضافة عضو جديد</h2>
                <div class="space-y-4">
                    <input type="text" id="name" placeholder="اسم العضو" class="w-full p-3 border rounded-xl outline-none focus:ring-2 focus:ring-blue-500">
                    <select id="comm" class="w-full p-3 border rounded-xl outline-none">
                        <option value="Presenting">Presenting</option>
                        <option value="Coaching">Coaching</option>
                        <option value="HR">HR</option>
                    </select>
                    <input type="text" id="pos" placeholder="المنصب (Leader/Member)" class="w-full p-3 border rounded-xl outline-none">
                    <button onclick="save()" id="btn" class="w-full bg-[#002147] text-white py-3 rounded-xl font-bold hover:bg-blue-800 transition shadow-md">حفظ في السحابة</button>
                </div>
            </div>

            <div class="lg:col-span-2 bg-white p-6 rounded-2xl shadow-lg">
                <div class="flex justify-between items-center mb-6 text-blue-900">
                    <h2 class="text-xl font-bold">أعضاء فريق Ingenious</h2>
                    <button onclick="load()" class="hover:rotate-180 transition-all duration-500"><i class="fa-solid fa-rotate"></i></button>
                </div>
                <div id="list" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <p class="text-gray-400 text-center col-span-2 py-10">جاري تحميل البيانات...</p>
                </div>
            </div>
        </main>

        <script>
            async function load() {
                try {
                    const res = await fetch('/members/all');
                    const data = await res.json();
                    const container = document.getElementById('list');
                    if (data.length === 0) {
                        container.innerHTML = '<p class="col-span-2 text-center text-gray-400 font-bold">لا يوجد أعضاء حالياً.</p>';
                        return;
                    }
                    container.innerHTML = data.map(m => `
                        <div class="p-4 border rounded-xl bg-slate-50 flex items-center gap-4 hover:shadow-md transition">
                            <div class="w-12 h-12 rounded-full bg-blue-900 text-white flex items-center justify-center font-bold text-xl">${m.name[0]}</div>
                            <div>
                                <h4 class="font-bold text-slate-800 text-lg">${m.name}</h4>
                                <p class="text-xs text-blue-600 font-bold">${m.committee} - ${m.position}</p>
                            </div>
                        </div>
                    `).join('');
                } catch (e) { console.error("Error:", e); }
            }

            async function save() {
                const name = document.getElementById('name').value;
                const committee = document.getElementById('comm').value;
                const position = document.getElementById('pos').value;
                const btn = document.getElementById('btn');

                if(!name || !position) return alert("يا محمود كمل البيانات الأول!");

                btn.disabled = true;
                btn.innerText = "جاري الحفظ...";

                try {
                    await fetch('/members/add', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ name, committee, position })
                    });
                    document.getElementById('name').value = '';
                    document.getElementById('pos').value = '';
                    load();
                } catch (e) { alert("خطأ في الاتصال!"); }
                finally {
                    btn.disabled = false;
                    btn.innerText = "حفظ في السحابة";
                }
            }
            window.onload = load;
        </script>
    </body>
    </html>
    """

# --- الأوامر البرمجية (API) ---
@app.get("/members/all")
async def get_all():
    members = await db.members.find().to_list(100)
    for m in members: m["_id"] = str(m["_id"])
    return members

@app.post("/members/add")
async def add(member: Member):
    await db.members.insert_one(member.dict())
    return {"status": "success"}
