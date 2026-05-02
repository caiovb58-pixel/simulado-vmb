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
        # Conexão automática via Secrets
        conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)
        df_usuarios = conn.read(worksheet="Usuarios")
        
        # Limpeza e padronização (ignora maiúsculas e trata números como texto)
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

# --- CONTROLE DE ESTADO (SESSION STATE) ---
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
            st.subheader("Login - Simulado ANCORD")
            nome_input = st.text_input("Usuário (Nome Completo)")
            senha_input = st.text_input("Senha", type="password")
            botao_entrar = st.form_submit_button("Entrar")
            
            if botao_entrar:
                if verificar_login(nome_input, senha_input):
                    st.session_state.logado = True
                    st.session_state.usuario_nome = nome_input.strip()
                    st.success("Acesso autorizado!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos na base de dados.")
    st.stop()

# --- MENU LATERAL (APÓS LOGIN) ---
st.sidebar.title(f"Olá, {st.session_state.usuario_nome}")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navegação", ["Início", "Simulado ANCORD", "Evolução"])

# Conexão global para as abas de Simulado e Evolução
conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)

# --- PÁGINA: INÍCIO ---
if menu == "Início":
    st.title(f"Bem-vindo, {st.session_state.usuario_nome}!")
    st.markdown("""
    ### Painel de Treinamento - VMB Invest
    Selecione uma opção no menu lateral para começar:
    *   **Simulado ANCORD**: Teste seus conhecimentos com questões reais.
    *   **Evolução**: Acompanhe seu histórico de notas e progresso.
    """)
    st.info("💡 Dica: A aprovação na ANCORD exige 70% de acerto total e mínimos por módulo.")

# --- PÁGINA: SIMULADO ---
elif menu == "Simulado ANCORD":
    st.title("Simulado ANCORD")
    
    # Sorteia as questões apenas uma vez por sessão
    if 'questoes_sorteadas' not in st.session_state:
        # Sorteia 10 questões do seu arquivo questoes.py
        st.session_state.questoes_sorteadas = random.sample(BANCO_QUESTOES, 10)
        st.session_state.respostas = {}

    with st.form("simulado_form"):
        for idx, q in enumerate(st.session_state.questoes_sorteadas):
            st.write(f"**{idx+1}. {q['pergunta']}**")
            st.session_state.respostas[idx] = st.radio(
                f"Selecione a resposta da questão {idx+1}:", 
                q['opcoes'], 
                key=f"quest_{idx}"
            )
            st.markdown("---")
            
        btn_enviar = st.form_submit_button("Finalizar Simulado")

    if btn_enviar:
        acertos = 0
        for idx, q in enumerate(st.session_state.questoes_sorteadas):
            if st.session_state.respostas[idx] == q['correta']:
                acertos += 1
        
        nota = (acertos / len(st.session_state.questoes_sorteadas)) * 100
        st.subheader(f"Resultado: {nota}% de Aproveitamento")
        
        # PREPARAÇÃO DOS DADOS PARA O GOOGLE SHEETS
        novo_resultado = pd.DataFrame([{
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Usuario": st.session_state.usuario_nome,
            "Acertos": acertos,
            "Nota": nota
        }])

        try:
            # Lê resultados antigos e anexa o novo
            df_historico = conn.read(worksheet="Resultados")
            df_final = pd.concat([df_historico, novo_resultado], ignore_index=True)
            conn.update(worksheet="Resultados", data=df_final)
            st.success("Desempenho salvo com sucesso na planilha!")
            
            # Limpa o sorteio para o próximo teste
            del st.session_state.questoes_sorteadas
        except Exception as e:
            st.error(f"Erro ao salvar na planilha: {e}")

# --- PÁGINA: EVOLUÇÃO ---
elif menu == "Evolução":
    st.title("Sua Evolução")
    try:
        df_evolucao = conn.read(worksheet="Resultados")
        # Filtra dados apenas do usuário logado
        meus_dados = df_evolucao[df_evolucao['Usuario'] == st.session_state.usuario_nome]
        
        if not meus_dados.empty:
            st.write("Gráfico de Desempenho (Nota %)")
            st.line_chart(meus_dados.set_index('Data')['Nota'])
            st.dataframe(meus_dados)
        else:
            st.warning("Você ainda não completou nenhum simulado.")
    except:
        st.error("Aba 'Resultados' não encontrada na planilha.")
