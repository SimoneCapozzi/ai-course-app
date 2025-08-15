import streamlit as st
import io, contextlib, math, random

# ---------------------------------------------------------
# PROVE LIBRERIE FACOLTATIVE (per demo ML/RAG)
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

# ---------------------------------------------------------
# UTILS
# ---------------------------------------------------------
st.set_page_config(page_title="AI Course - Full Edition", layout="wide")

if "progress" not in st.session_state:
    st.session_state.progress = {
        "m0": {"quiz": 0, "done": False},
        "m1": {"quiz": 0, "done": False},
        "m2": {"quiz": 0, "done": False},
        "m3": {"quiz": 0, "done": False},
        "m4": {"quiz": 0, "done": False},
        "m5": {"quiz": 0, "done": False},
    }

def md(lines):
    "Helper per markdown senza triple quotes."
    st.markdown("\n".join(lines))

def code_runner(user_code: str):
    "Esegue in sandbox minima; serve per gli esercizi di Python."
    env = {}
    stdout = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout):
            exec(user_code, {}, env)
        out = stdout.getvalue().strip()
        return ("success", out if out else "Esecuzione OK (nessun output).")
    except Exception as e:
        return ("error", f"Errore: {e}")

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.title("Moduli")
module = st.sidebar.radio(
    "Vai al modulo:",
    [
        "0) Setup & Roadmap",
        "1) Fondamenti di Python",
        "2) Git & GitHub Pro",
        "3) LLM & Fine-Tuning (demo pratica)",
        "4) RAG Systems (demo pratica)",
        "5) Agenti e Multi-Agenti (simulazioni)",
        "Career: come monetizzare"
    ],
)
st.sidebar.info("Suggerimento: fai i moduli in ordine. I progressi sono locali alla sessione.")

# =========================================================
# MODULO 0 — Setup & Roadmap
# =========================================================
def modulo_0():
    st.title("Modulo 0 - Setup & Roadmap")
    md([
        "Benvenuto! Qui prepari l'ambiente e capisci come useremo l'app.",
        "",
        "### Obiettivi",
        "- Installare/Verificare Python",
        "- Capire come eseguire esercizi direttamente qui",
        "- Panoramica dei moduli successivi"
    ])

    with st.expander("Setup rapido PC (Windows/macOS/Linux)"):
        md([
            "1) Installa Python 3.x dal sito ufficiale.",
            "2) Apri terminale e verifica: `python --version`.",
            "3) (Opzionale) Crea un virtualenv e attivalo.",
            "4) Esegui localmente con: `streamlit run app.py`."
        ])

    with st.expander("Esercizio - Hello Python"):
        sample = 'print("Hello AI!")'
        code = st.text_area("Scrivi e avvia:", value=sample, height=120, key="m0_hello")
        if st.button("Esegui codice (M0)"):
            s, out = code_runner(code)
            st.code(out) if s == "success" else st.error(out)

    st.subheader("Quiz (M0)")
    q1 = st.radio("1) A cosa serve un ambiente virtuale (venv)?",
                  ["A migliorare le prestazioni della GPU",
                   "A isolare le dipendenze del progetto",
                   "A eseguire codice in remoto"], index=None)
    q2 = st.radio("2) Quale comando avvia questa app in locale?",
                  ["python app.py", "streamlit run app.py", "flask run"], index=None)
    if st.button("Correggi quiz (M0)"):
        score = 0
        if q1 == "A isolare le dipendenze del progetto": score += 1
        if q2 == "streamlit run app.py": score += 1
        st.session_state.progress["m0"]["quiz"] = score
        st.success(f"Punteggio: {score}/2")
        if score == 2:
            st.session_state.progress["m0"]["done"] = True

