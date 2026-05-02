import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime
from questoes import BANCO_QUESTOES
from streamlit_gsheets import GSheetsConnection

# 1. Configuração da página
st.set_page_config(page_title="Simulado ANCORD - VMB Invest", page_icon="⚖️", layout="wide")

# --- FUNÇÃO DE AUTENTICAÇÃO LIMPA ---
def verificar_login(nome, senha):
    try:
        # Conexão silenciosa (sem st.info)
        conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)
        df_usuarios = conn.read(worksheet="Usuarios")
        
        nome_busca = str(nome).strip()
        senha_busca = str(senha).strip()
        
        # Validação ignorando maiúsculas/minúsculas e tratando números como texto
        usuario_valido = df_usuarios[
            (df_usuarios['Nome'].astype(str).str.strip().str.upper() == nome_busca.upper()) & 
            (df_usuarios['Senha'].astype(str).str.strip() == senha_busca)
        ]
        
        return not usuario_valido.empty
    except Exception as e:
        # Mantemos apenas o erro técnico caso a planilha caia
        st.error(f"Erro técnico na conexão: {e}")
        return False

# --- ESTADO DE LOGIN ---
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'usuario_nome' not in st.session_state:
    st.session_state.usuario_nome = ""

# --- TELA DE LOGIN ---
if not st.session_state.logado:
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        try:
            st.image("vmb_logo_fundo_preto.png", use_container_width=True)
        except:
            st.title("VMB Invest")
            
        with st.form("login_form"):
            st.subheader("Login")
            nome_input = st.text_input("Usuário (Nome Completo)")
            senha_input = st.text_input("Senha", type="password")
            botao_entrar = st.form_submit_button("Entrar")
            
            if botao_entrar:
                # O login agora acontece "em silêncio"
                if verificar_login(nome_input, senha_input):
                    st.session_state.logado = True
                    st.session_state.usuario_nome = nome_input.strip()
                    st.success("Acesso autorizado!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos.")
    st.stop()

# --- CONTEÚDO DO APP ABAIXO ---
# Aqui você insere o restante do seu código (Menu, Questões, etc.)

st.sidebar.title(f"Olá, {st.session_state.usuario_nome}")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navegação", ["Início", "Simulado ANCORD", "Evolução"])

if menu == "Início":
    st.title(f"Bem-vindo, {st.session_state.usuario_nome}!")
    st.write("Selecione uma opção no menu lateral para começar seu treinamento.")

elif menu == "Simulado ANCORD":
    st.title("Simulado ANCORD")
    # Insira aqui a lógica de sorteio das questões
    st.info("O sistema de questões será carregado aqui.")

elif menu == "Evolução":
    st.title("Sua Evolução")
    st.write("Aqui você verá seu histórico de acertos.")
