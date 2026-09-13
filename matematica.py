import random

def genera_esercizio(classe):
    if str(classe) == '1':
        # Prima Superiore: Equazioni di 1° Grado
        x_corretta = random.randint(-10, 10)
        a = random.choice([2, 3, 4, 5, -2, -3, -4, -5])
        b = random.randint(-20, 20)
        c = a * x_corretta + b
        
        segno_b = "+" if b >= 0 else ""
        testo = f"Risolvi l'equazione: {a}x {segno_b}{b} = {c}"
        indizio = f"💡 Suggerimento: Isola la x. Sposta {b} a destra dell'uguale cambiando il suo segno, poi dividi tutto per {a}."
        return testo, x_corretta, indizio
    else:
        # Seconda Superiore: Equazioni di 2° Grado pure/spurie/complete con soluzioni intere
        x1 = random.randint(-5, 5)
        x2 = random.randint(-5, 5)
        b = -(x1 + x2)
        c = x1 * x2
        
        segno_b = f"+ {b}" if b > 0 else f"- {abs(b)}" if b < 0 else ""
        segno_c = f"+ {c}" if c > 0 else f"- {abs(c)}" if c < 0 else ""
        
        termine_b = f"{segno_b}x " if b != 0 else ""
        termine_c = f"{segno_c} " if c != 0 else ""
        
        testo = f"Trova una delle soluzioni intere di: x² {termine_b}{termine_c}= 0"
        indizio = f"💡 Suggerimento: Puoi risolverla trovando due numeri che sommati danno {b} e moltiplicati danno {c}, oppure usando la formula del delta."
        return testo, [x1, x2], indizio
