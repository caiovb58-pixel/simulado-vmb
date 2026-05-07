import streamlit as st
import random
import pandas as pd
from datetime import datetime
import time
import os
import json
import re
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection

# --- QUESTÕES ---
try:
    from questoes import BANCO_QUESTOES
except ImportError:
    st.error("Arquivo 'questoes.py' não encontrado no repositório.")
    st.stop()

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="VMB - Simulado de Elite", layout="wide", page_icon="⚡")

# --- CSS PREMIUM (Injeção de Estilo) ---
def inject_custom_css():
    st.markdown("""
    <style>
        /* Fundo geral mais sofisticado */
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        
        /* Ocultar elementos padrão do Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Cards Premium com Glassmorphism e Hover */
        div[data-testid="stVerticalBlock"] div[style*="border"] {
            background: linear-gradient(145deg, rgba(22,27,34,0.95), rgba(14,17,23,0.98)) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 16px !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
            padding: 20px !important;
            transition: all 0.3s ease !important;
        }
        div[data-testid="stVerticalBlock"] div[style*="border"]:hover {
            transform: translateY(-4px) !important;
            border: 1px solid #3B82F6 !important;
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.2) !important;
        }

        /* Botões com Glow */
        .stButton>button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            border: none !important;
        }
        .stButton>button[kind="primary"] {
            background: linear-gradient(90deg, #2563EB, #1D4ED8) !important;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4) !important;
        }
        .stButton>button[kind="primary"]:hover {
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6) !important;
            transform: scale(1.02);
        }

        /* Inputs de Texto Modernos */
        .stTextInput input {
            border-radius: 8px !important;
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: white !important;
        }
        .stTextInput input:focus {
            border-color: #3B82F6 !important;
            box-shadow: 0 0 0 1px #3B82F6 !important;
        }

        /* Títulos */
        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
            font-weight: 700 !important;
            letter-spacing: -0.5px;
        }
        
        /* Barra Lateral */
        section[data-testid="stSidebar"] {
            background-color: #161B22 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# Módulos por simulado
DIC_SIMULADOS = {
    "Simulado 1 (Semanas 1 e 2)":["A Atividade do Assessor de Investimentos (AI)", "Lavagem de Dinheiro"],
    "Simulado 2 (Semanas 3 e 4)":["Mercado de Capitais", "Securitização de Recebíveis", "Derivativos"],
    "Simulado 3 (Semanas 5 e 6)":["Fundos de Investimentos", "Outros Fundos de Investimentos", "Clubes de Investimentos"],
    "Simulado 4 (Semanas 7 e 8)":["Mercado Financeiro", "Sistema Financeiro Nacional"],
    "Simulado 5 (Semanas 9 e 10)":["Instituições e Intermediadores Financeiros", "Economia"],
    "Simulado 6 (Semanas 11 e 12)":["Matemática Financeira", "Administração de Risco"]
}
SIMULADOS_ORDEM = list(DIC_SIMULADOS.keys())

# --- ESTADO DA SESSÃO ---
if "logado" not in st.session_state:
    st.session_state.update({
        "logado": False,
        "usuario": "",
        "page": "Login",
        "simulado_atual_indice": 0,
        "simulado_nome": "",
        "modulos_selecionados":[],
        "quiz_atual": None,
        "inicio_time": None,
        "fim_time": None,
        "respostas_usuario": {},
        "resultado_salvo": False,
        "xp_usuario": 0,
        "nivel_usuario": "Trainee"
    })

# --- FUNÇÕES CORE ---
def calcular_gamificacao(df_user):
    """Calcula XP e Nível baseado no histórico"""
    simulados_feitos = len(df_user)
    xp = simulados_feitos * 150  # 150 XP por simulado concluído
    
    if xp < 300: nivel = "SDR Trainee"
    elif xp < 750: nivel = "SDR Júnior"
    elif xp < 1200: nivel = "SDR Pleno"
    elif xp < 2000: nivel = "SDR Sênior"
    else: nivel = "SDR Elite 🏆"
    
    return xp, nivel

def selecionar_questoes_balanceadas(banco, modulos, total_desejado=20):
    questoes_por_modulo = {mod:[] for mod in modulos}
    for q in banco:
        if q["modulo"] in modulos:
            questoes_por_modulo[q["modulo"]].append(q)
            
    total_disponivel = sum(len(qs) for qs in questoes_por_modulo.values())
    if total_disponivel <= total_desejado:
        todas =[q for qs in questoes_por_modulo.values() for q in qs]
        random.shuffle(todas)
        return todas
        
    selecionadas =[]
    modulos_restantes =[mod for mod in modulos if len(questoes_por_modulo[mod]) > 0]
    vagas = total_desejado
    
    while vagas > 0 and modulos_restantes:
        cota = vagas // len(modulos_restantes)
        resto = vagas % len(modulos_restantes)
        novos_modulos_restantes =[]
        
        for i, mod in enumerate(modulos_restantes):
            cota_atual = cota + (1 if i < resto else 0)
            disponivel = len(questoes_por_modulo[mod])
            
            if disponivel <= cota_atual:
                selecionadas.extend(questoes_por_modulo[mod])
                vagas -= disponivel
                questoes_por_modulo[mod] =[]
            else:
                novos_modulos_restantes.append(mod)
                
        if len(novos_modulos_restantes) == len(modulos_restantes):
            for i, mod in enumerate(novos_modulos_restantes):
                cota_atual = cota + (1 if i < resto else 0)
                escolhidas = random.sample(questoes_por_modulo[mod], cota_atual)
                selecionadas.extend(escolhidas)
                vagas -= cota_atual
            break
            
        modulos_restantes = novos_modulos_restantes
        
    random.shuffle(selecionadas)
    return selecionadas

# --- INTERFACE ---
if not st.session_state.logado:
    # --- TELA DE LOGIN PREMIUM ---
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1.5, 2, 1.5])
    
    with col2:
        st.markdown("""
        <div style='text-align: center;'>
            <h1 style='color: #FAFAFA; margin-bottom: 0px;'>VMB INVEST</h1>
            <p style='color: #8B949E; font-size: 18px; margin-top: 0px;'>Treinamento de Alta Performance</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container(border=True):
            user = st.text_input("Usuário", placeholder="ID do Agente")
            pw = st.text_input("Senha", type="password", placeholder="••••••••")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("ACESSAR PLATAFORMA ⚡", use_container_width=True, type="primary"):
                with st.spinner("Autenticando credenciais..."):
                    try:
                        conn = st.connection("gsheets", type=GSheetsConnection)
                        df_usuarios = conn.read(worksheet="Usuarios", ttl=0) 
                        user_match = df_usuarios[
                            (df_usuarios['Usuario'].astype(str).str.lower() == user.lower()) & 
                            (df_usuarios['Senha'].astype(str) == pw)
                        ]
                        
                        if not user_match.empty or (user.lower() == "admin" and pw == "admin"):
                            usuario_formatado = user.capitalize()
                            st.session_state.logado = True
                            st.session_state.usuario = usuario_formatado
                            
                            # SINCRONIZAR PROGRESSO
                            try:
                                df_historico = conn.read(worksheet="Historico", ttl=0)
                                df_user_hist = df_historico[df_historico['Usuario'] == usuario_formatado]
                                
                                # Gamificação
                                xp, nivel = calcular_gamificacao(df_user_hist)
                                st.session_state.xp_usuario = xp
                                st.session_state.nivel_usuario = nivel

                                max_passed = -1
                                if not df_user_hist.empty:
                                    for _, row in df_user_hist.iterrows():
                                        nota = pd.to_numeric(str(row['Nota (%)']).replace(',', '.'), errors='coerce')
                                        if pd.notna(nota) and nota >= 70.0:
                                            sim_name = row['Simulado']
                                            if sim_name in SIMULADOS_ORDEM:
                                                idx = SIMULADOS_ORDEM.index(sim_name)
                                                if idx > max_passed: max_passed = idx
                                
                                prox_indice = min(max_passed + 1, len(SIMULADOS_ORDEM) - 1)
                                st.session_state.simulado_atual_indice = prox_indice
                            except Exception:
                                st.session_state.simulado_atual_indice = 0

                            st.session_state.page = "Home"
                            st.rerun()
                        else:
                            st.error("Acesso negado. Credenciais inválidas.")
                    except Exception as e:
                        st.error("Falha de conexão com os servidores.")

else:
    # --- BARRA LATERAL GAMIFICADA ---
    with st.sidebar:
        st.markdown(f"""
        <div style="background: rgba(37, 99, 235, 0.1); padding: 15px; border-radius: 12px; border: 1px solid rgba(37, 99, 235, 0.2); margin-bottom: 20px;">
            <div style="font-size: 14px; color: #8B949E;">Agente Conectado</div>
            <div style="font-size: 20px; font-weight: bold; color: white;">👤 {st.session_state.usuario}</div>
            <div style="margin-top: 10px; font-size: 13px; font-weight: bold; color: #3B82F6;">{st.session_state.nivel_usuario}</div>
            <div style="background: #0E1117; border-radius: 10px; height: 8px; margin-top: 5px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #3B82F6, #60A5FA); width: {(st.session_state.xp_usuario % 1000) / 10}%; height: 100%;"></div>
            </div>
            <div style="font-size: 11px; color: #8B949E; margin-top: 4px; text-align: right;">{st.session_state.xp_usuario} XP</div>
        </div>
        """, unsafe_allow_html=True)
        
        menu = st.radio("Navegação",["Dashboard Principal", "Evolução e IA", "Sair do Sistema"])
    
    if menu == "Sair do Sistema":
        st.session_state.clear()
        st.rerun()
    elif menu == "Evolução e IA" and st.session_state.page != "Evolução":
        st.session_state.page = "Evolução"
        st.rerun()
    elif menu == "Dashboard Principal" and st.session_state.page not in ["Home", "Instrucoes", "Simulado", "Resultado"]:
        st.session_state.page = "Home"
        st.rerun()

    # --- HOME / DASHBOARD ---
    if st.session_state.page == "Home":
        st.title("🎯 Central de Treinamento")
        
        # BURACO PARA AS MÉTRICAS INICIAIS (Buscando rápido no BD)
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            df_historico = conn.read(worksheet="Historico", ttl=0)
            df_user_hist = df_historico[df_historico['Usuario'] == st.session_state.usuario]
            
            avg_score = df_user_hist['Nota (%)'].mean() if not df_user_hist.empty else 0
            max_score = df_user_hist['Nota (%)'].max() if not df_user_hist.empty else 0
            qtd_sim = len(df_user_hist)
            
            # HTML CARDS (Top Level)
            st.markdown(f"""
            <div style="display: flex; gap: 15px; margin-bottom: 25px;">
                <div style="flex: 1; background: #161B22; padding: 15px; border-radius: 12px; border: 1px solid #30363D;">
                    <div style="color: #8B949E; font-size: 13px;">Aproveitamento Geral</div>
                    <div style="color: white; font-size: 24px; font-weight: bold;">{avg_score:.1f}%</div>
                </div>
                <div style="flex: 1; background: #161B22; padding: 15px; border-radius: 12px; border: 1px solid #30363D;">
                    <div style="color: #8B949E; font-size: 13px;">Melhor Nota</div>
                    <div style="color: #4ADE80; font-size: 24px; font-weight: bold;">🏆 {max_score:.1f}%</div>
                </div>
                <div style="flex: 1; background: #161B22; padding: 15px; border-radius: 12px; border: 1px solid #30363D;">
                    <div style="color: #8B949E; font-size: 13px;">Simulados Concluídos</div>
                    <div style="color: white; font-size: 24px; font-weight: bold;">⚡ {qtd_sim}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        except:
            pass # Falha silenciosa nas métricas para não travar a home

        st.markdown("### Selecione sua missão")
        for i, nome_sim in enumerate(SIMULADOS_ORDEM):
            with st.container(border=True):
                col_txt, col_btn = st.columns([4, 1])
                with col_txt:
                    st.markdown(f"<h4 style='margin:0; padding:0;'>{nome_sim}</h4>", unsafe_allow_html=True)
                    st.caption(f"{', '.join(DIC_SIMULADOS[nome_sim])}")
                
                with col_btn:
                    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
                    liberado = i <= st.session_state.simulado_atual_indice
                    if liberado:
                        if st.button("Iniciar", key=f"btn_{i}", use_container_width=True, type="primary"):
                            st.session_state.simulado_nome = nome_sim
                            st.session_state.modulos_selecionados = DIC_SIMULADOS[nome_sim]
                            st.session_state.page = "Instrucoes"
                            st.rerun()
                    else:
                        st.button("Bloqueado", key=f"btn_{i}", disabled=True, use_container_width=True)

    # --- TELA DE INSTRUÇÕES ---
    elif st.session_state.page == "Instrucoes":
        st.title(f"Operação: {st.session_state.simulado_nome}")
        
        st.markdown("""
        <div style="background: rgba(234, 179, 8, 0.1); border-left: 4px solid #EAB308; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h4 style="margin-top: 0; color: #EAB308;">Protocolo de Avaliação</h4>
            <ul style="color: #D1D5DB; margin-bottom: 0;">
                <li><b>Tempo restrito:</b> Exatos 30 minutos. O cronômetro entrará em modo crítico nos últimos 5 minutos.</li>
                <li><b>Estrutura:</b> 20 questões táticas, distribuídas uniformemente.</li>
                <li><b>Integridade:</b> Simule o ambiente oficial. Sem consultas, sem interrupções.</li>
                <li><b>Alerta do Sistema:</b> Não atualize a página (F5), ou a missão será abortada com perda total de dados.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Cancelar Missão", use_container_width=True):
                st.session_state.page = "Home"
                st.rerun()
        with col2:
            if st.button("ACEITO OS TERMOS - INICIAR ⚡", type="primary", use_container_width=True):
                quiz = selecionar_questoes_balanceadas(BANCO_QUESTOES, st.session_state.modulos_selecionados, 20)
                if len(quiz) > 0:
                    st.session_state.quiz_atual = quiz
                    st.session_state.inicio_time = time.time()
                    st.session_state.resultado_salvo = False
                    st.session_state.page = "Simulado"
                    st.rerun()
                else:
                    st.error("Banco de dados insuficiente.")

    # --- EXECUÇÃO DO SIMULADO (TIMER PREMIUM) ---
    elif st.session_state.page == "Simulado" and st.session_state.quiz_atual:
        timer_container = st.empty()
        with timer_container:
            js_timer = """
            <script>
            var countDownDate = new Date().getTime() + (30 * 60 * 1000); 
            var x = setInterval(function() {
              var now = new Date().getTime();
              var distance = countDownDate - now;
              
              var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
              var seconds = Math.floor((distance % (1000 * 60)) / 1000);
              minutes = minutes < 10 ? "0" + minutes : minutes;
              seconds = seconds < 10 ? "0" + seconds : seconds;
              
              var timerDiv = document.getElementById("timer");
              var glowDiv = document.getElementById("timer-glow");
              
              timerDiv.innerHTML = "⏳ " + minutes + ":" + seconds;
              
              // EFEITO VERMELHO NEON NOS ÚLTIMOS 5 MINUTOS
              if (minutes < 5) {
                  timerDiv.style.color = "#FF4B4B";
                  glowDiv.style.boxShadow = "0 0 20px rgba(255, 75, 75, 0.6)";
                  glowDiv.style.border = "1px solid #FF4B4B";
              }
              
              if (distance < 0) {
                clearInterval(x);
                timerDiv.innerHTML = "🚨 TEMPO ESGOTADO";
              }
            }, 1000);
            </script>
            <div id="timer-glow" style="position: sticky; top: 10px; z-index: 999; background: rgba(14, 17, 23, 0.8); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); padding: 10px 30px; border-radius: 50px; width: fit-content; margin: 0 auto; box-shadow: 0 4px 15px rgba(0,0,0,0.5); transition: all 0.3s ease;">
                <h2 id="timer" style="color: #60A5FA; margin: 0; font-family: monospace; font-size: 26px;">Carregando...</h2>
            </div>
            """
            components.html(js_timer, height=80)
        
        st.write("") # Espaçamento
        with st.form("form_simulado"):
            respostas_locais = {}
            for idx, q in enumerate(st.session_state.quiz_atual):
                st.markdown(f"#### Questão {idx+1}")
                st.markdown(f"<span style='color: #8B949E; font-size: 12px;'>MÓDULO: {q['modulo'].upper()}</span>", unsafe_allow_html=True)
                st.write(q['pergunta'])
                opcoes =[f"{k}) {v}" for k, v in q.get("opcoes", {}).items()]
                
                chave_unica = f"rad_{st.session_state.simulado_atual_indice}_{q['id']}_{idx}"
                respostas_locais[idx] = st.radio("Selecione:", opcoes, key=chave_unica, index=None, label_visibility="collapsed")
                st.markdown("<hr style='opacity: 0.2;'>", unsafe_allow_html=True)
            
            submitted = st.form_submit_button("ENVIAR RESPOSTAS", use_container_width=True, type="primary")
            if submitted:
                st.session_state.fim_time = time.time()
                st.session_state.respostas_usuario = respostas_locais
                st.session_state.page = "Resultado"
                time.sleep(0.2)
                st.rerun()

    # --- RESULTADOS ---
    elif st.session_state.page == "Resultado":
        st.title("Relatório de Missão")
        
        tempo_total_segundos = st.session_state.fim_time - st.session_state.inicio_time
        minutos = int(tempo_total_segundos // 60)
        segundos = int(tempo_total_segundos % 60)
        
        acertos = 0
        total_questoes = len(st.session_state.quiz_atual)
        tempo_medio = tempo_total_segundos / total_questoes if total_questoes > 0 else 0
        
        desempenho_modulos = {}
        for idx, q in enumerate(st.session_state.quiz_atual):
            mod = q['modulo']
            if mod not in desempenho_modulos:
                desempenho_modulos[mod] = {"total": 0, "acertos": 0}
            
            desempenho_modulos[mod]["total"] += 1
            resp = st.session_state.respostas_usuario.get(idx)
            if resp and resp.startswith(q['resposta_correta']):
                acertos += 1
                desempenho_modulos[mod]["acertos"] += 1

        percentual = (acertos / total_questoes) * 100 if total_questoes > 0 else 0

        # SALVAMENTO
        if not st.session_state.resultado_salvo:
            with st.spinner("Salvando telemetria..."):
                try:
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    df_historico = conn.read(worksheet="Historico", ttl=0)
                    detalhes_mod = {mod: round((dados['acertos'] / dados['total']) * 100, 1) for mod, dados in desempenho_modulos.items()}
                    
                    novo_registro = pd.DataFrame([{
                        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "Usuario": st.session_state.usuario,
                        "Simulado": st.session_state.simulado_nome,
                        "Nota (%)": round(percentual, 1),
                        "Tempo": f"{minutos}m {segundos}s",
                        "Detalhes_Modulos": json.dumps(detalhes_mod)
                    }])
                    
                    df_atualizado = pd.concat([df_historico, novo_registro], ignore_index=True)
                    conn.update(worksheet="Historico", data=df_atualizado)
                    st.session_state.resultado_salvo = True
                except Exception as e:
                    pass

        col1, col2, col3 = st.columns(3)
        col1.metric("Nota Final", f"{percentual:.1f}%", f"{acertos}/{total_questoes}")
        col2.metric("Pace (Tempo Médio)", f"{int(tempo_medio // 60)}m {int(tempo_medio % 60)}s")
        col3.metric("Status", "APROVADO ✅" if percentual >= 70 else "REPROVADO ❌")

        st.divider()
        st.markdown("### Correção Analítica")
        for idx, q in enumerate(st.session_state.quiz_atual):
            resp_usuario = st.session_state.respostas_usuario.get(idx)
            acertou = resp_usuario and resp_usuario.startswith(q['resposta_correta'])
            letra_correta = q['resposta_correta']
            texto_correto = q['opcoes'].get(letra_correta, "")

            status_color = "#10B981" if acertou else "#EF4444"
            status_text = "Acertou" if acertou else "Errou"
            
            with st.expander(f"Q{idx+1} - {status_text} | {q['modulo']}"):
                st.write(f"**{q['pergunta']}**")
                st.markdown(f"<span style='color:{status_color}; font-weight:bold;'>Sua marcação:</span> {resp_usuario if resp_usuario else 'Em branco'}", unsafe_allow_html=True)
                if not acertou:
                    st.markdown(f"<span style='color:#10B981; font-weight:bold;'>Correta:</span> {letra_correta}) {texto_correto}", unsafe_allow_html=True)
                st.info(f"💡 **Insights:** {q.get('explicacao', '')}")

        st.write("")
        if st.button("Finalizar Análise e Voltar", type="primary", use_container_width=True):
            if percentual >= 70 and st.session_state.simulado_nome == SIMULADOS_ORDEM[st.session_state.simulado_atual_indice]:
                if st.session_state.simulado_atual_indice < len(SIMULADOS_ORDEM) - 1:
                    st.session_state.simulado_atual_indice += 1
            st.session_state.page = "Home"
            st.rerun()

    # --- TELA EVOLUÇÃO E IA ---
    elif st.session_state.page == "Evolução":
        st.title("🧠 Inteligência de Dados e Evolução")
        
        with st.spinner("Processando heurística..."):
            try:
                conn = st.connection("gsheets", type=GSheetsConnection)
                df_historico_geral = conn.read(worksheet="Historico", ttl=0)
                df_user = df_historico_geral[df_historico_geral["Usuario"] == st.session_state.usuario].copy()
                
                if not df_user.empty:
                    df_user.reset_index(drop=True, inplace=True)
                    
                    # Cálculo de Tempo
                    total_secs = 0
                    valid_times = 0
                    for t_str in df_user['Tempo']:
                        match = re.search(r'(\d+)m\s*(\d+)s', str(t_str))
                        if match:
                            total_secs += int(match.group(1)) * 60 + int(match.group(2))
                            valid_times += 1
                    
                    media_secs = total_secs // valid_times if valid_times > 0 else 0
                    
                    # Processamento JSON
                    module_scores = {}
                    for _, row in df_user.iterrows():
                        if 'Detalhes_Modulos' in df_user.columns and pd.notna(row['Detalhes_Modulos']):
                            try:
                                detalhes = json.loads(row['Detalhes_Modulos'])
                                for mod, score in detalhes.items():
                                    if mod not in module_scores: module_scores[mod] =[]
                                    module_scores[mod].append(score)
                                continue 
                            except: pass
                        
                        sim_name = row['Simulado']
                        if sim_name in DIC_SIMULADOS:
                            for mod in DIC_SIMULADOS[sim_name]:
                                if mod not in module_scores: module_scores[mod] = []
                                module_scores[mod].append(row['Nota (%)'])
                                
                    avg_module_scores = {mod: sum(scores)/len(scores) for mod, scores in module_scores.items()}

                    col_radar, col_ia = st.columns([1.2, 1])

                    with col_radar:
                        st.markdown("<h3 style='text-align:center;'>Radar de Competências</h3>", unsafe_allow_html=True)
                        if avg_module_scores:
                            df_radar = pd.DataFrame(dict(
                                Força=list(avg_module_scores.values()),
                                Modulo=list(avg_module_scores.keys())
                            ))
                            df_radar = pd.concat([df_radar, df_radar.iloc[[0]]]) 
                            
                            fig = go.Figure()
                            
                            # O Seu radar
                            fig.add_trace(go.Scatterpolar(
                                r=df_radar['Força'],
                                theta=df_radar['Modulo'],
                                fill='toself',
                                name='Sua Força',
                                line_color='#3B82F6',
                                fillcolor='rgba(59, 130, 246, 0.4)'
                            ))
                            
                            # Radar Elite (Top 10% Fictício de meta)
                            fig.add_trace(go.Scatterpolar(
                                r=[85]*len(df_radar),
                                theta=df_radar['Modulo'],
                                fill='none',
                                name='Top 10% Elite',
                                line_color='rgba(16, 185, 129, 0.5)',
                                line_dash='dash'
                            ))

                            fig.update_layout(
                                polar=dict(
                                    bgcolor='rgba(0,0,0,0)',
                                    radialaxis=dict(visible=True, range=[0, 100], gridcolor='#30363D', color='#8B949E'),
                                    angularaxis=dict(gridcolor='#30363D', color='#FAFAFA')
                                ),
                                showlegend=True,
                                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                margin=dict(l=40, r=40, t=20, b=20)
                            )
                            st.plotly_chart(fig, use_container_width=True)

                    with col_ia:
                        st.markdown("### 🧠 Diagnóstico do Mentor")
                        
                        sorted_mods = sorted(avg_module_scores.items(), key=lambda item: item[1])
                        weak_mods =[mod for mod, score in sorted_mods if score < 70]
                        strong_mods =[mod for mod, score in sorted_mods if score >= 85]
                        
                        st.markdown("""
                        <div style="background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                            <p style="color:#8B949E; font-size:14px; margin-bottom:5px;">ANÁLISE HEURÍSTICA CONCLUÍDA</p>
                        """, unsafe_allow_html=True)
                        
                        if weak_mods:
                            st.markdown(f"**🚨 Atenção Crítica:**<br>Detectei falhas estruturais em **{weak_mods[0]}**. Redirecione 80% do seu próximo ciclo de estudos para a teoria base deste módulo.", unsafe_allow_html=True)
                        if strong_mods:
                            st.markdown(f"<br>**🏆 Dominância:**<br>O módulo de **{strong_mods[-1]}** atingiu padrão de excelência. Modo manutenção ativado.", unsafe_allow_html=True)

                        st.markdown("<br>**⏱️ Pacing de Prova:**", unsafe_allow_html=True)
                        if media_secs > 1500: 
                            st.markdown("⚠️ *Velocidade de risco:* Você está usando quase todo o tempo limite. Em prova oficial, você não terá fôlego para revisar. Pratique leitura dinâmica.")
                        elif media_secs > 0 and media_secs < 600: 
                            st.markdown("⚡ *Impulsividade:* Seu tempo de resposta está muito rápido. Isso levanta suspeita de desatenção a palavras como 'EXCETO' ou dupla negação.")
                        elif media_secs > 0:
                            st.markdown("✅ *Ritmo Cadenciado:* Seu controle de tempo está perfeitamente alinhado com candidatos aprovados.")
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.divider()
                    st.subheader("Data Grid (Registros Brutos)")
                    
                    # DataFrame Premium com Barra de Progresso nativa do Streamlit
                    df_display = df_user[['Data', 'Simulado', 'Nota (%)', 'Tempo']].copy()
                    
                    st.dataframe(
                        df_display,
                        column_config={
                            "Nota (%)": st.column_config.ProgressColumn(
                                "Desempenho",
                                help="Sua nota percentual",
                                format="%f%%",
                                min_value=0,
                                max_value=100,
                            ),
                            "Data": st.column_config.TextColumn("Data da Execução"),
                            "Simulado": st.column_config.TextColumn("Missão")
                        },
                        hide_index=True,
                        use_container_width=True
                    )

                else:
                    st.info("Aguardando telemetria inicial. Faça seu primeiro simulado.")
            except Exception as e:
                st.error("Falha ao processar banco de dados da IA.")
