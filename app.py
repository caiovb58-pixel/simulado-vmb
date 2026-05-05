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
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .timer-text { font-size: 20px; font-weight: bold; color: #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# --- CONTROLE DE ESTADO ---
# Inicialização robusta para evitar quedas no recarregamento
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'usuario_nome' not in st.session_state:
    st.session_state.usuario_nome = ""
if 'simulado_iniciado' not in st.session_state:
    st.session_state.simulado_iniciado = False
if 'tempo_fim' not in st.session_state:
    st.session_state.tempo_fim = None
if 'menu_atual' not in st.session_state:
    st.session_state.menu_atual = "Boas-vindas"

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
    
    # Sincroniza o rádio com o estado do menu para permitir o redirecionamento via botão
    opcoes_menu = ["Boas-vindas", "Simulado ANCORD", "Evolução"]
    indice_atual = opcoes_menu.index(st.session_state.menu_atual)
    
    escolha = st.radio("Navegação", opcoes_menu, index=indice_atual)
    
    # Se o usuário mudar manualmente no rádio, atualiza o estado
    if escolha != st.session_state.menu_atual:
        st.session_state.menu_atual = escolha
        st.rerun()
        
    st.markdown("---")
    if st.button("🚪 Sair"):
        logout()

conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)

# --- PÁGINA: BOAS-VINDAS ---
if st.session_state.menu_atual == "Boas-vindas":
    st.title(f"Bem-vindo, {st.session_state.usuario_nome}!")
    st.markdown("""
    ### Regras e Instruções do Simulado
    Este portal foi desenvolvido para preparar a elite da **VMB Invest** para a certificação ANCORD.
    
    *   **Meta de Aprovação:** Você precisa de no mínimo **70% de acertos** para ser considerado aprovado.
    *   **Tempo Limite:** Cada simulado tem duração máxima de **30 minutos**.
    *   **Foco Total:** Este simulado é uma ferramenta crucial para o seu desenvolvimento técnico e futuro na assessoria. Leve cada tentativa a sério.
    *   **Não saia da página:** Recarregar a página ou fechar o navegador encerrará sua tentativa atual.
    
    > "O sucesso é a soma de pequenos esforços repetidos dia após dia."
    """)
    
    # CORREÇÃO: Agora o botão muda o estado do menu e dá rerun
    if st.button("Entendido, ir para o Simulado"):
        st.session_state.menu_atual = "Simulado ANCORD"
        st.rerun()

# --- PÁGINA: SIMULADO ---
elif st.session_state.menu_atual == "Simulado ANCORD":
    if not st.session_state.simulado_iniciado:
        st.title("Configurar Novo Simulado")
        modulos = sorted(list(set([q['modulo'] for q in BANCO_QUESTOES])))
        sel = st.multiselect("Selecione os módulos:", modulos, default=modulos)
        qtd = st.number_input("Quantidade de questões:", min_value=1, max_value=80, value=20)

        if st.button("🚀 INICIAR SIMULADO"):
            pool = [q for q in BANCO_QUESTOES if q['modulo'] in sel]
            if pool:
                st.session_state.questoes_sorteadas = random.sample(pool, min(len(pool), qtd))
                st.session_state.respostas_usuario = {}
                st.session_state.tempo_fim = datetime.now() + timedelta(minutes=30)
                st.session_state.simulado_iniciado = True
                st.rerun()
            else:
                st.warning("Selecione ao menos um módulo com questões.")

    else:
        # --- CORREÇÃO DO CRONÔMETRO ---
        # Exibição do Cronômetro flutuante
        tempo_atual = datetime.now()
        restante = st.session_state.tempo_fim - tempo_atual
        
        if restante.total_seconds() <= 0:
            st.error("Tempo esgotado! O simulado será encerrado.")
            st.session_state.simulado_iniciado = False
            time.sleep(2)
            st.rerun()
        
        mins, secs = divmod(int(restante.total_seconds()), 60)
        st.markdown(f"""
            <div class="timer-container">
                <span class="timer-text">⏱️ Tempo: {mins:02d}:{secs:02d}</span>
            </div>
        """, unsafe_allow_html=True)

        # FORMULÁRIO DE QUESTÕES
        with st.form("simulado_form"):
            for idx, q in enumerate(st.session_state.questoes_sorteadas):
                st.markdown(f"**Questão {idx+1}** <span style='color:gray; font-size:12px;'>({q['modulo']})</span>", unsafe_allow_html=True)
                st.write(q['pergunta'])
                ops = [f"{k}) {v}" for k, v in q['opcoes'].items()]
                st.session_state.respostas_usuario[idx] = st.radio("Sua resposta:", ops, key=f"quest_{idx}", index=None)
                st.markdown("---")
            
            enviado = st.form_submit_button("FINALIZAR SIMULADO E SALVAR")

        if enviado:
            acertos = 0
            for idx, q in enumerate(st.session_state.questoes_sorteadas):
                resp = st.session_state.respostas_usuario[idx]
                correta = q['resposta_correta']
                if resp and resp.startswith(correta):
                    acertos += 1
                
            total = len(st.session_state.questoes_sorteadas)
            nota_final = (acertos / total) * 100
            
            if nota_final >= 70:
                st.success(f"🔥 APROVADO! Nota: {nota_final:.1f}% ({acertos}/{total})")
                st.balloons()
            else:
                st.error(f"⚠️ REPROVADO. Nota: {nota_final:.1f}% ({acertos}/{total}). Mínimo exigido: 70%.")

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
                st.info("Resultado registrado na base da VMB.")
                st.session_state.simulado_iniciado = False
                time.sleep(4)
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao salvar no GSheets: {e}")

# --- PÁGINA: EVOLUÇÃO ---
elif st.session_state.menu_atual == "Evolução":
    st.title("Desempenho Histórico")
    try:
        df = conn.read(worksheet="Resultados")
        dados_user = df[df['Usuario'] == st.session_state.usuario_nome]
        if not dados_user.empty:
            st.dataframe(dados_user.sort_values(by="Data", ascending=False), use_container_width=True)
            # Gráfico simples de evolução
            st.line_chart(dados_user.set_index("Data")["Nota"])
        else:
            st.warning("Ainda não existem registros de simulados para o seu usuário.")
    except:
        st.error("Erro ao conectar com a base de dados de evolução.")