# =========================================================
# MODULO 1 — Fondamenti di Python
# =========================================================
def modulo_1():
    st.title("Modulo 1 - Fondamenti di Python")
    md([
        "In questo modulo ripassi bene i concetti base e intermedi con **esercizi eseguibili**.",
        "",
        "### Programmazione Python - punti chiave",
        "- Tipi di dato: `int`, `float`, `str`, `bool`",
        "- Strutture: `list`, `dict`, `tuple`, `set`",
        "- Controllo di flusso: `if/elif/else`, `for`, `while`",
        "- Funzioni, comprensioni, eccezioni",
        "- Classi (OOP) e moduli"
    ])

    st.header("Esempi rapidi")
    st.code("x = 10\npi = 3.14\nname = 'Ada'\nflag = True\nprint(type(x), type(pi), type(name), type(flag))")
    st.code("nums = [1,2,3]\nnums.append(4)\nuser = {'name':'Ada','role':'engineer'}\nprint(nums, user['name'])")
    st.code("for i in range(3):\n    print(i, 'pari' if i % 2 == 0 else 'dispari')")

    st.subheader("Esercizio 1 - FizzBuzz")
    fb = (
        "for i in range(1, 21):\n"
        "    out = ''\n"
        "    if i % 3 == 0: out += 'Fizz'\n"
        "    if i % 5 == 0: out += 'Buzz'\n"
        "    print(out or i)"
    )
    code1 = st.text_area("Completa/studia e avvia:", value=fb, height=200, key="m1_e1")
    if st.button("Esegui Esercizio 1"):
        s, out = code_runner(code1); st.code(out) if s=="success" else st.error(out)

    st.subheader("Esercizio 2 - Dizionari")
    dflt = (
        "rubrica = {'Luca':'333123', 'Sara':'340999'}\n"
        "rubrica['Ada'] = '320555'\n"
        "print('Nominativi:', list(rubrica.keys()))\n"
        "print('Numero di Sara:', rubrica.get('Sara'))"
    )
    code2 = st.text_area("Prova:", value=dflt, height=180, key="m1_e2")
    if st.button("Esegui Esercizio 2"):
        s, out = code_runner(code2); st.code(out) if s=="success" else st.error(out)

    st.subheader("Esercizio 3 - Funzioni & Test")
    dflt3 = (
        "def is_palindrome(s):\n"
        "    s = ''.join(c.lower() for c in s if c.isalnum())\n"
        "    return s == s[::-1]\n\n"
        "print(is_palindrome('I topi non avevano nipoti'))"
    )
    code3 = st.text_area("Prova:", value=dflt3, height=200, key="m1_e3")
    if st.button("Esegui Esercizio 3"):
        s, out = code_runner(code3); st.code(out) if s=="success" else st.error(out)

    st.subheader("Quiz (M1)")
    q1 = st.radio("1) Quale struttura è mutabile?", ["tuple", "list", "str"], index=None)
    q2 = st.radio("2) Come definisci una funzione?", ["func my()", "def my():", "function my()"], index=None)
    q3 = st.radio("3) Cosa stampa len({'a':1,'b':2})?", ["1", "2", "3"], index=None)
    if st.button("Correggi quiz (M1)"):
        score = 0
        if q1 == "list": score += 1
        if q2 == "def my():": score += 1
        if q3 == "2": score += 1
        st.session_state.progress["m1"]["quiz"] = score
        st.success(f"Punteggio: {score}/3")
        if score >= 2:
            st.session_state.progress["m1"]["done"] = True

# =========================================================
# MODULO 2 — Git & GitHub Pro
# =========================================================
def modulo_2():
    st.title("Modulo 2 - Git & GitHub Pro")
    md([
        "Obiettivi:",
        "- Capire repository, commit, branch, merge, pull request",
        "- Flusso di lavoro reale con feature branch",
        "- Best practice dei messaggi di commit"
    ])

    st.header("Workflow moderno (riassunto)")
    st.code("\n".join([
        "# Clona una volta",
        "git clone <URL>",
        "cd repo",
        "",
        "# Nuova feature",
        "git checkout -b feature/nome",
        "# ...modifiche...",
        "git add .",
        "git commit -m \"feat: implementa X con Y\"",
        "git push -u origin feature/nome",
        "",
        "# Apri Pull Request su GitHub"
    ]))

    st.subheader("Esercizio - Costruisci il comando giusto")
    cmd = st.text_input("Scrivi il comando per creare e spostarti su un branch 'hotfix/login':", "")
    if st.button("Verifica comando"):
        ok = cmd.strip() in ["git checkout -b hotfix/login", "git switch -c hotfix/login"]
        st.success("Corretto!") if ok else st.error("Risposta attesa: 'git checkout -b hotfix/login' (oppure 'git switch -c hotfix/login').")

    st.subheader("Quiz (M2)")
    q1 = st.radio("1) A cosa serve una Pull Request?", [
        "A cancellare il repository",
        "A proporre e discutere modifiche prima del merge",
        "A clonare un repository"
    ], index=None)
    q2 = st.radio("2) Scopo di 'git rebase' (semplificando)?", [
        "Riscrivere la storia per avere commit lineari",
        "Scaricare dipendenze",
        "Creare tag"
    ], index=None)
    if st.button("Correggi quiz (M2)"):
        score = 0
        if q1 == "A proporre e discutere modifiche prima del merge": score += 1
        if q2 == "Riscrivere la storia per avere commit lineari": score += 1
        st.session_state.progress["m2"]["quiz"] = score
        st.success(f"Punteggio: {score}/2")
        if score == 2:
            st.session_state.progress["m2"]["done"] = True

