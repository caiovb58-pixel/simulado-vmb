import streamlit as st
import random
import time
from questoes import BANCO_QUESTOES

st.set_page_config(page_title="Simulado ANCORD - VMB Invest", page_icon="⚖️")

# 1. ESTADO INICIAL E CONFIGURAÇÃO
if 'simulado_iniciado' not in st.session_state:
    st.session_state.simulado_iniciado = False

# 2. MENU INICIAL
if not st.session_state.simulado_iniciado:
    st.title("🚀 Central de Simulados ANCORD")
    st.subheader("Configuração do Teste")
    
    modulos_existentes = sorted(list(set(q['modulo'] for q in BANCO_QUESTOES)))
    
    materias_selecionadas = st.multiselect(
        "Selecione as matérias que deseja treinar:",
        options=modulos_existentes,
        help="Se deixar vazio, o simulado será sobre todo o conteúdo."
    )
    
    st.info("ℹ️ Configuração fixa: 20 questões | Tempo: 30 minutos.")
    
    if st.button("🚀 Iniciar Simulado"):
        if materias_selecionadas:
            banco_filtrado = [q for q in BANCO_QUESTOES if q['modulo'] in materias_selecionadas]
        else:
            banco_filtrado = BANCO_QUESTOES
            
        if len(banco_filtrado) < 20:
            st.warning(f"O banco possui apenas {len(banco_filtrado)} questões. Selecione mais temas.")
        else:
            st.session_state.questoes_sorteadas = random.sample(banco_filtrado, k=20)
            st.session_state.respostas_usuario = {}
            st.session_state.finalizado = False
            st.session_state.inicio_tempo = time.time()
            st.session_state.simulado_iniciado = True
            st.rerun()

# 3. INTERFACE DO SIMULADO
else:
    tempo_limite = 30 * 60
    tempo_passado = time.time() - st.session_state.inicio_tempo
    tempo_restante = tempo_limite - tempo_passado

    st.sidebar.title("⏳ Tempo Restante")
    if tempo_restante > 0 and not st.session_state.finalizado:
        mins, secs = divmod(int(tempo_restante), 60)
        st.sidebar.header(f"{mins:02d}:{secs:02d}")
    else:
        if not st.session_state.finalizado:
            st.session_state.finalizado = True
            st.sidebar.error("🚨 Tempo Esgotado!")
            st.rerun()

    st.title("✍️ Simulado em Andamento")
    
    for i, q in enumerate(st.session_state.questoes_sorteadas):
        st.markdown(f"**Questão {i+1} de 20** | `{q['modulo']}`")
        st.write(q['pergunta'])
        
        key = f"q_{i}"
        
        # --- ALTERAÇÃO AQUI: format_func exibe "Letra) Conteúdo" ---
        opcoes_disponiveis = list(q['opcoes'].keys())
        st.session_state.respostas_usuario[key] = st.radio(
            "Escolha a alternativa:", 
            options=opcoes_disponiveis, 
            format_func=lambda x: f"{x}) {q['opcoes'][x]}", # Exibe a letra e o texto
            key=key, 
            index=None, 
            disabled=st.session_state.finalizado
        )
        st.divider()

    if not st.session_state.finalizado:
        if st.button("🏁 Finalizar Simulado"):
            st.session_state.finalizado = True
            st.rerun()

    # 4. GABARITO E FEEDBACK
    if st.session_state.finalizado:
        # Ajuste na contagem: comparamos apenas a letra escolhida com a letra da 'resposta_correta'
        acertos = sum(1 for i, q in enumerate(st.session_state.questoes_sorteadas) 
                      if st.session_state.respostas_usuario.get(f"q_{i}") == q['resposta_correta'])
        
        nota = (acertos / 20) * 100
        st.header(f"Resultado: {nota:.1f}%")
        
        if nota >= 70:
            st.success(f"Excelente! Você acertou {acertos} de 20 questões.")
        else:
            st.error(f"Atenção! Você acertou {acertos} de 20. Mínimo: 14 acertos (70%).")

        st.subheader("📚 Revisão das Respostas")
        for i, q in enumerate(st.session_state.questoes_sorteadas):
            resp_escolhida = st.session_state.respostas_usuario.get(f"q_{i}")
            correta = q['resposta_correta']
            
            with st.expander(f"Questão {i+1} - {'✅' if resp_escolhida == correta else '❌'}"):
                # Exibindo o texto da resposta escolhida
                txt_escolhida = q['opcoes'].get(resp_escolhida, "Não respondida")
                st.write(f"**Sua resposta:** {resp_escolhida}) {txt_escolhida}")
                st.write(f"**Gabarito:** {correta}) {q['opcoes'][correta]}")
                st.info(f"**Explicação:** {q['explicacao']}")

        if st.button("🔄 Voltar ao Menu Inicial"):
            st.session_state.simulado_iniciado = False
            st.rerun()
