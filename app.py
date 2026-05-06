import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Simulado ANCORD - VMB", layout="wide")

# =========================
# LOAD DATA
# =========================
@st.cache_data(ttl=600)
def load_data(url):
    try:
        # Força a leitura como CSV do Google Sheets
        if "edit" in url:
            url = url.replace("edit", "export?format=csv")
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Erro ao carregar planilha: {e}")
        return None

# =========================
# SESSION STATE (Inicialização)
# =========================
if "started" not in st.session_state:
    st.session_state.update({
        "started": False,
        "finished": False,
        "current_q": 0,
        "answers": {},
        "start_time": None,
        "quiz": None
    })

# =========================
# TELA INICIAL
# =========================
st.title("📊 Simulado ANCORD")

SHEET_URL = st.text_input("Cole o link da sua planilha do Google Sheets", 
                         placeholder="https://docs.google.com/spreadsheets/d/...")

if SHEET_URL and not st.session_state.started:
    df = load_data(SHEET_URL)
    
    if df is not None:
        temas = ["Todos"] + sorted(df["topic"].unique().tolist())
        tema_selecionado = st.selectbox("Selecione o Tema", temas)
        
        max_q = len(df) if tema_selecionado == "Todos" else len(df[df["topic"] == tema_selecionado])
        qtd = st.slider("Quantidade de questões", 5, min(max_q, 50), min(10, max_q))

        if st.button("🚀 Iniciar Simulado"):
            if tema_selecionado == "Todos":
                st.session_state.quiz = df.sample(n=qtd).reset_index(drop=True)
            else:
                st.session_state.quiz = df[df["topic"] == tema_selecionado].sample(n=qtd).reset_index(drop=True)
            
            st.session_state.started = True
            st.session_state.start_time = time.time()
            st.rerun()

# =========================
# TELA DE QUESTÕES
# =========================
if st.session_state.started and not st.session_state.finished:
    quiz = st.session_state.quiz
    i = st.session_state.current_q
    total = len(quiz)
    row = quiz.iloc[i]

    # Barra Lateral de Progresso
    st.sidebar.header(f"Questão {i+1} de {total}")
    st.sidebar.progress((i + 1) / total)
    
    if st.sidebar.button("❌ Abandonar"):
        st.session_state.started = False
        st.rerun()

    st.info(f"**Módulo:** {row['topic']}")
    st.write(f"### {row['question']}")

    # Importante: O rádio precisa de uma KEY única baseada no índice i
    options = [row["A"], row["B"], row["C"], row["D"]]
    
    # Recupera resposta anterior se existir
    current_answer = st.session_state.answers.get(i)
    
    selected = st.radio(
        "Selecione a alternativa:",
        options,
        index=options.index(current_answer) if current_answer in options else None,
        key=f"radio_q_{i}" # CORREÇÃO PARA O ERRO DE REMOVECHILD
    )

    if selected:
        st.session_state.answers[i] = selected

    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        if i > 0 and st.button("⬅️ Anterior"):
            st.session_state.current_q -= 1
            st.rerun()

    with col2:
        if i < total - 1:
            if st.button("Próxima ➡️"):
                st.session_state.current_q += 1
                st.rerun()

    with col3:
        if st.button("✅ Finalizar"):
            if len(st.session_state.answers) < total:
                st.warning("Responda todas antes de finalizar.")
            else:
                st.session_state.finished = True
                st.rerun()

# =========================
# TELA DE RESULTADOS
# =========================
if st.session_state.finished:
    st.header("🎯 Resultado Final")
    
    quiz = st.session_state.quiz
    ans = st.session_state.answers
    
    score = 0
    results_list = []

    for idx, row in quiz.iterrows():
        user_choice = ans.get(idx)
        # Mapeia o texto da opção de volta para a letra (A, B, C, D) para comparar
        user_letter = next((l for l in ["A", "B", "C", "D"] if row[l] == user_choice), None)
        
        correto = user_letter == row["correct"]
        if correto: score += 1
        results_list.append({"topic": row["topic"], "correct": correto})

    percent = round((score / len(quiz)) * 100, 2)
    st.metric("Aproveitamento", f"{percent}%", delta=f"{score}/{len(quiz)} acertos")

    # Gráfico
    res_df = pd.DataFrame(results_list)
    performance = res_df.groupby("topic")["correct"].mean() * 100
    st.subheader("📉 Desempenho por Módulo")
    st.bar_chart(performance)

    # Revisão
    with st.expander("Ver Revisão Detalhada"):
        for idx, row in quiz.iterrows():
            user_choice = ans.get(idx)
            is_correct = next((l for l in ["A", "B", "C", "D"] if row[l] == user_choice), None) == row["correct"]
            
            st.write(f"**{idx+1}. {row['question']}**")
            if is_correct:
                st.success(f"Sua resposta: {user_choice}")
            else:
                st.error(f"Sua resposta: {user_choice}")
                st.info(f"Correta: ({row['correct']}) {row[row['correct']]}")
            st.markdown("---")

    if st.button("🔄 Reiniciar"):
        st.session_state.clear()
        st.rerun()
