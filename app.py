import streamlit as st
import random
import time
from questoes import BANCO_QUESTOES

st.set_page_config(page_title="Simulado ANCORD - VMB Invest", page_icon="⚖️")

# --- FUNÇÃO DO CRONÔMETRO REFORMULADA ---
# O segredo é o run_every=1. Ele substitui o loop 'while' e o 'time.sleep'
@st.fragment(run_every=1)
def renderizar_cronometro():
    if st.session_state.simulado_iniciado and not st.session_state.finalizado:
        tempo_limite = 30 * 60
        tempo_passado = time.time() - st.session_state.inicio_tempo
        tempo_restante = max(0, tempo_limite - tempo_passado)

        if tempo_restante <= 0:
            st.session_state.finalizado = True
            st.rerun()

        mins, secs = divmod(int(tempo_restante), 60)
        
        # Renderiza direto na sidebar dentro do fragmento
        with st.sidebar:
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
        "Selecione as matérias que deseja treinar:",
        options=modulos_existentes
    )
    
    if st.button("🚀 Iniciar Simulado"):
        banco_filtrado = [q for q in BANCO_QUESTOES if q.get('modulo') in materias_selecionadas] if materias_selecionadas else BANCO_QUESTOES
            
        if not banco_filtrado:
            st.error("Nenhuma questão encontrada.")
        else:
            qtd = min(20, len(banco_filtrado))
            st.session_state.questoes_sorteadas = random.sample(banco_filtrado, k=qtd)
            st.session_state.respostas_usuario = {}
            st.session_state.inicio_tempo = time.time()
            st.session_state.simulado_iniciado = True
            st.session_state.finalizado = False
            st.rerun()

# 3. INTERFACE DO SIMULADO
else:
    # Chamada do cronômetro (ele agora roda de forma independente)
    renderizar_cronometro()

    st.title("✍️ Simulado em Andamento")
    
    # O formulário agora consegue ler st.session_state.questoes_sorteadas livremente
    with st.form("form_simulado"):
        for i, q in enumerate(st.session_state.questoes_sorteadas):
            st.markdown(f"**Questão {i+1}** | `{q.get('modulo', 'ANCORD')}`")
            st.write(q['pergunta'])
            
            key = f"q_{i}"
            opcoes = q['opcoes']
            
            # Buscamos a resposta se ela já existir para não resetar o rádio
            res_atual = st.session_state.respostas_usuario.get(key)
            idx_anterior = list(opcoes.keys()).index(res_atual) if res_atual in opcoes else None

            st.session_state.respostas_usuario[key] = st.radio(
                "Alternativas:", 
                options=list(opcoes.keys()), 
                format_func=lambda x: f"{x}) {opcoes[x]}",
                key=key,
                index=idx_anterior,
                disabled=st.session_state.finalizado
            )
            st.divider()

        if st.form_submit_button("🏁 Finalizar e Ver Resultado"):
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
            for key in ['simulado_iniciado', 'finalizado', 'questoes_sorteadas', 'respostas_usuario']:
                if key in st.session_state: del st.session_state[key]
            st.rerun()
