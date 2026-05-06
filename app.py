import streamlit as st
import pandas as pd
import time

# Configurações iniciais
st.set_page_config(page_title="Portal VMB - Simulado ANCORD", layout="wide")

# =========================
# FUNÇÕES DE APOIO
# =========================
@st.cache_data(ttl=600)
def load_data(url):
    try:
        if "edit" in url:
            url = url.replace("edit", "export?format=csv")
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Erro ao conectar com a planilha: {e}")
        return None

# =========================
# ESTADO DO SISTEMA
# =========================
if "page" not in st.session_state:
    st.session_state.update({
        "page": "login",
        "user_authenticated": False,
        "history": [], # Para mostrar evolução
        "unlocked_advanced": False, # Trava de segurança
        "answers": {},
        "current_q": 0,
        "quiz": None
    })

# =========================
# 1. TELA DE LOGIN
# =========================
if st.session_state.page == "login":
    st.title("🔐 Acesso Restrito - VMB Invest")
    with st.container(border=True):
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            # Lógica simples de login para a equipe
            if usuario.lower() == "vmb" and senha == "ancord2026":
                st.session_state.user_authenticated = True
                st.session_state.page = "boas_vindas"
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

# =========================
# 2. TELA DE BOAS-VINDAS
# =========================
elif st.session_state.page == "boas_vindas":
    st.title("👋 Bem-vindo ao Treinamento ANCORD")
    st.write("Selecione o nível do seu simulado abaixo.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📌 Nível 1: Fundamentos")
        st.write("Módulos básicos para certificação.")
        if st.button("Iniciar Nível 1"):
            st.session_state.page = "config_simulado"
            st.session_state.current_level = "Nível 1"
            st.rerun()
            
    with col2:
        st.subheader("🚀 Nível 2: Avançado")
        if st.session_state.unlocked_advanced:
            st.write("✅ Desbloqueado! Pronto para o próximo passo.")
            if st.button("Iniciar Nível 2"):
                st.session_state.page = "config_simulado"
                st.session_state.current_level = "Nível 2"
                st.rerun()
        else:
            st.warning("🔒 Bloqueado: Atinja 70% no Nível 1 para liberar.")
            st.button("Iniciar Nível 2", disabled=True)

    if st.session_state.history:
        st.divider()
        st.subheader("📈 Sua Evolução")
        hist_df = pd.DataFrame(st.session_state.history)
        st.line_chart(hist_df.set_index("Data")["Nota"])

# =========================
# 3. CONFIGURAÇÃO E SIMULADO
# =========================
elif st.session_state.page == "config_simulado":
    st.header(f"Configurando {st.session_state.current_level}")
    url = "https://docs.google.com/spreadsheets/d/1l96APcdo8fX4GnR4kHqLskTjgU0UzdFehPp7bhhGP8k/export?format=csv"
    df = load_data(url)
    
    if df is not None:
        qtd = st.slider("Quantidade de questões", 5, 20, 10)
        if st.button("Começar Agora"):
            st.session_state.quiz = df.sample(n=qtd).reset_index(drop=True)
            st.session_state.page = "executando_simulado"
            st.session_state.start_time = time.time()
            st.rerun()

elif st.session_state.page == "executando_simulado":
    quiz = st.session_state.quiz
    i = st.session_state.current_q
    row = quiz.iloc[i]
    
    st.caption(f"Questão {i+1} de {len(quiz)} | {st.session_state.current_level}")
    st.progress((i + 1) / len(quiz))
    
    st.write(f"### {row['question']}")
    
    options = [row["A"], row["B"], row["C"], row["D"]]
    res_anterior = st.session_state.answers.get(i)
    
    escolha = st.radio("Selecione:", options, 
                      index=options.index(res_anterior) if res_anterior else None,
                      key=f"q_{i}")
    
    if escolha:
        st.session_state.answers[i] = escolha

    c1, c2, c3 = st.columns(3)
    with c1:
        if i > 0 and st.button("⬅️"): st.session_state.current_q -= 1; st.rerun()
    with c2:
        if i < len(quiz) - 1 and st.button("➡️"): st.session_state.current_q += 1; st.rerun()
    with c3:
        if st.button("✅ Finalizar"):
            st.session_state.page = "resultados"
            st.rerun()

# =========================
# 4. RESULTADOS E EVOLUÇÃO
# =========================
elif st.session_state.page == "resultados":
    st.title("🎯 Resultados")
    quiz = st.session_state.quiz
    ans = st.session_state.answers
    
    acertos = 0
    for idx, row in quiz.iterrows():
        user_val = ans.get(idx)
        letra_user = next((l for l in ["A", "B", "C", "D"] if row[l] == user_val), None)
        if letra_user == row["correct"]: acertos += 1
        
    nota = round((acertos / len(quiz)) * 100, 1)
    
    # Lógica de Desbloqueio
    if nota >= 70:
        st.success(f"Excelente! Nota: {nota}%")
        st.session_state.unlocked_advanced = True
    else:
        st.error(f"Nota: {nota}%. Você precisa de 70% para liberar o nível avançado.")

    # Salva no histórico para o gráfico de evolução
    st.session_state.history.append({"Data": time.strftime("%H:%M:%S"), "Nota": nota})
    
    if st.button("Voltar ao Início"):
        # Reseta dados do simulado atual, mas mantém histórico e desbloqueio
        st.session_state.update({"page": "boas_vindas", "answers": {}, "current_q": 0, "quiz": None})
        st.rerun()
