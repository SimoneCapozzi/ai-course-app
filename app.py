import streamlit as st
import io, contextlib, sys, platform, math, random, statistics

# ---------------------------------------------------------
# Opzionale: librerie per demo ML/RAG (servono a Modulo 3 e 4)
# ---------------------------------------------------------
SKLEARN_OK = True
SKLEARN_ERR = ""
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, classification_report
except Exception as _e:
    SKLEARN_OK = False
    SKLEARN_ERR = str(_e)

st.set_page_config(page_title="Percorso di Studio AI & Dev - Full Edition", layout="wide")

# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------
def md(lines):
    st.markdown("\n".join(lines))

def run_py(code: str):
    env = {}
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(code, {}, env)
        out = buf.getvalue().strip()
        return True, (out if out else "Esecuzione OK (nessun output).")
    except Exception as e:
        return False, f"Errore: {e}"

if "progress" not in st.session_state:
    st.session_state.progress = {
        "m0": {"quiz": 0, "done": False},
        "m1": {"quiz": 0, "done": False},
        "m2": {"quiz": 0, "done": False},
        "m3": {"quiz": 0, "done": False},
        "m4": {"quiz": 0, "done": False},
        "m5": {"quiz": 0, "done": False},
        "career": {"notes": 0}
    }

# ---------------------------------------------------------
# Sidebar menu
# ---------------------------------------------------------
st.sidebar.title("Percorso di Studio")
module = st.sidebar.selectbox("Seleziona un modulo:", [
    "0) Setup & Strumenti",
    "1) Python da Zero (completo)",
    "2) Git & GitHub PRO",
    "3) LLM & Fine-Tuning (demo pratica)",
    "4) RAG Systems (demo pratica)",
    "5) Agenti e Multi-Agenti (simulazioni)",
    "6) Career & Portfolio"
])
st.sidebar.info("Suggerimento: affronta i moduli in ordine. I progressi sono locali alla sessione.")

# =========================================================
# MODULO 0 — Setup & Strumenti
# =========================================================
def modulo_0():
    st.title("Modulo 0 - Setup & Strumenti")
    sec = st.sidebar.radio("Sezioni (M0):", [
        "1) Obiettivi e roadmap",
        "2) Installazione Python e verifica",
        "3) Virtualenv e pip",
        "4) Editor (VS Code) e consigli",
        "5) Git e GitHub (setup)",
        "6) Avviare l'app in locale e online",
        "7) Esercizi pratici",
        "8) Quiz rapido"
    ])

    if sec.startswith("1)"):
        md([
            "Questo modulo ti mette in condizione di lavorare bene fin da subito.",
            "",
            "Obiettivi:",
            "- Installare/Verificare Python 3.x",
            "- Capire virtualenv (venv) e pip",
            "- Scegliere un editor (VS Code) e configurarlo",
            "- Creare un repo GitHub e mettere online l'app con Streamlit Cloud"
        ])

    elif sec.startswith("2)"):
        st.subheader("Installa e verifica Python")
        md([
            "1) Scarica Python 3.x dal sito ufficiale (Windows: spunta Add Python to PATH).",
            "2) Verifica nel terminale:"
        ])
        st.code("python --version\npython -c \"import sys, platform; print(sys.version); print(platform.platform())\"")
        code = "import sys, platform\nprint('Python:', sys.version)\nprint('OS:', platform.platform())"
        if st.button("Esegui verifica (qui)"):
            ok, out = run_py(code); st.code(out) if ok else st.error(out)

    elif sec.startswith("3)"):
        st.subheader("Virtualenv e pip")
        md([
            "Per isolare le dipendenze per progetto usa un venv:",
            "- Windows: python -m venv .venv  →  .venv\\Scripts\\Activate.ps1",
            "- macOS/Linux: python3 -m venv .venv  →  source .venv/bin/activate",
            "Installa dipendenze: pip install -r requirements.txt",
            "Disattiva: deactivate"
        ])
        st.code("pip install streamlit\npip freeze > requirements.txt")

    elif sec.startswith("4)"):
        st.subheader("Editor (VS Code) e best practice")
        md([
            "- Installa VS Code e l'estensione Python.",
            "- Apri la cartella del progetto e seleziona l'interprete del venv.",
            "- Usa il terminale integrato (View → Terminal).",
            "- Salva spesso e usa Git per versionare."
        ])

    elif sec.startswith("5)"):
        st.subheader("Git e GitHub - setup minimo")
        st.code("\n".join([
            "git init",
            "git add .",
            "git commit -m \"feat: primo commit\"",
            "git branch -M main",
            "git remote add origin <URL del repo>",
            "git push -u origin main"
        ]))
        md([
            "Suggerimento: usa commit piccoli e messaggi chiari.",
            "Per caricare file dal browser: Add file → Upload files su GitHub."
        ])

    elif sec.startswith("6)"):
        st.subheader("Avvio locale e deploy online")
        st.code("python -m streamlit run app.py")
        md([
            "Per online: usa Streamlit Community Cloud, collega il repo GitHub, imposta file principale app.py.",
            "Aggiornamenti: ogni commit ricostruisce automaticamente l'app."
        ])

    elif sec.startswith("7)"):
        st.subheader("Esercizi pratici Setup")
        md([
            "1) Crea un venv e installa streamlit.",
            "2) Avvia questa app in locale.",
            "3) Crea un repo GitHub e carica app.py e requirements.txt.",
            "4) Fai il deploy su Streamlit Cloud."
        ])
        demo = "print('Hello from your environment!')"
        st.code(demo)
        if st.button("Esegui demo (M0)"):
            ok, out = run_py(demo); st.code(out) if ok else st.error(out)

    else:
        st.subheader("Quiz rapido (M0)")
        q1 = st.radio("A cosa serve un venv?", ["Giocare", "Isolare le dipendenze", "Fare backup"], index=None)
        q2 = st.radio("Comando per avviare l'app in locale?", ["python app.py", "python -m streamlit run app.py", "flask run"], index=None)
        if st.button("Correggi quiz (M0)"):
            score = 0
            if q1 == "Isolare le dipendenze": score += 1
            if q2 == "python -m streamlit run app.py": score += 1
            st.session_state.progress["m0"]["quiz"] = score
            msg = f"Punteggio: {score}/2"
            st.success(msg) if score == 2 else st.warning(msg)

