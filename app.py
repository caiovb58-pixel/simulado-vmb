import streamlit as st
import pandas as pd
import time

st.set_page_config(layout="wide")

# =========================
# CONFIG
# =========================
st.title("📊 Simulado ANCORD")

SHEET_URL = st.text_input("Cole o link CSV da planilha")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

# =========================
# SESSION STATE
# =========================
if "started" not in st.session_state:
    st.session_state.started = False

if "finished" not in st.session_state:
    st.session_state.finished = False

if "current_q" not in st.session_state:
    st.session_state.current_q = 0

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "quiz" not in st.session_state:
    st.session_state.quiz = None

# =========================
# START SCREEN
# =========================
if SHEET_URL and not st.session_state.started:

    df = load_data(SHEET_URL)

    temas = df["topic"].unique()
    tema = st.selectbox("Tema", temas)
    qtd = st.slider("Quantidade de questões", 5, 20, 10)

    if st.button("🚀 Iniciar Simulado"):

        quiz = df[df["topic"] == tema].sample(n=qtd, random_state=42)

        st.session_state.quiz = quiz.reset_index(drop=True)
        st.session_state.started = True
        st.session_state.start_time = time.time()

        st.rerun()

# =========================
# QUIZ SCREEN
# =========================
if st.session_state.started and not st.session_state.finished:

    quiz = st.session_state.quiz
    total = len(quiz)
    i = st.session_state.current_q

    st.progress((i + 1) / total)

    row = quiz.iloc[i]

    st.subheader(f"Pergunta {i+1} de {total}")
    st.write(row["question"])

    options = [row["A"], row["B"], row["C"], row["D"]]

    resposta = st.radio(
        "Escolha:",
        options,
        index=options.index(st.session_state.answers.get(i, options[0]))
        if i in st.session_state.answers else 0
    )

    st.session_state.answers[i] = resposta

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⬅️ Voltar") and i > 0:
            st.session_state.current_q -= 1
            st.rerun()

    with col2:
        if st.button("➡️ Próxima") and i < total - 1:
            st.session_state.current_q += 1
            st.rerun()

    with col3:
        if st.button("✅ Finalizar"):
            st.session_state.finished = True
            st.rerun()

# =========================
# RESULT SCREEN
# =========================
if st.session_state.finished:

    quiz = st.session_state.quiz
    answers = st.session_state.answers

    results = []

    for i, row in quiz.iterrows():

        correto = answers.get(i) == row["correct"]

        results.append({
            "topic": row["topic"],
            "correct": correto
        })

    result_df = pd.DataFrame(results)

    score = round(result_df["correct"].mean() * 100, 2)

    tempo = round(time.time() - st.session_state.start_time, 2)

    st.success(f"🎯 Nota: {score}%")
    st.info(f"⏱ Tempo: {tempo} segundos")

    st.subheader("📉 Pontos fracos")

    weak = result_df.groupby("topic")["correct"].mean().sort_values()

    st.bar_chart(weak)

    st.subheader("📋 Revisão")

    for i, row in quiz.iterrows():

        user = answers.get(i)
        correct = row["correct"]

        if user == correct:
            st.success(f"{i+1}. ✔️ {row['question']}")
        else:
            st.error(f"{i+1}. ❌ {row['question']}")
            st.write(f"Sua resposta: {user}")
            st.write(f"Correta: {correct}")

    if st.button("🔄 Refazer Simulado"):

        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.rerun()
