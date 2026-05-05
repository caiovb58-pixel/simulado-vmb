import streamlit as st
import random
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
import plotly.graph_objects as go

# --- CONFIG ---
st.set_page_config(page_title="Simulado ANCORD", layout="wide")

from questoes import BANCO_QUESTOES

# --- SIMULADOS ---
DIC_SIMULADOS = {
    "Simulado 1": ["Atividade do AAI", "Lavagem de Dinheiro"],
    "Simulado 2": ["Mercado de Capitais", "Securitização", "Derivativos"],
    "Simulado 3": ["Fundos", "Outros Fundos"],
    "Simulado 4": ["Mercado Financeiro", "SFN"],
    "Simulado 5": ["Instituições", "Economia"],
    "Simulado 6": ["Matemática Financeira", "Risco"]
}

SIMULADOS_ORDEM = list(DIC_SIMULADOS.keys())

# --- SESSION ---
if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.usuario = ""
    st.session_state.simulado_iniciado = False
    st.session_state.resultado_final = False

# --- CONEXÃO ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- LOGIN ---
def login(u, p):
    df = conn.read(worksheet="Usuarios")
    return not df[(df["Nome"] == u) & (df["Senha"] == p)].empty

if not st.session_state.logado:
    with st.form("login_form"):
        st.title("🔐 Login")
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")

        if st.form_submit_button("Entrar"):
            if login(u, p):
                st.session_state.logado = True
                st.session_state.usuario = u
                st.rerun()
            else:
                st.error("Erro no login")
    st.stop()

# --- MENU ---
menu = st.sidebar.radio("Menu", ["Simulado", "Evolução"])

# =========================
# 🚀 SIMULADO
# =========================
if menu == "Simulado":

    if not st.session_state.simulado_iniciado:

        st.title("Escolha o Simulado")

        for i, nome in enumerate(SIMULADOS_ORDEM):
            if st.button(nome, key=f"sim_{i}"):

                materias = DIC_SIMULADOS[nome]
                pool = [q for q in BANCO_QUESTOES if q["modulo"] in materias]

                st.session_state.questoes = random.sample(pool, min(20, len(pool)))
                st.session_state.respostas = {}
                st.session_state.tempo = datetime.now() + timedelta(minutes=30)
                st.session_state.simulado_nome = nome
                st.session_state.simulado_iniciado = True
                st.session_state.resultado_final = False

                st.rerun()

    elif not st.session_state.resultado_final:

        # ⏱️ TIMER PASSIVO (não quebra app)
        restante = int((st.session_state.tempo - datetime.now()).total_seconds())
        minutos, segundos = divmod(max(restante, 0), 60)

        st.info(f"⏱️ {minutos:02d}:{segundos:02d}")

        with st.form("form_prova"):
            for i, q in enumerate(st.session_state.questoes):

                st.markdown(f"**{i+1}. {q['pergunta']}**")

                opcoes = list(q["opcoes"].keys())

                resp = st.radio(
                    "Escolha:",
                    opcoes,
                    key=f"q_{i}",
                    index=None
                )

                if resp is not None:
                    st.session_state.respostas[i] = resp

            enviar = st.form_submit_button("Finalizar")

        if enviar or restante <= 0:
            st.session_state.resultado_final = True
            st.rerun()

    else:

        acertos = 0
        por_modulo = {}

        for i, q in enumerate(st.session_state.questoes):
            mod = q["modulo"]
            por_modulo.setdefault(mod, [0,0])
            por_modulo[mod][1] += 1

            if st.session_state.respostas.get(i) == q["resposta_correta"]:
                acertos += 1
                por_modulo[mod][0] += 1

        nota = (acertos / len(st.session_state.questoes)) * 100

        st.success(f"Nota: {nota:.1f}%")

        # --- RADAR ---
        categorias = list(por_modulo.keys())
        valores = [(v[0]/v[1])*100 for v in por_modulo.values()]

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=valores,
            theta=categorias,
            fill='toself'
        ))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0,100])),
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

        # --- SALVAR RESULTADO (ROBUSTO) ---
        try:
            df = conn.read(worksheet="Resultados")
            colunas = ["Usuario","Simulado","Nota","Data"]

            for col in colunas:
                if col not in df.columns:
                    df[col] = None

            df = df[colunas]

        except:
            df = pd.DataFrame(columns=["Usuario","Simulado","Nota","Data"])

        novo = pd.DataFrame([{
            "Usuario": st.session_state.usuario,
            "Simulado": st.session_state.simulado_nome,
            "Nota": nota,
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M")
        }])

        df_final = pd.concat([df, novo], ignore_index=True)

        conn.update(
            worksheet="Resultados",
            data=df_final
        )

        if st.button("Refazer / Novo Simulado"):
            st.session_state.simulado_iniciado = False
            st.session_state.resultado_final = False
            st.rerun()

# =========================
# 📊 EVOLUÇÃO
# =========================
elif menu == "Evolução":

    df = conn.read(worksheet="Resultados")
    user = df[df["Usuario"] == st.session_state.usuario]

    if not user.empty:
        st.title("Sua evolução")
        st.line_chart(user["Nota"])
    else:
        st.info("Sem dados ainda")