# =========================================================
# MODULO 1 — Python da Zero (ESAUSTIVO)
# =========================================================
def modulo_1():
    st.title("Modulo 1 - Python da Zero (completo)")
    sec = st.sidebar.radio("Sezioni (M1):", [
        "1) Cos'e' la programmazione",
        "2) Variabili e tipi",
        "3) Operatori",
        "4) Strutture di controllo (if, for, while)",
        "5) Strutture dati (list, tuple, set, dict)",
        "6) Funzioni (def, argomenti, lambda)",
        "7) Errori ed eccezioni (try/except)",
        "8) Moduli, pacchetti e venv",
        "9) File I/O (leggere/scrivere)",
        "10) OOP base (classi, oggetti)",
        "11) Esercizi riepilogo",
        "12) Mini-app: analisi spese personali",
        "Quiz finale"
    ])

    if sec.startswith("1)"):
        md([
            "- Programmare significa descrivere passo-passo cosa deve fare il computer.",
            "- Un programma trasforma input → processo → output.",
            "- Python e' adatto ai principianti per sintassi semplice e librerie potenti."
        ])
        st.subheader("Esempio immediato")
        code = 'name = "Ada"\nprint("Ciao", name)\nprint(2 + 3)'
        st.code(code)
        if st.button("Esegui esempio (M1-1)"):
            ok, out = run_py(code); st.code(out) if ok else st.error(out)

    elif sec.startswith("2)"):
        st.subheader("Variabili e tipi")
        md([
            "Una variabile e' un nome che punta a un valore in memoria.",
            "Tipi base: int, float, str, bool, None.",
            "Conversioni: int('3'), float('3.5'), str(10)"
        ])
        st.code("x = 10\npi = 3.14\ns = 'ciao'\nok = True\nn = None\nprint(type(x), type(pi), type(s), type(ok), type(n))")
        st.subheader("Esercizio")
        ex = "a = 7\nb = '8'\nres = a + int(b)\nprint(res)"
        code = st.text_area("Completa/esegui:", value=ex, height=150, key="m1_s2")
        if st.button("Esegui (M1-2)"):
            ok, out = run_py(code); st.code(out) if ok else st.error(out)

    elif sec.startswith("3)"):
        st.subheader("Operatori")
        md([
            "Aritmetici: + - * / // % **",
            "Confronto: == != > >= < <=",
            "Logici: and or not",
            "Assegnazione: = += -= *= ...",
        ])
        st.code("print(7 // 3, 7 % 3, 2 ** 5)\nprint(3 > 2 and 5 < 10)\nx = 5; x += 2; print(x)")
        ex = "prezzo = 89.90\nsconto = 0.15\nfinale = prezzo * (1 - sconto)\nprint(round(finale, 2))"
        code = st.text_area("Calcola prezzo scontato (15%):", value=ex, height=120, key="m1_s3")
        if st.button("Esegui (M1-3)"):
            ok, out = run_py(code); st.code(out) if ok else st.error(out)

    elif sec.startswith("4)"):
        st.subheader("Strutture di controllo")
        col1, col2 = st.columns(2)
        with col1:
            st.caption("if/elif/else")
            st.code("eta = 19\nif eta < 18:\n    print('minorenne')\nelif eta < 65:\n    print('adulto')\nelse:\n    print('senior')")
        with col2:
            st.caption("for e while")
            st.code("for i in range(3):\n    print('for', i)\n\ni = 0\nwhile i < 3:\n    print('while', i)\n    i += 1")
        st.subheader("Esercizi")
        ex1 = "for n in range(1, 11):\n    if n % 2 == 0:\n        print(n)"
        code1 = st.text_area("Pari 1..10:", value=ex1, height=120, key="m1_s4a")
        if st.button("Esegui (M1-4a)"):
            ok, out = run_py(code1); st.code(out) if ok else st.error(out)
        ex2 = "tot = 0\nfor n in range(1, 101):\n    tot += n\nprint(tot)"
        code2 = st.text_area("Somma 1..100:", value=ex2, height=120, key="m1_s4b")
        if st.button("Esegui (M1-4b)"):
            ok, out = run_py(code2); st.code(out) if ok else st.error(out)

    elif sec.startswith("5)"):
        st.subheader("Strutture dati")
        md([
            "list (mutabile, ordinata), tuple (immutabile), set (univoco), dict (chiave->valore)."
        ])
        st.code("nums = [1,2,3]; nums.append(4)\nt = (10, 20)\ns = {1,2,2,3}\nd = {'nome':'Ada','eta':36}\nprint(nums, t, s, d['nome'])")
        ex = "frase = 'ciao ciao come stai ciao'\nconta = {}\nfor p in frase.split():\n    conta[p] = conta.get(p, 0) + 1\nprint(conta)"
        code = st.text_area("Conta parole:", value=ex, height=160, key="m1_s5")
        if st.button("Esegui (M1-5)"):
            ok, out = run_py(code); st.code(out) if ok else st.error(out)

    elif sec.startswith("6)"):
        st.subheader("Funzioni")
        md([
            "def nome(argomenti): return ...",
            "Positional vs keyword argument, default, scope, lambda."
        ])
        st.code("def area_rettangolo(base, altezza=1):\n    return base * altezza\n\nprint(area_rettangolo(5, 2))\nprint(area_rettangolo(base=3, altezza=4))\n\ndoppio = lambda x: x*2\nprint(doppio(7))")
        ex = "def media(values):\n    if not values: return 0\n    return sum(values)/len(values)\n\nprint(media([2,4,6]))"
        code = st.text_area("Implementa media:", value=ex, height=160, key="m1_s6")
        if st.button("Esegui (M1-6)"):
            ok, out = run_py(code); st.code(out) if ok else st.error(out)

    elif sec.startswith("7)"):
        st.subheader("Errori ed eccezioni")
        st.code("s = '10'\ntry:\n    n = int(s)\n    print(n*2)\nexcept ValueError:\n    print('Non e' un numero!')\nfinally:\n    print('Fatto')")
        ex = "def safe_divide(a, b):\n    try:\n        return a/b\n    except ZeroDivisionError:\n        return 'Divisione per zero'\n\nprint(safe_divide(10, 0))"
        code = st.text_area("safe_divide:", value=ex, height=180, key="m1_s7")
        if st.button("Esegui (M1-7)"):
            ok, out = run_py(code); st.code(out) if ok else st.error(out)

    elif sec.startswith("8)"):
        st.subheader("Moduli, pacchetti e venv")
        st.code("import math, statistics\nprint(math.sqrt(16))\nprint(statistics.mean([1,2,3,4]))")
        ex = "import random, statistics\nnums = [random.randint(1, 100) for _ in range(5)]\nprint(nums, statistics.mean(nums), max(nums))"
        code = st.text_area("random + statistics:", value=ex, height=140, key="m1_s8")
        if st.button("Esegui (M1-8)"):
            ok, out = run_py(code); st.code(out) if ok else st.error(out)

    elif sec.startswith("9)"):
        st.subheader("File I/O")
        st.code("text = 'riga1\\nriga2\\n'\nwith open('demo.txt','w',encoding='utf-8') as f:\n    f.write(text)\nwith open('demo.txt','r',encoding='utf-8') as f:\n    print(f.read())")
        ex = "righe = ['uno','due','tre']\nwith open('lista.txt','w',encoding='utf-8') as f:\n    for r in righe:\n        f.write(r+'\\n')\nwith open('lista.txt','r',encoding='utf-8') as f:\n    for i, r in enumerate(f, 1):\n        print(i, r.strip())"
        code = st.text_area("Scrivi/leggi lista:", value=ex, height=200, key="m1_s9")
        if st.button("Esegui (M1-9)"):
            ok, out = run_py(code); st.code(out) if ok else st.error(out)

    elif sec.startswith("10)"):
        st.subheader("OOP base")
        st.code(
            "class Conto:\n"
            "    def __init__(self, intestatario, saldo=0):\n"
            "        self.intestatario = intestatario\n"
            "        self.saldo = saldo\n"
            "    def deposita(self, importo):\n"
            "        self.saldo += importo\n"
            "    def preleva(self, importo):\n"
            "        if importo > self.saldo: raise ValueError('Fondi insufficienti')\n"
            "        self.saldo -= importo\n"
            "    def __str__(self):\n"
            "        return f'Conto({self.intestatario}, saldo={self.saldo})'\n\n"
            "c = Conto('Ada', 100)\n"
            "c.deposita(50)\n"
            "print(c)"
        )
        ex = (
            "class Prodotto:\n"
            "    def __init__(self, nome, prezzo):\n"
            "        self.nome = nome\n"
            "        self.prezzo = prezzo\n"
            "    def scontato(self, perc):\n"
            "        return round(self.prezzo * (1 - perc/100), 2)\n\n"
            "p = Prodotto('Libro', 20.0)\n"
            "print(p.scontato(10))"
        )
        code = st.text_area("Classe Prodotto:", value=ex, height=220, key="m1_s10")
        if st.button("Esegui (M1-10)"):
            ok, out = run_py(code); st.code(out) if ok else st.error(out)

    elif sec.startswith("11)"):
        st.subheader("Esercizi riepilogo")
        md([
            "1) Stringhe: normalizza una frase e conta vocali.",
            "2) Liste/dict: vendite mensili → media, max, mese migliore.",
            "3) Funzioni: calcola BMI e categoria.",
            "4) File: salva CSV spese e ricalcola totale."
        ])
        ex = (
            "# 1) vocali\n"
            "frase = 'Ciao Mondo!'\n"
            "pulita = ''.join(c.lower() for c in frase if c.isalpha() or c==' ')\n"
            "vocali = sum(1 for c in pulita if c in 'aeiou')\n"
            "print('vocali:', vocali)\n\n"
            "# 3) BMI\n"
            "def bmi(peso, altezza):\n"
            "    return round(peso/(altezza**2), 2)\n"
            "print('BMI:', bmi(70, 1.75))"
        )
        code = st.text_area("Lavora qui:", value=ex, height=260, key="m1_s11")
        if st.button("Esegui riepilogo (M1-11)"):
            ok, out = run_py(code); st.code(out) if ok else st.error(out)

    elif sec.startswith("12)"):
        st.subheader("Mini-app: Analisi spese personali")
        if "spese" not in st.session_state: st.session_state.spese = []
        c1, c2, c3 = st.columns(3)
        with c1: imp = st.number_input("Importo", min_value=0.0, value=10.0, step=1.0)
        with c2: cat = st.selectbox("Categoria", ["casa","spesa","trasporti","svago","altro"])
        with c3: mese = st.selectbox("Mese", ["01","02","03","04","05","06","07","08","09","10","11","12"])
        if st.button("Aggiungi spesa"):
            st.session_state.spese.append({"importo":imp,"categoria":cat,"mese":mese})
        if st.session_state.spese:
            tot = sum(x["importo"] for x in st.session_state.spese)
            st.write(f"Totale: {round(tot,2)}")
            agg = {}
            for x in st.session_state.spese:
                agg[x["categoria"]] = agg.get(x["categoria"], 0) + x["importo"]
            st.write({k: round(v,2) for k,v in agg.items()})
            worst = max(agg, key=agg.get)
            st.info(f"Consiglio: prova a ridurre '{worst}' del 10% il prossimo mese.")
        st.caption("Estensioni: esporta CSV, grafici, budget mensili, filtri per data.")

    else:
        st.subheader("Quiz finale (M1)")
        q1 = st.radio("Struttura immutabile?", ["list", "dict", "tuple"], index=None)
        q2 = st.radio("Blocco per gestire errori?", ["catch", "except", "final"], index=None)
        q3 = st.radio("len({'a':1,'b':2,'c':3})?", ["2", "3", "4"], index=None)
        if st.button("Correggi quiz (M1)"):
            score = 0
            if q1 == "tuple": score += 1
            if q2 == "except": score += 1
            if q3 == "3": score += 1
            st.session_state.progress["m1"]["quiz"] = score
            msg = f"Punteggio: {score}/3"
            st.success(msg) if score == 3 else st.warning(msg)

