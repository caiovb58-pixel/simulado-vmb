import streamlit as st
import random
import time
from questoes import BANCO_QUESTOES

st.set_page_config(page_title="Simulado ANCORD - VMB Invest", page_icon="⚖️")

# Configuração do Tempo (em minutos)
TEMPO_LIMITE_MINUTOS = 60

# Inicialização do Estado
if 'questoes_sorteadas' not in st.session_state:
    st.session_state.questoes_sorteadas = random.sample(BANCO_QUESTOES, k=min(20, len(BANCO_QUESTOES)))
    st.session_state.respostas_usuario = {}
    st.session_state.finalizado = False
    st.session_state.inicio_tempo = time.time()

# Lógica do Cronômetro na Sidebar
tempo_passado = time.time() - st.session_state.inicio_tempo
tempo_restante = (TEMPO_LIMITE_MINUTOS * 60) - tempo_passado

st.sidebar.title("⏳ Cronômetro")
if tempo_restante > 0 and not st.session_state.finalizado:
    mins, secs = divmod(int(tempo_restante), 60)
    st.sidebar.header(f"{mins:02d}:{secs:02d}")
    if tempo_restante < 300: # Aviso quando faltar 5 min
        st.sidebar.warning("Faltam menos de 5 minutos!")
else:
    if not st.session_state.finalizado:
        st.session_state.finalizado = True
        st.sidebar.error("Tempo Esgotado!")
        st.rerun()

st.title("🎓 Simulado Oficial ANCORD")
st.markdown(f"**Regras:** 20 questões aleatórias | Tempo: {TEMPO_LIMITE_MINUTOS} min | Aprovação: 70%")
st.markdown("---")

# Exibição das Questões
for i, q in enumerate(st.session_state.questoes_sorteadas):
    st.markdown(f"**Questão {i+1}** | *Módulo: {q['modulo']}*")
    st.write(q['pergunta'])
    
    key = f"q_{i}"
    st.session_state.respostas_usuario[key] = st.radio(
        "Selecione a opção correta:", 
        q['opcoes'], 
        key=key,
        index=None,
        disabled=st.session_state.finalizado
    )
    st.divider()

if not st.session_state.finalizado:
    if st.button("Finalizar e Ver Gabarito"):
        st.session_state.finalizado = True
        st.rerun()

# Feedback e Revisão
if st.session_state.finalizado:
    acertos = 0
    st.header("📊 Resultado do Simulado")
    
    for i, q in enumerate(st.session_state.questoes_sorteadas):
        resp = st.session_state.respostas_usuario.get(f"q_{i}")
        if resp and resp.startswith(q['correta']):
            acertos += 1
            
    nota = (acertos / len(st.session_state.questoes_sorteadas)) * 100
    st.metric("Sua Nota Final", f"{nota:.1f}%")
    
    # Validação de Módulos Específicos (Ex: CVM 497 e PLD exigem 50%)
    st.markdown("### 📝 Revisão Detalhada")
    for i, q in enumerate(st.session_state.questoes_sorteadas):
        resp = st.session_state.respostas_usuario.get(f"q_{i}")
        with st.expander(f"Questão {i+1} - {q['modulo']}"):
            if resp and resp.startswith(q['correta']):
                st.write("✅ **Correto**")
            else:
                st.write(f"❌ **Incorreto**. Resposta: {q['correta']}")
            st.info(f"**Gabarito Comentado:** {q['feedback']}")

    if st.button("Reiniciar Novo Simulado"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
