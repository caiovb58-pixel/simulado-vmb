import streamlit as st
import random
from questoes import BANCO_QUESTOES

st.set_page_config(page_title="Simulado ANCORD - VMB Invest", page_icon="⚖️")

# Inicialização do Estado
if 'questoes_sorteadas' not in st.session_state:
    # Sorteia 20 questões aleatórias do banco
    st.session_state.questoes_sorteadas = random.sample(BANCO_QUESTOES, k=min(20, len(BANCO_QUESTOES)))
    st.session_state.respostas_usuario = {}
    st.session_state.finalizado = False

st.title("🎓 Simulado Oficial ANCORD")
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

# Botão de Finalização
if not st.session_state.finalizado:
    if st.button("Finalizar e Ver Gabarito"):
        st.session_state.finalizado = True
        st.rerun()

# Resultado e Feedback Detalhado
if st.session_state.finalizado:
    acertos = 0
    st.header("📊 Resultado do Simulado")
    
    for i, q in enumerate(st.session_state.questoes_sorteadas):
        resp = st.session_state.respostas_usuario.get(f"q_{i}")
        acertou = resp and resp.startswith(q['correta'])
        if acertou:
            acertos += 1
            
    nota = (acertos / len(st.session_state.questoes_sorteadas)) * 100
    st.metric("Sua Nota Final", f"{nota:.1f}%")
    
    if nota >= 70:
        st.success("APROVADO! Você atingiu o critério global.")
    else:
        st.error("REPROVADO. Continue estudando os módulos técnicos.")

    st.markdown("### 📝 Revisão e Feedback das Questões")
    for i, q in enumerate(st.session_state.questoes_sorteadas):
        resp = st.session_state.respostas_usuario.get(f"q_{i}")
        correta = q['correta']
        
        with st.expander(f"Ver Gabarito - Questão {i+1}"):
            if resp and resp.startswith(correta):
                st.write("✅ **Você acertou!**")
            else:
                st.write(f"❌ **Você errou.** Resposta correta: **{correta}**")
            
            st.info(f"**Explicação Técnica:** {q['feedback']}")

    if st.button("Reiniciar Novo Simulado"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
    else:
        st.error(f"Reprovado. Acertos: {acertos}. O mínimo é 70%.")
        
    if st.button("Tentar Novamente (Novo Simulado)"):
        del st.session_state.questoes_sorteadas
        st.rerun()
