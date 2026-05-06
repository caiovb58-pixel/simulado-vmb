import streamlit as st
import pandas as pd
import time
import os

# Configurações de página
st.set_page_config(page_title="VMB Invest - High Performance", layout="wide")

# =========================
# FUNÇÕES DE APOIO
# =========================
@st.cache_data(ttl=600)
def load_data():
    # Link direto CSV para evitar erros de conexão
    URL = "https://docs.google.com/spreadsheets/d/1l96APcdo8fX4GnR4kHqLskTjgU0UzdFehPp7bhhGP8k/gviz/tq?tqx=out:csv"
    try:
        return pd.read_csv(URL)
    except:
        return None

def mostrar_logo():
    # Tenta carregar a imagem com o nome exato do seu repositório
    logo_path = "vmb_logo_fundo_preto (1).png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=180)
    else:
        # Se a imagem falhar, mostra um título estilizado para não quebrar o app
        st.markdown("## 🏛️ VMB INVEST")

# =========================
# INICIALIZAÇÃO DO ESTADO (Persistence)
# =========================
if "page" not in st.session_state:
    st.session_state.update({
        "page": "login",
        "unlocked_advanced": False,
        "history": [],
        "current_q": 0,
        "answers": {},
        "quiz": None
    })

# =========================
# 1. TELA DE LOGIN (Design Limpo)
# =========================
if st.session_state.page == "login":
    _, col2, _ = st.columns([1, 1.5, 1])
    with col2:
        st.write("#") # Espaçamento
        mostrar_logo()
        st.title("Portal de Treinamento")
        with st.form("login_vmb"):
            user = st.text_input("Usuário").strip()
            password = st.text_input("Senha", type="password")
            if st.form_submit_button("Acessar Plataforma"):
                if user.lower() == "vmb" and password == "ancord2026":
                    st.session_state.page = "menu"
                    st.rerun()
                else:
                    st.error("Credenciais inválidas para este terminal.")

# =========================
# 2. MENU PRINCIPAL & EVOLUÇÃO
# =========================
elif st.session_state.page == "menu":
    st.title("🚀 Dashboard de Performance")
    df = load_data()
    
    if df is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            with st.container(border=True):
                st.subheader("📌 Nível 1: Certificação")
                st.write("Base técnica ANCORD e legislação.")
                if st.button("Iniciar Simulado 01", type="primary"):
                    st.session_state.quiz = df.sample(15).reset_index(drop=True)
                    st.session_state.page = "simulado"
                    st.rerun()

        with col2:
            with st.container(border=True):
                st.subheader("🏆 Nível 2: Private Advisor")
                if st.session_state.unlocked_advanced:
                    st.success("Acesso Liberado!")
                    if st.button("Iniciar Simulado Avançado"):
                        st.session_state.quiz = df.sample(25).reset_index(drop=True)
                        st.session_state.page = "simulado"
                        st.rerun()
                else:
                    st.markdown("🔒 **Bloqueado**")
                    st.caption("Alcance 70% no Nível 1 para desbloquear este módulo.")
                    st.button("Módulo Bloqueado", disabled=True)

    # Gráfico de Evolução (Mostra a melhora do SDR ao longo do tempo)
    if st.session_state.history:
        st.divider()
        st.subheader("📈 Curva de Aprendizado")
        h_df = pd.DataFrame(st.session_state.history)
        st.line_chart(h_df, x="Tentativa", y="Nota")

# =========================
# 3. TELA DE SIMULADO (Foco Total)
# =========================
elif st.session_state.page == "simulado":
    quiz = st.session_state.quiz
    i = st.session_state.current_q
    row = quiz.iloc[i]
    
    # Header do Simulado
    c1, c2 = st.columns([3, 1])
    c1.subheader(f"Questão {i+1} de {len(quiz)}")
    if c2.button("Sair", help="Abandona o simulado atual"):
        st.session_state.update({"page": "menu", "current_q": 0, "answers": {}})
        st.rerun()

    st.progress((i + 1) / len(quiz))
    
    with st.container(border=True):
        st.caption(f"Tópico: {row['topic']}")
        st.markdown(f"#### {row['question']}")
        
        options = [row["A"], row["B"], row["C"], row["D"]]
        # KEY única é o segredo para não dar erro de Node no React
        resp = st.radio("Escolha a alternativa:", options, 
                        index=options.index(st.session_state.answers[i]) if i in st.session_state.answers else None,
                        key=f"radio_q_{i}")
        
        if resp:
            st.session_state.answers[i] = resp

    st.write("#")
    nav1, nav2, nav3 = st.columns([1, 1, 1])
    with nav1:
        if i > 0 and st.button("⬅️ Anterior"):
            st.session_state.current_q -= 1
            st.rerun()
    with nav3:
        if i < len(quiz) - 1:
            if st.button("Próxima ➡️"):
                st.session_state.current_q += 1
                st.rerun()
        else:
            if st.button("🎯 Finalizar e Corrigir", type="primary"):
                st.session_state.page = "resultado"
                st.rerun()

# =========================
# 4. RESULTADOS
# =========================
elif st.session_state.page == "resultado":
    st.title("🎯 Resultado da Operação")
    quiz = st.session_state.quiz
    ans = st.session_state.answers
    
    acertos = 0
    for idx, row in quiz.iterrows():
        # Compara se o texto da resposta escolhida corresponde à letra correta na planilha
        if ans.get(idx) == row[row['correct']]:
            acertos += 1
            
    nota = round((acertos / len(quiz)) * 100, 1)
    st.session_state.history.append({"Tentativa": len(st.session_state.history)+1, "Nota": nota})
    
    col_r1, col_r2 = st.columns(2)
    col_r1.metric("Aproveitamento", f"{nota}%")
    col_r2.metric("Acertos", f"{acertos}/{len(quiz)}")

    if nota >= 70:
        st.balloons()
        st.success("META ATINGIDA! Você demonstrou proficiência técnica.")
        st.session_state.unlocked_advanced = True
    else:
        st.error("Abaixo da nota de corte. Revise os pontos fracos e tente novamente.")

    if st.button("Voltar ao Painel Principal"):
        st.session_state.update({"page": "menu", "current_q": 0, "answers": {}, "quiz": None})
        st.rerun()
