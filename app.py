from flask import Flask, render_template, request, session, redirect, url_for
import matematica
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
        try:
            return sorted(list(reader), key=lambda x: float(x))[:10]
        except:
            return []

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
            if user in DATABASE_UTENTI: errore = "Username gia esistente!"
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
        if mod == 'competitiva': session['start_time'] = time.time()
        if 'testo_domanda' in session: del session['testo_domanda']
        return redirect(url_for('allena'))
    return render_template('menu.html', username=session['username'], classifica=leggi_classifica())

@app.route('/allena', methods=['GET', 'POST'])
def allena():
    if 'username' not in session or 'modalita' not in session: return redirect(url_for('menu'))
    if session['vite'] <= 0:
        return "<h2 style='color:red;text-align:center;margin-top:100px;'>💥 GAME OVER 💥</h2><br><center><a href='/menu'>Menu</a></center>"
    if session['domanda_attuale'] > session['max_domande']:
        if session['modalita'] == 'competitiva':
            t = time.time() - session['start_time']
            salva_in_classifica(session['username'], t)
            return f"<h2 style='text-align:center;margin-top:100px;'>🏆 COMPLETATO! Tempo: {t:.2f}s</h2><br><center><a href='/menu'>Menu</a></center>"
        return "<h2 style='text-align:center;margin-top:100px;'>🎉 ALLENAMENTO TERMINATO!</h2><br><center><a href='/menu'>Menu</a></center>"

    if request.method == 'POST':
        azione = request.form.get('azione')
        if azione == 'verifica':
            try:
                val = int(request.form.get('risposta'))
                esatto = (val == session['corretta']) if session['classe'] == '1' else (val in session['corretta'])
                if esatto:
                    session['punteggio'] += 1
                    session['messaggio'], session['colore_alert'] = "🎉 CORRETTO!", "#10b981"
                else:
                    if session['modalita'] != 'pratica': session['vite'] -= 1
                    session['messaggio'], session['colore_alert'] = f"❌ ERRORE! Era {session['corretta']}", "#ef4444"
                session['domanda_attuale'] += 1
                session['mostra_indizio'] = False
                if 'testo_domanda' in session: del session['testo_domanda']
                return redirect(url_for('allena'))
            except: pass
        elif azione == 'indizio' and session['indizi_rimasti'] > 0:
            if session['modalita'] != 'pratica': session['indizi_rimasti'] -= 1
            session['mostra_indizio'] = True

    if 'testo_domanda' not in session:
        t, c, i = matematica.genera_esercizio(session['classe'])
        session['testo_domanda'], session['corretta'], session['testo_indizio'] = t, c, i

    msg = session.get('messaggio', '')
    session['messaggio'] = ""
    vite_v = "❤️" * session['vite'] if session['modalita'] != 'pratica' else "∞"
    
    return render_template('allena.html', modalita=session['modalita'], attuale=session['domanda_attuale'], 
                           max_domande=session['max_domande'], vite=vite_v, messaggio=msg, 
                           colore_alert=session.get('colore_alert',''), testo_domanda=session['testo_domanda'], 
                           indizi_rimasti=session['indizi_rimasti'], mostra_indizio=session.get('mostra_indizio'), 
                           testo_indizio=session['testo_indizio'], punteggio=session['punteggio'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
