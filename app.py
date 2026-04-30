import streamlit as st
import random
import time
from questoes import BANCO_QUESTOES

st.set_page_config(page_title="Simulado ANCORD - VMB Invest", page_icon="⚖️")

# --- FUNÇÃO DO CRONÔMETRO EM TEMPO REAL ---
@st.fragment
def renderizar_cronometro(sidebar_placeholder):
    # O loop agora usa o placeholder que passamos como "terreno" para trabalhar
    while not st.session_state.finalizado:
        tempo_limite = 30 * 60
        tempo_passado = time.time() - st.session_state.inicio_tempo
        tempo_restante = tempo_limite - tempo_passado

        if tempo_restante <= 0:
            st.session_state.finalizado = True
            st.rerun()
            break

        mins, secs = divmod(int(tempo_restante), 60)
        
        # Estilização visual do cronômetro
        with sidebar_placeholder.container():
            st.title("⏳ Tempo")
            cor = "red" if tempo_restante < 300 else "white"
            st.markdown(f"<h1 style='text-align: center; color: {cor};'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
            if tempo_restante < 300:
                st.warning("⚠️ Menos de 5 min!")
        
        time.sleep(1) # Atualiza a cada 1 segundo

# 1. ESTADO INICIAL
if 'simulado_iniciado' not in st.session_state:
    st.session_state.simulado_iniciado = False
if 'finalizado' not in st.session_state:
    st.session_state.finalizado = False

# 2. MENU INICIAL
if not st.session_state.simulado_iniciado:
    st.title("🚀 Central de Simulados ANCORD")
    st.subheader("Configuração do Teste")
    
    modulos_existentes = sorted(list(set(q['modulo'] for q in BANCO_QUESTOES)))
    
    materias_selecionadas = st.multiselect(
        "Selecione as matérias que deseja treinar:",
        options=modulos_existentes
    )
    
    if st.button("🚀 Iniciar Simulado"):
        banco_filtrado = [q for q in BANCO_QUESTOES if q['modulo'] in materias_selecionadas] if materias_selecionadas else BANCO_QUESTOES
            
        if len(banco_filtrado) < 20:
            st.warning(f"O banco possui apenas {len(banco_filtrado)} questões.")
        else:
            st.session_state.questoes_sorteadas = random.sample(banco_filtrado, k=20)
            st.session_state.respostas_usuario = {}
            st.session_state.finalizado = False
            st.session_state.inicio_tempo = time.time()
            st.session_state.simulado_iniciado = True
            st.rerun()

# 3. INTERFACE DO SIMULADO
else:
    # --- AQUI ESTÁ A CORREÇÃO ---
    if not st.session_state.finalizado:
        # Primeiro criamos o espaço na sidebar
        espaco_vazio_sidebar = st.sidebar.empty()
        # Depois passamos esse espaço para a função
        renderizar_cronometro(espaco_vazio_sidebar)
    else:
        st.sidebar.error("🚨 Simulado Encerrado")
    # ----------------------------

    st.title("✍️ Simulado em Andamento")
    
    with st.form("form_simulado"):
        for i, q in enumerate(st.session_state.questoes_sorteadas):
            st.markdown(f"**Questão {i+1} de 20** | `{q['modulo']}`")
            st.write(q['pergunta'])
            
            key = f"q_{i}"
            opcoes_disponiveis = list(q['opcoes'].keys())
            
            st.session_state.respostas_usuario[key] = st.radio(
                "Alternativas:", 
                options=opcoes_disponiveis, 
                format_func=lambda x: f"{x}) {q['opcoes'][x]}",
                key=key,
                index=None if key not in st.session_state.respostas_usuario else opcoes_disponiveis.index(st.session_state.respostas_usuario[key]),
                disabled=st.session_state.finalizado
            )
            st.divider()

        submeteu = st.form_submit_button("🏁 Finalizar e Ver Resultado")
        if submeteu:
            st.session_state.finalizado = True
            st.rerun()

    # 4. GABARITO E FEEDBACK
    if st.session_state.finalizado:
        acertos = sum(1 for i, q in enumerate(st.session_state.questoes_sorteadas) 
                      if st.session_state.respostas_usuario.get(f"q_{i}") == q['resposta_correta'])
        
        nota = (acertos / 20) * 100
        st.header(f"Resultado: {nota:.1f}%")
        
        if nota >= 70:
            st.success(f"Aprovado! {acertos} acertos.")
        else:
            st.error(f"Reprovado. {acertos} acertos (Mínimo 14).")

        for i, q in enumerate(st.session_state.questoes_sorteadas):
            resp = st.session_state.respostas_usuario.get(f"q_{i}")
            correta = q['resposta_correta']
            with st.expander(f"Questão {i+1} - {'✅' if resp == correta else '❌'}"):
                st.write(f"**Sua resposta:** {resp}) {q['opcoes'].get(resp, 'N/A')}")
                st.write(f"**Gabarito:** {correta}) {q['opcoes'][correta]}")
                st.info(f"**Explicação:** {q['explicacao']}")

        if st.button("🔄 Novo Simulado"):
            st.session_state.simulado_iniciado = False
            st.session_state.finalizado = False
            st.rerun()
