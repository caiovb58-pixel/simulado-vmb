import streamlit as st
import pandas as pd
import time

# Configuração da página
st.set_page_config(page_title="Simulado ANCORD - VMB Invest", layout="wide")

# =========================
# FUNÇÕES DE DADOS
# =========================
@st.cache_data
def load_data():
    # Link da sua planilha formatado para exportação CSV
    SHEET_ID = "1l96APcdo8fX4GnR4kHqLskTjgU0UzdFehPp7bhhGP8k"
    URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"
    try:
        df = pd.read_csv(URL)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar planilha: {e}")
        return None

# =========================
# INICIALIZAÇÃO DO ESTADO
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
df = load_data()

if df is not None and not st.session_state.started:
    st.title("📊 Portal de Treinamento ANCORD")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Configurações do Simulado")
        temas = ["Todos"] + sorted(df["topic"].unique().tolist())
        tema_selecionado = st.selectbox("Selecione o Módulo:", temas)
        
        # Filtro dinâmico para quantidade máxima
        max_questoes = len(df) if tema_selecionado == "Todos" else len(df[df["topic"] == tema_selecionado])
        qtd = st.slider("Quantidade de questões:", 5, min(max_questoes, 50), min(10, max_questoes))

    if st.button("🚀 Iniciar Simulado"):
        if tema_selecionado == "Todos":
            quiz = df.sample(n=qtd)
        else:
            quiz = df[df["topic"] == tema_selecionado].sample(n=qtd)
            
        st.session_state.quiz = quiz.reset_index(drop=True)
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

    # Barra lateral de progresso
    with st.sidebar:
        st.header("Progresso")
        st.progress((i + 1) / total)
        st.write(f"Questão {i+1} de {total}")
        
        if st.button("❌ Abandonar Simulado"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()

    st.subheader(f"Módulo: {row['topic']}")
    st.info(row["question"])

    options = [row["A"], row["B"], row["C"], row["D"]]
    labels = ["A", "B", "C", "D"]
    
    # Mapeamento para salvar apenas a letra (A, B, C ou D)
    current_ans = st.session_state.answers.get(i, None)
    
    selection = st.radio(
        "Selecione a alternativa correta:",
        options,
        index=options.index(current_ans) if current_ans in options else None,
        key=f"q_{i}"
    )

    if selection:
        st.session_state.answers[i] = selection

    st.markdown("---")
    c1, c2, c3 = st.columns([1, 1, 1])
    
    with c1:
        if i > 0 and st.button("⬅️ Anterior"):
            st.session_state.current_q -= 1
            st.rerun()
    
    with c2:
        if i < total - 1:
            if st.button("Próxima ➡️"):
                st.session_state.current_q += 1
                st.rerun()
    
    with c3:
        if st.button("✅ Finalizar Simulado"):
            if len(st.session_state.answers) < total:
                st.warning("Responda todas as questões antes de finalizar!")
            else:
                st.session_state.finished = True
                st.rerun()

# =========================
# TELA DE RESULTADOS
# =========================
if st.session_state.finished:
    st.title("🎯 Resultado Final")
    
    quiz = st.session_state.quiz
    ans = st.session_state.answers
    
    # Cálculo de Acertos
    score = 0
    detailed_results = []
    for idx, row in quiz.iterrows():
        user_val = ans.get(idx)
        # Identifica a letra da resposta do usuário baseada no texto selecionado
        user_letter = "A" if user_val == row["A"] else "B" if user_val == row["B"] else "C" if user_val == row["C"] else "D"
        
        is_correct = user_letter == row["correct"]
        if is_correct: score += 1
        
        detailed_results.append({
            "topic": row["topic"],
            "status": is_correct
        })

    percent = round((score / len(quiz)) * 100, 1)
    
    col_r1, col_r2 = st.columns(2)
    col_r1.metric("Acertos", f"{score}/{len(quiz)}")
    col_r2.metric("Aproveitamento", f"{percent}%")

    if percent >= 70:
        st.success("Parabéns! Você atingiu a nota de corte da ANCORD (70%).")
    else:
        st.error("Atenção: Você precisa de no mínimo 70% de acertos para aprovação.")

    # Gráfico de Desempenho por Tema
    st.subheader("📊 Desempenho por Módulo")
    res_df = pd.DataFrame(detailed_results)
    perf_tema = res_df.groupby("topic")["status"].mean() * 100
    st.bar_chart(perf_tema)

    # Revisão das Questões
    st.subheader("📋 Revisão Detalhada")
    for idx, row in quiz.iterrows():
        user_val = ans.get(idx)
        correct_letter = row["correct"]
        correct_text = row[correct_letter]
        
        with st.expander(f"Questão {idx+1} - {row['topic']} {'✔️' if user_val == correct_text else '❌'}"):
            st.write(f"**Pergunta:** {row['question']}")
            st.write(f"**Sua resposta:** {user_val}")
            st.write(f"**Resposta correta:** ({correct_letter}) {correct_text}")
            if "explanation" in row and pd.notna(row["explanation"]):
                st.info(f"**Explicação:** {row['explanation']}")

    if st.button("🔄 Novo Simulado"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
