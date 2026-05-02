import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime
from questoes import BANCO_QUESTOES
from streamlit_gsheets import GSheetsConnection

# 1. Configuração da página e Identidade Visual
st.set_page_config(page_title="Simulado ANCORD - VMB Invest", page_icon="⚖️", layout="wide")

# Logo ajustada para fundo escuro
try:
    st.sidebar.image("vmb_logo_fundo_preto.png", use_container_width=True)
except:
    st.sidebar.title("VMB Invest")

# --- NAVEGAÇÃO LATERAL ---
st.sidebar.divider()
menu = st.sidebar.radio("Navegação", ["📝 Realizar Simulado", "📈 Minha Evolução"])

# --- FUNÇÃO PARA SALVAR NO GOOGLE SHEETS ---
def salvar_resultado(nome, materias, acertos, total):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)
        try:
            dados_existentes = conn.read(worksheet="Resultados")
        except Exception:
            dados_existentes = pd.DataFrame(columns=["Data", "Nome", "Materias", "Acertos", "Total", "Aproveitamento"])
        
        nova_linha = pd.DataFrame([{
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Nome": nome,
            "Materias": ", ".join(materias) if materias else "Geral",
            "Acertos": acertos,
            "Total": total,
            "Aproveitamento": f"{(acertos/total)*100:.1f}%"
        }])
        
        if dados_existentes is None or dados_existentes.empty:
            dados_atualizados = nova_linha
        else:
            dados_existentes = dados_existentes.dropna(how='all', axis=0).dropna(how='all', axis=1)
            dados_atualizados = pd.concat([dados_existentes, nova_linha], ignore_index=True)
        
        conn.update(worksheet="Resultados", data=dados_atualizados)
        st.success("✅ Desempenho registrado na planilha!")
    except Exception as e:
        st.error(f"Erro ao salvar dados: {e}")

# --- TELA: MINHA EVOLUÇÃO ---
if menu == "📈 Minha Evolução":
    st.title("📊 Painel de Evolução do SDR")
    login_nome = st.text_input("Digite seu Nome Completo para ver seu histórico:", placeholder="Ex: Caio Vitor")
    
    if login_nome:
        try:
            conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)
            df = conn.read(worksheet="Resultados")
            
            # Filtra os resultados pelo nome do SDR
            user_data = df[df['Nome'].str.contains(login_nome, case=False, na=False)].copy()
            
            if not user_data.empty:
                # Tratamento de dados para o gráfico
                user_data['Aproveitamento_Num'] = user_data['Aproveitamento'].str.replace('%', '').astype(float)
                user_data['Data_DT'] = pd.to_datetime(user_data['Data'], dayfirst=True)
                user_data = user_data.sort_values('Data_DT')

                # Métricas principais
                media = user_data['Aproveitamento_Num'].mean()
                total_sims = len(user_data)
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Total de Simulados", total_sims)
                m2.metric("Média de Acertos", f"{media:.1f}%")
                m3.metric("Melhor Resultado", f"{user_data['Aproveitamento_Num'].max()}%")

                st.divider()
                
                # Gráfico de Evolução
                st.subheader("📈 Progresso ao Longo do Tempo")
                st.line_chart(user_data.set_index('Data_DT')['Aproveitamento_Num'])

                # Tabela de Histórico
                st.subheader("📋 Histórico Detalhado")
                st.dataframe(user_data[['Data', 'Materias', 'Acertos', 'Total', 'Aproveitamento']], use_container_width=True)
            else:
                st.info("Ainda não encontramos resultados para este nome. Faça seu primeiro simulado!")
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")

