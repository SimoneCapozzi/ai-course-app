import streamlit as st
import io
import contextlib

st.set_page_config(page_title="AI Builder Course - Moduli 0-1", layout="wide")

# Stato minimale per progressi
if "progress" not in st.session_state:
    st.session_state.progress = {"mod0": {"quiz": 0, "done": False}, "mod1": {"quiz": 0, "done": False}}

# Sidebar
st.sidebar.title("Moduli")
module = st.sidebar.radio("Vai al modulo:", ["Modulo 0 - Setup e GitHub", "Modulo 1 - Fondamenti di Python"])
st.sidebar.info("Suggerimento: aggiungi ai preferiti questo link per riprendere da dove hai lasciato.")

# Runner codice per gli esercizi
def code_runner(user_code: str):
    env = {}
    stdout = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout):
            exec(user_code, {}, env)
        out = stdout.getvalue()
        return ("success", out if out.strip() else "Il codice e' stato eseguito senza output.")
    except Exception as e:
        return ("error", f"Errore in esecuzione: {e}")

# -----------------------------
# Quiz Modulo 0
# -----------------------------
def quiz_mod0():
    st.subheader("Quiz Modulo 0 (5 domande)")
    q1 = st.radio("1) Che cos'e' Git?", ["Un servizio di hosting", "Un sistema di controllo di versione", "Un editor di testo"], index=None)
    q2 = st.radio("2) A cosa serve GitHub?", ["A gestire versioni in locale", "A ospitare repository e collaborare", "A eseguire il codice"], index=None)
    q3 = st.radio("3) Qual e' il comando per inviare modifiche al repository remoto?", ["git push", "git init", "git status"], index=None)
    q4 = st.radio("4) Qual e' la sequenza corretta?", ["clone -> add -> commit -> push", "add -> push -> commit -> clone", "commit -> add -> push -> clone"], index=None)
    q5 = st.radio("5) Cosa contiene un commit?", ["Screenshot del codice", "Un pacchetto binario", "Uno snapshot dei file con un messaggio"], index=None)

    if st.button("Correggi quiz"):
        score = 0
        if q1 == "Un sistema di controllo di versione": score += 1
        if q2 == "A ospitare repository e collaborare": score += 1
        if q3 == "git push": score += 1
        if q4 == "clone -> add -> commit -> push": score += 1
        if q5 == "Uno snapshot dei file con un messaggio": score += 1
        st.session_state.progress["mod0"]["quiz"] = score
        st.success(f"Punteggio: {score}/5")
        if score >= 4:
            st.session_state.progress["mod0"]["done"] = True

# -----------------------------
# Modulo 0
# -----------------------------
def module_0():
    st.title("Modulo 0 - Setup e GitHub")

    st.markdown("\n".join([
        "Benvenuto! In questo modulo prepari l'ambiente in modo **rapido e pratico**, sia da **PC** che da **telefono**.",
        "",
        "### Obiettivi",
        "- Installare Python (o usare un editor online se non puoi installare)",
        "- Capire Git e GitHub in modo semplice",
        "- Pubblicare il tuo primo script online",
        "- Superare un mini-quiz di autovalutazione",
    ]))

    with st.expander("Opzione A - Installare Python su PC"):
        st.markdown("\n".join([
            "1) Scarica Python da **python.org** (versione 3.x) e durante l'installazione spunta **Add Python to PATH**.",
            "2) Apri il **Prompt dei comandi/Terminale** e verifica con:",
            "```",
            "python --version",
            "```",
            "3) Crea una cartella di lavoro (es. `ai-course`) e dentro crea `hello_ai.py` con:",
            "```",
            "print(\"Hello AI\")",
            "```",
        ]))

    with st.expander("Opzione B - Programmare da telefono/PC con Replit"):
        st.markdown("\n".join([
            "1) Vai su **replit.com** e crea un account.",
            "2) Nuovo Repl -> Template **Python**.",
            "3) Incolla nella finestra principale:",
            "```",
            "print(\"Hello AI\")",
            "```",
            "4) Clicca **Run**.",
        ]))

    st.markdown("---")
    st.header("Esercizio pratico - Hello AI")
    code = st.text_area("Il tuo codice Python:", value='print(\"Hello AI\")', height=120)
    if st.button("Esegui codice"):
        status, out = code_runner(code)
        st.code(out) if status == "success" else st.error(out)

    st.markdown("---")
    st.header("Git e GitHub in 5 minuti (versione semplice)")
    st.markdown("\n".join([
        "**Git** e' un sistema per tracciare le versioni del codice. **GitHub** e' il servizio online dove ospiti i progetti.",
        "",
        "**Passi tipici (PC):**",
        "```",
        "git clone <URL_DEL_REPO>",
        "git add .",
        "git commit -m \"Messaggio chiaro\"",
        "git push",
        "```",
        "**Passi tipici (telefono/Replit):**",
        "- Nel Repl usa **Version Control** -> scrivi un messaggio -> **Commit & Push**.",
    ]))

    quiz_mod0()

