import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime
from questoes import BANCO_QUESTOES
from streamlit_gsheets import GSheetsConnection

# 1. Configuração da página e Identidade Visual
st.set_page_config(page_title="Simulado ANCORD - VMB Invest", page_icon="⚖️")

# Logo (Certifique-se de que o arquivo existe no repositório)
try:
    st.image("vmb_logo_fundo_branco.png", use_container_width=True)
except:
    st.title("VMB Invest - Simulados")

# --- FUNÇÃO PARA SALVAR NO GOOGLE SHEETS ---
def salvar_resultado(nome, materias, acertos, total):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)
        
        # Tenta ler os dados atuais para anexar a nova linha
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
        
        if dados_existentes is None or dados_existentes.empty:
            dados_atualizados = nova_linha
        else:
            dados_existentes = dados_existentes.dropna(how='all', axis=0).dropna(how='all', axis=1)
            dados_atualizados = pd.concat([dados_existentes, nova_linha], ignore_index=True)
        
        conn.update(worksheet="Resultados", data=dados_atualizados)
        st.success("✅ Desempenho registrado na planilha com sucesso!")
        
    except Exception as e:
        st.error(f"Erro ao salvar dados: {e}")

# --- FUNÇÃO DO CRONÔMETRO (Fragment para não recarregar a página toda) ---
@st.fragment(run_every=1)
def renderizar_cronometro():
    if 'inicio_tempo' in st.session_state:
        tempo_limite = 30 * 60 # 30 minutos
        tempo_passado = time.time() - st.session_state.inicio_tempo
        tempo_restante = max(0, tempo_limite - tempo_passado)

        if tempo_restante <= 0:
            st.session_state.finalizado = True
            st.rerun()

        mins, secs = divmod(int(tempo_restante), 60)
        
        st.title("⏳ Tempo")
        cor = "red" if tempo_restante < 300 else "white"
        st.markdown(f"<h1 style='text-align: center; color: {cor};'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)

# --- CONTROLE DE ESTADO (Session State) ---
if 'simulado_iniciado' not in st.session_state:
    st.session_state.simulado_iniciado = False
if 'finalizado' not in st.session_state:
    st.session_state.finalizado = False
if 'questoes_sorteadas' not in st.session_state:
    st.session_state.questoes_sorteadas = []
if 'respostas_usuario' not in st.session_state:
    st.session_state.respostas_usuario = {}
if 'dados_enviados' not in st.session_state:
    st.session_state.dados_enviados = False

# --- LÓGICA DE NAVEGAÇÃO ---

# Interface 1: Menu de Início
if not st.session_state.simulado_iniciado:
    st.title("🚀 Central de Simulados ANCORD")
    nome_usuario = st.text_input("Seu Nome Completo:", placeholder="Ex: Caio Vitor")
    
    modulos_existentes = sorted(list(set(q.get('modulo', 'Geral') for q in BANCO_QUESTOES)))
    materias_selecionadas = st.multiselect("Selecione as matérias:", options=modulos_existentes)
    
    if st.button("🚀 Iniciar Simulado"):
        if not nome_usuario:
            st.error("Por favor, insira seu nome.")
        else:
            banco_filtrado = [q for q in BANCO_QUESTOES if q.get('modulo') in materias_selecionadas] if materias_selecionadas else BANCO_QUESTOES
            if banco_filtrado:
                st.session_state.nome_usuario = nome_usuario
                st.session_state.materias_selecionadas = materias_selecionadas
                st.session_state.questoes_sorteadas = random.sample(banco_filtrado, k=min(20, len(banco_filtrado)))
                st.session_state.inicio_tempo = time.time()
                st.session_state.simulado_iniciado = True
                st.rerun()

# Interface 2: O Simulado
elif not st.session_state.finalizado:
    with st.sidebar:
        st.write(f"SDR: **{st.session_state.nome_usuario}**")
        renderizar_cronometro()
            
    st.title("✍️ Simulado em Andamento")
    with st.form("form_simulado"):
        for i, q in enumerate(st.session_state.questoes_sorteadas):
            st.markdown(f"**Questão {i+1}** | `{q.get('modulo', 'ANCORD')}`")
            st.write(q['pergunta'])
            
            key = f"q_{i}"
            opcoes = q['opcoes']
            st.session_state.respostas_usuario[key] = st.radio(
                "Alternativas:", 
                options=list(opcoes.keys()), 
                format_func=lambda x: f"{x}) {opcoes[x]}",
                key=key
            )
            st.divider()

        if st.form_submit_button("🏁 Finalizar e Ver Resultado"):
            st.session_state.finalizado = True
            st.rerun()

# Interface 3: Resultado e Gabarito
else:
    total = len(st.session_state.questoes_sorteadas)
    acertos = sum(1 for i, q in enumerate(st.session_state.questoes_sorteadas) 
                  if st.session_state.respostas_usuario.get(f"q_{i}") == q['resposta_correta'])
    
    if not st.session_state.dados_enviados:
        salvar_resultado(st.session_state.nome_usuario, st.session_state.materias_selecionadas, acertos, total)
        st.session_state.dados_enviados = True

    st.header("📊 Resultado do Simulado")
    col1, col2 = st.columns(2)
    col1.metric("Acertos", f"{acertos} / {total}")
    col2.metric("Aproveitamento", f"{(acertos/total)*100:.1f}%")

    if st.button("🔄 Novo Simulado"):
        for k in ['simulado_iniciado', 'finalizado', 'questoes_sorteadas', 'respostas_usuario', 'dados_enviados']:
            del st.session_state[k]
        st.rerun()