# =========================================================
# MODULO 2 — Git & GitHub PRO (ESAUSTIVO)
# =========================================================
def modulo_2():
    st.title("Modulo 2 - Git & GitHub PRO")
    sec = st.sidebar.radio("Sezioni (M2):", [
        "1) Concetti chiave",
        "2) Workflow moderno (feature branch)",
        "3) Branching, merge, rebase",
        "4) Pull Request e Code Review",
        "5) Conflitti: come risolverli",
        "6) Commit message (Conventional Commits)",
        "7) Esercizi guidati",
        "8) Quiz finale"
    ])

    if sec.startswith("1)"):
        md([
            "Elementi principali:",
            "- Repository locale e remoto",
            "- Working tree → staging → commit",
            "- Remote: origin, fetch, pull, push"
        ])
        st.code("git init\ngit add .\ngit commit -m \"feat: primo commit\"\ngit remote add origin <URL>\ngit push -u origin main")

    elif sec.startswith("2)"):
        st.subheader("Workflow moderno")
        md([
            "1) Crea un branch per ogni feature",
            "2) Commit piccoli, chiari",
            "3) Push e Pull Request",
            "4) Code review e merge su main"
        ])
        st.code("git checkout -b feature/auth\n# ...modifiche...\ngit add .\ngit commit -m \"feat(auth): aggiunge login base\"\ngit push -u origin feature/auth\n# Apri PR su GitHub")

    elif sec.startswith("3)"):
        st.subheader("Branching, merge, rebase")
        md([
            "- merge unisce due storie mantenendo cronologia",
            "- rebase riscrive la base della tua storia per linearizzare",
            "Consiglio: rebase solo sui tuoi branch, non su main condiviso"
        ])
        st.code("git checkout feature/auth\ngit fetch origin\ngit rebase origin/main")

    elif sec.startswith("4)"):
        st.subheader("Pull Request e Code Review")
        md([
            "- PR piccole, descrizione chiara, screenshot se UI",
            "- Checklist: build verde, test, lint",
            "- Rispondi ai commenti, aggiorna la PR"
        ])

    elif sec.startswith("5)"):
        st.subheader("Conflitti")
        md([
            "Capitano quando due commit modificano le stesse righe.",
            "Strategia: apri il file, risolvi i marker <<<<<< ====== >>>>>> e poi:"
        ])
        st.code("git add <file_risolto>\n# se eri in rebase:\ngit rebase --continue\n# se eri in merge:\ngit commit")

    elif sec.startswith("6)"):
        st.subheader("Commit message (Conventional Commits)")
        md([
            "Prefix consigliati: feat, fix, docs, style, refactor, perf, test, chore",
            "Esempio: feat(auth): aggiunge reset password",
            "Per breaking change: feat!: modifica API ..."
        ])
        st.code("git commit -m \"feat(payments)!: cambia contratto API per i pagamenti\"")

    elif sec.startswith("7)"):
        st.subheader("Esercizi guidati (verifica comandi)")
        cmd1 = st.text_input("Crea e spostati su branch hotfix/login:", "")
        if st.button("Verifica 1"):
            ok = cmd1.strip() in ["git checkout -b hotfix/login", "git switch -c hotfix/login"]
            st.success("Corretto!") if ok else st.error("Atteso: git checkout -b hotfix/login (o git switch -c hotfix/login)")
        cmd2 = st.text_input("Collega il remoto origin:", "")
        if st.button("Verifica 2"):
            st.success("Corretto!") if cmd2.startswith("git remote add origin ") else st.error("Atteso: git remote add origin <URL>")
        cmd3 = st.text_input("Comando per portare le modifiche su remoto:", "")
        if st.button("Verifica 3"):
            st.success("Corretto!") if cmd3.strip() == "git push" or cmd3.startswith("git push ") else st.error("Atteso: git push (o git push -u origin <branch>)")

    else:
        st.subheader("Quiz finale (M2)")
        q1 = st.radio("A cosa serve una PR?", ["Cancellare repo", "Proporre e discutere modifiche", "Fare backup"], index=None)
        q2 = st.radio("Quando usare rebase?", ["Su main condiviso", "Sul tuo branch di lavoro", "Mai"], index=None)
        if st.button("Correggi quiz (M2)"):
            score = 0
            if q1 == "Proporre e discutere modifiche": score += 1
            if q2 == "Sul tuo branch di lavoro": score += 1
            st.session_state.progress["m2"]["quiz"] = score
            msg = f"Punteggio: {score}/2"
            st.success(msg) if score == 2 else st.warning(msg)

