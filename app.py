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
        try:
            st.image("vmb_logo_fundo_preto.png", use_container_width=True)
        except:
            st.title("VMB Invest")
            
        with st.form("login_form"):
            st.subheader("Login - Sistema de Treinamento")
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
    st.markdown("""
    ### Painel de Especialista ANCORD
    Prepare-se para a certificação com foco nas matérias que você mais precisa revisar.
    """)
    st.image("vmb_logo_fundo_preto.png", width=200)

# --- PÁGINA: SIMULADO ---
elif menu == "Simulado ANCORD":
    st.title("Simulado Personalizado ANCORD")

    # Passo 1: Escolha das matérias (Só aparece se o simulado não começou)
    if not st.session_state.simulado_iniciado:
        materias_disponiveis = sorted(list(set([q['materia'] for q in BANCO_QUESTOES])))
        
        st.subheader("Configuração do Simulado")
        materias_selecionadas = st.multiselect("Selecione as matérias que deseja praticar:", materias_disponiveis)
        num_questoes = st.slider("Quantidade de questões:", 5, 20, 10)

        if st.button("Iniciar Simulado"):
            if materias_selecionadas:
                # Filtra o banco de questões
                pool = [q for q in BANCO_QUESTOES if q['materia'] in materias_selecionadas]
                
                if len(pool) < num_questoes:
                    num_questoes = len(pool)
                
                st.session_state.questoes_sorteadas = random.sample(pool, num_questoes)
                st.session_state.respostas = {}
                st.session_state.simulado_iniciado = True
                st.rerun()
            else:
                st.warning("Por favor, selecione ao menos uma matéria.")

    # Passo 2: Execução do Simulado
    else:
        if st.button("⬅️ Voltar e Trocar Matérias"):
            st.session_state.simulado_iniciado = False
            st.rerun()

        with st.form("simulado_form"):
            for idx, q in enumerate(st.session_state.questoes_sorteadas):
                st.markdown(f"**Questão {idx+1}** | *{q['materia']}*")
                st.write(q['pergunta'])
                
                # Exibe as alternativas completas
                st.session_state.respostas[idx] = st.radio(
                    f"Selecione a alternativa correta:",
                    q['opcoes'], # Agora passa a lista de textos, não A, B, C...
                    key=f"q_{idx}",
                    index=None # Começa sem nada marcado
                )
                st.markdown("---")
            
            finalizar = st.form_submit_button("Finalizar e Gravar Resultados")

        if finalizar:
            acertos = 0
            # IMPORTANTE: A comparação deve ser o texto exato da opção correta
            for idx, q in enumerate(st.session_state.questoes_sorteadas):
                if st.session_state.respostas[idx] == q['correta']:
                    acertos += 1
            
            nota = (acertos / len(st.session_state.questoes_sorteadas)) * 100
            st.subheader(f"Resultado Final: {nota:.1f}%")
            
            # Gravação no GSheets
            novo_resultado = pd.DataFrame([{
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Usuario": st.session_state.usuario_nome,
                "Acertos": acertos,
                "Total": len(st.session_state.questoes_sorteadas),
                "Nota": nota
            }])

            try:
                df_hist = conn.read(worksheet="Resultados")
                df_final = pd.concat([df_hist, novo_resultado], ignore_index=True)
                conn.update(worksheet="Resultados", data=df_final)
                st.success("Desempenho salvo com sucesso!")
                st.session_state.simulado_iniciado = False # Reseta para o próximo
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")

# --- PÁGINA: EVOLUÇÃO ---
elif menu == "Evolução":
    st.title("Sua Evolução na VMB Invest")
    try:
        df_evolucao = conn.read(worksheet="Resultados")
        meus_dados = df_evolucao[df_evolucao['Usuario'] == st.session_state.usuario_nome]
        
        if not meus_dados.empty:
            st.line_chart(meus_dados.set_index('Data')['Nota'])
            st.dataframe(meus_dados)
        else:
            st.warning("Realize seu primeiro simulado para ver o gráfico.")
    except:
        st.error("Erro ao carregar aba 'Resultados'. Verifique se ela existe na planilha.")
