import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime
from questoes import BANCO_QUESTOES
from streamlit_gsheets import GSheetsConnection

# Configuração da página e Tema Fixo (Configurar .streamlit/config.toml para dark)
st.set_page_config(page_title="Simulado ANCORD - VMB Invest", page_icon="⚖️")

# Como o tema é fixo escuro, usamos o logo de fundo branco para contraste
st.image("vmb_logo_fundo_branco.png", use_container_width=True)

# --- FUNÇÃO PARA SALVAR NO GOOGLE SHEETS ---
def salvar_resultado(nome, materias, acertos, total):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        nova_linha = pd.DataFrame([{
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Nome": nome,
            "Materias": ", ".join(materias) if materias else "Geral",
            "Acertos": acertos,
            "Total": total,
            "Aproveitamento": f"{(acertos/total)*100:.1f}%"
        }])
        
        # Lê dados existentes e anexa o novo
        dados_existentes = conn.read(worksheet="Resultados")
        dados_atualizados = pd.concat([dados_existentes, nova_linha], ignore_index=True)
        
        conn.update(worksheet="Resultados", data=dados_atualizados)
    except Exception as e:
        st.error(f"Erro ao salvar dados: {e}")

# --- FUNÇÃO DO CRONÔMETRO ---
@st.fragment(run_every=1)
def renderizar_cronometro():
    tempo_limite = 30 * 60
    tempo_passado = time.time() - st.session_state.inicio_tempo
    tempo_restante = max(0, tempo_limite - tempo_passado)

    if tempo_restante <= 0:
        st.session_state.finalizado = True
        st.rerun()

    mins, secs = divmod(int(tempo_restante), 60)
    
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
if 'dados_enviados' not in st.session_state:
    st.session_state.dados_enviados = False

# 2. MENU INICIAL
if not st.session_state.simulado_iniciado:
    st.title("🚀 Central de Simulados ANCORD")
    
    # Identificação do SDR
    nome_usuario = st.text_input("Seu Nome Completo:", placeholder="Ex: Caio Vitor")
    
    st.subheader("Configuração do Teste")
    modulos_existentes = sorted(list(set(q.get('modulo', 'Geral') for q in BANCO_QUESTOES)))
    
    materias_selecionadas = st.multiselect(
        "Selecione as matérias:",
        options=modulos_existentes
    )
    
    if st.button("🚀 Iniciar Simulado"):
        if not nome_usuario:
            st.error("Por favor, insira seu nome para iniciar.")
        else:
            banco_filtrado = [q for q in BANCO_QUESTOES if q.get('modulo') in materias_selecionadas] if materias_selecionadas else BANCO_QUESTOES
                
            if banco_filtrado:
                st.session_state.nome_usuario = nome_usuario
                st.session_state.materias_selecionadas = materias_selecionadas
                qtd = min(20, len(banco_filtrado))
                st.session_state.questoes_sorteadas = random.sample(banco_filtrado, k=qtd)
                st.session_state.respostas_usuario = {}
                st.session_state.inicio_tempo = time.time()
                st.session_state.simulado_iniciado = True
                st.session_state.finalizado = False
                st.session_state.dados_enviados = False
                st.rerun()

# 3. INTERFACE DO SIMULADO
else:
    if not st.session_state.finalizado:
        with st.sidebar:
            st.write(f"SDR: **{st.session_state.nome_usuario}**")
            renderizar_cronometro()
    else:
        st.sidebar.error("🚨 Simulado Encerrado")

    st.title("✍️ Simulado em Andamento")
    
    if not st.session_state.finalizado:
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
                    index=idx
                )
                st.divider()

            if st.form_submit_button("🏁 Finalizar e Ver Resultado"):
                st.session_state.finalizado = True
                st.rerun()

    # 4. GABARITO E ENVIO DE DADOS
    else:
        total = len(st.session_state.questoes_sorteadas)
        acertos = sum(1 for i, q in enumerate(st.session_state.questoes_sorteadas) 
                      if st.session_state.respostas_usuario.get(f"q_{i}") == q['resposta_correta'])
        percentual = (acertos / total) * 100

        # Lógica de envio único para a planilha
        if not st.session_state.dados_enviados:
            salvar_resultado(st.session_state.nome_usuario, st.session_state.materias_selecionadas, acertos, total)
            st.session_state.dados_enviados = True

        st.header("📊 Resultado do Simulado")
        col1, col2 = st.columns(2)
        col1.metric("Acertos", f"{acertos} / {total}")
        col2.metric("Aproveitamento", f"{percentual:.1f}%")

        if percentual >= 70:
            st.success("✅ Parabéns! Você atingiu a meta para aprovação.")
        else:
            st.error("❌ Atenção! Você ficou abaixo dos 70% exigidos.")

        st.divider()
        st.subheader("📝 Revisão das Questões")

        for i, q in enumerate(st.session_state.questoes_sorteadas):
            resp_usuario = st.session_state.respostas_usuario.get(f"q_{i}")
            correta = q['resposta_correta']
            foi_correta = resp_usuario == correta
            titulo_expander = f"Questão {i+1}: {'✅ ACERTO' if foi_correta else '❌ ERRO'}"
            
            with st.expander(titulo_expander):
                st.write(f"**{q['pergunta']}**")
                for letra, texto in q['opcoes'].items():
                    if letra == correta:
                        st.markdown(f"🟢 **{letra}) {texto} (Correta)**")
                    elif letra == resp_usuario:
                        st.markdown(f"🔴 ~~{letra}) {texto} (Sua resposta)~~")
                    else:
                        st.write(f"{letra}) {texto}")
                st.info(f"**Explicação:** {q.get('explicacao', 'Sem explicação disponível.')}")

        if st.button("🔄 Iniciar Novo Simulado"):
            for k in ['simulado_iniciado', 'finalizado', 'questoes_sorteadas', 'respostas_usuario', 'dados_enviados']:
                if k in st.session_state: 
                    del st.session_state[k]
            st.rerun()
