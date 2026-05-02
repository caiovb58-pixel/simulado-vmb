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
        conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)
        df_usuarios = conn.read(worksheet="Usuarios")
        
        # Validação simples de nome e senha
        usuario_valido = df_usuarios[(df_usuarios['Nome'] == nome) & (df_usuarios['Senha'].astype(str) == str(senha))]
        
        return not usuario_valido.empty
    except Exception as e:
        st.error(f"Erro ao conectar com base de usuários: {e}")
        return False

# --- ESTADO DE LOGIN ---
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'usuario_nome' not in st.session_state:
    st.session_state.usuario_nome = ""

# --- TELA DE LOGIN ---
if not st.session_state.logado:
    st.container()
    with st.columns([1,2,1])[1]: # Centraliza o form
        try:
            st.image("vmb_logo_fundo_preto.png", use_container_width=True)
        except:
            st.header("VMB Invest - Acesso Restrito")
            
        with st.form("login_form"):
            st.subheader("Login do SDR")
            nome_input = st.text_input("Usuário (Nome Completo)")
            senha_input = st.text_input("Senha", type="password")
            botao_entrar = st.form_submit_button("Entrar")
            
            if botao_entrar:
                if verificar_login(nome_input, senha_input):
                    st.session_state.logado = True
                    st.session_state.usuario_nome = nome_input
                    st.success("Acesso autorizado!")
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos.")
    st.stop() # Interrompe a execução aqui se não estiver logado

# --- SE CHEGOU AQUI, ESTÁ LOGADO ---

# Menu Lateral (Agora visível apenas após login)
with st.sidebar:
    st.write(f"Conectado como: **{st.session_state.usuario_nome}**")
    if st.button("Sair/Logout"):
        st.session_state.logado = False
        st.rerun()
    st.divider()
    menu = st.radio("Navegação", ["📝 Realizar Simulado", "📈 Minha Evolução"])

# --- FUNÇÃO PARA SALVAR NO GOOGLE SHEETS ---
def salvar_resultado(nome, materias, acertos, total):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)
        try:
            dados_existentes = conn.read(worksheet="Resultados")
        except:
            dados_existentes = pd.DataFrame(columns=["Data", "Nome", "Materias", "Acertos", "Total", "Aproveitamento"])
        
        nova_linha = pd.DataFrame([{
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Nome": nome,
            "Materias": ", ".join(materias) if materias else "Geral",
            "Acertos": acertos,
            "Total": total,
            "Aproveitamento": f"{(acertos/total)*100:.1f}%"
        }])
        
        dados_atualizados = pd.concat([dados_existentes, nova_linha], ignore_index=True)
        conn.update(worksheet="Resultados", data=dados_atualizados)
        st.success("✅ Desempenho registrado!")
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")

# --- TELA: MINHA EVOLUÇÃO ---
if menu == "📈 Minha Evolução":
    st.title(f"📊 Evolução: {st.session_state.usuario_nome}")
    try:
        conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)
        df = conn.read(worksheet="Resultados")
        user_data = df[df['Nome'] == st.session_state.usuario_nome].copy()
        
        if not user_data.empty:
            user_data['Aproveitamento_Num'] = user_data['Aproveitamento'].str.replace('%', '').astype(float)
            user_data['Data_DT'] = pd.to_datetime(user_data['Data'], dayfirst=True)
            user_data = user_data.sort_values('Data_DT')

            m1, m2 = st.columns(2)
            m1.metric("Simulados", len(user_data))
            m2.metric("Média Geral", f"{user_data['Aproveitamento_Num'].mean():.1f}%")

            st.line_chart(user_data.set_index('Data_DT')['Aproveitamento_Num'])
            st.dataframe(user_data[['Data', 'Materias', 'Acertos', 'Total', 'Aproveitamento']], use_container_width=True)
        else:
            st.info("Nenhum histórico encontrado.")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")

# --- TELA: REALIZAR SIMULADO ---
else:
    # Lógica do Simulado (Cronômetro, Sorteio, Form)
    # Reutilize a estrutura que já temos, mas use st.session_state.usuario_nome para salvar
    st.title("📝 Simulado ANCORD")
    
    # Controle de Estado do Simulado
    if 'simulado_iniciado' not in st.session_state: st.session_state.simulado_iniciado = False
    if 'finalizado' not in st.session_state: st.session_state.finalizado = False

    if not st.session_state.simulado_iniciado:
        modulos = sorted(list(set(q.get('modulo', 'Geral') for q in BANCO_QUESTOES)))
        materias = st.multiselect("Selecione as matérias:", options=modulos)
        
        if st.button("🚀 Iniciar"):
            banco = [q for q in BANCO_QUESTOES if q.get('modulo') in materias] if materias else BANCO_QUESTOES
            st.session_state.questoes_sorteadas = random.sample(banco, k=min(20, len(banco)))
            st.session_state.inicio_tempo = time.time()
            st.session_state.simulado_iniciado = True
            st.rerun()

    # ... (Continuação da lógica de exibição das questões e finalização)
