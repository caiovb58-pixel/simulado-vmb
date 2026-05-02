import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection

# TENTA IMPORTAR O BANCO DE QUESTÕES
try:
    from questoes import BANCO_QUESTOES
except ImportError:
    st.error("Erro: O arquivo 'questoes.py' não foi encontrado.")
    st.stop()

# 1. Configuração da página
st.set_page_config(page_title="Simulado ANCORD - VMB Invest", page_icon="⚖️", layout="wide")

# --- ESTILIZAÇÃO CUSTOMIZADA (CSS) ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #002e5d; color: white; }
    .stRadio > label { font-weight: bold; }
    .timer-text { font-size: 24px; font-weight: bold; color: #ff4b4b; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- CONTROLE DE ESTADO ---
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'usuario_nome' not in st.session_state:
    st.session_state.usuario_nome = ""
if 'simulado_iniciado' not in st.session_state:
    st.session_state.simulado_iniciado = False
if 'tempo_fim' not in st.session_state:
    st.session_state.tempo_fim = None

# --- FUNÇÕES ---
def logout():
    st.session_state.logado = False
    st.session_state.usuario_nome = ""
    st.session_state.simulado_iniciado = False
    st.rerun()

def verificar_login(nome, senha):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)
        df_usuarios = conn.read(worksheet="Usuarios")
        nome_busca = str(nome).strip().upper()
        senha_busca = str(senha).strip()
        usuario_valido = df_usuarios[
            (df_usuarios['Nome'].astype(str).str.strip().str.upper() == nome_busca) & 
            (df_usuarios['Senha'].astype(str).str.strip() == senha_busca)
        ]
        return not usuario_valido.empty
    except:
        return False

# --- TELA DE LOGIN ---
if not st.session_state.logado:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        try:
            st.image("logo_vmb.png", width=200) # Certifique-se de ter esse arquivo
        except:
            st.title("VMB Invest")
        
        st.subheader("Acesso ao Simulado")
        with st.form("login"):
            u = st.text_input("Usuário")
            p = st.text_input("Senha", type="password")
            if st.form_submit_button("Entrar"):
                if verificar_login(u, p):
                    st.session_state.logado = True
                    st.session_state.usuario_nome = u.strip()
                    st.rerun()
                else:
                    st.error("Credenciais inválidas")
    st.stop()

# --- MENU LATERAL ---
with st.sidebar:
    st.image("logo_vmb.png", width=150) if 'logo_vmb.png' else st.title("VMB Invest")
    st.write(f"👤 **{st.session_state.usuario_nome}**")
    menu = st.radio("Navegação", ["Início", "Simulado ANCORD", "Evolução"])
    st.markdown("---")
    if st.button("🚪 Sair"):
        logout()

conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)

# --- PÁGINA: INÍCIO ---
if menu == "Início":
    st.title("Portal de Treinamento VMB")
    st.info("O simulado atual possui tempo limite de 30 minutos e foca na certificação ANCORD.")

# --- PÁGINA: SIMULADO ---
elif menu == "Simulado ANCORD":
    if not st.session_state.simulado_iniciado:
        st.title("Configurar Novo Simulado")
        modulos = sorted(list(set([q['modulo'] for q in BANCO_QUESTOES])))
        sel = st.multiselect("Selecione os módulos:", modulos, default=modulos)
        qtd = st.number_input("Quantidade de questões:", min_value=5, max_value=20, value=20)

        if st.button("🚀 INICIAR SIMULADO"):
            pool = [q for q in BANCO_QUESTOES if q['modulo'] in sel]
            st.session_state.questoes_sorteadas = random.sample(pool, min(len(pool), qtd))
            st.session_state.respostas_usuario = {}
            st.session_state.tempo_fim = datetime.now() + timedelta(minutes=30)
            st.session_state.simulado_iniciado = True
            st.rerun()

    else:
        # CRONÔMETRO
        placeholder_tempo = st.empty()
        tempo_restante = st.session_state.tempo_fim - datetime.now()
        
        if tempo_restante.total_seconds() <= 0:
            st.error("Tempo esgotado! Enviando respostas automaticamente...")
            # Aqui você pode chamar a lógica de salvar automaticamente
            st.session_state.simulado_iniciado = False
            st.stop()

        mins, secs = divmod(int(tempo_restante.total_seconds()), 60)
        placeholder_tempo.markdown(f"<div class='timer-text'>⏱️ Tempo Restante: {mins:02d}:{secs:02d}</div>", unsafe_allow_html=True)

        with st.form("simulado"):
            for idx, q in enumerate(st.session_state.questoes_sorteadas):
                st.markdown(f"#### Questão {idx+1}")
                st.write(q['pergunta'])
                ops = [f"{k}) {v}" for k, v in q['opcoes'].items()]
                st.session_state.respostas_usuario[idx] = st.radio("Escolha:", ops, key=f"q_{idx}", index=None)
                st.markdown("---")
            
            if st.form_submit_button("FINALIZAR E SALVAR"):
                # Cálculo de Resultados
                resultados_por_modulo = {}
                acertos_totais = 0
                
                for idx, q in enumerate(st.session_state.questoes_sorteadas):
                    mod = q['modulo']
                    if mod not in resultados_por_modulo:
                        resultados_por_modulo[mod] = {"acertos": 0, "total": 0}
                    
                    resultados_por_modulo[mod]["total"] += 1
                    resp = st.session_state.respostas_usuario[idx]
                    if resp and resp[0] == q['resposta_correta']:
                        acertos_totais += 1
                        resultados_por_modulo[mod]["acertos"] += 1

                # Salvar no GSheets
                try:
                    df_res = conn.read(worksheet="Resultados")
                    # Salva uma linha por módulo para a evolução detalhada
                    novos_dados = []
                    for mod, dados in resultados_por_modulo.items():
                        perc = (dados['acertos'] / dados['total']) * 100
                        novos_dados.append({
                            "Data": datetime.now().strftime("%d/%m/%Y"),
                            "Usuario": st.session_state.usuario_nome,
                            "Modulo": mod,
                            "Acertos": dados['acertos'],
                            "Total": dados['total'],
                            "Nota": perc
                        })
                    
                    df_novo = pd.concat([df_res, pd.DataFrame(novos_dados)], ignore_index=True)
                    conn.update(worksheet="Resultados", data=df_novo)
                    st.success("Simulado finalizado com sucesso!")
                    st.session_state.simulado_iniciado = False
                    st.balloons()
                    time.sleep(2)
                    st.rerun()
                except:
                    st.error("Erro ao salvar resultados.")

# --- PÁGINA: EVOLUÇÃO ---
elif menu == "Evolução":
    st.title("Sua Evolução na VMB")
    try:
        df = conn.read(worksheet="Resultados")
        meus = df[df['Usuario'] == st.session_state.usuario_nome]
        
        if not meus.empty:
            tab1, tab2 = st.tabs(["Geral", "Por Matéria"])
            
            with tab1:
                # Evolução temporal média
                meus['Data'] = pd.to_datetime(meus['Data'], format="%d/%m/%Y")
                evolucao_diaria = meus.groupby('Data')['Nota'].mean()
                st.line_chart(evolucao_diaria)
            
            with tab2:
                # Desempenho por módulo
                progresso_modulo = meus.groupby('Modulo')['Nota'].mean().reset_index()
                st.bar_chart(data=progresso_modulo, x='Modulo', y='Nota')
                st.dataframe(progresso_modulo, use_container_width=True)
        else:
            st.warning("Você ainda não completou nenhum simulado.")
    except:
        st.error("Erro ao carregar dados de evolução.")