# =========================================================
# MODULO 3 — LLM & Fine-Tuning (demo pratica con sklearn)
# =========================================================
def modulo_3():
    st.title("Modulo 3 - LLM & Fine-Tuning (concetti + demo)")
    sec = st.sidebar.radio("Sezioni (M3):", [
        "1) Concetti chiave",
        "2) Preparazione dataset",
        "3) Addestramento (demo leggera)",
        "4) Valutazione e predizione",
        "5) Roadmap verso LLM reali"
    ])

    if sec.startswith("1)"):
        md([
            "- Fine-tuning: adattare un modello pre-addestrato ai tuoi dati.",
            "- Usa FT per comportamento/stile; usa RAG per conoscenza variabile.",
            "Pipeline: dataset pulito → split → addestramento → validazione → test → deploy."
        ])

    elif sec.startswith("2)"):
        md([
            "Crea un CSV con colonne: testo,etichetta",
            "Bilancia classi, rimuovi duplicati, normalizza i testi."
        ])
        st.code("testo,etichetta\nprodotto fantastico,pos\nservizio pessimo,neg\nfelice dell'acquisto,pos\nmai piu',neg")

    elif sec.startswith("3)"):
        if not SKLEARN_OK:
            st.warning("Per la demo pratica serve scikit-learn. Errore import: " + SKLEARN_ERR)
            return
        csv_text = st.text_area("Dataset CSV:", height=200, value="testo,etichetta\nbene,pos\nmale,neg\nok,pos\npessimo,neg\n")
        if st.button("Addestra modello (M3)"):
            try:
                rows = [r.strip() for r in csv_text.splitlines() if r.strip()]
                texts, labels = [], []
                for r in rows[1:]:
                    parts = r.split(",")
                    if len(parts) >= 2: texts.append(parts[0]); labels.append(parts[1])
                Xtr, Xte, Ytr, Yte = train_test_split(texts, labels, test_size=0.3, random_state=42, stratify=labels)
                pipe = Pipeline([("vec", TfidfVectorizer()), ("clf", LogisticRegression(max_iter=1000))])
                pipe.fit(Xtr, Ytr)
                preds = pipe.predict(Xte)
                acc = accuracy_score(Yte, preds)
                st.success(f"Accuracy: {acc:.2f}")
                st.code(classification_report(Yte, preds))
                st.session_state.m3_model = pipe
            except Exception as e:
                st.error(f"Errore addestramento: {e}")

    elif sec.startswith("4)"):
        if "m3_model" not in st.session_state:
            st.warning("Addestra prima il modello.")
        else:
            q = st.text_input("Frase da classificare:", "servizio mediocre ma accettabile")
            if st.button("Predici (M3)"):
                try:
                    pred = st.session_state.m3_model.predict([q])[0]
                    st.info(f"Predizione: {pred}")
                except Exception as e:
                    st.error(str(e))

    else:
        md([
            "Per passare a veri LLM:",
            "- Usa HuggingFace Transformers (LoRA/PEFT) su GPU.",
            "- Monitora loss/metrics, usa early-stopping, logging.",
            "- Valuta su set realistici con metriche adeguate.",
            "- Deploy su endpoint con cache, rate-limit, monitoraggio."
        ])

