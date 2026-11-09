import sqlite3
from flask import Flask, flash, redirect, render_template_string, request, session, url_for

app = Flask(__name__)
app.secret_key = "clave-secreta-demo"  # Hallazgo: secreto escrito en el código.
DATABASE = "tasks.db"

PAGE = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <title>TaskBloom · Demo Vibe</title>
  <style>
    :root { --ink:#18233b; --muted:#718096; --purple:#7357ff; --pink:#ef6bb5; --line:#e9e7f5; }
    * { box-sizing:border-box; }
    body { margin:0; min-height:100vh; font-family:Inter,Segoe UI,Arial,sans-serif; color:var(--ink); background:linear-gradient(135deg,#f6f3ff 0%,#fff7fb 48%,#eefcff 100%); }
    .shell { width:min(1000px,92%); margin:0 auto; padding:42px 0 56px; }
    .brand { display:flex; align-items:center; justify-content:space-between; margin-bottom:28px; }
    .logo { display:flex; align-items:center; gap:11px; font-weight:800; letter-spacing:-.5px; font-size:20px; }
    .logo-mark { display:grid; place-items:center; width:42px; height:42px; border-radius:14px; color:white; background:linear-gradient(135deg,var(--purple),var(--pink)); box-shadow:0 10px 25px #7357ff35; }
    .tag { padding:8px 13px; border:1px solid #ded9ff; border-radius:99px; color:#6556b5; background:#ffffffaa; font-size:12px; font-weight:700; }
    .hero { display:grid; grid-template-columns:1.1fr .9fr; gap:24px; align-items:center; margin-bottom:25px; }
    h1 { margin:0 0 10px; font-size:clamp(34px,5vw,58px); line-height:1.03; letter-spacing:-2.5px; }
    .gradient { background:linear-gradient(90deg,var(--purple),var(--pink)); color:transparent; background-clip:text; }
    .subtitle { max-width:560px; margin:0; color:var(--muted); font-size:16px; line-height:1.6; }
    .orb { min-height:170px; border-radius:28px; background:radial-gradient(circle at 30% 30%,#fff 0 8%,transparent 9%),linear-gradient(135deg,#dcd5ff,#ffc9e7); box-shadow:inset 0 0 0 1px #fff8,0 18px 45px #b7a9e540; display:grid; place-items:center; font-size:72px; }
    .card { background:#fffffff0; border:1px solid #ffffff; border-radius:24px; padding:28px; box-shadow:0 18px 55px #4e3f8315; }
    .card h2 { margin:0 0 18px; font-size:22px; }
    .auth-grid { display:grid; grid-template-columns:1fr 1fr; gap:20px; }
    .auth-grid .card h2 { font-size:18px; }
    form { display:grid; gap:12px; }
    input { width:100%; padding:13px 14px; border:1px solid var(--line); border-radius:12px; outline:none; font:inherit; color:var(--ink); background:#fbfaff; }
    input:focus { border-color:#a89cff; box-shadow:0 0 0 4px #7357ff18; }
    button, .button { border:0; border-radius:12px; padding:13px 18px; color:white; background:linear-gradient(100deg,var(--purple),#9b62e8); font:inherit; font-weight:750; cursor:pointer; text-decoration:none; text-align:center; }
    button:hover, .button:hover { transform:translateY(-1px); box-shadow:0 8px 18px #7357ff30; }
    .secondary { color:#6a5bb6; background:#f0edff; }
    .message { margin:0 0 15px; padding:12px 14px; border-radius:12px; color:#76501a; background:#fff4d8; }
    .session { display:flex; align-items:center; justify-content:space-between; gap:14px; margin-bottom:20px; color:var(--muted); }
    .session strong { color:var(--ink); }
    .new-task { display:flex; gap:10px; margin-bottom:22px; }
    .new-task input { flex:1; }
    .task-list { display:grid; gap:11px; padding:0; margin:0; list-style:none; }
    .task { display:flex; align-items:center; justify-content:space-between; gap:12px; padding:16px; border:1px solid var(--line); border-radius:16px; background:#fff; }
    .task-title { font-weight:700; }
    .task-meta { display:block; margin-top:5px; color:var(--muted); font-size:12px; }
    .task-actions { display:flex; gap:8px; }
    .task-actions a { padding:8px 10px; border-radius:9px; color:#6556b5; background:#f4f1ff; text-decoration:none; font-size:12px; font-weight:700; }
    .empty { padding:25px; border:1px dashed #d8d1f7; border-radius:16px; color:var(--muted); text-align:center; }
    @media (max-width:700px) { .hero,.auth-grid { grid-template-columns:1fr; } .orb { min-height:110px; font-size:48px; } .brand { margin-bottom:20px; } .task { align-items:flex-start; flex-direction:column; } .task-actions { width:100%; } .task-actions a { flex:1; text-align:center; } }
  </style>
</head>
<body><main class="shell">
  <header class="brand"><div class="logo"><span class="logo-mark">✓</span> TaskBloom</div><span class="tag">DEMO VIBE · FLASK</span></header>
  {% with messages = get_flashed_messages() %}{% for message in messages %}<p class="message">{{ message }}</p>{% endfor %}{% endwith %}
  {% if session.get('user_id') %}
    <section class="card">
      <div class="session"><span>Hola, <strong>{{ session['email'] }}</strong> 👋</span><a class="button secondary" href="{{ url_for('logout') }}">Cerrar sesión</a></div>
      <h2>Mis tareas</h2>
      <form class="new-task" method="post" action="{{ url_for('create_task') }}"><input name="title" placeholder="¿Qué quieres lograr hoy?"><button>+ Agregar tarea</button></form>
      {% if tasks %}<ul class="task-list">{% for task in tasks %}<li class="task"><div><span class="task-title">{{ task[1] }}</span><span class="task-meta">#{{ task[0] }} · {{ 'Completada ✨' if task[2] else 'Pendiente' }}</span></div><div class="task-actions"><a href="{{ url_for('toggle_task', task_id=task[0]) }}">{{ 'Reabrir' if task[2] else 'Completar' }}</a><a href="{{ url_for('delete_task', task_id=task[0]) }}">Eliminar</a></div></li>{% endfor %}</ul>{% else %}<div class="empty">Aún no tienes tareas. ¡Crea la primera!</div>{% endif %}
    </section>
  {% else %}
    <section class="hero"><div><h1>Pequeños pasos.<br><span class="gradient">Grandes logros.</span></h1><p class="subtitle">Organiza tus pendientes, mantén el enfoque y convierte tus ideas en tareas completadas.</p></div><div class="orb">🌱</div></section>
    <section class="auth-grid"><div class="card"><h2>Crear una cuenta</h2><form method="post" action="{{ url_for('register') }}"><input name="email" placeholder="Correo electrónico"><input name="password" type="password" placeholder="Contraseña"><button>Comenzar ahora</button></form></div><div class="card"><h2>Qué bueno verte de nuevo</h2><form method="post" action="{{ url_for('login') }}"><input name="email" placeholder="Correo electrónico"><input name="password" type="password" placeholder="Contraseña"><button class="secondary">Iniciar sesión</button></form></div></section>
  {% endif %}
</main></body></html>
"""


def db():
    connection = sqlite3.connect(DATABASE)
    connection.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE, password TEXT)")
    connection.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT, done INTEGER, user_id INTEGER)")
    return connection


@app.get("/")
def index():
    connection = db()
    tasks = connection.execute("SELECT id, title, done FROM tasks WHERE user_id = ?", (session.get("user_id"),)).fetchall()
    connection.close()
    return render_template_string(PAGE, tasks=tasks)


@app.post("/register")
def register():
    email = request.form.get("email", "")
    password = request.form.get("password", "")  # Hallazgo: contraseña sin hash.
    connection = db()
    try:
        cursor = connection.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        connection.commit()
        session["user_id"] = cursor.lastrowid
        session["email"] = email
    except sqlite3.IntegrityError:
        flash("El correo ya está registrado")
    connection.close()
    return redirect(url_for("index"))


@app.post("/login")
def login():
    connection = db()
    user = connection.execute("SELECT id, email FROM users WHERE email = ? AND password = ?", (request.form.get("email"), request.form.get("password"))).fetchone()
    connection.close()
    if user:
        session["user_id"], session["email"] = user
    else:
        flash("Credenciales inválidas")
    return redirect(url_for("index"))


@app.post("/tasks")
def create_task():
    connection = db()
    connection.execute("INSERT INTO tasks (title, done, user_id) VALUES (?, 0, ?)", (request.form.get("title"), session.get("user_id")))
    connection.commit()
    connection.close()
    return redirect(url_for("index"))


@app.get("/tasks/<int:task_id>/toggle")
def toggle_task(task_id):
    connection = db()
    connection.execute("UPDATE tasks SET done = 1 - done WHERE id = ?", (task_id,))  # Hallazgo: no verifica propietario.
    connection.commit()
    connection.close()
    return redirect(url_for("index"))


@app.get("/tasks/<int:task_id>/delete")
def delete_task(task_id):
    connection = db()
    connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))  # Hallazgo: no verifica propietario.
    connection.commit()
    connection.close()
    return redirect(url_for("index"))


@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

