import secrets
import string
import math
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from datetime import datetime

import base64
import hashlib
from cryptography.fernet import Fernet, InvalidToken

# ---------------------------------------------------------
# Globale Konfiguration / Konstanten
# ---------------------------------------------------------

HISTORY_DATEI = "passwort_tresor.txt"
MASTER_PASSWORD = None

COMMON_PASSWORDS = {
    "123456", "password", "123456789", "12345", "qwerty",
    "111111", "12345678", "abc123", "123123", "000000",
    "passwort", "hallo123", "iloveyou"
}

PROFILE_CONFIGS = {
    "1": {"name": "Ultra-Sicher", "laenge": 20, "buchstaben": True, "zahlen": True, "sonder": True, "eindeutig": False},
    "2": {"name": "Einfach zu merken", "laenge": 12, "buchstaben": True, "zahlen": True, "sonder": False, "eindeutig": True},
    "3": {"name": "Nur Zahlen", "laenge": 8, "buchstaben": False, "zahlen": True, "sonder": False, "eindeutig": False},
    "4": {"name": "Gaming-Passwort", "laenge": 16, "buchstaben": True, "zahlen": True, "sonder": False, "eindeutig": False},
}

# ---------------------------------------------------------
# 1. Zeichenpool & Generierung
# ---------------------------------------------------------

def ermittle_zeichenpool(buchstaben, zahlen, sonder, custom_zeichen, nur_eindeutige):
    """Baut den String aller möglichen Zeichen zusammen und gibt ihn zurück."""
    zeichen = ""
    if buchstaben: zeichen += string.ascii_letters
    if zahlen: zeichen += string.digits
    if sonder: zeichen += string.punctuation
    if custom_zeichen: zeichen += custom_zeichen

    if nur_eindeutige:
        for c in "l1IO0":
            zeichen = zeichen.replace(c, "")
            
    # set() entfernt eventuelle Duplikate durch custom_zeichen
    return "".join(set(zeichen))

def passwort_generieren(laenge=12, buchstaben=True, zahlen=True, sonder=True, custom_zeichen="", nur_eindeutige=False):
    zeichen = ermittle_zeichenpool(buchstaben, zahlen, sonder, custom_zeichen, nur_eindeutige)
    if not zeichen:
        raise ValueError("Keine Zeichenarten ausgewählt!")
    return ''.join(secrets.choice(zeichen) for _ in range(laenge))

# ---------------------------------------------------------
# 2. Mathematische Entropie-Berechnung (NEU)
# ---------------------------------------------------------

def berechne_entropie(laenge, pool_groesse):
    """Berechnet die Entropie in Bits."""
    if pool_groesse == 0 or laenge == 0:
        return 0
    return laenge * math.log2(pool_groesse)

def bewerte_entropie(bits):
    """Gibt Level, Farbe und Prozentwert für die Progressbar zurück."""
    if bits < 50:
        return "Schwach", "red", min((bits / 50) * 33, 33)
    elif bits < 80:
        return "Mittel", "orange", 33 + min(((bits - 50) / 30) * 33, 33)
    else:
        # Alles über 80 Bits ist sehr stark (120 Bits gilt als unknackbar)
        return "Stark", "green", 66 + min(((bits - 80) / 40) * 34, 34)

# ---------------------------------------------------------
# 3. Verschlüsselung (Unverändert)
# ---------------------------------------------------------

def generiere_schluessel(master_pw):
    digest = hashlib.sha256(master_pw.encode()).digest()
    return base64.urlsafe_b64encode(digest)

def history_speichern_verschluesselt(pw, laenge):
    global MASTER_PASSWORD
    if not MASTER_PASSWORD: return
    zeit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    eintrag = f"[{zeit}] Länge={laenge}, Passwort={pw}"
    f = Fernet(generiere_schluessel(MASTER_PASSWORD))
    try:
        with open(HISTORY_DATEI, "ab") as file:
            file.write(f.encrypt(eintrag.encode()) + b"\n")
    except Exception as e:
        print("Konnte Tresor nicht aktualisieren:", e)

