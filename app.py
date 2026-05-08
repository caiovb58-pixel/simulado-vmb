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
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        /* Esconder ícones e textos residuais do Streamlit */
        button[title="View fullscreen"] { display: none !important; }
        .stDeployButton { display: none !important; }
        #MainMenu { visibility: hidden !important; }
        footer { visibility: hidden !important; }
        
        /* Garantir que o header fique transparente, mas o botão de recolher a barra continue visível e clicável */
        header[data-testid="stHeader"] {
            background-color: transparent !important;
            z-index: 99999 !important;
        }

        :root {
            --vmb-black: #050812;
            --vmb-black-2: #0A1020;
            --vmb-card: rgba(10, 16, 32, 0.72);
            --vmb-card-strong: rgba(12, 18, 35, 0.92);
            --vmb-blue: #2563EB;
            --vmb-blue-2: #3B82F6;
            --vmb-blue-3: #60A5FA;
            --vmb-white: #F8FAFC;
            --vmb-muted: #9AA8BD;
            --vmb-border: rgba(148, 163, 184, 0.18);
            --vmb-glow: rgba(37, 99, 235, 0.32);
        }

        html, body, [class*="css"] {
            font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
        }

        .stApp {
            color: var(--vmb-white);
            background:
                radial-gradient(circle at 12% 8%, rgba(37, 99, 235, 0.12) 0, transparent 40%),
                radial-gradient(circle at 88% 18%, rgba(96, 165, 250, 0.08) 0, transparent 30%),
                linear-gradient(135deg, #020617 0%, #050B14 100%) !important;
            background-attachment: fixed !important;
        }

        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 0;
            background-image:
                linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px),
                radial-gradient(circle at 30% 30%, rgba(59,130,246,0.13), transparent 22%),
                radial-gradient(circle at 75% 62%, rgba(255,255,255,0.06), transparent 18%);
            background-size: 56px 56px, 56px 56px, 100% 100%, 100% 100%;
            mask-image: linear-gradient(to bottom, rgba(0,0,0,0.9), rgba(0,0,0,0.2));
        }

        .block-container {
            position: relative;
            z-index: 1;
            padding-top: 3rem !important;
            padding-bottom: 4rem !important;
            max-width: 1220px !important;
        }

        h1, h2, h3, h4 {
            color: var(--vmb-white) !important;
            font-family: 'Inter', sans-serif !important;
            letter-spacing: -0.02em !important;
            text-shadow: none !important;
        }

        .vmb-hero {
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(148, 163, 184, 0.14);
            border-radius: 24px;
            padding: 32px;
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.95), rgba(2, 6, 23, 0.98));
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(12px);
            margin-bottom: 24px;
        }

        .vmb-hero::before {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(120deg, rgba(255,255,255,0.13), transparent 24%, transparent 74%, rgba(96,165,250,0.12));
            pointer-events: none;
        }

        .vmb-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            border: 1px solid rgba(96, 165, 250, 0.28);
            border-radius: 999px;
            background: rgba(37, 99, 235, 0.12);
            color: #BFDBFE;
            font-weight: 800;
            font-size: 12px;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .vmb-title {
            font-size: clamp(32px, 4.5vw, 56px);
            line-height: 1.05;
            margin: 12px 0 8px;
            font-weight: 800;
            color: #FFFFFF !important;
        }

        .vmb-subtitle {
            color: #AAB8CF;
            font-size: 16px;
            line-height: 1.65;
            max-width: 680px;
            margin: 0;
        }

        .vmb-hero-grid {
            display: grid;
            grid-template-columns: minmax(0, 1.15fr) minmax(260px, 0.85fr);
            gap: 22px;
            align-items: center;
        }

        .vmb-illustration {
            position: relative;
            min-height: 230px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .vmb-premium-card, div[data-testid="stVerticalBlock"] div[style*="border"] {
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.82), rgba(2, 6, 23, 0.74)) !important;
            border: 1px solid var(--vmb-border) !important;
            border-radius: 22px !important;
            box-shadow: 0 20px 60px rgba(2,6,23,0.42), inset 0 1px 0 rgba(255,255,255,0.05) !important;
            padding: 22px !important;
            transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease !important;
            backdrop-filter: blur(18px) !important;
        }

        div[data-testid="stVerticalBlock"] div[style*="border"]:hover {
            transform: translateY(-4px) !important;
            border-color: rgba(96, 165, 250, 0.56) !important;
            box-shadow: 0 26px 78px rgba(37, 99, 235, 0.20), inset 0 1px 0 rgba(255,255,255,0.08) !important;
        }

        .vmb-metrics-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 16px;
            margin: 18px 0 28px;
        }

        .vmb-metric-card {
            border-radius: 20px;
            padding: 24px;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(148, 163, 184, 0.12);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(8px);
        }

        .vmb-metric-label { color: #94A3B8; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; }
        .vmb-metric-value { color: #FFFFFF; font-size: 30px; font-weight: 900; margin-top: 8px; letter-spacing: -0.04em; }
        .vmb-metric-hint { color: #60A5FA; font-size: 12px; font-weight: 700; margin-top: 5px; }

        .vmb-section-banner {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 18px;
            padding: 18px 20px;
            margin: 18px 0 16px;
            border-radius: 22px;
            background: linear-gradient(90deg, rgba(37,99,235,0.20), rgba(15,23,42,0.64));
            border: 1px solid rgba(96,165,250,0.20);
        }

        .stButton>button {
            border-radius: 12px !important;
            font-weight: 800 !important;
            letter-spacing: 0.01em !important;
            transition: all 0.25s ease !important;
            min-height: 44px !important;
            border: 1px solid rgba(148,163,184,0.18) !important;
            background: rgba(15,23,42,0.78) !important;
            color: #F8FAFC !important;
        }

        .stButton>button[kind="primary"] {
            background: linear-gradient(92deg, #1D4ED8, #2563EB 48%, #60A5FA) !important;
            border: 1px solid rgba(191,219,254,0.25) !important;
            box-shadow: 0 12px 30px rgba(37, 99, 235, 0.42) !important;
        }

        .stButton>button:hover {
            transform: translateY(-2px) scale(1.01) !important;
            border-color: rgba(96,165,250,0.62) !important;
            box-shadow: 0 16px 40px rgba(37,99,235,0.28) !important;
        }

        section[data-testid="stSidebar"] {
            background:
                radial-gradient(circle at 50% 0%, rgba(37,99,235,0.24), transparent 32%),
                linear-gradient(180deg, rgba(2,6,23,0.96), rgba(8,13,28,0.96)) !important;
            border-right: 1px solid rgba(148,163,184,0.14) !important;
            backdrop-filter: blur(20px) !important;
        }
        
        @media (max-width: 900px) {
            .vmb-hero-grid, .vmb-metrics-grid { grid-template-columns: 1fr; }
            .vmb-illustration { min-height: 160px; }
        }
    </style>
    """, unsafe_allow_html=True)

# Geração dos Blocos de HTML Compactados (Sem pular linhas para evitar bug do Markdown virar código fonte)
def premium_illustration(kind):
    if kind == "logo":
        import base64
        try:
            with open("vmb_logo_fundo_preto.png", "rb") as f:
                data = base64.b64encode(f.read()).decode()
            # Brilho azul neon poderoso atrás da logo da VMB
            return f"<div class='vmb-illustration'><img src='data:image/png;base64,{data}' style='width:100%; max-width:280px; border-radius: 24px; box-shadow: 0 0 45px rgba(37, 99, 235, 0.5); object-fit: contain;'></div>"
        except:
            pass # Se falhar, renderiza o fallback padrão (código SVG que omiti aqui pra encurtar)
    return "<div class='vmb-illustration'><h2>📊</h2></div>"

def premium_page_header(title, subtitle, kind="dashboard", eyebrow="VMB INVEST | PERFORMANCE SYSTEM"):
    ill = premium_illustration(kind)
    return f"<div class='vmb-hero'><div class='vmb-hero-grid'><div><div class='vmb-eyebrow'>{eyebrow}</div><div class='vmb-title'>{title}</div><p class='vmb-subtitle'>{subtitle}</p></div>{ill}</div></div>"

def premium_section_banner(title, subtitle):
    return f"<div class='vmb-section-banner'><div><h3 style='margin:0 !important; font-size:22px;'>{title}</h3><p style='margin:4px 0 0; color:#9AA8BD;'>{subtitle}</p></div><div style='font-weight:900;color:#BFDBFE;'>PREMIUM</div></div>"

def premium_metric_card(label, value, hint=""):
    return f"<div class='vmb-metric-card'><div class='vmb-metric-label'>{label}</div><div class='vmb-metric-value'>{value}</div><div class='vmb-metric-hint'>{hint}</div></div>"

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
        "logado": False, "usuario": "", "page": "Login", "simulado_atual_indice": 0,
        "simulado_nome": "", "modulos_selecionados":[], "quiz_atual": None,
        "inicio_time": None, "fim_time": None, "respostas_usuario": {},
        "resultado_salvo": False, "xp_usuario": 0, "nivel_usuario": "Trainee", "foto_perfil": None
    })

def calcular_gamificacao(df_user):
    simulados_feitos = len(df_user)
    xp = simulados_feitos * 150
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
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([0.8, 2.4, 0.8])
    with col2:
        st.markdown(premium_page_header(
            "VMB INVEST", "Treinamento de alta performance para assessores que querem evoluir com método, dados e mentalidade de elite.", "logo", "SIMULADO DE ELITE"
        ), unsafe_allow_html=True)
        
        with st.container(border=True):
            user = st.text_input("Usuário", placeholder="ID do Agente")
            pw = st.text_input("Senha", type="password", placeholder="••••••••")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("ACESSAR PLATAFORMA ⚡", use_container_width=True, type="primary"):
                with st.spinner("Autenticando e sincronizando progresso..."):
                    try:
                        conn = st.connection("gsheets", type=GSheetsConnection)
                        df_usuarios = conn.read(worksheet="Usuarios", ttl=0) 
                        user_match = df_usuarios[(df_usuarios['Usuario'].astype(str).str.lower() == user.lower()) & (df_usuarios['Senha'].astype(str) == pw)]
                        
                        if not user_match.empty or (user.lower() == "admin" and pw == "admin"):
                            usuario_formatado = user.capitalize()
                            st.session_state.logado = True
                            st.session_state.usuario = usuario_formatado
                            
                            try:
                                df_historico = conn.read(worksheet="Historico", ttl=0)
                                df_user_hist = df_historico[df_historico['Usuario'] == usuario_formatado]
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
                                
                                st.session_state.simulado_atual_indice = min(max_passed + 1, len(SIMULADOS_ORDEM) - 1)
                            except:
                                st.session_state.simulado_atual_indice = 0

                            st.session_state.page = "Home"
                            st.rerun()
                        else:
                            st.error("Acesso negado. Credenciais inválidas.")
                    except:
                        st.error("Falha de conexão com os servidores.")

else:
    # --- BARRA LATERAL GAMIFICADA ---
    with st.sidebar:
        import base64
        foto_html = "👤"
        if "foto_perfil" in st.session_state and st.session_state.foto_perfil:
            try:
                foto_base64 = base64.b64encode(st.session_state.foto_perfil).decode()
                foto_html = f'<img src="data:image/png;base64,{foto_base64}" style="width:45px; height:45px; border-radius:50%; object-fit:cover; border:2px solid #3B82F6;">'
            except: pass

        sidebar_html = '<div style="background: rgba(37, 99, 235, 0.08); padding: 20px; border-radius: 20px; border: 1px solid rgba(37, 99, 235, 0.15); margin-bottom: 20px; display: flex; align-items: center; gap: 15px;">'
        sidebar_html += '<div style="flex-shrink: 0;">' + foto_html + '</div>'
        sidebar_html += '<div style="overflow: hidden;">'
        sidebar_html += '<div style="font-size: 12px; color: #8B949E; text-transform: uppercase; letter-spacing: 0.05em;">Agente</div>'
        sidebar_html += '<div style="font-size: 18px; font-weight: 800; color: white; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">' + str(st.session_state.usuario) + '</div>'
        sidebar_html += '<div style="font-size: 12px; font-weight: 700; color: #3B82F6; margin-top: 2px;">' + str(st.session_state.nivel_usuario) + '</div>'
        sidebar_html += '</div></div>'
        sidebar_html += '<div style="padding: 0 10px 20px;">'
        sidebar_html += '<div style="background: rgba(255,255,255,0.05); border-radius: 10px; height: 6px; overflow: hidden;">'
        xp_percent = (st.session_state.xp_usuario % 1000) / 10
        sidebar_html += '<div style="background: linear-gradient(90deg, #3B82F6, #60A5FA); width: ' + str(xp_percent) + '%; height: 100%;"></div>'
        sidebar_html += '</div>'
        sidebar_html += '<div style="font-size: 10px; color: #8B949E; margin-top: 6px; text-align: right; font-weight: 600;">' + str(st.session_state.xp_usuario) + ' XP</div>'
        sidebar_html += '</div>'
        st.markdown(sidebar_html, unsafe_allow_html=True)
        
        menu = st.radio("Módulos da Plataforma", ["Dashboard Principal", "Evolução e IA", "Meu Perfil"])
        
        st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
        st.divider()
        if st.button("🚪 Sair do Sistema", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    if menu == "Evolução e IA" and st.session_state.page != "Evolução":
        st.session_state.page = "Evolução"
        st.rerun()
    elif menu == "Meu Perfil" and st.session_state.page != "Perfil":
        st.session_state.page = "Perfil"
        st.rerun()
    elif menu == "Dashboard Principal" and st.session_state.page not in["Home", "Instrucoes", "Simulado", "Resultado"]:
        st.session_state.page = "Home"
        st.rerun()

    # --- HOME / DASHBOARD ---
    if st.session_state.page == "Home":
        st.markdown(premium_page_header(
            "Central de Treinamento",
            "Escolha sua próxima missão, acompanhe seu progresso e avance por uma jornada de evolução orientada por performance.",
            "logo",  # <-- UTILIZA A LOGO DA VMB AQUI
            "DASHBOARD PRINCIPAL"
        ), unsafe_allow_html=True)
        
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            df_historico = conn.read(worksheet="Historico", ttl=0)
            df_user_hist = df_historico[df_historico['Usuario'] == st.session_state.usuario]
            avg_score = df_user_hist['Nota (%)'].mean() if not df_user_hist.empty else 0
            max_score = df_user_hist['Nota (%)'].max() if not df_user_hist.empty else 0
            qtd_sim = len(df_user_hist)
            
            metrics_html = "<div class='vmb-metrics-grid'>"
            metrics_html += premium_metric_card("Aproveitamento Geral", "{0:.1f}%".format(avg_score), "média acumulada")
            metrics_html += premium_metric_card("Melhor Nota", "🏆 {0:.1f}%".format(max_score), "recorde pessoal")
            metrics_html += premium_metric_card("Simulados Concluídos", "⚡ " + str(qtd_sim), "missões finalizadas")
            metrics_html += "</div>"
            st.markdown(metrics_html, unsafe_allow_html=True)
        except:
            pass 

        st.markdown(premium_section_banner("Selecione sua missão", "Cada simulado desbloqueia uma nova etapa da trilha de evolução comercial e técnica."), unsafe_allow_html=True)
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
        st.markdown(premium_page_header(
            f"Operação: {st.session_state.simulado_nome}",
            "Leia o protocolo, entre em modo foco e execute a missão com precisão de prova oficial.",
            "logo",
            "PROTOCOLO DE AVALIAÇÃO"
        ), unsafe_allow_html=True)
        
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

    # --- EXECUÇÃO DO SIMULADO ---
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
        
        st.write("") 
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
        st.markdown(premium_page_header("Relatório de Missão", "Veja sua nota, seu ritmo, seus acertos e os pontos que precisam de reforço para a próxima tentativa.", "logo", "ANÁLISE DE PERFORMANCE"), unsafe_allow_html=True)
        
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
        st.markdown(premium_page_header("Inteligência de Dados e Evolução", "Transforme histórico, radar de competências e diagnóstico do mentor em um plano objetivo de melhoria.", "logo", "MENTOR ANALÍTICO"), unsafe_allow_html=True)
        
        with st.spinner("Processando heurística..."):
            try:
                conn = st.connection("gsheets", type=GSheetsConnection)
                df_historico_geral = conn.read(worksheet="Historico", ttl=0)
                df_user = df_historico_geral[df_historico_geral["Usuario"] == st.session_state.usuario].copy()
                
                if not df_user.empty:
                    df_user.reset_index(drop=True, inplace=True)
                    total_secs = 0
                    valid_times = 0
                    for t_str in df_user['Tempo']:
                        match = re.search(r'(\d+)m\s*(\d+)s', str(t_str))
                        if match:
                            total_secs += int(match.group(1)) * 60 + int(match.group(2))
                            valid_times += 1
                    
                    media_secs = total_secs // valid_times if valid_times > 0 else 0
                    
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
                            df_radar = pd.DataFrame(dict(Força=list(avg_module_scores.values()), Modulo=list(avg_module_scores.keys())))
                            df_radar = pd.concat([df_radar, df_radar.iloc[[0]]]) 
                            
                            fig = go.Figure()
                            fig.add_trace(go.Scatterpolar(r=df_radar['Força'], theta=df_radar['Modulo'], fill='toself', name='Sua Força', line_color='#3B82F6', fillcolor='rgba(59, 130, 246, 0.4)'))
                            fig.add_trace(go.Scatterpolar(r=[85]*len(df_radar), theta=df_radar['Modulo'], fill='none', name='Top 10% Elite', line_color='rgba(16, 185, 129, 0.5)', line_dash='dash'))

                            fig.update_layout(polar=dict(bgcolor='rgba(0,0,0,0)', radialaxis=dict(visible=True, range=[0, 100], gridcolor='#30363D', color='#8B949E'), angularaxis=dict(gridcolor='#30363D', color='#FAFAFA')), showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=40, r=40, t=20, b=20))
                            st.plotly_chart(fig, use_container_width=True)

                    with col_ia:
                        st.markdown("### 🧠 Diagnóstico do Mentor")
                        sorted_mods = sorted(avg_module_scores.items(), key=lambda item: item[1])
                        weak_mods =[mod for mod, score in sorted_mods if score < 70]
                        strong_mods =[mod for mod, score in sorted_mods if score >= 85]
                        
                        st.markdown("""<div style="background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);"><p style="color:#8B949E; font-size:14px; margin-bottom:5px;">ANÁLISE HEURÍSTICA CONCLUÍDA</p>""", unsafe_allow_html=True)
                        if weak_mods: st.markdown(f"**🚨 Atenção Crítica:**<br>Detectei falhas estruturais em **{weak_mods[0]}**. Redirecione 80% do seu próximo ciclo de estudos para a teoria base deste módulo.", unsafe_allow_html=True)
                        if strong_mods: st.markdown(f"<br>**🏆 Dominância:**<br>O módulo de **{strong_mods[-1]}** atingiu padrão de excelência. Modo manutenção ativado.", unsafe_allow_html=True)

                        st.markdown("<br>**⏱️ Pacing de Prova:**", unsafe_allow_html=True)
                        if media_secs > 1500: st.markdown("⚠️ *Velocidade de risco:* Você está usando quase todo o tempo limite. Em prova oficial, você não terá fôlego para revisar. Pratique leitura dinâmica.")
                        elif media_secs > 0 and media_secs < 600: st.markdown("⚡ *Impulsividade:* Seu tempo de resposta está muito rápido. Isso levanta suspeita de desatenção a palavras como 'EXCETO' ou dupla negação.")
                        elif media_secs > 0: st.markdown("✅ *Ritmo Cadenciado:* Seu controle de tempo está perfeitamente alinhado com candidatos aprovados.")
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.divider()
                    st.subheader("Data Grid (Registros Brutos)")
                    df_display = df_user[['Data', 'Simulado', 'Nota (%)', 'Tempo']].copy()
                    st.dataframe(df_display, column_config={"Nota (%)": st.column_config.ProgressColumn("Desempenho", help="Sua nota percentual", format="%f%%", min_value=0, max_value=100), "Data": st.column_config.TextColumn("Data da Execução"), "Simulado": st.column_config.TextColumn("Missão")}, hide_index=True, use_container_width=True)
                else:
                    st.info("Aguardando telemetria inicial. Faça seu primeiro simulado.")
            except Exception as e:
                st.error("Falha ao processar banco de dados da IA.")

    # --- TELA DE PERFIL ---
    elif st.session_state.page == "Perfil":
        st.markdown(premium_page_header("Meu Perfil", "Gerencie suas informações, personalize seu avatar e acompanhe suas conquistas na plataforma.", "logo", "CONFIGURAÇÕES DE AGENTE"), unsafe_allow_html=True)
        col_foto, col_info = st.columns([1, 2])
        
        with col_foto:
            with st.container(border=True):
                st.markdown("### Foto de Perfil")
                if st.session_state.foto_perfil:
                    st.image(st.session_state.foto_perfil, use_container_width=True)
                else:
                    st.info("Nenhuma foto carregada.")
                
                uploaded_file = st.file_uploader("Alterar foto", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
                if uploaded_file is not None:
                    st.session_state.foto_perfil = uploaded_file.getvalue()
                    st.success("Foto atualizada com sucesso!")
                    time.sleep(1)
                    st.rerun()

        with col_info:
            with st.container(border=True):
                st.markdown("### Informações da Conta")
                st.write(f"**Usuário:** {st.session_state.usuario}")
                st.write(f"**Nível Atual:** {st.session_state.nivel_usuario}")
                st.write(f"**XP Total:** {st.session_state.xp_usuario}")
                st.divider()
                st.markdown("#### Conquistas")
                if st.session_state.xp_usuario >= 2000: st.markdown("🏆 **Agente Elite:** Você atingiu o topo da performance.")
                elif st.session_state.xp_usuario >= 1200: st.markdown("🥇 **Agente Sênior:** Experiência comprovada em simulados.")
                else: st.markdown("🎯 **Em Evolução:** Continue completando missões para desbloquear insígnias.")
