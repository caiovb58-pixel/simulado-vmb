import streamlit as st
import random
import time
from questoes import BANCO_QUESTOES

st.set_page_config(page_title="Simulado ANCORD - VMB Invest", page_icon="⚖️")

# --- FUNÇÃO DO CRONÔMETRO EM TEMPO REAL ---
@st.fragment
def renderizar_cronometro(sidebar_placeholder):
    while not st.session_state.get('finalizado', False):
        tempo_limite = 30 * 60
        inicio = st.session_state.get('inicio_tempo', time.time())
        tempo_passado = time.time() - inicio
        tempo_restante = max(0, tempo_limite - tempo_passado)

        if tempo_restante <= 0:
            st.session_state.finalizado = True
            st.rerun()
            break

        mins, secs = divmod(int(tempo_restante), 60)
        
        with sidebar_placeholder.container():
            st.title("⏳ Tempo")
            cor = "red" if tempo_restante < 300 else "white"
            st.markdown(f"<h1 style='text-align: center; color: {cor};'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
            if tempo_restante < 300:
                st.warning("⚠️ Menos de 5 min!")
        
        time.sleep(1)

# 1. ESTADO INICIAL
if 'simulado_iniciado' not in st.session_state:
    st.session_state.simulado_iniciado = False
if 'finalizado' not in st.session_state:
    st.session_state.finalizado = False
if 'questoes_sorteadas' not in st.session_state:
    st.session_state.questoes_sorteadas = []

# 2. MENU INICIAL
if not st.session_state.simulado_iniciado:
    st.title("🚀 Central de Simulados ANCORD")
    st.subheader("Configuração do Teste")
    
    modulos_existentes = sorted(list(set(q.get('modulo', 'Geral') for q in BANCO_QUESTOES)))
    
    materias_selecionadas = st.multiselect(
        "Selecione as matérias que deseja treinar:",
        options=modulos_existentes
    )
    
    if st.button("🚀 Iniciar Simulado"):
        banco_filtrado = [q for q in BANCO_QUESTOES if q.get('modulo') in materias_selecionadas] if materias_selecionadas else BANCO_QUESTOES
            
        if not banco_filtrado:
            st.error("Nenhuma questão encontrada para os módulos selecionados.")
        else:
            # Sorteia 20 ou o máximo disponível se for menor que 20
            qtd = min(20, len(banco_filtrado))
            st.session_state.questoes_sorteadas = random.sample(banco_filtrado, k=qtd)
            st.session_state.respostas_usuario = {}
            st.session_state.inicio_tempo = time.time()
            st.session_state.simulado_iniciado = True
            st.session_state.finalizado = False
            st.rerun()

# 3. INTERFACE DO SIMULADO
elif st.session_state.simulado_iniciado:
    # Mostra cronômetro na sidebar apenas se não finalizou
    if not st.session_state.finalizado:
        espaco_vazio_sidebar = st.sidebar.empty()
        renderizar_cronometro(espaco_vazio_sidebar)
    else:
        st.sidebar.error("🚨 Simulado Encerrado")

    st.title("✍️ Simulado em Andamento")
    
    # IMPORTANTE: Se as questões sumirem, o loop abaixo não terá o que mostrar.
    # Usamos o 'questoes_sorteadas' que foi salvo no clique do botão.
    with st.form("form_simulado"):
        for i, q in enumerate(st.session_state.questoes_sorteadas):
            st.markdown(f"**Questão {i+1}** | `{q.get('modulo', 'ANCORD')}`")
            st.write(q['pergunta'])
            
            key = f"q_{i}"
            opcoes = q['opcoes']
            
            # Recupera resposta anterior se houver para não perder no reload do cronômetro
            idx_anterior = None
            if key in st.session_state.respostas_usuario:
                idx_anterior = list(opcoes.keys()).index(st.session_state.respostas_usuario[key])

            st.session_state.respostas_usuario[key] = st.radio(
                "Alternativas:", 
                options=list(opcoes.keys()), 
                format_func=lambda x: f"{x}) {opcoes[x]}",
                key=key,
                index=idx_anterior,
                disabled=st.session_state.finalizado
            )
            st.divider()

        submeteu = st.form_submit_button("🏁 Finalizar e Ver Resultado")
        if submeteu:
            st.session_state.finalizado = True
            st.rerun()

    # 4. GABARITO E FEEDBACK
    if st.session_state.finalizado:
        total_q = len(st.session_state.questoes_sorteadas)
        acertos = sum(1 for i, q in enumerate(st.session_state.questoes_sorteadas) 
                      if st.session_state.respostas_usuario.get(f"q_{i}") == q['resposta_correta'])
        
        nota = (acertos / total_q) * 100 if total_q > 0 else 0
        st.header(f"Resultado: {nota:.1f}%")
        
        if nota >= 70:
            st.success(f"Aprovado! {acertos} de {total_q} acertos.")
        else:
            st.error(f"Reprovado. {acertos} de {total_q} acertos (Mínimo 70%).")

        for i, q in enumerate(st.session_state.questoes_sorteadas):
            resp = st.session_state.respostas_usuario.get(f"q_{i}")
            correta = q['resposta_correta']
            with st.expander(f"Questão {i+1} - {'✅' if resp == correta else '❌'}"):
                st.write(f"**Sua resposta:** {resp}) {q['opcoes'].get(resp, 'Não respondida')}")
                st.write(f"**Gabarito:** {correta}) {q['opcoes'][correta]}")
                st.info(f"**Explicação:** {q['explicacao']}")

        if st.button("🔄 Novo Simulado"):
            st.session_state.simulado_iniciado = False
            st.session_state.finalizado = False
            st.session_state.questoes_sorteadas = []
            st.rerun()
