import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime
from questoes import BANCO_QUESTOES
from streamlit_gsheets import GSheetsConnection

# 1. Configuração da página
st.set_page_config(page_title="Simulado ANCORD - VMB Invest", page_icon="⚖️", layout="wide")

# --- FUNÇÃO DE AUTENTICAÇÃO ---
def verificar_login(nome, senha):
    try:
        # Criamos a conexão sem passar parâmetros manuais
        conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)
        
        # Lemos a aba de usuários
        df_usuarios = conn.read(worksheet="Usuarios")
        
        # Limpeza de dados para comparação
        nome_busca = str(nome).strip()
        senha_busca = str(senha).strip()
        
        # Validação robusta
        usuario_valido = df_usuarios[
            (df_usuarios['Nome'].astype(str).str.strip() == nome_busca) & 
            (df_usuarios['Senha'].astype(str).str.strip() == senha_busca)
        ]
        
        return not usuario_valido.empty
    except Exception as e:
        # Isso nos mostrará o erro real se a conexão falhar
        st.error(f"Erro na conexão com a base de dados: {e}")
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
                if verificar_login(nome_input, senha_input):
                    st.session_state.logado = True
                    st.session_state.usuario_nome = nome_input.strip()
                    st.success("Acesso autorizado!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos.")
    st.stop()

# --- CONTEÚDO DO APP ABAIXO ---
st.write(f"Bem-vindo, {st.session_state.usuario_nome}!")
