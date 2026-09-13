import random

def genera_esercizio(classe):
    if str(classe) == '1':
        argomenti = ['equazioni', 'potenze', 'monomi']
    else:
        argomenti = ['equazioni_2g', 'radicali']
        
    argomento = random.choice(argomenti)

    if argomento == 'equazioni':
        x_corretta = random.randint(-10, 10)
        a = random.choice([2, 3, 4, 5, -2, -3, -4, -5])
        b = random.randint(-20, 20)
        c = a * x_corretta + b
        segno_b = "+" if b >= 0 else ""
        return f"Risolvi l'equazione: {a}x {segno_b}{b} = {c}", x_corretta, "equazioni"

    elif argomento == 'potenze':
        base = random.randint(2, 5)
        esp1 = random.randint(2, 5)
        esp2 = random.randint(2, 5)
        return f"Semplifica le potenze: ({base}^{esp1}) * ({base}^{esp2}) = {base}^?", (esp1 + esp2), "potenze"

    elif argomento == 'monomi':
        coeff1 = random.choice([2, 3, 4, -2, -3])
        coeff2 = random.choice([2, 5, -1, 3])
        return f"Trova il coefficiente finale: ({coeff1}x) * ({coeff2}x²)", (coeff1 * coeff2), "monomi"

    elif argomento == 'equazioni_2g':
        x1 = random.randint(-5, 5)
        x2 = random.randint(-5, 5)
        b = -(x1 + x2)
        c = x1 * x2
        segno_b = f"+ {b}" if b > 0 else f"- {abs(b)}" if b < 0 else ""
        segno_c = f"+ {c}" if c > 0 else f"- {abs(c)}" if c < 0 else ""
        termine_b = f"{segno_b}x " if b != 0 else ""
        termine_c = f"{segno_c} " if c != 0 else ""
        return f"Trova una soluzione intera di: x² {termine_b}{termine_c}= 0", [x1, x2], "equazioni_2g"

    else:
        base_rad = random.choice([2, 3, 5, 6])
        esp_rad = random.choice([4, 6, 8, 10])
        return f"Porta fuori dal radicale (scrivi l'esponente di {base_rad}): √({base_rad}^{esp_rad})", (esp_rad // 2), "radicali"

def ottieni_consiglio_recupero(argomenti_falliti):
    report = []
    percorso_studio = set(argomenti_falliti)
    
    for arg in percorso_studio:
        if arg == 'equazioni':
            report.append({
                "titolo": "📝 RIPASSO: Equazioni di 1° Grado",
                "consiglio": "Ricorda la regola del trasporto: quando sposti un termine da un membro all'altro dell'uguale, devi SEMPRE cambiare il suo segno! Isola prima i termini con la x e poi dividi per il coefficiente.",
                "esercizi_extra": ["Risolvi per esercizio: 3x - 6 = 12 (Risultato: x = 6)", "Risolvi per esercizio: -2x + 5 = -5 (Risultato: x = 5)"]
            })
        elif arg == 'potenze':
            report.append({
                "titolo": "📝 RIPASSO: Proprietà delle Potenze",
                "consiglio": "Nel prodotto di potenze con la stessa base, la base resta uguale e gli esponenti si SOMMANO. Es: a³ * a⁴ = a⁷.",
                "esercizi_extra": ["Semplifica sul quaderno: 2⁴ * 2³ = 2⁷", "Semplifica sul quaderno: 5² * 5³ = 5⁵"]
            })
        elif arg == 'monomi':
            report.append({
                "titolo": "📝 RIPASSO: Moltiplicazione tra Monomi",
                "consiglio": "Moltiplica tra loro i coefficienti numerici (attenzione ai segni!) e somma gli esponenti delle lettere uguali.",
                "esercizi_extra": ["Calcola: (4x) * (-3x³) = -12x⁴", "Calcola: (-2x²) * (-5x) = 10x³"]
            })
        elif arg == 'equazioni_2g':
            report.append({
                "titolo": "📝 RIPASSO: Equazioni di 2° Grado",
                "consiglio": "Se l'equazione è del tipo x² + bx + c = 0, puoi trovare due numeri la cui somma sia -b e il prodotto sia c.",
                "esercizi_extra": ["Risolvi: x² - 5x + 6 = 0 (Soluzioni: 2 e 3)", "Risolvi: x² - 4 = 0 (Soluzioni: -2 e 2)"]
            })
        elif arg == 'radicali':
            report.append({
                "titolo": "📝 RIPASSO: Semplificazione di Radicali",
                "consiglio": "Per portare un fattore fuori dalla radice quadrata, dividi il suo esponente per 2. Es: √(3⁶) diventa 3³.",
                "esercizi_extra": ["Semplifica: √(3⁴) = 3²", "Semplifica: √(2¹⁰) = 2⁵"]
            })
    return report