# --- TELA: REALIZAR SIMULADO ---
else:
    # --- FUNÇÃO DO CRONÔMETRO ---
    @st.fragment(run_every=1)
    def renderizar_cronometro():
        if 'inicio_tempo' in st.session_state:
            tempo_limite = 30 * 60 
            tempo_passado = time.time() - st.session_state.inicio_tempo
            tempo_restante = max(0, tempo_limite - tempo_passado)

            if tempo_restante <= 0:
                st.session_state.finalizado = True
                st.rerun()

            mins, secs = divmod(int(tempo_restante), 60)
            st.sidebar.title("⏳ Tempo")
            cor = "red" if tempo_restante < 300 else "white"
            st.sidebar.markdown(f"<h1 style='text-align: center; color: {cor};'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)

    # --- CONTROLE DE ESTADO ---
    if 'simulado_iniciado' not in st.session_state: st.session_state.simulado_iniciado = False
    if 'finalizado' not in st.session_state: st.session_state.finalizado = False
    if 'questoes_sorteadas' not in st.session_state: st.session_state.questoes_sorteadas = []
    if 'respostas_usuario' not in st.session_state: st.session_state.respostas_usuario = {}
    if 'dados_enviados' not in st.session_state: st.session_state.dados_enviados = False

    if not st.session_state.simulado_iniciado:
        st.title("🚀 Central de Simulados ANCORD")
        nome_usuario = st.text_input("Seu Nome Completo:", placeholder="Ex: Caio Vitor")
        
        modulos_existentes = sorted(list(set(q.get('modulo', 'Geral') for q in BANCO_QUESTOES)))
        materias_selecionadas = st.multiselect("Selecione as matérias:", options=modulos_existentes)
        
        if st.button("🚀 Iniciar Simulado"):
            if not nome_usuario:
                st.error("Por favor, insira seu nome.")
            else:
                banco_filtrado = [q for q in BANCO_QUESTOES if q.get('modulo') in materias_selecionadas] if materias_selecionadas else BANCO_QUESTOES
                if banco_filtrado:
                    st.session_state.respostas_usuario = {}
                    st.session_state.nome_usuario = nome_usuario
                    st.session_state.materias_selecionadas = materias_selecionadas
                    st.session_state.questoes_sorteadas = random.sample(banco_filtrado, k=min(20, len(banco_filtrado)))
                    st.session_state.inicio_tempo = time.time()
                    st.session_state.simulado_iniciado = True
                    st.session_state.dados_enviados = False
                    st.rerun()

    elif not st.session_state.finalizado:
        with st.sidebar:
            st.write(f"SDR: **{st.session_state.get('nome_usuario', '')}**")
            renderizar_cronometro()
                
        st.title("✍️ Simulado em Andamento")
        with st.form("form_simulado"):
            for i, q in enumerate(st.session_state.questoes_sorteadas):
                st.markdown(f"**Questão {i+1}** | `{q.get('modulo', 'ANCORD')}`")
                st.write(q['pergunta'])
                key = f"q_{i}"
                opcoes = q['opcoes']
                st.session_state.respostas_usuario[key] = st.radio(
                    "Alternativas:", options=list(opcoes.keys()), 
                    format_func=lambda x: f"{x}) {opcoes[x]}", key=key, index=None
                )
                st.divider()
            if st.form_submit_button("🏁 Finalizar e Ver Resultado"):
                st.session_state.finalizado = True
                st.rerun()

    else:
        total = len(st.session_state.questoes_sorteadas)
        acertos = sum(1 for i, q in enumerate(st.session_state.questoes_sorteadas) 
                      if st.session_state.respostas_usuario.get(f"q_{i}") == q['resposta_correta'])
        
        if not st.session_state.dados_enviados:
            salvar_resultado(st.session_state.nome_usuario, st.session_state.materias_selecionadas, acertos, total)
            st.session_state.dados_enviados = True

        st.header("📊 Resultado")
        c1, c2 = st.columns(2)
        c1.metric("Acertos", f"{acertos} / {total}")
        c2.metric("Aproveitamento", f"{(acertos/total)*100:.1f}%")

        if st.button("🔄 Novo Simulado"):
            for k in ['simulado_iniciado', 'finalizado', 'questoes_sorteadas', 'respostas_usuario', 'dados_enviados', 'inicio_tempo']:
                if k in st.session_state: del st.session_state[k]
            st.rerun()
