from flask import render_template, request, session, redirect, url_for, render_template_string
import matematica
import time

def gestisci_allenamento(salva_classifica_fun):
    if 'username' not in session or 'modalita' not in session: 
        return redirect(url_for('menu'))
    
    if session['vite'] <= 0 or session['domanda_attuale'] > session['max_domande']:
        consigli = matematica.ottieni_consiglio_recupero(session.get('errori_partita', []))
        
        html_fine = """
        <!DOCTYPE html><html><head><title>WebMath - Report</title><style>
        body { font-family: 'Segoe UI', sans-serif; text-align: center; background: radial-gradient(circle, #0f172a 0%, #020617 100%); color: #e2e8f0; padding: 40px 10px; }
        .box { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); padding: 40px; border-radius: 20px; display: inline-block; box-shadow: 0 0 30px rgba(0, 242, 254, 0.15); border: 1px solid rgba(0, 242, 254, 0.3); min-width: 400px; max-width: 600px; text-align: left; }
        h1, h2 { color: #00f2fe; text-align: center; text-transform: uppercase; }
        .punteggio-f { font-size: 22px; text-align: center; color: #10b981; font-weight: bold; }
        .card-recupero { background: #0f172a; padding: 20px; border-radius: 12px; margin-bottom: 20px; border-left: 5px solid #ffc107; }
        .card-recupero h4 { margin-top: 0; color: #ffc107; }
        .esercizi-list { background: rgba(0,0,0,0.2); padding: 10px; border-radius: 8px; color: #38bdf8; font-family: monospace; }
        .back-btn { display: block; text-align: center; margin-top: 30px; font-size: 18px; color: #00f2fe; font-weight: bold; text-decoration: none; }
        </style></head><body><div class="box">
        {% if session['vite'] <= 0 %}<h1 style="color:#ef4444;">💥 GAME OVER 💥</h1>{% else %}<h1>🏆 SFIDA COMPLETATA!</h1>{% endif %}
        <p class="punteggio-f">Punteggio: {{ session['punteggio'] }}/{{ session['max_domande'] }}</p><hr style="border-color:#334155;">
        <h2>🧠 CONSIGLI DI RIPASSO E COMPITI</h2>
        {% if consigli %}
            {% for c in consigli %}
                <div class="card-recupero"><h4>{{ c.titolo }}</h4><p>{{ c.consiglio }}</p><p><b>🎯 Esercizi di recupero consigliati:</b></p>
                <div class="esercizi-list">{% for es in c.esercizi_extra %}• {{ es }}<br>{% endfor %}</div></div>
            {% endfor %}
        {% else %}
            <p style="color:#10b981; text-align:center;">🔥 ECCELLENTE! Nessun errore commesso!</p>
        {% endif %}
        <a class="back-btn" href="/menu">⬅️ Torna al Menu</a></div></body></html>
        """
        if session['modalita'] == 'competitiva' and session['vite'] > 0:
            t = time.time() - session['start_time']
            salva_classifica_fun(session['username'], t)
        return render_template_string(html_fine, consigli=consigli)

    if request.method == 'POST':
        azione = request.form.get('azione')
        if azione == 'verifica':
            try:
                val = float(request.form.get('risposta'))
                if session['classe'] == '1':
                    esatto = (val == float(session['corretta']))
                else:
                    esatto = (int(val) in session['corretta'])
                
                if esatto:
                    session['punteggio'] += 1
                    session['messaggio'], session['colore_alert'] = "🎉 CORRETTO!", "#10b981"
                else:
                    if session['modalita'] != 'pratica': session['vite'] -= 1
                    session['messaggio'], session['colore_alert'] = f"❌ ERRORE! Era {session['corretta']}", "#ef4444"
                    lista_errori = session.get('errori_partita', [])
                    lista_errori.append(session.get('argomento_corrente'))
                    session['errori_partita'] = lista_errori
                session['domanda_attuale'] += 1
                session['mostra_indizio'] = False
                if 'testo_domanda' in session: del session['testo_domanda']
                return redirect(url_for('game_router'))
            except: pass
        elif azione == 'indizio' and session['indizi_rimasti'] > 0:
            if session['modalita'] != 'pratica': session['indizi_rimasti'] -= 1
            session['mostra_indizio'] = True

    if 'testo_domanda' not in session:
        t, c, arg = matematica.genera_esercizio(session['classe'])
        session['testo_domanda'], session['corretta'], session['argomento_corrente'] = t, c, arg

    msg = session.get('messaggio', '')
    session['messaggio'] = ""
    vite_v = "❤️" * session['vite'] if session['modalita'] != 'pratica' else "∞"
    
    return render_template('allena.html', modalita=session['modalita'], attuale=session['domanda_attuale'], 
                           max_domande=session['max_domande'], vite=vite_v, messaggio=msg, 
                           colore_alert=session.get('colore_alert',''), testo_domanda=session['testo_domanda'], 
                           indizi_rimasti=session['indizi_rimasti'], mostra_indizio=session.get('mostra_indizio'), 
                           testo_indizio=session.get('testo_indizio',''), punteggio=session['punteggio'])