def history_lesen_verschluesselt():
    global MASTER_PASSWORD
    if not MASTER_PASSWORD: return "Bitte zuerst Master-Passwort setzen."
    f = Fernet(generiere_schluessel(MASTER_PASSWORD))
    ausgabe = []
    try:
        with open(HISTORY_DATEI, "rb") as file:
            for zeile in file:
                if zeile.strip():
                    try:
                        ausgabe.append(f.decrypt(zeile.strip()).decode())
                    except InvalidToken:
                        return "Falsches Master-Passwort! Entschlüsselung fehlgeschlagen."
        return "\n".join(ausgabe) if ausgabe else "Der Tresor ist leer."
    except FileNotFoundError:
        return "Noch kein Tresor vorhanden."

# ---------------------------------------------------------
# 4. GUI-Version (Aktualisiert mit Entropy-Bar)
# ---------------------------------------------------------

def gui_start():
    global MASTER_PASSWORD
    fenster = tk.Tk()
    fenster.title("Pro-Passwort-Manager")
    fenster.geometry("450x520")
    fenster.configure(bg="#1e1e1e")

    MASTER_PASSWORD = simpledialog.askstring(
        "Master-Passwort", 
        "Bitte lege ein Master-Passwort fest oder gib dein bestehendes ein:",
        show="*"
    )

    style = ttk.Style(fenster)
    try: style.theme_use("clam")
    except: pass
    style.configure("TLabel", background="#1e1e1e", foreground="white")
    style.configure("TCheckbutton", background="#1e1e1e", foreground="white")
    # Styling für die Progressbar
    style.configure("Horizontal.TProgressbar", background="#005500", troughcolor="#2b2b2b")

    var_laenge = tk.IntVar(value=12)
    var_buchstaben = tk.BooleanVar(value=True)
    var_zahlen = tk.BooleanVar(value=True)
    var_sonder = tk.BooleanVar(value=True)
    var_eindeutig = tk.BooleanVar(value=False)
    var_custom = tk.StringVar()
    var_staerke_text = tk.StringVar(value="Entropie: 0 Bits")

    def aktualisiere_staerke_preview(*args):
        try:
            pool_str = ermittle_zeichenpool(var_buchstaben.get(), var_zahlen.get(), var_sonder.get(), var_custom.get(), var_eindeutig.get())
            pool_groesse = len(pool_str)
            laenge = var_laenge.get()
            
            bits = berechne_entropie(laenge, pool_groesse)
            level, farbe, prozent = bewerte_entropie(bits)
            
            var_staerke_text.set(f"{level} (~{int(bits)} Bits)")
            label_staerke.config(fg=farbe)
            progress_entropie['value'] = prozent
            
        except Exception:
            var_staerke_text.set("Fehler bei Berechnung")
            progress_entropie['value'] = 0

    def generieren():
        try:
            pw = passwort_generieren(var_laenge.get(), var_buchstaben.get(), var_zahlen.get(), var_sonder.get(), var_custom.get(), var_eindeutig.get())
            ausgabe.delete(0, tk.END)
            ausgabe.insert(0, pw)
            aktualisiere_staerke_preview()
            history_speichern_verschluesselt(pw, var_laenge.get())

            if pw in COMMON_PASSWORDS:
                messagebox.showwarning("Warnung", "Dieses Passwort ist sehr häufig und unsicher!")
        except Exception as e:
            messagebox.showerror("Fehler", f"Ungültige Eingabe!\n{e}")

    def tresor_oeffnen():
        inhalt = history_lesen_verschluesselt()
        tresor_fenster = tk.Toplevel(fenster)
        tresor_fenster.title("Mein Passwort-Tresor")
        tresor_fenster.geometry("500x350")
        text_feld = tk.Text(tresor_fenster, bg="#2b2b2b", fg="white", wrap=tk.WORD, font=("Consolas", 10))
        text_feld.pack(expand=True, fill='both')
        text_feld.insert(tk.END, inhalt)
        text_feld.config(state=tk.DISABLED)

    def in_zwischenablage():
        pw = ausgabe.get()
        if not pw: return
        fenster.clipboard_clear()
        fenster.clipboard_append(pw)
        fenster.update()
        messagebox.showinfo("Kopiert", "Passwort kopiert!")

    def profil_auswaehlen(event=None):
        profil_name = combo_profile.get()
        for key, cfg in PROFILE_CONFIGS.items():
            if cfg["name"] == profil_name:
                var_laenge.set(cfg["laenge"])
                var_buchstaben.set(cfg["buchstaben"])
                var_zahlen.set(cfg["zahlen"])
                var_sonder.set(cfg["sonder"])
                var_eindeutig.set(cfg["eindeutig"])
                aktualisiere_staerke_preview()
                break

    # --- Widgets ---
    ttk.Label(fenster, text="Profil:").pack(pady=(10, 0))
    combo_profile = ttk.Combobox(fenster, values=[cfg["name"] for cfg in PROFILE_CONFIGS.values()], state="readonly")
    combo_profile.pack()
    combo_profile.bind("<<ComboboxSelected>>", profil_auswaehlen)

    ttk.Label(fenster, text="Länge:").pack(pady=(10, 0))
    tk.Spinbox(fenster, from_=4, to=128, textvariable=var_laenge, command=aktualisiere_staerke_preview, bg="#2b2b2b", fg="white").pack()

    frame_checks = tk.Frame(fenster, bg="#1e1e1e")
    frame_checks.pack(pady=5)

    tk.Checkbutton(frame_checks, text="Buchstaben", variable=var_buchstaben, bg="#1e1e1e", fg="white", selectcolor="#333", command=aktualisiere_staerke_preview).grid(row=0, column=0, sticky="w")
    tk.Checkbutton(frame_checks, text="Zahlen", variable=var_zahlen, bg="#1e1e1e", fg="white", selectcolor="#333", command=aktualisiere_staerke_preview).grid(row=0, column=1, sticky="w")
    tk.Checkbutton(frame_checks, text="Sonderzeichen", variable=var_sonder, bg="#1e1e1e", fg="white", selectcolor="#333", command=aktualisiere_staerke_preview).grid(row=1, column=0, sticky="w")
    tk.Checkbutton(frame_checks, text="Keine (l, 1, I, O, 0)", variable=var_eindeutig, bg="#1e1e1e", fg="white", selectcolor="#333", command=aktualisiere_staerke_preview).grid(row=1, column=1, sticky="w")

    ttk.Label(fenster, text="Eigene Zeichen (optional):").pack()
    entry_custom = tk.Entry(fenster, textvariable=var_custom, bg="#2b2b2b", fg="white")
    entry_custom.pack()
    entry_custom.bind("<KeyRelease>", aktualisiere_staerke_preview)

    # --- NEU: Entropie Anzeige ---
    frame_entropie = tk.Frame(fenster, bg="#1e1e1e")
    frame_entropie.pack(pady=10, fill="x", padx=40)
    
    label_staerke = tk.Label(frame_entropie, textvariable=var_staerke_text, bg="#1e1e1e", fg="white", font=("Arial", 10, "bold"))
    label_staerke.pack()
    
    progress_entropie = ttk.Progressbar(frame_entropie, orient="horizontal", length=300, mode="determinate")
    progress_entropie.pack(pady=5)
    # -----------------------------

    tk.Button(fenster, text="Generieren", command=generieren, bg="#3c3c3c", fg="white", font=("Arial", 10, "bold")).pack(pady=5)

    ausgabe = tk.Entry(fenster, width=40, bg="#2b2b2b", fg="white", font=("Consolas", 12), justify="center")
    ausgabe.pack(pady=(5, 0))

    tk.Button(fenster, text="In Zwischenablage kopieren", command=in_zwischenablage, bg="#3c3c3c", fg="white").pack(pady=5)
    tk.Button(fenster, text="🔐 Tresor öffnen", command=tresor_oeffnen, bg="#005500", fg="white", font=("Arial", 10, "bold")).pack(pady=15)

    aktualisiere_staerke_preview()
    fenster.mainloop()

if __name__ == "__main__":
    gui_start()
