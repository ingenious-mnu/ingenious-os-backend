import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List

app = FastAPI(title="Ingenious OS")

MONGODB_URI = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient(MONGODB_URI)
db = client.ingenious_database

class Member(BaseModel):
    name: str
    committee: str
    position: str

# ==========================================
# واجهة النظام الشاملة (Frontend OS)
# ==========================================
@app.get("/", response_class=HTMLResponse)
async def get_os():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ingenious OS | نظام تشغيل الكيانات</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
        <style>
            body { font-family: 'Cairo', sans-serif; background-color: #f4f7f6; overflow: hidden; }
            .sidebar { background: linear-gradient(180deg, #001f3f 0%, #00152a 100%); transition: 0.3s; }
            .nav-item { transition: all 0.2s ease; border-right: 4px solid transparent; }
            .nav-item:hover, .nav-item.active { background: rgba(255,255,255,0.05); border-color: #FFC300; color: #FFC300; }
            .glass-panel { background: white; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
            .os-page { display: none; animation: slideUp 0.4s ease forwards; height: calc(100vh - 100px); overflow-y: auto; padding-bottom: 50px; }
            .os-page.active { display: block; }
            @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
            
            /* Custom Scrollbar */
            ::-webkit-scrollbar { width: 8px; }
            ::-webkit-scrollbar-track { background: #f1f1f1; }
            ::-webkit-scrollbar-thumb { background: #001f3f; border-radius: 10px; }
        </style>
    </head>
    <body class="flex h-screen">

        <aside class="sidebar w-72 text-gray-300 flex flex-col h-full z-20 shadow-2xl relative">
            <div class="p-6 flex items-center gap-4 border-b border-gray-700">
                <div class="bg-[#FFC300] text-[#001f3f] w-12 h-12 flex items-center justify-center rounded-xl font-black text-2xl shadow-lg">I</div>
                <div>
                    <h1 class="text-xl font-bold text-white tracking-wider">INGENIOUS</h1>
                    <p class="text-[10px] text-[#FFC300] font-bold tracking-widest uppercase">Operating System v1.1</p>
                </div>
            </div>
            
            <div class="px-6 py-4">
                <p class="text-xs text-gray-500 uppercase font-bold mb-2">بوابات النظام</p>
            </div>

            <nav class="flex-grow overflow-y-auto">
                <a href="javascript:void(0)" onclick="nav('dashboard')" id="nav-dashboard" class="nav-item active flex items-center px-6 py-4 text-sm font-semibold gap-4 text-white">
                    <i class="fa-solid fa-border-all text-lg w-6 text-center"></i> بوابة الأعضاء (Dashboard)
                </a>
                <a href="javascript:void(0)" onclick="nav('gamification')" id="nav-gamification" class="nav-item flex items-center px-6 py-4 text-sm font-semibold gap-4">
                    <i class="fa-solid fa-gamepad text-lg w-6 text-center"></i> محرك التلعيب (Gamification)
                </a>
                <a href="javascript:void(0)" onclick="nav('clinic')" id="nav-clinic" class="nav-item flex items-center px-6 py-4 text-sm font-semibold gap-4">
                    <i class="fa-solid fa-chalkboard-user text-lg w-6 text-center"></i> عيادة التوجيه (Coaching)
                </a>
                <a href="javascript:void(0)" onclick="nav('hr')" id="nav-hr" class="nav-item flex items-center px-6 py-4 text-sm font-semibold gap-4">
                    <i class="fa-solid fa-id-card-clip text-lg w-6 text-center"></i> شؤون الأعضاء (HR)
                </a>
                <a href="javascript:void(0)" onclick="nav('events')" id="nav-events" class="nav-item flex items-center px-6 py-4 text-sm font-semibold gap-4">
                    <i class="fa-solid fa-qrcode text-lg w-6 text-center"></i> الفعاليات (Event Master)
                </a>
            </nav>

            <div class="p-6 border-t border-gray-700 bg-[#00152a]">
                <div class="flex items-center gap-3">
                    <img src="https://ui-avatars.com/api/?name=Mahmoud&background=FFC300&color=001f3f&bold=true" class="w-10 h-10 rounded-full border-2 border-[#FFC300]">
                    <div>
                        <p class="text-white font-bold text-sm">محمود</p>
                        <p class="text-xs text-gray-400">Super Admin / Leader</p>
                    </div>
                </div>
            </div>
        </aside>

        <main class="flex-grow flex flex-col relative w-full h-full bg-[#f4f7f6]">
            
            <header class="bg-white h-20 px-8 flex items-center justify-between shadow-sm z-10">
                <h2 id="page-title" class="text-2xl font-bold text-[#001f3f]">بوابة الأعضاء</h2>
                <div class="flex items-center gap-4">
                    <span class="bg-red-100 text-red-600 px-3 py-1 rounded-full text-xs font-bold flex items-center gap-2"><i class="fa-solid fa-bell"></i> 3 إنذارات معلقة</span>
                    <span class="bg-[#001f3f] text-[#FFC300] px-4 py-2 rounded-full text-sm font-bold shadow-md"><i class="fa-solid fa-bolt mr-2"></i> 1250 فولت</span>
                </div>
            </header>

            <section id="page-dashboard" class="os-page active p-8">
                <div class="glass-panel p-8 mb-8 bg-gradient-to-l from-[#001f3f] to-[#003366] text-white relative overflow-hidden">
                    <i class="fa-solid fa-quote-right absolute -left-4 -top-4 text-9xl opacity-10"></i>
                    <h3 class="text-2xl font-bold mb-2 text-[#FFC300]">رسالة اليوم التحفيزية</h3>
                    <p class="text-lg">"القائد الحقيقي ليس من يصنع أتباعاً، بل من يصنع قادة." - استعد لليوم يا ليدر، عندك 5 فيديوهات للتقييم في عيادة التوجيه.</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div class="glass-panel p-6 text-center border-t-4 border-[#FFC300]">
                        <img src="https://ui-avatars.com/api/?name=Mahmoud&background=001f3f&color=fff&size=128" class="w-24 h-24 rounded-full mx-auto mb-4 shadow-lg border-4 border-white">
                        <h4 class="text-xl font-bold text-[#001f3f]">محمود</h4>
                        <p class="text-sm font-bold text-gray-500 mb-4">Leader - Presenting & Coaching</p>
                        <div class="w-full bg-gray-200 rounded-full h-2.5 mb-1">
                            <div class="bg-[#FFC300] h-2.5 rounded-full" style="width: 75%"></div>
                        </div>
                        <p class="text-xs text-gray-400 text-right">المستوى: Master (75%)</p>
                    </div>

                    <div class="glass-panel p-6 md:col-span-2">
                        <h4 class="text-lg font-bold text-[#001f3f] mb-4 border-b pb-2"><i class="fa-solid fa-list-check text-[#FFC300] ml-2"></i> لوحة المهام (Task Board)</h4>
                        <div class="space-y-3">
                            <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg border-r-4 border-red-500">
                                <div><p class="font-bold text-sm">تقييم تدريبات الـ Pitching</p><p class="text-xs text-gray-500">لجنة Presenting</p></div>
                                <span class="bg-red-100 text-red-600 text-xs px-2 py-1 rounded font-bold">اليوم</span>
                            </div>
                            <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg border-r-4 border-green-500">
                                <div><p class="font-bold text-sm">اعتماد لوحة الشرف</p><p class="text-xs text-gray-500">إدارة الـ HR</p></div>
                                <span class="bg-green-100 text-green-600 text-xs px-2 py-1 rounded font-bold">مكتمل</span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section id="page-gamification" class="os-page p-8">
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <div class="glass-panel p-6">
                        <h4 class="text-xl font-bold text-[#001f3f] mb-6"><i class="fa-solid fa-store text-[#FFC300] ml-2"></i> متجر الكروت الافتراضي</h4>
                        <div class="grid grid-cols-2 gap-4">
                            <div class="border rounded-xl p-4 text-center cursor-pointer hover:shadow-lg transition bg-gradient-to-br from-yellow-50 to-white">
                                <i class="fa-solid fa-bolt text-3xl text-[#FFC300] mb-2"></i>
                                <h5 class="font-bold text-sm text-[#001f3f]">دبل فولت</h5>
                                <p class="text-xs text-gray-500 mb-3">يضاعف نقاط المهمة القادمة</p>
                                <button class="w-full bg-[#001f3f] text-white text-xs py-2 rounded-lg font-bold">شراء بـ 500 فولت</button>
                            </div>
                            <div class="border rounded-xl p-4 text-center cursor-pointer hover:shadow-lg transition bg-gradient-to-br from-red-50 to-white">
                                <i class="fa-solid fa-shield-halved text-3xl text-red-500 mb-2"></i>
                                <h5 class="font-bold text-sm text-[#001f3f]">كارت إعفاء</h5>
                                <p class="text-xs text-gray-500 mb-3">إلغاء إنذار تأخير واحد</p>
                                <button class="w-full bg-[#001f3f] text-white text-xs py-2 rounded-lg font-bold">شراء بـ 1000 فولت</button>
                            </div>
                        </div>
                    </div>
                    <div class="glass-panel p-6 bg-[#001f3f] text-white">
                        <h4 class="text-xl font-bold text-[#FFC300] mb-6"><i class="fa-solid fa-ranking-star ml-2"></i> لوحة الشرف (Top Performers)</h4>
                        <div class="space-y-4">
                            <div class="flex items-center gap-4 p-3 bg-white/10 rounded-xl">
                                <span class="text-2xl font-black text-[#FFC300]">1</span>
                                <div class="w-10 h-10 rounded-full bg-gray-300"></div>
                                <div class="flex-grow"><p class="font-bold text-sm">أحمد علي</p><p class="text-xs text-gray-400">Coaching</p></div>
                                <span class="font-bold text-[#FFC300]">3450 <i class="fa-solid fa-bolt text-xs"></i></span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section id="page-clinic" class="os-page p-8">
                <div class="glass-panel p-8 text-center max-w-2xl mx-auto border-dashed border-2 border-gray-300">
                    <i class="fa-solid fa-video text-6xl text-gray-300 mb-4"></i>
                    <h3 class="text-xl font-bold text-[#001f3f] mb-2">مساحة الـ Mock Pitches</h3>
                    <p class="text-gray-500 mb-6">اسحب وأفلت فيديو التدريب هنا ليتلقى تعليقات زمنية من قيادات لجنة Presenting.</p>
                    <button class="bg-[#FFC300] text-[#001f3f] px-8 py-3 rounded-xl font-bold shadow-md hover:scale-105 transition">
                        <i class="fa-solid fa-upload ml-2"></i> رفع فيديو التقييم
                    </button>
                </div>
            </section>

            <section id="page-hr" class="os-page p-8">
                <div class="glass-panel p-6 mb-6 flex justify-between items-center bg-blue-50">
                    <h3 class="text-lg font-bold text-[#001f3f]">إدارة قاعدة بيانات الأعضاء</h3>
                    <button onclick="toggleForm()" class="bg-[#001f3f] text-white px-4 py-2 rounded-lg text-sm font-bold"><i class="fa-solid fa-plus ml-1"></i> تسجيل عضو جديد</button>
                </div>
                
                <div id="addForm" class="glass-panel p-6 mb-6 hidden border-t-4 border-green-500">
                    <div class="grid grid-cols-3 gap-4 mb-4">
                        <input type="text" id="mName" placeholder="الاسم الرباعي" class="p-3 border rounded-lg bg-slate-50 outline-none">
                        <select id="mComm" class="p-3 border rounded-lg bg-slate-50 outline-none">
                            <option value="Presenting">Presenting</option>
                            <option value="Coaching">Coaching</option>
                            <option value="HR">HR</option>
                        </select>
                        <input type="text" id="mPos" placeholder="المسمى الوظيفي" class="p-3 border rounded-lg bg-slate-50 outline-none">
                    </div>
                    <button onclick="saveMember()" class="w-full bg-green-600 text-white py-3 rounded-lg font-bold">إصدار ID وحفظ في السيستم</button>
                </div>

                <div class="glass-panel p-0 overflow-hidden">
                    <table class="w-full text-right text-sm">
                        <thead class="bg-[#001f3f] text-white">
                            <tr><th class="p-4">الاسم</th><th class="p-4">اللجنة</th><th class="p-4">المستوى</th><th class="p-4">الإجراء</th></tr>
                        </thead>
                        <tbody id="hr-members-list" class="divide-y">
                            <tr><td colspan="4" class="p-8 text-center text-gray-400">جاري الاتصال بقاعدة البيانات...</td></tr>
                        </tbody>
                    </table>
                </div>
            </section>

            <section id="page-events" class="os-page p-8">
                <div class="glass-panel p-10 text-center max-w-lg mx-auto">
                    <div class="w-32 h-32 bg-gray-100 rounded-2xl mx-auto flex items-center justify-center border-4 border-[#001f3f] mb-6">
                        <i class="fa-solid fa-qrcode text-6xl text-[#001f3f]"></i>
                    </div>
                    <h3 class="text-2xl font-bold text-[#001f3f] mb-2">Delegated Check-in</h3>
                    <p class="text-gray-500 mb-6">وحدة مسح تذاكر الحضور وتوليد الشهادات الآلية مغلقة حالياً. سيتم تفعيلها يوم الحدث القادم.</p>
                    <button class="bg-gray-200 text-gray-500 px-8 py-3 rounded-xl font-bold cursor-not-allowed">تفعيل الـ Scanner</button>
                </div>
            </section>

        </main>

        <script>
            // --- OS Navigation System ---
            const titles = {
                'dashboard': 'بوابة الأعضاء',
                'gamification': 'محرك التلعيب والمتجر',
                'clinic': 'عيادة التوجيه والتدريب',
                'hr': 'إدارة شؤون الأعضاء والـ IDs',
                'events': 'وحدة إدارة الفعاليات'
            };

            function nav(page) {
                document.querySelectorAll('.os-page').forEach(el => el.classList.remove('active'));
                document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
                
                document.getElementById('page-' + page).classList.add('active');
                document.getElementById('nav-' + page).classList.add('active');
                document.getElementById('page-title').innerText = titles[page];
                
                if(page === 'hr') loadHRData();
            }

            function toggleForm() {
                const form = document.getElementById('addForm');
                form.classList.toggle('hidden');
            }

            // --- Database Connection (MongoDB via FastAPI) ---
            async function loadHRData() {
                try {
                    const res = await fetch('/api/members');
                    const data = await res.json();
                    const list = document.getElementById('hr-members-list');
                    if(data.length === 0) {
                        list.innerHTML = '<tr><td colspan="4" class="p-8 text-center text-gray-400">لا يوجد بيانات مسجلة.</td></tr>';
                        return;
                    }
                    list.innerHTML = data.map(m => `
                        <tr class="hover:bg-slate-50 transition">
                            <td class="p-4 font-bold text-[#001f3f]">${m.name}</td>
                            <td class="p-4 text-blue-600 font-semibold">${m.committee}</td>
                            <td class="p-4"><span class="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-xs font-bold">${m.position}</span></td>
                            <td class="p-4"><button class="text-red-500 hover:text-red-700"><i class="fa-solid fa-trash"></i></button></td>
                        </tr>
                    `).join('');
                } catch(e) { console.log(e); }
            }

            async function saveMember() {
                const name = document.getElementById('mName').value;
                const committee = document.getElementById('mComm').value;
                const position = document.getElementById('mPos').value;
                if(!name) return alert('برجاء إدخال الاسم!');
                
                await fetch('/api/members', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({name, committee, position})
                });
                
                document.getElementById('mName').value = '';
                toggleForm();
                loadHRData();
            }
        </script>
    </body>
    </html>
    """

# ==========================================
# محركات البيانات (Backend APIs)
# ==========================================
@app.get("/api/members")
async def get_members():
    members = await db.members.find().to_list(100)
    for m in members: m["_id"] = str(m["_id"])
    return members

@app.post("/api/members")
async def add_member(member: Member):
    await db.members.insert_one(member.dict())
    return {"status": "success"}
