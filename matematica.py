import random

def genera_esercizio(classe):
    if str(classe) == '1':
        # Inserita una nuova variante per la 1° superiore: Espressioni letterali
        argomenti = ['equazioni', 'potenze', 'monomi', 'espressioni_letterali']
    else:
        # Inserito il nuovo argomento richiesto per la 2° superiore: Scomposizioni
        argomenti = ['equazioni_2g', 'radicali', 'scomposizioni']
        
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

    elif argomento == 'espressioni_letterali':
        # Calcolo del valore di un polinomio sostituendo alla x un numero fisso
        val_x = random.choice([2, 3, -1])
        coeff = random.randint(2, 5)
        costante = random.randint(-10, 10)
        testo = f"Calcola il valore del polinomio '{coeff}x + ({costante})' se x = {val_x}"
        risposta = (coeff * val_x) + costante
        return testo, risposta, "espressioni_letterali"

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

    elif argomento == 'scomposizioni':
        # Scomposizione di un prodotto notevole (Differenza di quadrati): x² - A = 0
        soluzione_positiva = random.randint(2, 8)
        quadrato = soluzione_positiva ** 2
        testo = f"Trova la soluzione POSITIVA della scomposizione (differenza di quadrati): x² - {quadrato} = 0"
        return testo, soluzione_positiva, "scomposizioni"

    else:
        return "Semplifica il radicale: √(3⁴) = 3^?", 2, "radicali"

def ottieni_consiglio_recupero(argomenti_falliti):
    report = []
    percorso_studio = set(argomenti_falliti)
    
    for arg in percorso_studio:
        if arg == 'equazioni':
            report.append({
                "titolo": "📝 RIPASSO: Equazioni di 1° Grado",
                "consiglio": "Sposta tutti i termini con la x a sinistra e i numeri a destra. Quando sposti un termine ricorda di cambiare il segno!",
                "esercizi_extra": ["3x - 6 = 12 (Risultato: x = 6)", "-2x + 5 = -5 (Risultato: x = 5)"]
            })
        elif arg == 'potenze':
            report.append({
                "titolo": "📝 RIPASSO: Proprietà delle Potenze",
                "consiglio": "Nella moltiplicazione tra potenze con la stessa base, la base resta uguale e gli esponenti si SOMMANO.",
                "esercizi_extra": ["2⁴ * 2³ = 2⁷", "5² * 5³ = 5⁵"]
            })
        elif arg == 'monomi':
            report.append({
                "titolo": "📝 RIPASSO: Moltiplicazione tra Monomi",
                "consiglio": "Moltiplica i numeri tra loro seguendo la regola dei segni e somma gli esponenti delle lettere uguali.",
                "esercizi_extra": ["(4x) * (-3x³) = -12x⁴", "(-2x²) * (-5x) = 10x³"]
            })
        elif arg == 'espressioni_letterali':
            report.append({
                "titolo": "📝 RIPASSO: Valutazione di Espressioni Letterali",
                "consiglio": "Sostituisci il valore numerico fornito al posto della lettera x dentro l'espressione, facendo molta attenzione alle precedenze delle operazioni e ai segni dei numeri negativi.",
                "esercizi_extra": ["Trova il valore di 3x - 4 se x = 2 (Risultato: 2)", "Trova il valore di 2x + 5 se x = -1 (Risultato: 3)"]
            })
        elif arg == 'equazioni_2g':
            report.append({
                "titolo": "📝 RIPASSO: Equazioni di 2° Grado",
                "consiglio": "Se l'equazione è del tipo x² + bx + c = 0, puoi trovare le due soluzioni cercando due numeri la cui somma sia -b e il prodotto sia c.",
                "esercizi_extra": ["x² - 5x + 6 = 0 (Soluzioni: 2 e 3)", "x² - 4 = 0 (Soluzioni: -2 e 2)"]
            })
        elif arg == 'scomposizioni':
            report.append({
                "titolo": "📝 RIPASSO: Scomposizioni (Differenza di Quadrati)",
                "consiglio": "Un'espressione del tipo x² - a² si scompone nel prodotto della somma delle basi per la loro differenza: (x + a)(x - a) = 0. Le soluzioni saranno quindi x = a e x = -a.",
                "esercizi_extra": ["Trova la sol. positiva di x² - 9 = 0 (Risultato: 3)", "Trova la sol. positiva di x² - 16 = 0 (Risultato: 4)"]
            })
        elif arg == 'radicali':
            report.append({
                "titolo": "📝 RIPASSO: Semplificazione di Radicali",
                "consiglio": "Per portare un fattore fuori dalla radice quadrata, dividi il suo esponente per 2. Es: √(3⁶) diventa 3³.",
                "esercizi_extra": ["√(3⁴) = 3²", "√(2¹⁰) = 2⁵"]
            })
    return report
