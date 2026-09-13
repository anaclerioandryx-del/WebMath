from flask import Flask, render_template, request, session, redirect, url_for, render_template_string
import matematica
import sfida
import time
import csv
import os

app = Flask(__name__)
app.secret_key = 'webmath_cyber_key_2026'
CSV_FILE = 'classifica.csv'
DATABASE_UTENTI = {"admin": "admin123"}

def leggi_classifica():
    if not os.path.exists(CSV_FILE) or os.stat(CSV_FILE).st_size == 0:
        return []
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        try: return sorted(list(reader), key=lambda x: float(x))[:10]
        except: return []

def salva_in_classifica(username, tempo):
    classifica = leggi_classifica()
    classifica.append([username, f"{tempo:.2f}"])
    classifica = sorted(classifica, key=lambda x: float(x))[:10]
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(classifica)

@app.route('/', methods=['GET', 'POST'])
def login():
    errore, successo = "", ""
    if request.method == 'POST':
        tipo = request.form.get('tipo_azione')
        user = request.form.get('username')
        pas = request.form.get('password')
        if tipo == 'login':
            if user in DATABASE_UTENTI and DATABASE_UTENTI[user] == pas:
                session['username'] = user
                return redirect(url_for('menu'))
            errore = "Username o Password errati!"
        elif tipo == 'registrazione':
            if user in DATABASE_UTENTI: errore = "Username già esistente!"
            elif len(user) < 3 or len(pas) < 4: errore = "Dati troppo corti!"
            else:
                DATABASE_UTENTI[user] = pas
                successo = "Account creato! Accedi."
    return render_template('login.html', errore=errore, successo=successo)

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if 'username' not in session: return redirect(url_for('login'))
    if request.method == 'POST':
        mod = request.form.get('modalita')
        session['modalita'] = mod
        session['classe'] = request.form.get('classe')
        session['punteggio'] = 0
        session['domanda_attuale'] = 1
        session['vite'] = 999 if mod == 'pratica' else 3
        session['indizi_rimasti'] = 999 if mod == 'pratica' else (3 if mod == 'normale' else 0)
        session['max_domande'] = 15 if mod == 'pratica' else (20 if mod == 'normale' else 30)
        session['errori_partita'] = []
        if mod == 'competitiva': session['start_time'] = time.time()
        if 'testo_domanda' in session: del session['testo_domanda']
        return redirect(url_for('game_router'))
    return render_template('menu.html', username=session['username'], classifica=leggi_classifica())

@app.route('/allena', methods=['GET', 'POST'])
def game_router():
    return sfida.gestisci_allenamento(salva_in_classifica)

@app.route('/calcolatrice', methods=['GET', 'POST'])
def calcolatrice():
    risultato, espressione = "", ""
    if request.method == 'POST':
        espressione = request.form.get('espressione', '')
        if all(c in "0123456789+-*/(). " for c in espressione):
            try: risultato = eval(espressione)
            except: risultato = "Errore di sintassi!"
        else: risultato = "Caratteri non ammessi!"
    return render_template_string("""
    <!DOCTYPE html><html><head><title>WebMath - Calcolatrice</title><style>
    body { font-family: 'Segoe UI', sans-serif; text-align: center; background: radial-gradient(circle, #0f172a 0%, #020617 100%); color: #e2e8f0; padding-top: 50px; }
    .box { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); padding: 40px; border-radius: 20px; display: inline-block; box-shadow: 0 0 30px rgba(0, 242, 254, 0.15); border: 1px solid rgba(0, 242, 254, 0.3); min-width: 400px; }
    h1 { color: #00f2fe; text-transform: uppercase; }
    input { font-size: 20px; padding: 12px; width: 80%; background: #0f172a; color: #fff; border: 2px solid #334155; border-radius: 10px; text-align: center; outline: none; margin-bottom: 20px; }
    button { font-size: 16px; padding: 12px 28px; background: linear-gradient(135deg, #007bff, #00f2fe); color: white; border: none; border-radius: 10px; cursor: pointer; font-weight: bold; }
    .res { font-size: 24px; color: #10b981; font-weight: bold; margin-top: 20px; background: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #334155; }
    a { display: block; margin-top: 25px; color: #38bdf8; text-decoration: none; font-weight: bold; }
    </style></head><body><div class="box"><h1>🖥️ CALCOLATRICE CORE</h1>
    <form method="POST"><input type="text" name="espressione" value="{{ espressione }}" placeholder="Scrivi qui..." required autocomplete="off"><br><button type="submit">Calcola</button></form>
    {% if risultato != "" %}<div class="res">RISULTATO: {{ risultato }}</div>{% endif %}<a href="/menu">⬅️ Menu</a></div></body></html>
    """, risultato=risultato, espressione=espressione)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
