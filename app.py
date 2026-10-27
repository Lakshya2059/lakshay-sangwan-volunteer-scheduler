from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os
from pathlib import Path
from datetime import datetime

APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR / "volunteer_scheduler.db"
app = Flask(__name__)

PAGE = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lakshay Sangwan | Community Event Volunteer Scheduler</title>
<style>
:root{--bg:#f5f7fb;--panel:#fff;--ink:#172033;--muted:#68738a;--line:#e7ebf3;--brand:#635bff;--brand2:#8b5cf6;--mint:#dcfce7;--red:#fee2e2;--amber:#fef3c7;--shadow:0 12px 35px rgba(26,35,70,.07)}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Arial}
button,input,select,textarea{font:inherit}button{cursor:pointer;border:0;border-radius:11px;padding:10px 14px;font-weight:700;transition:.15s}button:hover{transform:translateY(-1px);filter:brightness(.98)}
.layout{display:grid;grid-template-columns:240px 1fr;min-height:100vh}.sidebar{background:#171a32;color:#fff;padding:26px 17px;display:flex;flex-direction:column;gap:24px}.brand{display:flex;gap:11px;align-items:center;font-size:19px;font-weight:850;padding:0 8px}.brandmark{background:linear-gradient(135deg,#8b5cf6,#4f46e5);width:38px;height:38px;border-radius:12px;display:grid;place-items:center;font-size:20px}.navlabel{font-size:10px;color:#8d93b3;letter-spacing:1.6px;font-weight:800;padding:0 12px}.nav button{display:flex;align-items:center;gap:12px;width:100%;text-align:left;color:#b8bdd4;background:transparent;margin:4px 0}.nav button.active,.nav button:hover{background:#2b2e4b;color:#fff}.sidefoot{margin-top:auto;background:#242744;border-radius:16px;padding:15px;color:#c7cbe0;font-size:12px}.sidefoot strong{display:block;color:white;font-size:14px;margin-bottom:5px}
main{min-width:0;padding:28px clamp(16px,3vw,42px) 48px}.topbar{display:flex;justify-content:space-between;align-items:center;gap:15px;margin-bottom:26px}.eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:1.4px;color:var(--brand);font-weight:850}.topbar h1{font-size:clamp(25px,3vw,34px);margin:4px 0 0;letter-spacing:-1px}.topright{display:flex;align-items:center;gap:12px}.avatar{width:40px;height:40px;display:grid;place-items:center;background:#e9e7ff;color:#5145e5;border-radius:50%;font-weight:900}.primary{background:var(--brand);color:white}.secondary{background:#f0efff;color:#5145e5}.danger{background:#fff0f0;color:#c24141}.subtle{background:#f2f4f8;color:#475168}.small{padding:7px 10px;font-size:12px}.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-bottom:22px}.stat,.panel{background:var(--panel);border:1px solid var(--line);border-radius:18px;box-shadow:var(--shadow)}.stat{padding:19px}.stathead{display:flex;justify-content:space-between;align-items:center;color:var(--muted);font-size:13px;font-weight:650}.staticon{width:37px;height:37px;display:grid;place-items:center;border-radius:12px;background:#efedff;font-size:18px}.statnum{font-size:30px;font-weight:850;letter-spacing:-1px;margin:12px 0 2px}.statnote{font-size:12px;color:var(--muted)}.columns{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(280px,.85fr);gap:18px}.panel{padding:21px;margin-bottom:18px}.panelhead{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:17px}.panelhead h2{margin:0;font-size:17px;letter-spacing:-.3px}.panelhead p{margin:4px 0 0;color:var(--muted);font-size:12px}.eventlist{display:grid;gap:12px}.event{border:1px solid var(--line);border-radius:15px;padding:15px;display:grid;grid-template-columns:48px 1fr auto;gap:13px;align-items:center}.datebox{background:#f0efff;color:#5145e5;border-radius:12px;text-align:center;padding:7px 3px;font-weight:850}.datebox span{display:block;font-size:10px;text-transform:uppercase;letter-spacing:1px}.event h3{font-size:14px;margin:0 0 4px}.eventmeta{font-size:12px;color:var(--muted)}.pill{display:inline-block;font-size:11px;font-weight:750;border-radius:20px;padding:5px 8px;background:#eff6ff;color:#2563eb;white-space:nowrap}.progress{height:6px;background:#edf0f6;border-radius:10px;overflow:hidden;margin-top:9px;max-width:260px}.progress span{display:block;height:100%;background:linear-gradient(90deg,var(--brand),var(--brand2));border-radius:10px}.volrow{display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid var(--line);gap:10px}.volrow:last-child{border-bottom:0}.volname{font-weight:750;font-size:13px}.volsub{color:var(--muted);font-size:11px;margin-top:3px}.status{font-size:10px;padding:5px 8px;border-radius:20px;background:#fff7df;color:#9a6700;font-weight:800}.status.present{background:var(--mint);color:#15803d}.empty{padding:28px;text-align:center;color:var(--muted);border:1px dashed #d8deeb;border-radius:14px}.formgrid{display:grid;grid-template-columns:1fr 1fr;gap:13px}.field{display:flex;flex-direction:column;gap:6px}.field.full{grid-column:1/-1}.field label{font-size:12px;color:#59647a;font-weight:750}.field input,.field select,.field textarea,.search{width:100%;border:1px solid #dfe4ef;border-radius:10px;padding:11px 12px;background:#fff;outline:none;color:var(--ink)}.field input:focus,.field select:focus,.field textarea:focus,.search:focus{border-color:#817bff;box-shadow:0 0 0 3px #635bff1b}.field textarea{min-height:75px;resize:vertical}.actions{display:flex;gap:8px;justify-content:flex-end;margin-top:17px}.toolbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:16px}.search{max-width:300px}.tablewrap{overflow:auto}table{border-collapse:collapse;width:100%;min-width:620px}th,td{text-align:left;border-bottom:1px solid var(--line);padding:12px 10px;font-size:12px}th{color:var(--muted);font-weight:800;background:#fafbfe}td{color:#333e53}.toast{position:fixed;right:22px;bottom:22px;background:#171a32;color:#fff;padding:13px 18px;border-radius:12px;box-shadow:var(--shadow);opacity:0;transform:translateY(10px);pointer-events:none;transition:.2s;z-index:20}.toast.show{opacity:1;transform:translateY(0)}.modalback{position:fixed;inset:0;background:#10132988;display:none;align-items:center;justify-content:center;padding:18px;z-index:10}.modalback.open{display:flex}.modal{background:white;border-radius:20px;width:min(640px,100%);max-height:92vh;overflow:auto;padding:24px;box-shadow:0 25px 80px #0003}.modalhead{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px}.modalhead h2{margin:0}.close{background:#f1f3f8;font-size:20px;padding:4px 10px}.section{display:none}.section.active{display:block}.hint{font-size:12px;color:var(--muted);margin-top:10px}.mobilemenu{display:none}
@media(max-width:1000px){.stats{grid-template-columns:repeat(2,minmax(0,1fr))}.columns{grid-template-columns:1fr}}
@media(max-width:650px){.layout{grid-template-columns:1fr}.sidebar{padding:12px;gap:12px}.brand{padding:4px}.navlabel,.sidefoot{display:none}.nav{display:flex;overflow:auto;gap:5px}.nav button{width:auto;white-space:nowrap;margin:0;padding:9px 11px}.topbar{align-items:flex-start}.topright .avatar{display:none}main{padding:18px 13px 35px}.stats{gap:9px}.stat{padding:13px}.statnum{font-size:25px}.event{grid-template-columns:42px 1fr}.event>.pill{grid-column:2;justify-self:start}.formgrid{grid-template-columns:1fr}.field.full{grid-column:auto}.panel{padding:15px}}
</style>
</head>
<body>
<div class="layout">
<aside class="sidebar">
  <div class="brand"><div class="brandmark">✦</div><div>Lakshay<span style="color:#a9a4ff"> Sangwan</span><div style="font-size:10px;color:#b8bdd4;font-weight:600;letter-spacing:.3px">VOLUNTEER SCHEDULER</div></div></div>
  <div class="navlabel">WORKSPACE</div>
  <nav class="nav">
    <button class="active" data-page="dashboard">◫ &nbsp; Dashboard</button>
    <button data-page="events">▦ &nbsp; Events</button>
    <button data-page="volunteers">♙ &nbsp; Volunteers</button>
    <button data-page="attendance">✓ &nbsp; Attendance & hours</button>
  </nav>
  <div class="sidefoot"><strong>Make every hour count.</strong>Organize people, simplify shifts, and make a difference in your community.</div>
</aside>
<main>
<header class="topbar"><div><div class="eyebrow">Volunteer operations</div><h1 id="pageTitle">Good morning, Organizer 👋</h1><div style="color:var(--muted);font-size:13px;margin-top:5px" id="pageSubtitle">Here's what's happening in your community.</div></div><div class="topright"><button class="primary" onclick="openEventModal()">＋ Create event</button><div class="avatar">O</div></div></header>
<section id="dashboard" class="section active">
  <div class="stats">
    <div class="stat"><div class="stathead">Total events <span class="staticon">▦</span></div><div class="statnum" id="statEvents">0</div><div class="statnote">Events in your workspace</div></div>
    <div class="stat"><div class="stathead">Volunteers <span class="staticon">♙</span></div><div class="statnum" id="statVolunteers">0</div><div class="statnote">Unique registered people</div></div>
    <div class="stat"><div class="stathead">Shift assignments <span class="staticon">↗</span></div><div class="statnum" id="statAssignments">0</div><div class="statnote">Across all events</div></div>
    <div class="stat"><div class="stathead">Hours completed <span class="staticon">◷</span></div><div class="statnum" id="statHours">0</div><div class="statnote">Attendance-confirmed hours</div></div>
  </div>
  <div class="columns">
    <div class="panel"><div class="panelhead"><div><h2>Upcoming events</h2><p>Keep every event running smoothly.</p></div><button class="secondary small" onclick="showPage('events')">View all →</button></div><div id="dashEvents" class="eventlist"></div></div>
    <div>
      <div class="panel"><div class="panelhead"><div><h2>Latest assignments</h2><p>Recent volunteer sign-ups.</p></div></div><div id="latestAssignments"></div></div>
      <div class="panel"><div class="panelhead"><div><h2>Quick actions</h2></div></div><div style="display:grid;gap:9px"><button class="secondary" onclick="openEventModal()">＋ Create a community event</button><button class="subtle" onclick="openSignupModal()">♙ Register a volunteer</button><button class="subtle" onclick="showPage('attendance')">✓ Mark attendance</button></div><p class="hint">Tip: create an event before registering volunteers.</p></div>
    </div>
  </div>
</section>
<section id="events" class="section">
  <div class="panel"><div class="panelhead"><div><h2>All events</h2><p>Create and manage your community activities.</p></div><button class="primary" onclick="openEventModal()">＋ New event</button></div><div class="toolbar"><input id="eventSearch" class="search" placeholder="Search events..." oninput="renderEvents()"><span class="hint" id="eventCount"></span></div><div id="allEvents" class="eventlist"></div></div>
</section>
<section id="volunteers" class="section">
  <div class="panel"><div class="panelhead"><div><h2>Volunteer directory</h2><p>Every sign-up and assigned shift in one place.</p></div><button class="primary" onclick="openSignupModal()">＋ Register volunteer</button></div><div class="toolbar"><input id="volSearch" class="search" placeholder="Search volunteers..." oninput="renderVolunteers()"></div><div class="tablewrap"><table><thead><tr><th>VOLUNTEER</th><th>EVENT</th><th>ROLE / SHIFT</th><th>ATTENDANCE</th><th>ACTION</th></tr></thead><tbody id="volTable"></tbody></table></div></div>
</section>
<section id="attendance" class="section">
  <div class="panel"><div class="panelhead"><div><h2>Attendance & hours</h2><p>Mark attendance to calculate completed volunteer hours.</p></div></div><div class="tablewrap"><table><thead><tr><th>VOLUNTEER</th><th>EVENT</th><th>SHIFT</th><th>DURATION</th><th>STATUS</th><th>ACTION</th></tr></thead><tbody id="attendanceTable"></tbody></table></div><p class="hint">Hours count toward the total only after an assignment is marked Present.</p></div>
</section>
</main>
</div>
<div class="modalback" id="eventModal"><div class="modal"><div class="modalhead"><h2 id="eventModalTitle">Create an event</h2><button class="close" onclick="closeModal('eventModal')">×</button></div><form id="eventForm"><input type="hidden" id="editEventId"><div class="formgrid">
<div class="field full"><label>Event name *</label><input id="eventName" required placeholder="e.g. Community Clean-up Drive"></div>
<div class="field"><label>Date *</label><input id="eventDate" type="date" required></div><div class="field"><label>Venue *</label><input id="eventVenue" required placeholder="Community centre"></div>
<div class="field"><label>Volunteer capacity *</label><input id="eventCapacity" type="number" min="1" max="10000" value="20" required></div><div class="field"><label>Event category</label><select id="eventCategory"><option>Community</option><option>Fundraising</option><option>Environment</option><option>Education</option><option>Health</option><option>Sports</option><option>Other</option></select></div>
<div class="field full"><label>Description</label><textarea id="eventDescription" placeholder="What will volunteers do?"></textarea></div>
</div><div class="actions"><button type="button" class="subtle" onclick="closeModal('eventModal')">Cancel</button><button class="primary" type="submit">Save event</button></div></form></div></div>
<div class="modalback" id="signupModal"><div class="modal"><div class="modalhead"><h2>Register a volunteer</h2><button class="close" onclick="closeModal('signupModal')">×</button></div><form id="signupForm"><div class="formgrid">
<div class="field"><label>Full name *</label><input id="volName" required placeholder="Volunteer name"></div><div class="field"><label>Email *</label><input id="volEmail" type="email" required placeholder="name@example.com"></div>
<div class="field full"><label>Choose event *</label><select id="signupEvent" required></select></div>
<div class="field"><label>Role *</label><select id="signupRole"><option>Registration desk</option><option>Food distribution</option><option>Crowd management</option><option>First aid support</option><option>Setup and logistics</option><option>Clean-up team</option><option>General volunteer</option></select></div>
<div class="field"><label>Shift *</label><select id="signupShift"><option value="09:00-12:00">Morning · 9 AM–12 PM</option><option value="12:00-15:00">Afternoon · 12 PM–3 PM</option><option value="15:00-18:00">Evening · 3 PM–6 PM</option><option value="09:00-17:00">Full day · 9 AM–5 PM</option></select></div>
</div><p class="hint">The system checks event capacity and overlapping assignments before saving.</p><div class="actions"><button type="button" class="subtle" onclick="closeModal('signupModal')">Cancel</button><button class="primary" type="submit">Confirm registration</button></div></form></div></div>
<div class="toast" id="toast"></div>
<script>
let events=[], assignments=[], stats={};
const $=id=>document.getElementById(id);
async function api(url, options={}){const res=await fetch(url,{headers:{'Content-Type':'application/json'},...options});let data={};try{data=await res.json()}catch{}if(!res.ok)throw new Error(data.error||'Something went wrong');return data}
function esc(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function toast(msg){$('toast').textContent=msg;$('toast').classList.add('show');setTimeout(()=>$('toast').classList.remove('show'),3000)}
function closeModal(id){$(id).classList.remove('open')}
function openEventModal(ev=null){$('eventForm').reset();$('editEventId').value=ev?.id||'';$('eventModalTitle').textContent=ev?'Edit event':'Create an event';if(ev){$('eventName').value=ev.name;$('eventDate').value=ev.date;$('eventVenue').value=ev.venue;$('eventCapacity').value=ev.capacity;$('eventCategory').value=ev.category;$('eventDescription').value=ev.description||''}else{$('eventCapacity').value=20} $('eventModal').classList.add('open')}
function openSignupModal(){$('signupForm').reset();populateEventSelect();$('signupModal').classList.add('open')}
function showPage(page){document.querySelectorAll('.section').forEach(x=>x.classList.toggle('active',x.id===page));document.querySelectorAll('.nav button').forEach(x=>x.classList.toggle('active',x.dataset.page===page));const titles={dashboard:['Good morning, Organizer 👋',"Here's what's happening in your community."],events:['Events','Plan and manage your community activities.'],volunteers:['Volunteers','Build your volunteer team.'],attendance:['Attendance & hours','Track attendance and recognize every contribution.']};$('pageTitle').textContent=titles[page][0];$('pageSubtitle').textContent=titles[page][1]}
document.querySelectorAll('.nav button').forEach(b=>b.onclick=()=>showPage(b.dataset.page));
$('eventForm').addEventListener('submit',async e=>{e.preventDefault();const id=$('editEventId').value;const payload={name:$('eventName').value.trim(),date:$('eventDate').value,venue:$('eventVenue').value.trim(),capacity:Number($('eventCapacity').value),category:$('eventCategory').value,description:$('eventDescription').value.trim()};try{await api(id?'/api/events/'+id:'/api/events',{method:id?'PUT':'POST',body:JSON.stringify(payload)});closeModal('eventModal');toast(id?'Event updated':'Event created successfully');await loadAll()}catch(err){toast(err.message)}});
$('signupForm').addEventListener('submit',async e=>{e.preventDefault();const payload={name:$('volName').value.trim(),email:$('volEmail').value.trim(),event_id:Number($('signupEvent').value),role:$('signupRole').value,shift:$('signupShift').value};try{await api('/api/assignments',{method:'POST',body:JSON.stringify(payload)});closeModal('signupModal');toast('Volunteer registered successfully');await loadAll()}catch(err){toast(err.message)}});
function dateBits(date){if(!date)return ['TBD','--'];const d=new Date(date+'T12:00:00');return [d.toLocaleDateString('en',{month:'short'}),d.getDate()]}
function eventCard(ev){const [mon,day]=dateBits(ev.date);const percent=ev.capacity?Math.min(100,Math.round(ev.signup_count/ev.capacity*100)):0;return `<article class="event"><div class="datebox"><span>${esc(mon)}</span>${esc(day)}</div><div><h3>${esc(ev.name)}</h3><div class="eventmeta">⌖ ${esc(ev.venue)} · ${esc(ev.category)} · ${ev.signup_count}/${ev.capacity} volunteers</div><div class="progress"><span style="width:${percent}%"></span></div></div><span class="pill">${percent>=100?'At capacity':esc(ev.date||'No date')}</span></article>`}
function renderDashboard(){ $('statEvents').textContent=stats.events||0;$('statVolunteers').textContent=stats.volunteers||0;$('statAssignments').textContent=stats.assignments||0;$('statHours').textContent=stats.hours||0;const sorted=[...events].sort((a,b)=>(a.date||'').localeCompare(b.date||''));$('dashEvents').innerHTML=sorted.slice(0,4).map(eventCard).join('')||'<div class="empty">No events yet. Create your first event to get started.</div>';const latest=[...assignments].slice(-5).reverse();$('latestAssignments').innerHTML=latest.map(a=>`<div class="volrow"><div><div class="volname">${esc(a.name)}</div><div class="volsub">${esc(a.role)} · ${esc(a.event_name)}</div></div><span class="status ${a.attendance==='Present'?'present':''}">${esc(a.attendance)}</span></div>`).join('')||'<div class="empty">No sign-ups yet.</div>'}
function renderEvents(){const q=($('eventSearch')?.value||'').toLowerCase();const list=events.filter(e=>(e.name+' '+e.venue+' '+e.category).toLowerCase().includes(q));$('eventCount').textContent=`${list.length} event(s)`;$('allEvents').innerHTML=list.map(e=>`<article class="event"><div class="datebox"><span>${esc(dateBits(e.date)[0])}</span>${esc(dateBits(e.date)[1])}</div><div><h3>${esc(e.name)}</h3><div class="eventmeta">${esc(e.description||'Community event')}<br>⌖ ${esc(e.venue)} · ${esc(e.category)} · ${e.signup_count}/${e.capacity} volunteers</div><div class="progress"><span style="width:${Math.min(100,e.signup_count/Math.max(1,e.capacity)*100)}%"></span></div></div><div style="display:grid;gap:6px"><button class="secondary small" onclick="editEvent(${e.id})">Edit</button><button class="subtle small" onclick="signupFor(${e.id})">＋ Volunteer</button><button class="danger small" onclick="deleteEvent(${e.id})">Delete</button></div></article>`).join('')||'<div class="empty">No matching events found.</div>'}
function populateEventSelect(selected){$('signupEvent').innerHTML=events.map(e=>`<option value="${e.id}" ${selected===e.id?'selected':''}>${esc(e.name)} — ${esc(e.date)}</option>`).join('');if(!events.length)$('signupEvent').innerHTML='<option value="">Create an event first</option>'}
function renderVolunteers(){const q=($('volSearch')?.value||'').toLowerCase();const list=assignments.filter(a=>(a.name+' '+a.email+' '+a.event_name+' '+a.role).toLowerCase().includes(q));$('volTable').innerHTML=list.map(a=>`<tr><td><strong>${esc(a.name)}</strong><br><span style="color:#68738a">${esc(a.email)}</span></td><td>${esc(a.event_name)}</td><td>${esc(a.role)}<br><span style="color:#68738a">${esc(a.shift)}</span></td><td><span class="status ${a.attendance==='Present'?'present':''}">${esc(a.attendance)}</span></td><td><button class="danger small" onclick="deleteAssignment(${a.id})">Remove</button></td></tr>`).join('')||'<tr><td colspan="5">No volunteer registrations yet.</td></tr>'}
function renderAttendance(){$('attendanceTable').innerHTML=assignments.map(a=>`<tr><td><strong>${esc(a.name)}</strong><br><span style="color:#68738a">${esc(a.email)}</span></td><td>${esc(a.event_name)}</td><td>${esc(a.shift)}</td><td>${a.duration} hours</td><td><span class="status ${a.attendance==='Present'?'present':''}">${esc(a.attendance)}</span></td><td><button class="${a.attendance==='Present'?'subtle':'primary'} small" onclick="markAttendance(${a.id},'${a.attendance==='Present'?'Absent':'Present'}')">${a.attendance==='Present'?'Mark absent':'Mark present'}</button></td></tr>`).join('')||'<tr><td colspan="6">No assignments to track yet.</td></tr>'}
async function loadAll(){try{const d=await api('/api/overview');events=d.events;assignments=d.assignments;stats=d.stats;renderDashboard();renderEvents();renderVolunteers();renderAttendance()}catch(e){toast(e.message)}}
async function editEvent(id){const ev=events.find(e=>e.id===id);if(ev)openEventModal(ev)}
async function signupFor(id){openSignupModal();$('signupEvent').value=String(id)}
async function deleteEvent(id){if(!confirm('Delete this event and its volunteer assignments?'))return;try{await api('/api/events/'+id,{method:'DELETE'});toast('Event deleted');await loadAll()}catch(e){toast(e.message)}}
async function deleteAssignment(id){if(!confirm('Remove this volunteer assignment?'))return;try{await api('/api/assignments/'+id,{method:'DELETE'});toast('Assignment removed');await loadAll()}catch(e){toast(e.message)}}
async function markAttendance(id,status){try{await api('/api/assignments/'+id+'/attendance',{method:'PATCH',body:JSON.stringify({attendance:status})});toast('Attendance updated');await loadAll()}catch(e){toast(e.message)}}
loadAll();
</script>
</body>
</html>
"""

def connect():
    con = sqlite3.connect(DB_PATH, timeout=10)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con

def init_db():
    with connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS events(
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, date TEXT NOT NULL,
            venue TEXT NOT NULL, capacity INTEGER NOT NULL CHECK(capacity > 0),
            category TEXT NOT NULL DEFAULT 'Community', description TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)""")
        con.execute("""CREATE TABLE IF NOT EXISTS assignments(
            id INTEGER PRIMARY KEY AUTOINCREMENT, event_id INTEGER NOT NULL,
            name TEXT NOT NULL, email TEXT NOT NULL, role TEXT NOT NULL, shift TEXT NOT NULL,
            attendance TEXT NOT NULL DEFAULT 'Pending',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(event_id) REFERENCES events(id) ON DELETE CASCADE)""")

init_db()

def event_dict(row, count=0):
    d = dict(row)
    d["signup_count"] = count
    return d

def duration(shift):
    try:
        start, end = shift.split("-")
        a = datetime.strptime(start, "%H:%M")
        b = datetime.strptime(end, "%H:%M")
        return max(0, (b-a).total_seconds()/3600)
    except Exception:
        return 0

def fetch_overview():
    with connect() as con:
        rows = con.execute("""SELECT e.*, COUNT(a.id) AS signup_count
            FROM events e LEFT JOIN assignments a ON a.event_id=e.id
            GROUP BY e.id ORDER BY e.date, e.id""").fetchall()
        events = [event_dict(r, r["signup_count"]) for r in rows]
        rows = con.execute("""SELECT a.*, e.name AS event_name FROM assignments a
            JOIN events e ON e.id=a.event_id ORDER BY a.id""").fetchall()
        assignments = []
        for r in rows:
            d = dict(r)
            d["duration"] = duration(d["shift"])
            assignments.append(d)
        stats = {
            "events": len(events),
            "volunteers": len({a["email"].lower() for a in assignments}),
            "assignments": len(assignments),
            "hours": round(sum(a["duration"] for a in assignments if a["attendance"] == "Present"), 1)
        }
        return {"events": events, "assignments": assignments, "stats": stats}

@app.get("/")
def home():
    return render_template_string(PAGE)

@app.get("/api/overview")
def overview():
    return jsonify(fetch_overview())

@app.post("/api/events")
def create_event():
    d = request.get_json(silent=True) or {}
    required = ["name", "date", "venue", "capacity"]
    if any(not str(d.get(k, "")).strip() for k in required):
        return jsonify(error="Please complete all required event fields."), 400
    try:
        capacity = int(d["capacity"])
        if capacity < 1 or capacity > 10000: raise ValueError()
        datetime.strptime(d["date"], "%Y-%m-%d")
    except (ValueError, TypeError):
        return jsonify(error="Enter a valid date and a capacity from 1 to 10000."), 400
    with connect() as con:
        con.execute("INSERT INTO events(name,date,venue,capacity,category,description) VALUES(?,?,?,?,?,?)",
                    (d["name"].strip(), d["date"], d["venue"].strip(), capacity,
                     d.get("category", "Community"), d.get("description", "")))
    return jsonify(ok=True), 201

@app.put("/api/events/<int:event_id>")
def update_event(event_id):
    d = request.get_json(silent=True) or {}
    try:
        capacity = int(d["capacity"])
        datetime.strptime(d["date"], "%Y-%m-%d")
        if capacity < 1: raise ValueError()
    except (KeyError, ValueError, TypeError):
        return jsonify(error="Enter a valid date and capacity."), 400
    with connect() as con:
        event = con.execute("SELECT id FROM events WHERE id=?", (event_id,)).fetchone()
        if not event: return jsonify(error="Event not found."), 404
        count = con.execute("SELECT COUNT(*) FROM assignments WHERE event_id=?", (event_id,)).fetchone()[0]
        if capacity < count: return jsonify(error=f"Capacity cannot be lower than the {count} existing registrations."), 400
        con.execute("""UPDATE events SET name=?,date=?,venue=?,capacity=?,category=?,description=? WHERE id=?""",
                    (d.get("name","").strip(), d["date"], d.get("venue","").strip(), capacity,
                     d.get("category","Community"), d.get("description",""), event_id))
    return jsonify(ok=True)

@app.delete("/api/events/<int:event_id>")
def delete_event(event_id):
    with connect() as con:
        con.execute("DELETE FROM assignments WHERE event_id=?", (event_id,))
        cur = con.execute("DELETE FROM events WHERE id=?", (event_id,))
        if cur.rowcount == 0: return jsonify(error="Event not found."), 404
    return jsonify(ok=True)

@app.post("/api/assignments")
def create_assignment():
    d = request.get_json(silent=True) or {}
    for key in ("name", "email", "event_id", "role", "shift"):
        if not str(d.get(key, "")).strip():
            return jsonify(error="Please complete all volunteer fields."), 400
    try: event_id = int(d["event_id"])
    except (ValueError, TypeError): return jsonify(error="Choose a valid event."), 400
    shift = d["shift"]
    if duration(shift) <= 0: return jsonify(error="Choose a valid shift."), 400
    with connect() as con:
        con.execute("BEGIN IMMEDIATE")
        ev = con.execute("SELECT * FROM events WHERE id=?", (event_id,)).fetchone()
        if not ev: return jsonify(error="That event no longer exists."), 404
        count = con.execute("SELECT COUNT(*) FROM assignments WHERE event_id=?", (event_id,)).fetchone()[0]
        if count >= ev["capacity"]:
            return jsonify(error="This event has reached its volunteer capacity."), 400
        email = d["email"].strip().lower()
        # Prevent a volunteer from taking the same event/shift twice.
        dup = con.execute("""SELECT id FROM assignments WHERE event_id=? AND lower(email)=? AND shift=?""",
                          (event_id, email, shift)).fetchone()
        if dup: return jsonify(error="This volunteer is already registered for that event and shift."), 400
        # For this demo, identical shift time ranges are treated as overlapping across events.
        other = con.execute("""SELECT a.id, e.name FROM assignments a JOIN events e ON e.id=a.event_id
            WHERE lower(a.email)=? AND a.shift=?""", (email, shift)).fetchone()
        if other: return jsonify(error=f"Scheduling conflict: this volunteer already has the same time slot for “{other['name']}”."), 400
        con.execute("INSERT INTO assignments(event_id,name,email,role,shift) VALUES(?,?,?,?,?)",
                    (event_id, d["name"].strip(), email, d["role"], shift))
    return jsonify(ok=True), 201

@app.delete("/api/assignments/<int:assignment_id>")
def delete_assignment(assignment_id):
    with connect() as con:
        cur = con.execute("DELETE FROM assignments WHERE id=?", (assignment_id,))
        if cur.rowcount == 0: return jsonify(error="Assignment not found."), 404
    return jsonify(ok=True)

@app.patch("/api/assignments/<int:assignment_id>/attendance")
def update_attendance(assignment_id):
    d = request.get_json(silent=True) or {}
    status = d.get("attendance")
    if status not in ("Present", "Absent", "Pending"):
        return jsonify(error="Invalid attendance status."), 400
    with connect() as con:
        cur = con.execute("UPDATE assignments SET attendance=? WHERE id=?", (status, assignment_id))
        if cur.rowcount == 0: return jsonify(error="Assignment not found."), 404
    return jsonify(ok=True)

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    print(f"\\nLakshay Sangwan Volunteer Scheduler is running on port {port}")
    app.run(debug=True, host="0.0.0.0", port=port)
