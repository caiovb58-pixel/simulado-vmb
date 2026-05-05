import streamlit as st
import random
import pandas as pd
import os
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

DIC_SIMULADOS = {
    "Simulado 1": ["Atividade do AAI", "Lavagem de Dinheiro"],
    "Simulado 2": ["Mercado de Capitais", "Derivativos"],
    "Simulado 3": ["Fundos de Investimentos"],
}

# --- CSS ---
st.markdown("""
<style>
.timer {
position: fixed; top: 20px; right: 20px;
background: white; padding: 10px;
border: 2px solid red; border-radius: 10px;
font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --- SESSION ---
for key, val in {
    "logado": False,
    "simulado_iniciado": False,
    "mostrar_resultado": False,
    "nivel": 1
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

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
                st.error("Erro login")
    st.stop()

# --- PRIMEIRO ACESSO ---
if "primeiro" not in st.session_state:
    st.title("Simulado ANCORD - Preparação Profissional")

    st.markdown("""
    ### Diretrizes Oficiais do Simulado

    - 20 questões por simulado
    - Tempo máximo: 30 minutos
    - Proibido consulta externa
    - Não recarregar a página durante a prova
    - Critério de aprovação: mínimo de 70%

    Este ambiente simula condições reais da certificação.
    """)

    if st.button("Iniciar"):
        st.session_state.primeiro=False
        st.rerun()
    st.stop()

# --- MENU ---
menu = st.sidebar.radio("Menu", ["Simulado", "Evolução"])

conn = st.connection("gsheets", type=GSheetsConnection)

# --- SIMULADO ---
if menu == "Simulado":

    if not st.session_state.simulado_iniciado:
        sim = st.selectbox("Escolha", list(DIC_SIMULADOS.keys()))

        if st.button("Começar"):
            materias = DIC_SIMULADOS[sim]

            # ADAPTATIVO
            if st.session_state.nivel >= 2:
                pool = [q for q in BANCO_QUESTOES if q["modulo"] in materias and q.get("dificuldade","medio")!="facil"]
            else:
                pool = [q for q in BANCO_QUESTOES if q["modulo"] in materias]

            st.session_state.questoes = random.sample(pool, min(20,len(pool)))
            st.session_state.respostas={}
            st.session_state.tempo = datetime.now()+timedelta(minutes=30)
            st.session_state.simulado_iniciado=True
            st.rerun()

    else:
        restante = int((st.session_state.tempo-datetime.now()).total_seconds())

        if restante <= 0:
            st.session_state.mostrar_resultado=True

        minutos, segundos = divmod(max(restante,0),60)

        st.markdown(f"<div class='timer'>⏱️ {minutos:02d}:{segundos:02d}</div>", unsafe_allow_html=True)

        with st.form("form"):
            for i,q in enumerate(st.session_state.questoes):

                st.write(f"**{i+1}. {q['pergunta']}**")

                ops=[f"{k}) {v}" for k,v in q["opcoes"].items()]

                st.session_state.respostas[i]=st.radio(
                    "Resposta",
                    ops,
                    key=f"q{i}",
                    index=None,
                    disabled=st.session_state.mostrar_resultado
                )

                if st.session_state.mostrar_resultado:
                    correta=f"{q['resposta_correta']}) {q['opcoes'][q['resposta_correta']]}"
                    r=st.session_state.respostas[i]

                    if r and r.startswith(q['resposta_correta']):
                        st.success("Correto")
                    else:
                        st.error(f"Errado: {correta}")

                    with st.expander("Explicação"):
                        st.write(q.get("explicacao","-"))

                st.markdown("---")

            enviar=st.form_submit_button("Finalizar")

        if enviar:
            acertos=0
            por_materia={}

            for i,q in enumerate(st.session_state.questoes):
                r=st.session_state.respostas[i]
                mod=q["modulo"]

                por_materia.setdefault(mod,[0,0])

                por_materia[mod][1]+=1

                if r and r.startswith(q["resposta_correta"]):
                    acertos+=1
                    por_materia[mod][0]+=1

            total=len(st.session_state.questoes)
            nota=(acertos/total)*100

            # ADAPTATIVO
            if nota>=80:
                st.session_state.nivel+=1
            elif nota<50:
                st.session_state.nivel=1

            # salvar
            try:
                df=conn.read(worksheet="Resultados")

                novo=pd.DataFrame([{
                    "Usuario":st.session_state.usuario,
                    "Nota":nota,
                    "Data":datetime.now().strftime("%d/%m"),
                }])

                conn.update(worksheet="Resultados", data=pd.concat([df,novo]))

            except:
                pass

            st.session_state.mostrar_resultado=True

            st.success(f"Nota: {nota:.1f}%")

            # % por matéria
            st.subheader("Desempenho por matéria")
            df_mat=pd.DataFrame([
                {"Materia":k,"%":v[0]/v[1]*100}
                for k,v in por_materia.items()
            ])
            st.bar_chart(df_mat.set_index("Materia"))

            st.rerun()

# --- EVOLUÇÃO ---
else:
    st.title("Dashboard de Performance")

    try:
        df=conn.read(worksheet="Resultados")

        # ranking
        st.subheader("Ranking")
        ranking=df.groupby("Usuario")["Nota"].mean().sort_values(ascending=False)
        st.dataframe(ranking)

        # heatmap simples
        st.subheader("Heatmap de notas")
        st.dataframe(df.pivot_table(index="Usuario", values="Nota", aggfunc="mean"))

        # gráfico
        user=df[df["Usuario"]==st.session_state.usuario]
        st.line_chart(user["Nota"])

    except:
        st.error("Erro ao carregar")
