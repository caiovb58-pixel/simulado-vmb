import streamlit as st
import random
import time
import pandas as pd
import os
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection

# TENTA IMPORTAR O BANCO DE QUESTÕES
try:
    from questoes import BANCO_QUESTOES
except ImportError:
    st.error("Erro: O arquivo 'questoes.py' não foi encontrado.")
    st.stop()

# --- CONFIGURAÇÃO DO CRONOGRAMA ---
# Mapeamento dos simulados por semanas
DIC_SIMULADOS = {
    "Simulado 1 (Semanas 1 e 2)": ["Atividade do AAI", "Lavagem de Dinheiro"],
    "Simulado 2 (Semanas 3 e 4)": ["Mercado de Capitais", "Securitização e Recebíveis", "Derivativos"],
    "Simulado 3 (Semanas 5 e 6)": ["Fundos de Investimentos", "Outros Fundos", "Clube de Investimentos"],
    "Simulado 4 (Semanas 7 e 8)": ["Mercado Financeiro", "Sistema Financeiro Nacional"],
    "Simulado 5 (Semanas 9 e 10)": ["Instituições Financeiras", "Economia"],
    "Simulado 6 (Semanas 11 e 12)": ["Matemática Financeira", "Administração de Risco", "Clube de Investimentos"]
}

# 1. Configuração da página
st.set_page_config(page_title="Simulado ANCORD - VMB Invest", page_icon="⚖️", layout="wide")

# (Mantenha o CSS e as funções de Login/Logout que você já tem...)
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #002e5d; color: white; }
    .stRadio > label { font-weight: bold; }
    .timer-container { 
        position: fixed; top: 50px; right: 20px; z-index: 1000;
        background-color: white; padding: 10px; border: 2px solid #ff4b4b; border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .timer-text { font-size: 20px; font-weight: bold; color: #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

if 'logado' not in st.session_state: st.session_state.logado = False
if 'usuario_nome' not in st.session_state: st.session_state.usuario_nome = ""
if 'simulado_iniciado' not in st.session_state: st.session_state.simulado_iniciado = False
if 'tempo_fim' not in st.session_state: st.session_state.tempo_fim = None
if 'primeiro_acesso' not in st.session_state: st.session_state.primeiro_acesso = True
if 'menu_atual' not in st.session_state: st.session_state.menu_atual = "Simulado ANCORD"

def logout():
    for key in list(st.session_state.keys()): del st.session_state[key]
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
    except: return False

# --- TELA DE LOGIN (Omitida por brevidade, manter igual a sua) ---
if not st.session_state.logado:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if os.path.exists("logo_vmb.png"): st.image("logo_vmb.png", width=200)
        else: st.title("VMB Invest")
        st.subheader("Acesso ao Simulado")
        with st.form("login"):
            u = st.text_input("Usuário")
            p = st.text_input("Senha", type="password")
            if st.form_submit_button("Entrar"):
                if verificar_login(u, p):
                    st.session_state.logado = True
                    st.session_state.usuario_nome = u.strip()
                    st.rerun()
                else: st.error("Credenciais inválidas")
    st.stop()

if st.session_state.primeiro_acesso:
    st.title(f"Bem-vindo, {st.session_state.usuario_nome}!")
    st.markdown("### Regras e Instruções do Simulado...")
    if st.button("Entendido, ir para o Simulado"):
        st.session_state.primeiro_acesso = False
        st.session_state.menu_atual = "Simulado ANCORD"
        st.rerun()
    st.stop()

with st.sidebar:
    if os.path.exists("logo_vmb.png"): st.image("logo_vmb.png", width=150)
    st.write(f"👤 **{st.session_state.usuario_nome}**")
    opcoes_menu = ["Simulado ANCORD", "Evolução"]
    escolha = st.radio("Navegação", opcoes_menu, index=opcoes_menu.index(st.session_state.menu_atual))
    if escolha != st.session_state.menu_atual:
        st.session_state.menu_atual = escolha
        st.rerun()
    st.markdown("---")
    if st.button("🚪 Sair"): logout()

conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)