# =========================================================
# MODULO 4 — RAG Systems (demo pratica leggera)
# =========================================================
def modulo_4():
    st.title("Modulo 4 - RAG (Retrieval-Augmented Generation)")
    sec = st.sidebar.radio("Sezioni (M4):", [
        "1) Cos'e' RAG",
        "2) Ingestion e indicizzazione",
        "3) Retrieval + risposta bozza",
        "4) Esercizi e miglioramenti"
    ])

    if sec.startswith("1)"):
        md([
            "RAG combina recupero documenti + generazione.",
            "Quando usarlo: conoscenza ampia/aggiornabile.",
            "Pipeline: chunking → embeddings → vector DB → top-k → prompt LLM."
        ])

    elif sec.startswith("2)"):
        if not SKLEARN_OK:
            st.warning("Per la demo di retrieval serve scikit-learn. Errore import: " + SKLEARN_ERR)
            return
        docs = st.text_area("Incolla documenti separati da ---", height=200, value="A: Streamlit crea web app Python.\n---\nB: Git gestisce versioni del codice.\n---\nC: RAG combina retrieval e LLM.")
        if st.button("Indicizza (M4)"):
            parts = [p.strip() for p in docs.split("---") if p.strip()]
            st.session_state.m4_parts = parts
            st.session_state.m4_vec = TfidfVectorizer().fit(parts)
            st.success(f"Indicizzati {len(parts)} documenti.")

    elif sec.startswith("3)"):
        if "m4_vec" not in st.session_state:
            st.warning("Indicizza prima dei documenti.")
        else:
            k = st.slider("Top-k", 1, 5, 2)
            q = st.text_input("Domanda:", "Cos'e' RAG?")
            if st.button("Recupera + Rispondi (M4)"):
                vec = st.session_state.m4_vec
                parts = st.session_state.m4_parts
                D = vec.transform(parts)
                qv = vec.transform([q])
                sims = (D @ qv.T).toarray().ravel()
                idx = sims.argsort()[::-1][:k]
                retrieved = [parts[i] for i in idx]
                md(["**Rilevanti:**"] + [f"- {r}" for r in retrieved])
                st.info("Bozza di risposta: " + (" ".join(retrieved) if retrieved else "N/A"))

    else:
        md([
            "- Aggiungi chunking dei documenti.",
            "- Implementa stop-words personalizzate.",
            "- Evidenziazioni dei passaggi (passage highlighting).",
            "- Sostituisci TF-IDF con embeddings (FAISS/Chroma) in versione pro."
        ])

