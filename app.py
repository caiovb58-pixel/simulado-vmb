import streamlit as st
import random
import time
from questoes import BANCO_QUESTOES

st.set_page_config(page_title="Simulado ANCORD - VMB Invest", page_icon="⚖️")

# --- FUNÇÃO DO CRONÔMETRO CORRIGIDA ---
@st.fragment(run_every=1)
def renderizar_cronometro():
    # Cálculo do tempo
    tempo_limite = 30 * 60
    tempo_passado = time.time() - st.session_state.inicio_tempo
    tempo_restante = max(0, tempo_limite - tempo_passado)

    if tempo_restante <= 0:
        st.session_state.finalizado = True
        st.rerun()

    mins, secs = divmod(int(tempo_restante), 60)
    
    # Renderização: Note que não usamos 'st.sidebar' aqui dentro
    # A função será chamada já dentro do contexto da sidebar
    st.title("⏳ Tempo")
    cor = "red" if tempo_restante < 300 else "white"
    st.markdown(f"<h1 style='text-align: center; color: {cor};'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
    if tempo_restante < 300:
        st.warning("⚠️ Menos de 5 min!")

# 1. ESTADO INICIAL
if 'simulado_iniciado' not in st.session_state:
    st.session_state.simulado_iniciado = False
if 'finalizado' not in st.session_state:
    st.session_state.finalizado = False
if 'questoes_sorteadas' not in st.session_state:
    st.session_state.questoes_sorteadas = []
if 'respostas_usuario' not in st.session_state:
    st.session_state.respostas_usuario = {}

# 2. MENU INICIAL
if not st.session_state.simulado_iniciado:
    st.title("🚀 Central de Simulados ANCORD")
    st.subheader("Configuração do Teste")
    
    modulos_existentes = sorted(list(set(q.get('modulo', 'Geral') for q in BANCO_QUESTOES)))
    
    materias_selecionadas = st.multiselect(
        "Selecione as matérias:",
        options=modulos_existentes
    )
    
    if st.button("🚀 Iniciar Simulado"):
        banco_filtrado = [q for q in BANCO_QUESTOES if q.get('modulo') in materias_selecionadas] if materias_selecionadas else BANCO_QUESTOES
            
        if banco_filtrado:
            qtd = min(20, len(banco_filtrado))
            st.session_state.questoes_sorteadas = random.sample(banco_filtrado, k=qtd)
            st.session_state.respostas_usuario = {}
            st.session_state.inicio_tempo = time.time()
            st.session_state.simulado_iniciado = True
            st.session_state.finalizado = False
            st.rerun()

# 3. INTERFACE DO SIMULADO
else:
    # --- CORREÇÃO DA CHAMADA ---
    if not st.session_state.finalizado:
        with st.sidebar: # Abrimos a sidebar AQUI
            renderizar_cronometro() # Chamamos o fragmento AQUI DENTRO
    else:
        st.sidebar.error("🚨 Simulado Encerrado")

    st.title("✍️ Simulado em Andamento")
    
    with st.form("form_simulado"):
        for i, q in enumerate(st.session_state.questoes_sorteadas):
            st.markdown(f"**Questão {i+1}** | `{q.get('modulo', 'ANCORD')}`")
            st.write(q['pergunta'])
            
            key = f"q_{i}"
            opcoes = q['opcoes']
            res_atual = st.session_state.respostas_usuario.get(key)
            idx = list(opcoes.keys()).index(res_atual) if res_atual in opcoes else None

            st.session_state.respostas_usuario[key] = st.radio(
                "Alternativas:", 
                options=list(opcoes.keys()), 
                format_func=lambda x: f"{x}) {opcoes[x]}",
                key=key,
                index=idx,
                disabled=st.session_state.finalizado
            )
            st.divider()

        if st.form_submit_button("🏁 Finalizar"):
            st.session_state.finalizado = True
            st.rerun()

    # 4. GABARITO (Resumido para o exemplo)
    if st.session_state.finalizado:
        acertos = sum(1 for i, q in enumerate(st.session_state.questoes_sorteadas) 
                      if st.session_state.respostas_usuario.get(f"q_{i}") == q['resposta_correta'])
        st.header(f"Resultado: {(acertos/len(st.session_state.questoes_sorteadas))*100:.1f}%")
        
        if st.button("🔄 Novo Simulado"):
            for k in ['simulado_iniciado', 'finalizado', 'questoes_sorteadas', 'respostas_usuario']:
                if k in st.session_state: del st.session_state[k]
            st.rerun()
