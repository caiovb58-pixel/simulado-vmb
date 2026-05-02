import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# TENTA IMPORTAR O BANCO DE QUESTÕES
try:
    from questoes import BANCO_QUESTOES
except ImportError:
    st.error("Erro: O arquivo 'questoes.py' não foi encontrado ou está com erro de importação circular.")
    st.stop()

# 1. Configuração da página
st.set_page_config(page_title="Simulado ANCORD - VMB Invest", page_icon="⚖️", layout="wide")

# --- FUNÇÃO DE AUTENTICAÇÃO ---
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
    except Exception as e:
        st.error(f"Erro na base de dados: {e}")
        return False

# --- CONTROLE DE ESTADO ---
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'usuario_nome' not in st.session_state:
    st.session_state.usuario_nome = ""
if 'simulado_iniciado' not in st.session_state:
    st.session_state.simulado_iniciado = False

# --- TELA DE LOGIN ---
if not st.session_state.logado:
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        # Tenta carregar a logo, se não houver, usa texto
        st.title("VMB Invest")
        st.subheader("Simulado ANCORD")
            
        with st.form("login_form"):
            nome_input = st.text_input("Usuário (Nome Completo)")
            senha_input = st.text_input("Senha", type="password")
            botao_entrar = st.form_submit_button("Entrar")
            
            if botao_entrar:
                if verificar_login(nome_input, senha_input):
                    st.session_state.logado = True
                    st.session_state.usuario_nome = nome_input.strip()
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos.")
    st.stop()

# --- MENU LATERAL ---
st.sidebar.title(f"Olá, {st.session_state.usuario_nome}")
menu = st.sidebar.radio("Navegação", ["Início", "Simulado ANCORD", "Evolução"])
st.sidebar.markdown("---")

conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)

# --- PÁGINA: INÍCIO ---
if menu == "Início":
    st.title(f"Bem-vindo, {st.session_state.usuario_nome}!")
    st.markdown("### Treinamento de Elite - SDR & Trainees")
    st.write("Acesse o menu 'Simulado ANCORD' para começar.")

# --- PÁGINA: SIMULADO ---
elif menu == "Simulado ANCORD":
    st.title("Simulado Personalizado ANCORD")

    if not st.session_state.simulado_iniciado:
        modulos_disponiveis = sorted(list(set([q['modulo'] for q in BANCO_QUESTOES])))
        
        st.subheader("Configuração")
        modulos_selecionados = st.multiselect("Escolha os módulos:", modulos_disponiveis)
        qtd = st.slider("Quantidade de questões:", 1, len(BANCO_QUESTOES), 5)

        if st.button("Gerar Simulado"):
            if modulos_selecionados:
                pool = [q for q in BANCO_QUESTOES if q['modulo'] in modulos_selecionados]
                if len(pool) < qtd: qtd = len(pool)
                
                st.session_state.questoes_sorteadas = random.sample(pool, qtd)
                st.session_state.respostas_usuario = {}
                st.session_state.simulado_iniciado = True
                st.rerun()
            else:
                st.warning("Selecione ao menos um módulo.")

    else:
        if st.button("⬅️ Trocar Configuração"):
            st.session_state.simulado_iniciado = False
            st.rerun()

        with st.form("form_simulado"):
            for idx, q in enumerate(st.session_state.questoes_sorteadas):
                st.markdown(f"**Questão {idx+1}** | *{q['modulo']}*")
                st.write(q['pergunta'])
                
                # Monta as opções dinamicamente do dicionário
                opcoes_display = [f"{k}) {v}" for k, v in q['opcoes'].items()]
                
                st.session_state.respostas_usuario[idx] = st.radio(
                    "Selecione:",
                    options=opcoes_display,
                    key=f"r_{idx}",
                    index=None
                )
                st.markdown("---")
            
            if st.form_submit_button("Finalizar"):
                acertos = 0
                total = len(st.session_state.questoes_sorteadas)
                
                for idx, q in enumerate(st.session_state.questoes_sorteadas):
                    resp = st.session_state.respostas_usuario[idx]
                    if resp and resp[0] == q['resposta_correta']:
                        acertos += 1
                
                nota = (acertos / total) * 100
                st.subheader(f"Resultado: {acertos}/{total} ({nota:.1f}%)")

                try:
                    df_res = conn.read(worksheet="Resultados")
                    novo = pd.DataFrame([{
                        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "Usuario": st.session_state.usuario_nome,
                        "Acertos": acertos,
                        "Total": total,
                        "Nota": nota
                    }])
                    conn.update(worksheet="Resultados", data=pd.concat([df_res, novo], ignore_index=True))
                    st.success("Salvo com sucesso!")
                    st.session_state.simulado_iniciado = False
                except:
                    st.error("Erro ao salvar na planilha.")

# --- PÁGINA: EVOLUÇÃO ---
elif menu == "Evolução":
    st.title("Evolução")
    try:
        df = conn.read(worksheet="Resultados")
        meus = df[df['Usuario'] == st.session_state.usuario_nome]
        if not meus.empty:
            st.line_chart(meus.set_index('Data')['Nota'])
            st.table(meus)
    except:
        st.error("Erro ao carregar.")