# =========================================================
# MODULO 5 — Agenti e Multi-Agenti (simulazioni)
# =========================================================
def modulo_5():
    st.title("Modulo 5 - Agenti e Multi-Agenti (simulazioni)")
    sec = st.sidebar.radio("Sezioni (M5):", [
        "1) Concetti base",
        "2) Agente con tools (simulazione)",
        "3) Pipeline multi-agente",
        "4) Esercizi di progettazione"
    ])

    if sec.startswith("1)"):
        md([
            "Un agente segue: percezione → pianificazione → azione → memoria.",
            "I tools sono funzioni esterne (calc, web, email...).",
            "Multi-agente: ruoli diversi che collaborano (planner, worker, critico)."
        ])

    elif sec.startswith("2)"):
        md(["Regole: se il task contiene 'somma' usa calcolatrice; se 'search' usa knowledge base."])
        KB = {"rag":"RAG unisce retrieval e LLM.", "git":"Git gestisce versioni.", "streamlit":"Streamlit crea web app."}
        default = (
            "task = 'somma 8 e 12'\n"
            "if 'somma' in task:\n"
            "    print('Uso calcolatrice ->', 8+12)\n"
            "elif 'search' in task:\n"
            "    print('Uso KB ->', 'rag', '=>', 'RAG unisce retrieval e LLM.')\n"
            "else:\n"
            "    print('Nessun tool adatto')"
        )
        code = st.text_area("Modifica il task (es. 'search rag') e avvia:", value=default, height=200, key="m5_t1")
        if st.button("Esegui agente (M5-2)"):
            ok, out = run_py(code); st.code(out) if ok else st.error(out)

    elif sec.startswith("3)"):
        md(["Planner scompone, Worker esegue, Critico controlla la qualita'."])
        default = (
            "problem = 'Piano social 1 settimana per palestra locale'\n"
            "steps = ['analisi target', 'idee post', 'calendario']\n"
            "results = []\n"
            "for s in steps:\n"
            "    results.append(f'eseguo: {s}')\n"
            "draft = '\\n'.join(results)\n"
            "critic_ok = all(len(r) > 5 for r in results)\n"
            "print('BOZZA:\\n'+draft)\n"
            "print('APPROVATO?', critic_ok)"
        )
        code = st.text_area("Modifica le regole del critico per alzare la qualità:", value=default, height=220, key="m5_t2")
        if st.button("Esegui pipeline (M5-3)"):
            ok, out = run_py(code); st.code(out) if ok else st.error(out)

    else:
        md([
            "- Definisci 3 tools: web_search, calc, email_stub.",
            "- Progetta un agente che sceglie il tool in base al task.",
            "- Aggiungi memoria: salva risultati e riutilizzali.",
            "- Estendi con pianificazione multi-step (planner → esecutori)."
        ])

