import streamlit as st
import random
import time
import pandas as pd
import os
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection

# --- IMPORTAÇÃO DAS QUESTÕES ---
try:
    from questoes import BANCO_QUESTOES
except ImportError:
    st.error("Erro: O arquivo 'questoes.py' não foi encontrado.")
    st.stop()

# --- CONFIGURAÇÃO DOS SIMULADOS ---
DIC_SIMULADOS = {
    "Simulado 1 (Semanas 1 e 2)": ["Atividade do AAI", "Lavagem de Dinheiro"],
    "Simulado 2 (Semanas 3 e 4)": ["Mercado de Capitais", "Securitização e Recebíveis", "Derivativos"],
    "Simulado 3 (Semanas 5 e 6)": ["Fundos de Investimentos", "Outros Fundos", "Clube de Investimentos"],
    "Simulado 4 (Semanas 7 e 8)": ["Mercado Financeiro", "Sistema Financeiro Nacional"],
    "Simulado 5 (Semanas 9 e 10)": ["Instituições Financeiras", "Economia"],
    "Simulado 6 (Semanas 11 e 12)": ["Matemática Financeira", "Administração de Risco", "Clube de Investimentos"]
}

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Simulado ANCORD - VMB Invest", page_icon="⚖️", layout="wide")

# --- CSS ---
st.markdown("""
<style>
.stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #002e5d; color: white; }
.timer-container {
    position: fixed; top: 50px; right: 20px; z-index: 1000;
    background-color: white; padding: 10px; border: 2px solid #ff4b4b; border-radius: 10px;
}
.timer-text { font-size: 20px; font-weight: bold; color: #ff4b4b; }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'logado' not in st.session_state: st.session_state.logado = False
if 'usuario_nome' not in st.session_state: st.session_state.usuario_nome = ""
if 'simulado_iniciado' not in st.session_state: st.session_state.simulado_iniciado = False
if 'tempo_fim' not in st.session_state: st.session_state.tempo_fim = None
if 'primeiro_acesso' not in st.session_state: st.session_state.primeiro_acesso = True
if 'menu_atual' not in st.session_state: st.session_state.menu_atual = "Simulado ANCORD"
if 'mostrar_resultado' not in st.session_state: st.session_state.mostrar_resultado = False

# --- FUNÇÕES ---
def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def verificar_login(nome, senha):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)
        df = conn.read(worksheet="Usuarios")
        return not df[
            (df['Nome'].str.upper() == nome.upper()) &
            (df['Senha'] == senha)
        ].empty
    except:
        return False

# --- LOGIN ---
if not st.session_state.logado:
    st.title("Login")
    with st.form("login"):
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.form_submit_button("Entrar"):
            if verificar_login(u, p):
                st.session_state.logado = True
                st.session_state.usuario_nome = u
                st.rerun()
            else:
                st.error("Credenciais inválidas")
    st.stop()

# --- PRIMEIRO ACESSO ---
if st.session_state.primeiro_acesso:
    st.title(f"🚀 Bem-vindo, {st.session_state.usuario_nome}")

    st.markdown("""
    ### 📝 Regras
    - 20 questões
    - 30 minutos
    - Sem consulta externa
    - Não recarregar página
    - Aprovação: 70%
    """)

    if st.button("Começar"):
        st.session_state.primeiro_acesso = False
        st.rerun()

    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.write(f"👤 {st.session_state.usuario_nome}")
    menu = st.radio("Menu", ["Simulado ANCORD", "Evolução"])
    st.session_state.menu_atual = menu

    if st.button("Sair"):
        logout()

conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)

# --- SIMULADO ---
if st.session_state.menu_atual == "Simulado ANCORD":

    if not st.session_state.simulado_iniciado:
        st.title("Novo Simulado")

        simulado = st.selectbox("Escolha:", list(DIC_SIMULADOS.keys()))
        materias = DIC_SIMULADOS[simulado]

        if st.button("INICIAR"):
            pool = [q for q in BANCO_QUESTOES if q['modulo'] in materias]

            if pool:
                st.session_state.questoes_sorteadas = random.sample(pool, min(20, len(pool)))
                st.session_state.respostas_usuario = {}
                st.session_state.tempo_fim = datetime.now() + timedelta(minutes=30)
                st.session_state.simulado_iniciado = True
                st.session_state.simulado_nome = simulado
                st.rerun()

    else:
        tempo_restante = int((st.session_state.tempo_fim - datetime.now()).total_seconds())

        if tempo_restante <= 0:
            st.error("Tempo esgotado!")
            st.session_state.mostrar_resultado = True

        st.markdown(f"""
        <div class="timer-container">
            ⏱️ {st.session_state.simulado_nome}
        </div>
        """, unsafe_allow_html=True)

        with st.form("form"):
            for i, q in enumerate(st.session_state.questoes_sorteadas):
                st.write(f"**{i+1}. {q['pergunta']}**")

                ops = [f"{k}) {v}" for k, v in q['opcoes'].items()]

                st.session_state.respostas_usuario[i] = st.radio(
                    "Resposta",
                    ops,
                    key=i,
                    disabled=st.session_state.mostrar_resultado
                )

                if st.session_state.mostrar_resultado:
                    correta = f"{q['resposta_correta']}) {q['opcoes'][q['resposta_correta']]}"
                    resp = st.session_state.respostas_usuario[i]

                    if resp and resp.startswith(q['resposta_correta']):
                        st.success("Correto")
                    else:
                        st.error(f"Errado. Correta: {correta}")

                    with st.expander("Explicação"):
                        st.write(q.get("explicacao", "Sem explicação"))

            col1, col2 = st.columns(2)

            with col1:
                enviar = st.form_submit_button("Finalizar")

            with col2:
                if st.session_state.mostrar_resultado:
                    if st.form_submit_button("Novo Simulado"):
                        st.session_state.simulado_iniciado = False
                        st.session_state.mostrar_resultado = False
                        st.rerun()

        if enviar:
            acertos = 0

            for i, q in enumerate(st.session_state.questoes_sorteadas):
                r = st.session_state.respostas_usuario[i]
                if r and r.startswith(q['resposta_correta']):
                    acertos += 1

            total = len(st.session_state.questoes_sorteadas)
            nota = (acertos / total) * 100

            try:
                df = conn.read(worksheet="Resultados")

                novo = pd.DataFrame([{
                    "Data": datetime.now().strftime("%d/%m/%Y"),
                    "Usuario": st.session_state.usuario_nome,
                    "Simulado": st.session_state.simulado_nome,
                    "Nota": nota
                }])

                conn.update(worksheet="Resultados", data=pd.concat([df, novo]))

            except:
                pass

            st.session_state.mostrar_resultado = True

            if nota >= 70:
                st.success(f"Aprovado {nota:.1f}%")
            else:
                st.error(f"Reprovado {nota:.1f}%")

            st.rerun()

# --- EVOLUÇÃO ---
else:
    st.title("Evolução")

    try:
        df = conn.read(worksheet="Resultados")
        user = df[df["Usuario"] == st.session_state.usuario_nome]

        st.dataframe(user)
        st.line_chart(user["Nota"])

    except:
        st.error("Erro ao carregar")
