import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional
from datetime import datetime

app = FastAPI()

# الربط بقاعدة بيانات مانجو (بياخد الرابط من Vercel)
MONGODB_URI = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient(MONGODB_URI)
db = client.ingenious_database

# --- نماذج البيانات (Models) ---
class Member(BaseModel):
    name: str
    committee: str
    position: str

class Task(BaseModel):
    title: str
    assigned_to: str
    deadline: str
    status: str = "Pending"

# --- واجهة النظام الكاملة (Dashboard) ---
@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ingenious | لوحة التحكم المركزية</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
        <style>
            body { font-family: 'Cairo', sans-serif; background-color: #f1f5f9; }
            .sidebar { background-color: #002147; transition: all 0.3s; }
            .nav-link { transition: 0.2s; border-radius: 12px; margin-bottom: 5px; }
            .nav-link:hover, .nav-link.active { background-color: #C5A021; color: #002147; }
            .card { background: white; border-radius: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
            .page-section { display: none; }
            .page-section.active { display: block; animation: fadeIn 0.3s; }
            @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        </style>
    </head>
    <body class="flex min-h-screen">

        <!-- Sidebar Navigation -->
        <aside class="sidebar w-64 text-white p-6 hidden md:flex flex-col">
            <div class="flex items-center gap-3 mb-10">
                <div class="bg-yellow-500 text-blue-900 w-10 h-10 flex items-center justify-center rounded-xl font-bold text-xl shadow-lg">I</div>
                <h1 class="text-xl font-bold tracking-wider">INGENIOUS</h1>
            </div>
            
            <nav class="flex-grow">
                <a href="javascript:void(0)" onclick="showPage('home')" id="link-home" class="nav-link active flex items-center p-3 gap-3">
                    <i class="fa-solid fa-house"></i> الرئيسية
                </a>
                <a href="javascript:void(0)" onclick="showPage('team')" id="link-team" class="nav-link flex items-center p-3 gap-3">
                    <i class="fa-solid fa-users"></i> أعضاء الفريق
                </a>
                <a href="javascript:void(0)" onclick="showPage('tasks')" id="link-tasks" class="nav-link flex items-center p-3 gap-3">
                    <i class="fa-solid fa-list-check"></i> المهام والطلبات
                </a>
                <a href="javascript:void(0)" onclick="showPage('stats')" id="link-stats" class="nav-link flex items-center p-3 gap-3">
                    <i class="fa-solid fa-chart-pie"></i> الإحصائيات
                </a>
            </nav>

            <div class="mt-auto pt-6 border-t border-blue-800 text-xs text-blue-300 text-center">
                إصدار v1.0.2 - محمود (المقاول)
            </div>
        </aside>

        <!-- Main Content Area -->
        <main class="flex-grow p-4 md:p-10 overflow-y-auto">
            
            <!-- Top Bar -->
            <header class="flex justify-between items-center mb-10">
                <h2 id="page-title" class="text-2xl font-bold text-slate-800">نظرة عامة</h2>
                <div class="flex items-center gap-4">
                    <button onclick="loadAllData()" class="p-2 bg-white rounded-full shadow hover:bg-slate-50 transition"><i class="fa-solid fa-rotate text-blue-900"></i></button>
                    <div class="flex items-center gap-2 bg-white px-4 py-2 rounded-full shadow border">
                        <div class="w-8 h-8 rounded-full bg-yellow-500 text-blue-900 flex items-center justify-center font-bold">M</div>
                        <span class="text-sm font-bold text-slate-700">محمود</span>
                    </div>
                </div>
            </header>

            <!-- PAGE: HOME (Dashboard) -->
            <section id="page-home" class="page-section active">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                    <div class="card p-6 border-r-4 border-blue-900">
                        <p class="text-slate-400 text-sm font-bold mb-1">إجمالي الأعضاء</p>
                        <h3 class="text-3xl font-bold text-blue-900" id="stat-members">0</h3>
                    </div>
                    <div class="card p-6 border-r-4 border-yellow-500">
                        <p class="text-slate-400 text-sm font-bold mb-1">المهام الجارية</p>
                        <h3 class="text-3xl font-bold text-blue-900" id="stat-tasks">0</h3>
                    </div>
                    <div class="card p-6 border-r-4 border-green-500">
                        <p class="text-slate-400 text-sm font-bold mb-1">حالة السيستم</p>
                        <h3 class="text-xl font-bold text-green-600">نشط الآن</h3>
                    </div>
                </div>
                
                <div class="card p-8 text-center bg-gradient-to-l from-blue-900 to-blue-800 text-white">
                    <h3 class="text-2xl font-bold mb-2">أهلاً بك يا ليدر محمود في منصة Ingenious</h3>
                    <p class="text-blue-200">من هنا تقدر تدير لجان الـ Presenting و Coaching وتوزع المهام بضغطة زرار.</p>
                </div>
            </section>

            <!-- PAGE: TEAM MANAGEMENT -->
            <section id="page-team" class="page-section">
                <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
                    <!-- Form -->
                    <div class="lg:col-span-4 card p-6">
                        <h3 class="text-lg font-bold mb-6 text-blue-900">إضافة عضو للفريق</h3>
                        <div class="space-y-4">
                            <input type="text" id="mName" placeholder="اسم العضو" class="w-full p-3 bg-slate-50 border rounded-xl outline-none focus:ring-2 focus:ring-yellow-500">
                            <select id="mComm" class="w-full p-3 bg-slate-50 border rounded-xl outline-none">
                                <option value="Presenting">Presenting</option>
                                <option value="Coaching">Coaching</option>
                                <option value="HR">HR</option>
                            </select>
                            <input type="text" id="mPos" placeholder="المنصب (Leader/Member)" class="w-full p-3 bg-slate-50 border rounded-xl outline-none">
                            <button onclick="saveMember()" id="saveMemberBtn" class="w-full bg-blue-900 text-white py-3 rounded-xl font-bold hover:bg-blue-800 transition">إرسال لمانجو</button>
                        </div>
                    </div>
                    <!-- List -->
                    <div class="lg:col-span-8 card p-6">
                        <h3 class="text-lg font-bold mb-6 text-blue-900">الأعضاء المسجلين</h3>
                        <div id="membersContainer" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <p class="text-gray-400">جاري التحميل...</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- PAGE: TASKS -->
            <section id="page-tasks" class="page-section">
                <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
                    <div class="lg:col-span-4 card p-6">
                        <h3 class="text-lg font-bold mb-6 text-blue-900">إنشاء مهمة جديدة</h3>
                        <div class="space-y-4">
                            <input type="text" id="tTitle" placeholder="عنوان المهمة" class="w-full p-3 bg-slate-50 border rounded-xl outline-none">
                            <input type="text" id="tUser" placeholder="تعيين لـ (اسم العضو)" class="w-full p-3 bg-slate-50 border rounded-xl outline-none">
                            <input type="date" id="tDeadline" class="w-full p-3 bg-slate-50 border rounded-xl outline-none">
                            <button onclick="saveTask()" id="saveTaskBtn" class="w-full bg-yellow-500 text-blue-900 py-3 rounded-xl font-bold hover:bg-yellow-600 transition">إرسال المهمة</button>
                        </div>
                    </div>
                    <div class="lg:col-span-8 card p-6">
                        <h3 class="text-lg font-bold mb-6 text-blue-900">جدول المهام</h3>
                        <div id="tasksContainer" class="space-y-4">
                            <p class="text-gray-400">جاري التحميل...</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- PAGE: STATS -->
            <section id="page-stats" class="page-section text-center py-20">
                <div class="card p-10 max-w-lg mx-auto">
                    <i class="fa-solid fa-microchip text-6xl text-blue-900 mb-6"></i>
                    <h3 class="text-2xl font-bold text-blue-900 mb-2">إحصائيات ذكية</h3>
                    <p class="text-gray-500 mb-6">هنا هيظهر لك تحليل كامل لأداء اللجان ونسبة إنجاز المهام فور اكتمال البيانات.</p>
                    <div class="bg-blue-50 p-4 rounded-xl">
                        <p class="font-bold text-blue-900">تحت التطوير في المرحلة Pilot</p>
                    </div>
                </div>
            </section>

        </main>

        <script>
            // --- Navigation Logic ---
            function showPage(pageId) {
                // Hide all
                document.querySelectorAll('.page-section').forEach(p => p.classList.remove('active'));
                document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                
                // Show selected
                document.getElementById('page-' + pageId).classList.add('active');
                document.getElementById('link-' + pageId).classList.add('active');
                
                // Set Title
                const titles = { 'home': 'نظرة عامة', 'team': 'إدارة الفريق', 'tasks': 'إدارة المهام', 'stats': 'الإحصائيات والتقارير' };
                document.getElementById('page-title').innerText = titles[pageId];
            }

            // --- API Logic ---
            async function loadAllData() {
                loadMembers();
                loadTasks();
            }

            async function loadMembers() {
                try {
                    const res = await fetch('/members/all');
                    const data = await res.json();
                    document.getElementById('stat-members').innerText = data.length;
                    const container = document.getElementById('membersContainer');
                    if (data.length === 0) {
                        container.innerHTML = '<p class="text-gray-400">لا يوجد أعضاء.</p>';
                        return;
                    }
                    container.innerHTML = data.map(m => `
                        <div class="p-4 border rounded-2xl bg-white flex items-center gap-3 shadow-sm">
                            <div class="w-10 h-10 rounded-lg bg-blue-900 text-white flex items-center justify-center font-bold">${m.name[0]}</div>
                            <div>
                                <h4 class="font-bold text-sm text-slate-800">${m.name}</h4>
                                <p class="text-[10px] text-blue-600 font-bold uppercase">${m.committee} - ${m.position}</p>
                            </div>
                        </div>
                    `).join('');
                } catch (e) { console.error(e); }
            }

            async function saveMember() {
                const name = document.getElementById('mName').value;
                const committee = document.getElementById('mComm').value;
                const position = document.getElementById('mPos').value;
                const btn = document.getElementById('saveMemberBtn');
                if(!name || !position) return alert("البيانات ناقصة يا محمود!");
                
                btn.disabled = true; btn.innerText = "جاري الحفظ...";
                await fetch('/members/add', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ name, committee, position })
                });
                document.getElementById('mName').value = '';
                document.getElementById('mPos').value = '';
                btn.disabled = false; btn.innerText = "إرسال لمانجو";
                loadMembers();
            }

            async function loadTasks() {
                try {
                    const res = await fetch('/tasks/all');
                    const data = await res.json();
                    document.getElementById('stat-tasks').innerText = data.length;
                    const container = document.getElementById('tasksContainer');
                    if (data.length === 0) {
                        container.innerHTML = '<p class="text-gray-400">لا يوجد مهام حالياً.</p>';
                        return;
                    }
                    container.innerHTML = data.map(t => `
                        <div class="p-4 border rounded-2xl flex justify-between items-center bg-white shadow-sm">
                            <div>
                                <h4 class="font-bold text-slate-800">${t.title}</h4>
                                <p class="text-xs text-gray-400">مكلف بها: <span class="text-blue-900 font-bold">${t.assigned_to}</span></p>
                            </div>
                            <div class="text-left">
                                <span class="px-3 py-1 bg-yellow-100 text-yellow-700 text-[10px] rounded-full font-bold">${t.status}</span>
                                <p class="text-[10px] text-gray-400 mt-1">${t.deadline}</p>
                            </div>
                        </div>
                    `).join('');
                } catch (e) { console.error(e); }
            }

            async function saveTask() {
                const title = document.getElementById('tTitle').value;
                const assigned_to = document.getElementById('tUser').value;
                const deadline = document.getElementById('tDeadline').value;
                const btn = document.getElementById('saveTaskBtn');
                if(!title || !assigned_to) return alert("اكمل بيانات المهمة!");

                btn.disabled = true; btn.innerText = "جاري الحفظ...";
                await fetch('/tasks/add', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ title, assigned_to, deadline })
                });
                document.getElementById('tTitle').value = '';
                document.getElementById('tUser').value = '';
                btn.disabled = false; btn.innerText = "إرسال المهمة";
                loadTasks();
            }

            window.onload = loadAllData;
        </script>
    </body>
    </html>
    """

# --- الأوامر البرمجية (API) ---
@app.get("/members/all")
async def get_all_members():
    members = await db.members.find().to_list(100)
    for m in members: m["_id"] = str(m["_id"])
    return members

@app.post("/members/add")
async def add_member(member: Member):
    await db.members.insert_one(member.dict())
    return {"status": "success"}

@app.get("/tasks/all")
async def get_all_tasks():
    tasks = await db.tasks.find().to_list(100)
    for t in tasks: t["_id"] = str(t["_id"])
    return tasks

@app.post("/tasks/add")
async def add_task(task: Task):
    await db.tasks.insert_one(task.dict())
    return {"status": "success"}