# =========================================================
# MODULO 6 — Career & Portfolio
# =========================================================
def modulo_career():
    st.title("Modulo 6 - Career & Portfolio")
    md([
        "Roadmap (6-10 settimane, 1-2h al giorno):",
        "1) Moduli 0-2: basi solide (Python + Git).",
        "2) Moduli 3-4: LLM, Fine-Tuning e RAG con mini-progetti.",
        "3) Modulo 5: agenti, automatizzazioni e demo multi-agente.",
        "",
        "Portfolio minimo (3 progetti in Streamlit):",
        "- Chatbot RAG su documenti di un cliente (manuali/FAQ).",
        "- Classificatore custom (intent/support ticket) addestrato su dati del cliente.",
        "- Automazione con agente (email, fogli di calcolo, API).",
        "",
        "Come trovare i primi clienti:",
        "- Problema specifico + demo pubblica + messaggio chiaro.",
        "- LinkedIn/Upwork con case study e metriche (accuracy, tempo risparmiato).",
        "- Pricing onesto all’inizio, poi alza con prove e risultati."
    ])
    st.text_input("Nota personale (obiettivi prossime 2 settimane):", key="career_note")
    if st.session_state.get("career_note"):
        st.success("Ottimo! Salva questa nota anche nel README del tuo repo come impegno personale.")

# =========================================================
# ROUTER
# =========================================================
if module.startswith("0)"):
    modulo_0()
elif module.startswith("1)"):
    modulo_1()
elif module.startswith("2)"):
    modulo_2()
elif module.startswith("3)"):
    modulo_3()
elif module.startswith("4)"):
    modulo_4()
elif module.startswith("5)"):
    modulo_5()
else:
    modulo_career()

st.sidebar.markdown("---")
st.sidebar.write("Progressi:")
st.sidebar.write(st.session_state.progress)
