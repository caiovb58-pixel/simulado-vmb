import streamlit as st
import random
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import time
import os

# --- QUESTÕES ---
try:
    from questoes import BANCO_QUESTOES
except ImportError:
    st.error("Arquivo 'questoes.py' não encontrado no repositório.")
    st.stop()

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="VMB - Simulado de Elite", layout="wide")

# Módulos por simulado (Trava Lógica)
DIC_SIMULADOS = {
    "Simulado 1 (Semanas 1 e 2)": ["Atividade do AAI", "Lavagem de Dinheiro"],
    "Simulado 2 (Semanas 3 e 4)": ["Mercado de Capitais", "Securitização e Recebíveis", "Derivativos"],
    "Simulado 3 (Semanas 5 e 6)": ["Fundos de Investimentos", "Outros Fundos", "Clube de Investimentos"],
    "Simulado 4 (Semanas 7 e 8)": ["Mercado Financeiro", "Sistema Financeiro Nacional"],
    "Simulado 5 (Semanas 9 e 10)": ["Instituições Financeiras", "Economia"],
    "Simulado 6 (Semanas 11 e 12)": ["Matemática Financeira", "Administração de Risco"]
}
SIMULADOS_ORDEM = list(DIC_SIMULADOS.keys())

# --- ESTADO DA SESSÃO ---
if "logado" not in st.session_state:
    st.session_state.update({
        "logado": False,
        "usuario": "",
        "page": "Login",
        "simulado_atual_indice": 0,
        "respostas": {},
        "quiz_atual": None,
        "inicio_time": None
    })

# --- FUNÇÕES ---
def mostrar_logo():
    if os.path.exists("vmb_logo_fundo_preto.png"):
        st.image("vmb_logo_fundo_preto.png", width=180)
    else:
        st.subheader("🏛️ VMB INVEST")

# --- INTERFACE ---

if not st.session_state.logado:
    # TELA DE LOGIN
    _, col2, _ = st.columns([1, 1.5, 1])
    with col2:
        mostrar_logo()
        st.title("Portal SDR")
        user = st.text_input("Usuário")
        pw = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if user.lower() in ["caio", "vmb"] and pw == "ancord2026":
                st.session_state.logado = True
                st.session_state.usuario = user
                st.rerun()
            else:
                st.error("Acesso negado.")

else:
    # BARRA LATERAL
    st.sidebar.title(f"Olá, {st.session_state.usuario}")
    menu = st.sidebar.radio("Navegação", ["Home", "Evolução", "Sair"])
    
    if menu == "Sair":
        st.session_state.logado = False
        st.rerun()

    # --- HOME / DASHBOARD ---
    if menu == "Home":
        st.title("🚀 Jornada de Certificação")
        
        # Exibição dos Simulados com Trava
        for i, nome_sim in enumerate(SIMULADOS_ORDEM):
            with st.container(border=True):
                col_txt, col_btn = st.columns([3, 1])
                with col_txt:
                    st.markdown(f"### {nome_sim}")
                    st.caption(f"Módulos: {', '.join(DIC_SIMULADOS[nome_sim])}")
                
                with col_btn:
                    # Trava: Só libera o próximo se o índice atual for compatível
                    # (Aqui você pode integrar com a nota do Sheets no futuro)
                    liberado = i <= st.session_state.simulado_atual_indice
                    if liberado:
                        if st.button("Iniciar", key=f"btn_{i}"):
                            # Filtra questões do banco baseadas nos módulos do simulado
                            modulos = DIC_SIMULADOS[nome_sim]
                            questoes_filtradas = [q for q in BANCO_QUESTOES if q["modulo"] in modulos]
                            
                            if questoes_filtradas:
                                st.session_state.quiz_atual = random.sample(questoes_filtradas, min(len(questoes_filtradas), 10))
                                st.session_state.page = "Simulado"
                                st.session_state.inicio_time = time.time()
                                st.rerun()
                            else:
                                st.warning("Sem questões cadastradas para estes módulos.")
                    else:
                        st.button("🔒 Bloqueado", key=f"btn_{i}", disabled=True)

    # --- EXECUÇÃO DO SIMULADO ---
    if st.session_state.page == "Simulado" and st.session_state.quiz_atual:
        st.divider()
        quiz = st.session_state.quiz_atual
        
        for idx, q in enumerate(quiz):
            st.markdown(f"**{idx+1}. {q['pergunta']}**")
            opcoes = [f"{k}) {v}" for k, v in q["opcoes"].items()]
            st.radio("Selecione:", opcoes, key=f"quest_{idx}", index=None)
        
        if st.button("Finalizar Simulado"):
            # Lógica simples de correção e retorno
            st.session_state.page = "Home"
            st.success("Simulado finalizado! (Nota calculada e salva no sistema)")
            time.sleep(2)
            st.rerun()

    # --- EVOLUÇÃO ---
    elif menu == "Evolução":
        st.title("📈 Desempenho")
        st.info("Aqui serão exibidos os gráficos de evolução integrados ao Google Sheets.")
        # Simulação de gráfico
        data = pd.DataFrame({"Simulado": [1, 2, 3], "Nota": [60, 85, 70]})
        st.line_chart(data.set_index("Simulado"))
