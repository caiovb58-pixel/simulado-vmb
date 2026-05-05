import streamlit as st
import random
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
import matplotlib.pyplot as plt
import numpy as np

# --- CONFIG ---
st.set_page_config(page_title="Simulado ANCORD", layout="wide")

ADMINS = ["Caio", "Admin"]

from questoes import BANCO_QUESTOES

# --- SIMULADOS ---
DIC_SIMULADOS = {
    "Simulado 1 (Semanas 1 e 2)": ["Atividade do AAI", "Lavagem de Dinheiro"],
    "Simulado 2 (Semanas 3 e 4)": ["Mercado de Capitais", "Securitização e Recebíveis", "Derivativos"],
    "Simulado 3 (Semanas 5 e 6)": ["Fundos de Investimentos", "Outros Fundos", "Clube de Investimentos"],
    "Simulado 4 (Semanas 7 e 8)": ["Mercado Financeiro", "Sistema Financeiro Nacional"],
    "Simulado 5 (Semanas 9 e 10)": ["Instituições Financeiras", "Economia"],
    "Simulado 6 (Semanas 11 e 12)": ["Matemática Financeira", "Administração de Risco", "Clube de Investimentos"]
}

SIMULADOS_ORDEM = list(DIC_SIMULADOS.keys())

# --- SESSION ---
defaults = {
    "logado": False,
    "simulado_iniciado": False,
    "tempo": None,
    "usuario": "",
    "simulado_atual_indice": 0,
    "inicio_prova": None
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- CONEXÃO ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- PROGRESSO ---
def carregar_progresso(usuario):
    try:
        df = conn.read(worksheet="Progresso")
        user = df[df["Usuario"] == usuario]
        if not user.empty:
            return int(user.iloc[0]["Simulado_Atual"])
        return 0
    except:
        return 0

def salvar_progresso(usuario, indice, status):
    try:
        df = conn.read(worksheet="Progresso")

        if usuario in df["Usuario"].values:
            df.loc[df["Usuario"] == usuario, "Simulado_Atual"] = indice
            df.loc[df["Usuario"] == usuario, "Ultimo_Status"] = status
        else:
            novo = pd.DataFrame([{
                "Usuario": usuario,
                "Simulado_Atual": indice,
                "Ultimo_Status": status
            }])
            df = pd.concat([df, novo], ignore_index=True)

        conn.update(worksheet="Progresso", data=df)
    except:
        pass

# --- LOGIN ---
def login(u, p):
    df = conn.read(worksheet="Usuarios")
    return not df[(df["Nome"] == u) & (df["Senha"] == p)].empty

if not st.session_state.logado:
    with st.form("login"):
        st.title("🔐 Acesso ao Simulado")
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")

        if st.form_submit_button("Entrar"):
            if login(u, p):
                st.session_state.logado = True
                st.session_state.usuario = u
                st.session_state.simulado_atual_indice = carregar_progresso(u)
                st.rerun()
            else:
                st.error("Credenciais inválidas")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.write(f"👤 {st.session_state.usuario}")

    menu = st.radio("Menu", ["Simulado", "Evolução"] + (["Admin"] if st.session_state.usuario in ADMINS else []))

    if st.button("🚪 Sair"):
        st.session_state.clear()
        st.rerun()

# --- BOAS VINDAS ---
if "primeiro" not in st.session_state:

    st.image("vmb_logo_fundo_preto.png", use_container_width=True)

    st.title("Simulado ANCORD - VMB Invest")

    st.markdown("""
    ### 🎯 Objetivo
    Simular a prova ANCORD em nível profissional.

    ### 📋 Estrutura
    - 20 questões  
    - Tempo: 30 minutos  

    ### ⚠️ Regras
    - Não consultar material  
    - Não atualizar a página  
    - Foco total  

    ### 🏆 Aprovação
    - 70% ou mais  

    ---
    💬 **"Disciplina hoje, liberdade amanhã."**
    """)

    if st.button("🔥 Começar"):
        st.session_state.primeiro = False
        st.rerun()

    st.stop()

# --- SIMULADO ---
if menu == "Simulado":

    progresso = st.session_state.simulado_atual_indice
    total = len(SIMULADOS_ORDEM)

    st.progress(progresso / total)
    st.write(f"Progresso: {progresso}/{total}")

    for i, nome in enumerate(SIMULADOS_ORDEM):
        if i <= progresso:
            if st.button(f"✅ {nome}", key=f"sim_{i}"):
                st.session_state.simulado_escolhido = i
                st.session_state.simulado_iniciado = False
                st.rerun()
        else:
            st.button(f"🔒 {nome}", disabled=True)

    if "simulado_escolhido" in st.session_state:

        indice = st.session_state.simulado_escolhido
        sim_atual = SIMULADOS_ORDEM[indice]

        if not st.session_state.simulado_iniciado:

            if st.button("Iniciar Simulado"):

                materias = DIC_SIMULADOS[sim_atual]
                pool = [q for q in BANCO_QUESTOES if q["modulo"] in materias]

                st.session_state.questoes = random.sample(pool, min(20, len(pool)))
                st.session_state.respostas = {}
                st.session_state.tempo = datetime.now() + timedelta(minutes=30)
                st.session_state.inicio_prova = datetime.now()
                st.session_state.simulado_iniciado = True
                st.rerun()

        else:
            restante = int((st.session_state.tempo - datetime.now()).total_seconds())
            minutos, segundos = divmod(max(restante, 0), 60)

            st.info(f"⏱️ {minutos:02d}:{segundos:02d}")

            with st.form("form"):
                for i, q in enumerate(st.session_state.questoes):

                    st.markdown(f"**{i+1}. {q['pergunta']}**")

                    opcoes_map = {f"{k}) {v}": k for k,v in q["opcoes"].items()}

                    resp = st.radio(
                        "Resposta:",
                        list(opcoes_map.keys()),
                        key=f"q{i}",
                        index=None
                    )

                    if resp:
                        st.session_state.respostas[i] = opcoes_map[resp]

                enviar = st.form_submit_button("Finalizar")

            if enviar or restante <= 0:

                tempo_total = (datetime.now() - st.session_state.inicio_prova).total_seconds()
                tempo_medio = tempo_total / len(st.session_state.questoes)

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
                status = "Aprovado" if nota >= 70 else "Reprovado"

                st.success(f"Nota: {nota:.1f}%")
                st.write(f"⏱️ Tempo médio por questão: {tempo_medio:.1f}s")

                # --- RADAR CHART REAL ---
                if por_modulo:
                    st.subheader("🎯 Radar de Performance")

                    categorias = list(por_modulo.keys())
                    valores = [(v[0]/v[1])*100 for v in por_modulo.values()]

                    valores += valores[:1]
                    categorias += categorias[:1]

                    angulos = np.linspace(0, 2*np.pi, len(categorias), endpoint=True)

                    fig, ax = plt.subplots(subplot_kw=dict(polar=True))
                    ax.plot(angulos, valores)
                    ax.fill(angulos, valores, alpha=0.1)

                    ax.set_xticks(angulos)
                    ax.set_xticklabels(categorias)

                    ax.set_yticks([20,40,60,80,100])
                    ax.set_yticklabels(["20","40","60","80","100"])

                    st.pyplot(fig)

                # --- SALVAR RESULTADO ---
                try:
                    df_res = conn.read(worksheet="Resultados")
                except:
                    df_res = pd.DataFrame(columns=["Usuario","Simulado","Nota","Tempo_medio","Data"])

                novo = pd.DataFrame([{
                    "Usuario": st.session_state.usuario,
                    "Simulado": sim_atual,
                    "Nota": nota,
                    "Tempo_medio": tempo_medio,
                    "Data": datetime.now().strftime("%d/%m/%Y %H:%M")
                }])

                df_final = pd.concat([df_res, novo], ignore_index=True)

                conn.update(worksheet="Resultados", data=df_final)

                # progresso
                novo_idx = progresso
                if status == "Aprovado" and indice == progresso:
                    novo_idx += 1

                salvar_progresso(st.session_state.usuario, novo_idx, status)
                st.session_state.simulado_atual_indice = novo_idx
                st.session_state.simulado_iniciado = False
                st.rerun()

# --- EVOLUÇÃO ---
elif menu == "Evolução":

    st.title("📊 Sua Evolução")

    df = conn.read(worksheet="Resultados")
    user = df[df["Usuario"] == st.session_state.usuario]

    if not user.empty:
        st.line_chart(user["Nota"])

        if "Tempo_medio" in user.columns:
            st.line_chart(user["Tempo_medio"])
    else:
        st.info("Nenhum dado ainda.")

# --- ADMIN ---
elif menu == "Admin":
    if st.session_state.usuario not in ADMINS:
        st.error("Acesso restrito")
        st.stop()

    st.dataframe(conn.read(worksheet="Resultados"))