# =========================================================
# MODULO 3 — LLM & Fine-Tuning (demo pratica con sklearn)
# =========================================================
def modulo_3():
    st.title("Modulo 3 - LLM & Fine-Tuning (concetti + demo)")

    md([
        "Concetti chiave:",
        "- Fine-tuning = adattare un modello pre-addestrato su **tuo** dataset",
        "- Problemi tipici: classificazione, estrazione, stile, intent",
        "- Quando usare FT vs RAG: FT per **comportamenti/stile**; RAG per **conoscenza variabile**"
    ])

    if not SKLEARN_OK:
        st.warning("Per la demo pratica serve 'scikit-learn'. Errore import: " + SKLEARN_ERR)
        return

    st.subheader("Demo: 'simuliamo' un fine-tuning con TF-IDF + LogisticRegression")
    md([
        "Carica/Inserisci un mini-dataset (testo, etichetta) e addestra un classificatore.",
        "Questa è una **proxy** leggera: in produzione useresti Transformers (HuggingFace) su GPU."
    ])

    sample_data = "testo,etichetta\nquesto prodotto è fantastico,pos\nodio usare questo servizio,neg\nsoddisfatto e felice,pos\nassistenza pessima,neg\n"
    data_csv = st.text_area("Dataset CSV (testo,etichetta):", value=sample_data, height=150, key="m3_csv")

    if st.button("Addestra modello (demo)"):
        try:
            rows = [r.strip() for r in data_csv.splitlines() if r.strip()]
            header = rows[0].split(",")
            texts, labels = [], []
            for r in rows[1:]:
                parts = r.split(",")
                if len(parts) >= 2:
                    texts.append(parts[0])
                    labels.append(parts[1])

            X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.3, random_state=42)
            pipe = Pipeline([("tfidf", TfidfVectorizer()), ("clf", LogisticRegression(max_iter=1000))])
            pipe.fit(X_train, y_train)
            preds = pipe.predict(X_test)
            acc = accuracy_score(y_test, preds)
            st.success(f"Accuracy: {acc:.2f}")
            st.code(classification_report(y_test, preds))
            st.session_state.m3_model = pipe
        except Exception as e:
            st.error(f"Errore addestramento: {e}")

    if "m3_model" in st.session_state:
        q = st.text_input("Prova una frase da classificare:", "servizio mediocre ma accettabile")
        if st.button("Predici"):
            try:
                pred = st.session_state.m3_model.predict([q])[0]
                st.info(f"Predizione: {pred}")
            except Exception as e:
                st.error(str(e))

# =========================================================
# MODULO 4 — RAG Systems (demo pratica leggera)
# =========================================================
def modulo_4():
    st.title("Modulo 4 - RAG (Retrieval-Augmented Generation)")

    md([
        "Idea: invece di 'insegnare' al modello la conoscenza, la **recuperiamo** da un archivio aggiornabile.",
        "Pipeline tipica: Ingestion -> Index (vectordb) -> Retrieval -> Prompt LLM.",
        "Qui facciamo una **demo leggera** con TF-IDF per il retrieval (concetto analogo ai vettori)."
    ])

    if not SKLEARN_OK:
        st.warning("Per la demo di retrieval serve 'scikit-learn'. Errore import: " + SKLEARN_ERR)
        return

    docs = st.text_area(
        "Incolla documenti (usa '---' per separare):",
        value="Documento A: Streamlit permette di creare app dati in Python.\n---\nDocumento B: Git gestisce versioni del codice e supporta branching.\n---\nDocumento C: RAG combina recupero documenti e generazione di testo."
    , height=180, key="m4_docs")

    topk = st.slider("Quanti passaggi recuperare (top-k)?", 1, 5, 2)

    if st.button("Indicizza documenti"):
        try:
            parts = [p.strip() for p in docs.split("---") if p.strip()]
            st.session_state.m4_parts = parts
            st.session_state.m4_vec = TfidfVectorizer().fit(parts)
            st.success(f"Indicizzati {len(parts)} documenti.")
        except Exception as e:
            st.error(f"Errore indicizzazione: {e}")

    q = st.text_input("Domanda:", "Cos'è RAG?")
    if st.button("Recupera + Rispondi"):
        if "m4_parts" not in st.session_state:
            st.warning("Indicizza prima i documenti.")
        else:
            vec = st.session_state.m4_vec
            parts = st.session_state.m4_parts
            try:
                import numpy as np
                D = vec.transform(parts)
                qv = vec.transform([q])
                sims = (D @ qv.T).toarray().ravel()
                idx = sims.argsort()[::-1][:topk]
                retrieved = [parts[i] for i in idx]
                md(["**Contenuti rilevanti:**"] + [f"- {p}" for p in retrieved])
                st.info("Bozza di risposta (rule-based): " + (" ".join(retrieved) if retrieved else "N/A"))
            except Exception as e:
                st.error(str(e))

