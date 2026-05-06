import streamlit as st
import pandas as pd
import time

# Configurações de página para um visual profissional
st.set_page_config(page_title="VMB Invest - Portal de Treinamento", layout="wide")

# =========================
# ESTILIZAÇÃO E ASSETS
# =========================
def aplicar_estilo():
    st.markdown("""
        <style>
        .main { background-color: #0e1117; }
        .stButton>button { width: 100%; border-radius: 5px; height: 3em; font-weight: bold; }
        .stProgress > div > div > div > div { background-color: #1c83e1; }
        </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=600)
def load_data():
    # Link direto da sua planilha de questões
    URL = "https://docs.google.com/spreadsheets/d/1l96APcdo8fX4GnR4kHqLskTjgU0UzdFehPp7bhhGP8k/gviz/tq?tqx=out:csv"
    try:
        return pd.read_csv(URL)
    except:
        return None

# =========================
# INICIALIZAÇÃO DO ESTADO
# =========================
if "page" not in st.session_state:
    st.session_state.update({
        "page": "login",
        "authenticated": False,
        "unlocked_level_2": False,
        "history": [],
        "current_q": 0,
        "answers": {},
        "quiz": None
    })

aplicar_estilo()
df = load_data()

# =========================
# LÓGICA DE NAVEGAÇÃO
# =========================

# 1. TELA DE LOGIN
if st.session_state.page == "login":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("vmb_logo_fundo_preto (1).png", width=200) # Se o arquivo existir no seu GitHub
        st.title("Acesso ao Portal SDR")
        with st.form("login_form"):
            user = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            if st.form_submit_button("Entrar"):
                if user.lower() == "vmb" and password == "ancord2026":
                    st.session_state.authenticated = True
                    st.session_state.page = "boas_vindas"
                    st.rerun()
                else:
                    st.error("Credenciais inválidas.")

# 2. TELA DE BOAS-VINDAS E MENU
elif st.session_state.page == "boas_vindas":
    st.title("🚀 Bem-vindo ao Treinamento de Alta Performance")
    st.subheader("Escolha seu desafio de hoje:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 📘 Nível 1: Certificação ANCORD")
            st.write("Foco em legislação, módulos básicos e operacional.")
            if st.button("Iniciar Simulado Nível 1"):
                st.session_state.quiz = df.sample(10).reset_index(drop=True) # Exemplo de 10 questões
                st.session_state.page = "simulado"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown("### 🏆 Nível 2: Especialista VMB")
            if st.session_state.unlocked_level_2:
                st.success("✅ Acesso Liberado!")
                if st.button("Iniciar Simulado Nível 2"):
                    st.session_state.quiz = df.sample(20).reset_index(drop=True)
                    st.session_state.page = "simulado"
                    st.rerun()
            else:
                st.markdown("🔒 **Bloqueado**")
                st.info("Atinja 70% de acerto no Nível 1 para desbloquear.")
                st.button("Iniciar Simulado Nível 2", disabled=True)

    # Gráfico de Evolução
    if st.session_state.history:
        st.divider()
        st.subheader("📈 Sua Evolução")
        hist_df = pd.DataFrame(st.session_state.history)
        st.line_chart(hist_df.set_index("Tentativa")["Nota"])

# 3. TELA DO SIMULADO
elif st.session_state.page == "simulado":
    quiz = st.session_state.quiz
    i = st.session_state.current_q
    row = quiz.iloc[i]
    
    st.sidebar.title("Progresso")
    st.sidebar.progress((i + 1) / len(quiz))
    st.sidebar.write(f"Questão {i+1} de {len(quiz)}")
    
    if st.sidebar.button("Abandonar Simulado"):
        st.session_state.page = "boas_vindas"
        st.session_state.current_q = 0
        st.session_state.answers = {}
        st.rerun()

    with st.container(border=True):
        st.caption(f"Módulo: {row['topic']}")
        st.markdown(f"#### {row['question']}")
        
        options = [row["A"], row["B"], row["C"], row["D"]]
        prev_ans = st.session_state.answers.get(i)
        
        # KEY ÚNICA para evitar erro de renderização
        escolha = st.radio("Selecione a alternativa correta:", options, 
                          index=options.index(prev_ans) if prev_ans else None,
                          key=f"radio_{i}")
        
        if escolha:
            st.session_state.answers[i] = escolha

    st.write("")
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if i > 0 and st.button("⬅️ Anterior"):
            st.session_state.current_q -= 1
            st.rerun()
    with c2:
        if i < len(quiz) - 1:
            if st.button("Próxima ➡️"):
                st.session_state.current_q += 1
                st.rerun()
    with c3:
        if st.button("✅ Finalizar"):
            st.session_state.page = "resultados"
            st.rerun()

# 4. TELA DE RESULTADOS
elif st.session_state.page == "resultados":
    st.title("🎯 Resultado do Simulado")
    quiz = st.session_state.quiz
    ans = st.session_state.answers
    
    acertos = 0
    for idx, row in quiz.iterrows():
        user_val = ans.get(idx)
        letra = next((l for l in ["A", "B", "C", "D"] if row[l] == user_val), None)
        if letra == row["correct"]:
            acertos += 1
            
    nota = (acertos / len(quiz)) * 100
    
    col_n1, col_n2 = st.columns(2)
    col_n1.metric("Sua Nota", f"{nota}%")
    col_n2.metric("Acertos", f"{acertos}/{len(quiz)}")

    if nota >= 70:
        st.balloons()
        st.success("Parabéns! Você atingiu a meta.")
        st.session_state.unlocked_level_2 = True
    else:
        st.warning("Continue estudando! Você precisa de 70% para o Nível 2.")

    # Registra no histórico
    tentativa_num = len(st.session_state.history) + 1
    st.session_state.history.append({"Tentativa": tentativa_num, "Nota": nota})
    
    if st.button("Voltar ao Menu Principal"):
        st.session_state.update({"page": "boas_vindas", "current_q": 0, "answers": {}, "quiz": None})
        st.rerun()
