import streamlit as st
import random
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
import time

# --- QUESTÕES ---
try:
    from questoes import BANCO_QUESTOES
except ImportError:
    st.error("Arquivo 'questoes.py' não encontrado.")
    st.stop()

# --- CONFIG ---
st.set_page_config(page_title="Simulado ANCORD", layout="wide")

# --- ADMINS ---
ADMINS = ["Caio", "Admin"]

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
    "mostrar_resultado": False,
    "tempo": None,
    "usuario": "",
    "simulado_atual_indice": 0
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

        if "Usuario" not in df.columns:
            df = pd.DataFrame(columns=["Usuario","Simulado_Atual","Ultimo_Status","Atualizado_em"])

        if usuario in df["Usuario"].values:
            df.loc[df["Usuario"] == usuario, "Simulado_Atual"] = indice
            df.loc[df["Usuario"] == usuario, "Ultimo_Status"] = status
            df.loc[df["Usuario"] == usuario, "Atualizado_em"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        else:
            novo = pd.DataFrame([{
                "Usuario": usuario,
                "Simulado_Atual": indice,
                "Ultimo_Status": status,
                "Atualizado_em": datetime.now().strftime("%d/%m/%Y %H:%M")
            }])
            df = pd.concat([df, novo], ignore_index=True)

        conn.update(worksheet="Progresso", data=df)

    except Exception as e:
        st.error(f"Erro ao salvar progresso: {e}")

# --- LOGOUT ---
def logout():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

# --- LOGIN ---
def login(u, p):
    try:
        df = conn.read(worksheet="Usuarios")
        return not df[(df["Nome"] == u) & (df["Senha"] == p)].empty
    except:
        return False

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

    menu_opcoes = ["Simulado", "Evolução"]
    if st.session_state.usuario in ADMINS:
        menu_opcoes.append("Admin")

    menu = st.radio("Menu", menu_opcoes)

    if st.button("🚪 Sair"):
        logout()

# --- BOAS VINDAS ---
if "primeiro" not in st.session_state:
    st.title("🚀 Simulado ANCORD - Preparação Profissional")

    st.markdown("""
    ### 🎯 Objetivo
    Simular a prova real ANCORD com alto nível de exigência.

    ### 📋 Estrutura
    - Até 20 questões
    - Tempo: 30 minutos
    - Baseado no plano de 12 semanas

    ### ⚠️ Regras
    - Sem consulta externa
    - Não atualizar página
    - Foco total

    ### 🏆 Aprovação
    - 70% ou mais

    ---
    ### 💬 Mentalidade
    > "Disciplina supera motivação."
    """)

    if st.button("🔥 Começar"):
        st.session_state.primeiro = False
        st.rerun()

    st.stop()

# --- SIMULADO ---
if menu == "Simulado":

    st.title("Escolha seu Simulado")

    progresso = st.session_state.simulado_atual_indice
    total_simulados = len(SIMULADOS_ORDEM)

    # 🔥 BARRA DE PROGRESSO
    st.progress(progresso / total_simulados)
    st.write(f"Progresso: {progresso}/{total_simulados} simulados concluídos")

    st.markdown("---")

    # 🔥 LISTA COM BLOQUEIO
    for i, nome in enumerate(SIMULADOS_ORDEM):

        if i <= progresso:
            if st.button(f"✅ {nome}", key=f"sim_{i}"):
                st.session_state.simulado_escolhido = i
                st.session_state.simulado_iniciado = False
                st.rerun()
        else:
            st.button(f"🔒 {nome}", disabled=True)

    # --- INICIAR SIMULADO ---
    if "simulado_escolhido" in st.session_state:

        indice = st.session_state.simulado_escolhido
        sim_atual = SIMULADOS_ORDEM[indice]

        if not st.session_state.simulado_iniciado:

            st.subheader(f"Iniciar: {sim_atual}")

            if st.button("Iniciar Simulado"):
                materias = DIC_SIMULADOS[sim_atual]
                pool = [q for q in BANCO_QUESTOES if q["modulo"] in materias]

                qtd = min(20, len(pool))

                st.session_state.questoes = random.sample(pool, qtd)
                st.session_state.respostas = {}
                st.session_state.tempo = datetime.now() + timedelta(minutes=30)
                st.session_state.simulado_nome = sim_atual
                st.session_state.simulado_iniciado = True
                st.session_state.mostrar_resultado = False
                st.rerun()

        else:
            restante = int((st.session_state.tempo - datetime.now()).total_seconds())

            if restante <= 0:
                st.session_state.mostrar_resultado = True
                restante = 0

            minutos, segundos = divmod(restante, 60)
            st.info(f"⏱️ Tempo restante: {minutos:02d}:{segundos:02d}")

            with st.form("form"):
                for i, q in enumerate(st.session_state.questoes):

                    st.markdown(f"**{i+1}. {q['pergunta']}**")

                    opcoes_map = {f"{k}) {v}": k for k, v in q["opcoes"].items()}
                    resposta = st.radio("Resposta:", list(opcoes_map.keys()), key=f"q{i}", index=None)

                    if resposta:
                        st.session_state.respostas[i] = opcoes_map[resposta]

                    st.markdown("---")

                enviar = st.form_submit_button("Finalizar Simulado")

            if not st.session_state.mostrar_resultado and not enviar:
                time.sleep(1)
                st.rerun()

            if enviar or restante == 0:

                acertos = sum(
                    1 for i, q in enumerate(st.session_state.questoes)
                    if st.session_state.respostas.get(i) == q["resposta_correta"]
                )

                total = len(st.session_state.questoes)
                nota = (acertos / total) * 100 if total else 0
                status = "Aprovado" if nota >= 70 else "Reprovado"

                # salvar resultado
                try:
                    df = conn.read(worksheet="Resultados")

                    novo = pd.DataFrame([{
                        "Usuario": st.session_state.usuario,
                        "Simulado": st.session_state.simulado_nome,
                        "Nota": nota,
                        "Status": status,
                        "Data": datetime.now().strftime("%d/%m/%Y %H:%M")
                    }])

                    conn.update(worksheet="Resultados", data=pd.concat([df, novo]))
                except:
                    pass

                # progresso
                novo_indice = progresso
                if status == "Aprovado" and indice == progresso:
                    novo_indice += 1

                salvar_progresso(st.session_state.usuario, novo_indice, status)
                st.session_state.simulado_atual_indice = novo_indice

                st.success(f"Nota: {nota:.1f}%")
                st.markdown(f"### Status: {status}")

                st.session_state.simulado_iniciado = False

# --- EVOLUÇÃO ---
elif menu == "Evolução":
    st.title("Meu Desempenho")

    try:
        df = conn.read(worksheet="Resultados")
        user = df[df["Usuario"] == st.session_state.usuario]

        st.dataframe(user.sort_values(by="Data", ascending=False))
        st.line_chart(user["Nota"])
    except:
        st.error("Erro ao carregar dados")

# --- ADMIN ---
elif menu == "Admin":

    if st.session_state.usuario not in ADMINS:
        st.error("Acesso restrito.")
        st.stop()

    st.title("📊 Dashboard Admin")

    df = conn.read(worksheet="Resultados")
    st.dataframe(df)

    st.subheader("Média por usuário")
    st.dataframe(df.groupby("Usuario")["Nota"].mean())
