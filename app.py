import streamlit as st
import random
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection

# --- QUESTÕES ---
try:
    from questoes import BANCO_QUESTOES
except ImportError:
    st.error("Arquivo 'questoes.py' não encontrado.")
    st.stop()

# --- CONFIG ---
st.set_page_config(page_title="Simulado ANCORD", layout="wide")

# --- SIMULADOS (12 SEMANAS) ---
DIC_SIMULADOS = {
    "Simulado 1 (Semanas 1 e 2)": ["Atividade do AAI", "Lavagem de Dinheiro"],
    "Simulado 2 (Semanas 3 e 4)": ["Mercado de Capitais", "Securitização e Recebíveis", "Derivativos"],
    "Simulado 3 (Semanas 5 e 6)": ["Fundos de Investimentos", "Outros Fundos", "Clube de Investimentos"],
    "Simulado 4 (Semanas 7 e 8)": ["Mercado Financeiro", "Sistema Financeiro Nacional"],
    "Simulado 5 (Semanas 9 e 10)": ["Instituições Financeiras", "Economia"],
    "Simulado 6 (Semanas 11 e 12)": ["Matemática Financeira", "Administração de Risco", "Clube de Investimentos"]
}

# --- SESSION ---
defaults = {
    "logado": False,
    "simulado_iniciado": False,
    "mostrar_resultado": False,
    "tempo": None,
    "usuario": ""
}

for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- LOGIN ---
def login(u,p):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(worksheet="Usuarios")
        return not df[(df["Nome"]==u)&(df["Senha"]==p)].empty
    except:
        return False

if not st.session_state.logado:
    with st.form("login"):
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.form_submit_button("Entrar"):
            if login(u,p):
                st.session_state.logado=True
                st.session_state.usuario=u
                st.rerun()
            else:
                st.error("Credenciais inválidas")
    st.stop()

# --- PRIMEIRO ACESSO ---
if "primeiro" not in st.session_state:
    st.title("Simulado ANCORD - Preparação Profissional")

    st.markdown("""
    ### Diretrizes Oficiais

    • 20 questões por simulado  
    • Tempo limite: 30 minutos  
    • Ambiente controlado (sem consulta externa)  
    • Não atualizar a página durante a execução  
    • Aprovação: mínimo de 70% de acerto  

    Este simulado replica as condições reais da certificação ANCORD.
    """)

    if st.button("Iniciar Simulado"):
        st.session_state.primeiro = False
        st.rerun()

    st.stop()

# --- MENU ---
menu = st.sidebar.radio("Menu", ["Simulado", "Evolução"])
conn = st.connection("gsheets", type=GSheetsConnection)

# --- SIMULADO ---
if menu == "Simulado":

    if not st.session_state.simulado_iniciado:
        st.title("Configurar Simulado")

        sim = st.selectbox("Escolha o simulado:", list(DIC_SIMULADOS.keys()))

        if st.button("Iniciar"):
            materias = DIC_SIMULADOS[sim]
            pool = [q for q in BANCO_QUESTOES if q["modulo"] in materias]

            st.session_state.questoes = random.sample(pool, min(20,len(pool)))
            st.session_state.respostas = {}
            st.session_state.tempo = datetime.now() + timedelta(minutes=30)
            st.session_state.simulado_nome = sim
            st.session_state.simulado_iniciado = True
            st.session_state.mostrar_resultado = False
            st.rerun()

    else:
        # --- TIMER REAL ---
        restante = int((st.session_state.tempo - datetime.now()).total_seconds())

        if restante <= 0:
            st.warning("Tempo esgotado.")
            st.session_state.mostrar_resultado = True
            restante = 0

        minutos, segundos = divmod(restante, 60)

        st.info(f"⏱️ Tempo restante: {minutos:02d}:{segundos:02d}")

        # Auto refresh a cada segundo
        st.experimental_rerun if False else None

        with st.form("form"):
            for i, q in enumerate(st.session_state.questoes):

                st.markdown(f"**{i+1}. {q['pergunta']}**")

                opcoes_map = {f"{k}) {v}": k for k,v in q["opcoes"].items()}
                opcoes_lista = list(opcoes_map.keys())

                resposta = st.radio(
                    "Resposta:",
                    opcoes_lista,
                    key=f"q{i}",
                    index=None,
                    disabled=st.session_state.mostrar_resultado
                )

                if resposta:
                    st.session_state.respostas[i] = opcoes_map[resposta]

                # --- CORREÇÃO ---
                if st.session_state.mostrar_resultado:
                    correta = q["resposta_correta"]
                    user = st.session_state.respostas.get(i)

                    texto_correta = f"{correta}) {q['opcoes'][correta]}"

                    if user == correta:
                        st.success(f"✅ Correto — {texto_correta}")
                    else:
                        st.error(f"❌ Incorreto — {texto_correta}")

                    # EXPLICAÇÃO REAL DO BANCO
                    st.markdown(f"**Explicação:** {q.get('explicacao','Não disponível')}")

                st.markdown("---")

            enviar = st.form_submit_button("Finalizar Simulado")

        if enviar:
            acertos = 0
            por_materia = {}

            for i, q in enumerate(st.session_state.questoes):
                correta = q["resposta_correta"]
                user = st.session_state.respostas.get(i)
                mod = q["modulo"]

                por_materia.setdefault(mod, [0,0])
                por_materia[mod][1] += 1

                if user == correta:
                    acertos += 1
                    por_materia[mod][0] += 1

            total = len(st.session_state.questoes)
            nota = (acertos / total) * 100

            # salvar
            try:
                df = conn.read(worksheet="Resultados")

                novo = pd.DataFrame([{
                    "Usuario": st.session_state.usuario,
                    "Nota": nota,
                    "Data": datetime.now().strftime("%d/%m/%Y %H:%M")
                }])

                conn.update(worksheet="Resultados", data=pd.concat([df, novo]))

            except:
                pass

            st.session_state.mostrar_resultado = True

            st.success(f"Resultado final: {nota:.1f}%")

            # desempenho por matéria
            st.subheader("Desempenho por matéria")
            df_mat = pd.DataFrame([
                {"Matéria": k, "Aproveitamento (%)": v[0]/v[1]*100}
                for k,v in por_materia.items()
            ])
            st.bar_chart(df_mat.set_index("Matéria"))

            st.rerun()

# --- EVOLUÇÃO ---
else:
    st.title("Meu Desempenho")

    try:
        df = conn.read(worksheet="Resultados")
        user = df[df["Usuario"] == st.session_state.usuario]

        st.dataframe(user.sort_values(by="Data", ascending=False))
        st.line_chart(user["Nota"])

    except:
        st.error("Erro ao carregar dados")