# =========================================================
# MODULO 5 — Agenti e Multi-Agenti (simulazioni)
# =========================================================
def modulo_5():
    st.title("Modulo 5 - Agenti e Multi-Agenti (simulazioni)")

    md([
        "Obiettivi:",
        "- Capire loop di percezione-azione-memoria",
        "- Simulare strumenti (tools) e pianificazione",
        "- Vedere uno scambio multi-agente semplificato"
    ])

    st.subheader("Simulazione: agente con strumenti")
    st.write("Regole semplici: se il task contiene 'add' o 'somma', usa calcolatrice; se contiene 'search', usa knowledge base.")

    def tool_sum(x, y): return x + y
    KB = {
        "rag": "RAG unisce retrieval e LLM.",
        "git": "Git gestisce versioni del codice.",
        "streamlit": "Streamlit crea web app in Python."
    }
    def tool_search(keyword): return KB.get(keyword.lower(), "Nessun risultato.")

    dflt = (
        "task = 'somma 3 e 7'\n"
        "if 'somma' in task or 'add' in task:\n"
        "    print('Uso calcolatrice ->', 3+7)\n"
        "elif 'search' in task:\n"
        "    print('Uso KB ->', 'rag', '=>', 'RAG unisce retrieval e LLM.')\n"
        "else:\n"
        "    print('Nessun tool adatto')"
    )
    code = st.text_area("Prova a cambiare il task (es: 'search rag'):", value=dflt, height=220, key="m5_t1")
    if st.button("Esegui simulazione (agente singolo)"):
        s, out = code_runner(code); st.code(out) if s=="success" else st.error(out)

    st.subheader("Multi-agente (planner -> worker -> critico)")
    md([
        "Scenario: il Planner scompone il problema, il Worker esegue, il Critico controlla.",
        "Esercizio: modifica le regole del Critico per migliorare la qualità."
    ])
    dflt2 = (
        "problem = 'Genera 3 idee per un corso AI per designer'\n"
        "steps = ['ricerca target', 'elenco moduli', 'cta finale']\n"
        "results = []\n"
        "for s in steps:\n"
        "    results.append(f'eseguo: {s}')\n"
        "draft = '\\n'.join(results)\n"
        "critic_ok = all(len(r) > 5 for r in results)\n"
        "print('BOZZA:\\n'+draft)\n"
        "print('APPROVATO?' , critic_ok)"
    )
    code2 = st.text_area("Modifica/avvia:", value=dflt2, height=220, key="m5_t2")
    if st.button("Esegui simulazione (multi-agente)"):
        s, out = code_runner(code2); st.code(out) if s=="success" else st.error(out)

# =========================================================
# CAREER — come monetizzare / cambiare lavoro
# =========================================================
def modulo_career():
    st.title("Career - trovare lavoro o mettersi in proprio")
    md([
        "Percorso consigliato (6-10 settimane, lavorando 1-2 ore al giorno):",
        "1) Moduli 0-2: basi solide (Python + Git).",
        "2) Moduli 3-4: LLM, Fine-Tuning e RAG con mini-progetti.",
        "3) Modulo 5: agenti, automatizzazioni e demo multi-agente.",
        "",
        "Portfolio minimo (3 progetti):",
        "- Chatbot RAG sui documenti del cliente (PDF/FAQ interni).",
        "- Classificatore custom (intent/support ticket) con addestramento leggero.",
        "- Automazione con 'agente' che usa tool (email, fogli, API).",
        "",
        "Come trovare i primi clienti:",
        "- Micro-prodotto su problemi specifici (es: RAG su manuali interni).",
        "- Proposte su LinkedIn/Upwork con demo pubblica (Streamlit).",
        "- Prezzo iniziale onesto + case study con metriche (accuracy, tempo risparmiato)."
    ])

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
