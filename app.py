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

# 1. Configuração da página
st.set_page_config(page_title="Simulado ANCORD - VMB Invest", page_icon="⚖️", layout="wide")

# --- ESTILIZAÇÃO CUSTOMIZADA (CSS) ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #002e5d; color: white; }
    .stRadio > label { font-weight: bold; }
    .timer-container { 
        position: fixed; top: 50px; right: 20px; z-index: 1000;
        background-color: white; padding: 10px; border: 2px solid #ff4b4b; border-radius: 10px;
    }
    .timer-text { font-size: 20px; font-weight: bold; color: #ff4b4b; }
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
    for key in list(st.session_state.keys()):
        del st.session_state[key]
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
        if os.path.exists("logo_vmb.png"):
            st.image("logo_vmb.png", width=200)
        else:
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
    if os.path.exists("logo_vmb.png"):
        st.image("logo_vmb.png", width=150)
    st.write(f"👤 **{st.session_state.usuario_nome}**")
    # Removi "Início" do rádio para ser a página padrão quando nada estiver selecionado
    menu = st.radio("Navegação", ["Boas-vindas", "Simulado ANCORD", "Evolução"])
    st.markdown("---")
    if st.button("🚪 Sair"):
        logout()

conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)

# --- PÁGINA: BOAS-VINDAS ---
if menu == "Boas-vindas":
    st.title(f"Bem-vindo, {st.session_state.usuario_nome}!")
    st.markdown("""
    ### Regras e Instruções do Simulado
    Este portal foi desenvolvido para preparar a elite da **VMB Invest** para a certificação ANCORD.
    
    *   **Meta de Aprovação:** Você precisa de no mínimo **70% de acertos** para ser considerado aprovado.
    *   **Tempo Limite:** Cada simulado tem duração máxima de **30 minutos**.
    *   **Foco Total:** Este simulado é uma ferramenta crucial para o seu desenvolvimento técnico e futuro na assessoria. Leve cada tentativa a sério.
    *   **Não saia da página:** Recarregar a página pode resetar o seu progresso atual.
    
    > "O sucesso é a soma de pequenos esforços repetidos dia após dia." - Leve seu treinamento a sério.
    """)
    if st.button("Entendido, ir para o Simulado"):
        st.info("Selecione 'Simulado ANCORD' no menu lateral para começar.")

# --- PÁGINA: SIMULADO ---
elif menu == "Simulado ANCORD":
    if not st.session_state.simulado_iniciado:
        st.title("Configurar Novo Simulado")
        modulos = sorted(list(set([q['modulo'] for q in BANCO_QUESTOES])))
        sel = st.multiselect("Selecione os módulos:", modulos, default=modulos)
        qtd = st.number_input("Quantidade de questões:", min_value=1, max_value=80, value=20)

        if st.button("🚀 INICIAR SIMULADO"):
            pool = [q for q in BANCO_QUESTOES if q['modulo'] in sel]
            st.session_state.questoes_sorteadas = random.sample(pool, min(len(pool), qtd))
            st.session_state.respostas_usuario = {}
            st.session_state.tempo_fim = datetime.now() + timedelta(minutes=30)
            st.session_state.simulado_iniciado = True
            st.rerun()

    else:
        # CRONÔMETRO EM TEMPO REAL
        timer_placeholder = st.empty()
        
        # O loop de atualização em tempo real
        tempo_atual = datetime.now()
        restante = st.session_state.tempo_fim - tempo_atual
        
        if restante.total_seconds() <= 0:
            st.error("Tempo esgotado!")
            st.session_state.simulado_iniciado = False
            st.rerun()
        
        mins, secs = divmod(int(restante.total_seconds()), 60)
        timer_placeholder.markdown(f"""
            <div class="timer-container">
                <span class="timer-text">⏱️ {mins:02d}:{secs:02d}</span>
            </div>
        """, unsafe_allow_html=True)

        # FORMULÁRIO DE QUESTÕES
        with st.form("simulado_form"):
            for idx, q in enumerate(st.session_state.questoes_sorteadas):
                st.markdown(f"**Questão {idx+1}** ({q['modulo']})")
                st.write(q['pergunta'])
                ops = [f"{k}) {v}" for k, v in q['opcoes'].items()]
                st.session_state.respostas_usuario[idx] = st.radio("Sua resposta:", ops, key=f"quest_{idx}", index=None)
                st.markdown("---")
            
            enviado = st.form_submit_button("FINALIZAR SIMULADO")

        if enviado:
            acertos = 0
            detalhes_resultado = []
            
            for idx, q in enumerate(st.session_state.questoes_sorteadas):
                resp = st.session_state.respostas_usuario[idx]
                correta = q['resposta_correta']
                if resp and resp.startswith(correta):
                    acertos += 1
                
            total = len(st.session_state.questoes_sorteadas)
            nota_final = (acertos / total) * 100
            
            # Verificação de Aprovação (70%)
            if nota_final >= 70:
                st.success(f"🔥 APROVADO! Sua nota foi {nota_final:.1f}% ({acertos}/{total})")
                st.balloons()
            else:
                st.error(f"⚠️ REPROVADO. Sua nota foi {nota_final:.1f}% ({acertos}/{total}). O mínimo é 70%.")

            # Salvar no Google Sheets
            try:
                df_res = conn.read(worksheet="Resultados")
                novo_registro = pd.DataFrame([{
                    "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Usuario": st.session_state.usuario_nome,
                    "Acertos": acertos,
                    "Total": total,
                    "Nota": nota_final,
                    "Status": "Aprovado" if nota_final >= 70 else "Reprovado"
                }])
                df_final = pd.concat([df_res, novo_registro], ignore_index=True)
                conn.update(worksheet="Resultados", data=df_final)
                st.info("Resultado salvo com sucesso.")
                st.session_state.simulado_iniciado = False
                time.sleep(3)
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")

# --- PÁGINA: EVOLUÇÃO ---
elif menu == "Evolução":
    st.title("Desempenho Histórico")
    try:
        df = conn.read(worksheet="Resultados")
        dados_user = df[df['Usuario'] == st.session_state.usuario_nome]
        if not dados_user.empty:
            st.dataframe(dados_user.sort_values(by="Data", ascending=False), use_container_width=True)
            st.line_chart(dados_user.set_index("Data")["Nota"])
        else:
            st.warning("Nenhum histórico encontrado.")
    except:
        st.error("Erro ao carregar dados.")