# --- PÁGINA: SIMULADO ---
if st.session_state.menu_atual == "Simulado ANCORD":
    if not st.session_state.simulado_iniciado:
        st.title("Configurar Novo Simulado Quinzenal")
        
        # Seleção do Simulado baseado nas semanas
        simulado_selecionado = st.selectbox("Escolha o Simulado (Cronograma 12 Semanas):", list(DIC_SIMULADOS.keys()))
        materias = DIC_SIMULADOS[simulado_selecionado]
        
        st.info(f"Este simulado conterá questões de: {', '.join(materias)}")
        
        # Parâmetros fixos conforme sua solicitação (20 questões / 30 min)
        qtd = 20 

        if st.button("🚀 INICIAR SIMULADO"):
            # Filtra questões que pertençam a qualquer uma das matérias das duas semanas
            pool = [q for q in BANCO_QUESTOES if q['modulo'] in materias]
            
            if len(pool) >= 1:
                st.session_state.questoes_sorteadas = random.sample(pool, min(len(pool), qtd))
                st.session_state.respostas_usuario = {}
                st.session_state.tempo_fim = datetime.now() + timedelta(minutes=30)
                st.session_state.simulado_iniciado = True
                st.session_state.simulado_nome = simulado_selecionado # Para salvar no histórico
                st.rerun()
            else:
                st.warning(f"Não encontramos questões cadastradas para os módulos: {materias}")

    else:
        # --- EXECUÇÃO DO SIMULADO ---
        tempo_atual = datetime.now()
        restante = st.session_state.tempo_fim - tempo_atual
        
        if restante.total_seconds() <= 0:
            st.error("Tempo esgotado!")
            st.session_state.simulado_iniciado = False
            time.sleep(2)
            st.rerun()
        
        mins, secs = divmod(int(restante.total_seconds()), 60)
        st.markdown(f'<div class="timer-container"><span class="timer-text">⏱️ {st.session_state.simulado_nome} | Faltam: {mins:02d}:{secs:02d}</span></div>', unsafe_allow_html=True)

        with st.form("simulado_form"):
            for idx, q in enumerate(st.session_state.questoes_sorteadas):
                # Exibe o módulo da questão para o SDR saber do que se trata
                st.markdown(f"**Questão {idx+1}** <span style='color:#002e5d; font-weight:bold; font-size:14px;'>[{q['modulo']}]</span>", unsafe_allow_html=True)
                st.write(q['pergunta'])
                ops = [f"{k}) {v}" for k, v in q['opcoes'].items()]
                st.session_state.respostas_usuario[idx] = st.radio("Sua resposta:", ops, key=f"quest_{idx}", index=None)
                st.markdown("---")
            
            enviado = st.form_submit_button("FINALIZAR SIMULADO E SALVAR")

        if enviado:
            acertos = sum(1 for idx, q in enumerate(st.session_state.questoes_sorteadas) 
                         if st.session_state.respostas_usuario[idx] and st.session_state.respostas_usuario[idx].startswith(q['resposta_correta']))
            
            total = len(st.session_state.questoes_sorteadas)
            nota_final = (acertos / total) * 100
            
            # (Lógica de salvamento igual à sua, mas adicionando o nome do simulado se quiser no futuro)
            try:
                df_res = conn.read(worksheet="Resultados")
                novo_registro = pd.DataFrame([{
                    "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Usuario": st.session_state.usuario_nome,
                    "Simulado": st.session_state.simulado_nome,
                    "Acertos": acertos, "Total": total, "Nota": nota_final,
                    "Status": "Aprovado" if nota_final >= 70 else "Reprovado"
                }])
                conn.update(worksheet="Resultados", data=pd.concat([df_res, novo_registro], ignore_index=True))
                
                if nota_final >= 70:
                    st.success(f"🔥 APROVADO! Nota: {nota_final:.1f}%")
                    st.balloons()
                else:
                    st.error(f"⚠️ REPROVADO. Nota: {nota_final:.1f}%")
                
                st.session_state.simulado_iniciado = False
                time.sleep(3)
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")

# --- PÁGINA: EVOLUÇÃO (Mantenha igual) ---
elif st.session_state.menu_atual == "Evolução":
    st.title("Desempenho Histórico")
    try:
        df = conn.read(worksheet="Resultados")
        dados_user = df[df['Usuario'] == st.session_state.usuario_nome]
        if not dados_user.empty:
            st.dataframe(dados_user.sort_values(by="Data", ascending=False), use_container_width=True)
            st.line_chart(dados_user.set_index("Data")["Nota"])
        else: st.warning("Sem histórico.")
    except: st.error("Erro ao carregar dados.")
