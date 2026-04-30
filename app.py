import streamlit as st
import random
import time
from questoes import BANCO_QUESTOES

st.set_page_config(page_title="Simulado ANCORD Pro - VMB", page_icon="⚖️")

# 1. Configurações e Filtros na Lateral
st.sidebar.title("⚙️ Configurações")

# Extrair módulos únicos do banco de dados
modulos_disponiveis = sorted(list(set(q['modulo'] for q in BANCO_QUESTOES)))
selecao_modulos = st.sidebar.multiselect(
    "Filtrar por Módulos (Deixe vazio para tudo):",
    options=modulos_disponiveis,
    default=[]
)

quantidade_questoes = st.sidebar.slider("Quantidade de questões:", 5, 40, 20)
tempo_limite = st.sidebar.number_input("Tempo (minutos):", 10, 120, 60)

# Botão para Resetar / Iniciar novo sorteio
if st.sidebar.button("Gerar Novo Simulado"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# 2. Lógica de Sorteio Filtrado
if 'questoes_sorteadas' not in st.session_state:
    # Filtrar banco se houver seleção
    if selecao_modulos:
        banco_filtrado = [q for q in BANCO_QUESTOES if q['modulo'] in selecao_modulos]
    else:
        banco_filtrado = BANCO_QUESTOES
    
    # Sorteio aleatório
    if len(banco_filtrado) >= quantidade_questoes:
        st.session_state.questoes_sorteadas = random.sample(banco_filtrado, k=quantidade_questoes)
    else:
        st.session_state.questoes_sorteadas = banco_filtrado # Pega o que tiver se o banco for menor que o pedido
        
    st.session_state.respostas_usuario = {}
    st.session_state.finalizado = False
    st.session_state.inicio_tempo = time.time()

# 3. Cronômetro
tempo_passado = time.time() - st.session_state.inicio_tempo
tempo_restante = (tempo_limite * 60) - tempo_passado

if tempo_restante > 0 and not st.session_state.finalizado:
    mins, secs = divmod(int(tempo_restante), 60)
    st.sidebar.subheader(f"⏳ Tempo: {mins:02d}:{secs:02d}")
else:
    if not st.session_state.finalizado:
        st.session_state.finalizado = True
        st.rerun()

st.title("🎓 Simulado Personalizado ANCORD")
st.info(f"Modo: {', '.join(selecao_modulos) if selecao_modulos else 'Simulado Completo'}")

# 4. Exibição
for i, q in enumerate(st.session_state.questoes_sorteadas):
    st.markdown(f"**Questão {i+1}** | `{q['modulo']}`")
    st.write(q['pergunta'])
    
    key = f"q_{i}"
    st.session_state.respostas_usuario[key] = st.radio(
        "Selecione:", q['opcoes'], key=key, index=None, disabled=st.session_state.finalizado
    )
    st.divider()

if not st.session_state.finalizado:
    if st.button("Finalizar Simulado"):
        st.session_state.finalizado = True
        st.rerun()

# 5. Feedback e Gabarito
if st.session_state.finalizado:
    acertos = sum(1 for i, q in enumerate(st.session_state.questoes_sorteadas) 
                  if st.session_state.respostas_usuario.get(f"q_{i}") and st.session_state.respostas_usuario.get(f"q_{i}").startswith(q['correta']))
    
    nota = (acertos / len(st.session_state.questoes_sorteadas)) * 100
    st.metric("Resultado", f"{nota:.1f}%", f"{acertos} acertos")

    st.subheader("📝 Revisão Técnica")
    for i, q in enumerate(st.session_state.questoes_sorteadas):
        with st.expander(f"Questão {i+1} - Gabarito"):
            st.write(f"**Sua resposta:** {st.session_state.respostas_usuario.get(f'q_{i}')}")
            st.write(f"**Correta:** {q['correta']}")
            st.info(f"**Explicação:** {q['feedback']}")