# -----------------------------
# Quiz Modulo 1
# -----------------------------
def quiz_mod1():
    st.subheader("Quiz Modulo 1 (4 domande)")
    q1 = st.radio("1) Quale tipo di dato rappresenta una sequenza mutabile?", ["tuple", "list", "str"], index=None)
    q2 = st.radio("2) Come si itera su una lista items?", ["for i in range(items):", "for x in items:", "items.for()"], index=None)
    q3 = st.radio("3) Come si definisce una funzione in Python?", ["func my():", "def my_func():", "function my():"], index=None)
    q4 = st.radio("4) Cosa stampa print(len({'a':1,'b':2}))?", ["1", "2", "3"], index=None)

    if st.button("Correggi quiz Modulo 1"):
        score = 0
        if q1 == "list": score += 1
        if q2 == "for x in items:": score += 1
        if q3 == "def my_func():": score += 1
        if q4 == "2": score += 1
        st.session_state.progress["mod1"]["quiz"] = score
        st.success(f"Punteggio: {score}/4")
        if score >= 3:
            st.session_state.progress["mod1"]["done"] = True

# -----------------------------
# Modulo 1
# -----------------------------
def module_1():
    st.title("Modulo 1 - Fondamenti di Python")

    st.markdown("\n".join([
        "Contenuti",
        "- Variabili e tipi (int, float, str, bool)",
        "- Strutture dati (list, dict, tuple)",
        "- Condizioni e cicli (if, for, while)",
        "- Funzioni e moduli",
    ]))

    st.header("Esempi rapidi")
    st.code("x = 10\npi = 3.14\nname = \"Ada\"\nflag = True\nprint(type(x), type(pi), type(name), type(flag))")
    st.code("nums = [1, 2, 3]\nnums.append(4)\nuser = {\"name\": \"Ada\", \"role\": \"engineer\"}\nprint(nums, user[\"name\"])")
    st.code("for i in range(3):\n    if i % 2 == 0:\n        print(i, \"pari\")\n    else:\n        print(i, \"dispari\")")
    st.code("def greet(name):\n    return f\"Ciao, {name}!\"\nprint(greet(\"Ada\"))")

    st.markdown("---")
    st.header("Esercizi pratici")

    with st.expander("1) Calcolatrice base"):
        st.write("Scrivi una funzione calc(a, b, op) che esegue +, -, *, /.")
        code1 = st.text_area("Codice esercizio 1:", value=(
            "def calc(a, b, op):\n"
            "    if op == '+':\n        return a + b\n"
            "    elif op == '-':\n        return a - b\n"
            "    elif op == '*':\n        return a * b\n"
            "    elif op == '/':\n        return a / b\n"
            "    else:\n        return 'Operatore non valido'\n\n"
            "print(calc(6, 3, '+'))"
        ), height=220, key="calc1")
        if st.button("Esegui esercizio 1"):
            status, out = code_runner(code1)
            st.code(out) if status == "success" else st.error(out)

    with st.expander("2) Lista spesa"):
        st.write("Gestisci una lista (aggiungi, rimuovi, mostra).")
        code2 = st.text_area("Codice esercizio 2:", value=(
            "shopping = []\n"
            "shopping.append('latte')\n"
            "shopping.append('pane')\n"
            "shopping.remove('latte')\n"
            "print('Lista:', shopping)"
        ), height=180, key="list2")
        if st.button("Esegui esercizio 2"):
            status, out = code_runner(code2)
            st.code(out) if status == "success" else st.error(out)

    with st.expander("3) Generatore di password"):
        st.write("Crea una password casuale di n caratteri usando random e string.")
        code3 = st.text_area("Codice esercizio 3:", value=(
            "import random, string\n\n"
            "def gen_password(n=10):\n"
            "    chars = string.ascii_letters + string.digits\n"
            "    return ''.join(random.choice(chars) for _ in range(n))\n\n"
            "print(gen_password(12))"
        ), height=220, key="pwd3")
        if st.button("Esegui esercizio 3"):
            status, out = code_runner(code3)
            st.code(out) if status == "success" else st.error(out)

    st.markdown("---")
    quiz_mod1()

# -----------------------------
# Router
# -----------------------------
if module.startswith("Modulo 0"):
    module_0()
else:
    module_1()

st.sidebar.markdown("---")
st.sidebar.write("Progresso:")
st.sidebar.write(st.session_state.progress)
