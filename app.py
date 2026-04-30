import streamlit as st
import random
from questoes import BANCO_QUESTOES

st.set_page_config(page_title="Simulado SDR - VMB Invest", page_icon="📈")

# 1. Lógica de Inicialização e Embaralhamento
if 'questoes_sorteadas' not in st.session_state:
    # Sorteia 20 questões aleatórias do banco sem repetir
    st.session_state.questoes_sorteadas = random.sample(BANCO_QUESTOES, k=min(20, len(BANCO_QUESTOES)))
    st.session_state.respostas_usuario = {}
    st.session_state.finalizado = False

st.title("🎯 Simulado de Qualificação SDR")
st.subheader("Padrão Ancord | VMB Invest")

# 2. Exibição das Questões
for i, q in enumerate(st.session_state.questoes_sorteadas):
    st.markdown(f"**Questão {i+1}:** {q['pergunta']}")
    
    # Armazena a resposta no estado da sessão
    key = f"q_{i}"
    st.session_state.respostas_usuario[key] = st.radio(
        "Selecione a opção:", 
        q['opcoes'], 
        key=key,
        index=None
    )
    st.divider()

# 3. Finalização e Score
if st.button("Finalizar Simulado"):
    acertos = 0
    for i, q in enumerate(st.session_state.questoes_sorteadas):
        resp = st.session_state.respostas_usuario.get(f"q_{i}")
        # Pega a letra inicial da opção (A, B, C ou D)
        if resp and resp.startswith(q['correta']):
            acertos += 1
            
    nota = (acertos / len(st.session_state.questoes_sorteadas)) * 100
    
    st.metric("Sua Nota", f"{nota:.1f}%")
    
    if nota >= 70:
        st.success(f"Aprovado! Você acertou {acertos} de {len(st.session_state.questoes_sorteadas)}.")
    else:
        st.error(f"Reprovado. Acertos: {acertos}. O mínimo é 70%.")
        
    if st.button("Tentar Novamente (Novo Sorteio)"):
        del st.session_state.questoes_sorteadas
        st.rerun()
