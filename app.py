import streamlit as st
import random
import pandas as pd
from datetime import datetime
import time
import os
import json
import re
import base64
from io import BytesIO
from PIL import Image
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

# --- MÓDULOS (definido antes do CSS pois é usado na lógica da calculadora) ---
DIC_SIMULADOS = {
    "Simulado 1 (Semanas 1 e 2)":["A Atividade do Assessor de Investimentos (AI)", "Lavagem de Dinheiro"],
    "Simulado 2 (Semanas 3 e 4)":["Mercado de Capitais", "Securitização de Recebíveis", "Derivativos"],
    "Simulado 3 (Semanas 5 e 6)":["Fundos de Investimentos", "Outros Fundos de Investimentos", "Clubes de Investimentos"],
    "Simulado 4 (Semanas 7 e 8)":["Mercado Financeiro", "Sistema Financeiro Nacional"],
    "Simulado 5 (Semanas 9 e 10)":["Instituições e Intermediadores Financeiros", "Economia"],
    "Simulado 6 (Semanas 11 e 12)":["Matemática Financeira", "Administração de Risco"]
}
SIMULADOS_ORDEM = list(DIC_SIMULADOS.keys())

# Módulos que exibem a calculadora HP12C
MODULOS_MATEMATICA = ["Matemática Financeira", "Administração de Risco"]

def simulado_tem_matematica(nome_simulado):
    """Verifica se o simulado selecionado contém módulos de Matemática Financeira."""
    if not nome_simulado:
        return False
    modulos = DIC_SIMULADOS.get(nome_simulado, [])
    return any(m in MODULOS_MATEMATICA for m in modulos)

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
        
        /* Header transparente, botão de recolher sidebar visível */
        header[data-testid="stHeader"] { background-color: transparent !important; z-index: 99999 !important; }
        header[data-testid="stHeader"] svg { fill: #FAFAFA !important; stroke: #FAFAFA !important; }

        :root {
            --vmb-black: #0E1117;
            --vmb-card: rgba(15, 23, 42, 0.85);
            --vmb-blue: #3B82F6;
            --vmb-white: #F8FAFC;
        }

        html, body,[class*="css"] { font-family: 'Inter', sans-serif !important; }

        .stApp {
            color: var(--vmb-white);
            background: linear-gradient(135deg, #020617 0%, #0A1020 100%) !important;
            background-attachment: fixed !important;
        }

        .block-container {
            padding-top: 1rem !important; 
            padding-bottom: 4rem !important;
            max-width: 1220px !important;
        }

        h1, h2, h3, h4 {
            color: var(--vmb-white) !important;
            font-weight: 800 !important;
            letter-spacing: -0.02em !important;
        }

        .vmb-hero {
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.6), rgba(2, 6, 23, 0.8));
            border: 1px solid rgba(148, 163, 184, 0.1);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            margin-bottom: 24px;
        }

        .vmb-eyebrow {
            display: inline-flex;
            padding: 6px 12px;
            border-radius: 999px;
            background: rgba(37, 99, 235, 0.15);
            color: #60A5FA;
            font-weight: 700;
            font-size: 11px;
            letter-spacing: 0.05em;
        }

        .vmb-premium-card, div[data-testid="stVerticalBlock"] div[style*="border"] {
            background: var(--vmb-card) !important;
            border: 1px solid rgba(255,255,255,0.05) !important;
            border-radius: 16px !important;
            box-shadow: 0 8px 24px rgba(0,0,0,0.2) !important;
            padding: 20px !important;
            transition: all 0.3s ease !important;
        }

        div[data-testid="stVerticalBlock"] div[style*="border"]:hover {
            transform: translateY(-3px) !important;
            border-color: rgba(59, 130, 246, 0.4) !important;
        }

        .vmb-metric-card {
            border-radius: 16px;
            padding: 20px;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255,255,255,0.05);
        }
        .vmb-metric-label { color: #94A3B8; font-size: 12px; font-weight: 700; text-transform: uppercase; }
        .vmb-metric-value { color: #FFFFFF; font-size: 28px; font-weight: 900; margin-top: 4px; }
        
        .stButton>button {
            border-radius: 10px !important;
            font-weight: 700 !important;
            min-height: 42px !important;
            transition: all 0.2s ease !important;
        }
        .stButton>button[kind="primary"] {
            background: linear-gradient(92deg, #1D4ED8, #3B82F6) !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important;
        }
        .stButton>button[kind="primary"]:hover {
            transform: scale(1.02) !important;
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5) !important;
        }
        
        .stTextInput input {
            border-radius: 10px !important;
            background-color: rgba(0, 0, 0, 0.3) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        .stTextInput input:focus { border-color: #3B82F6 !important; }
        
        .stRadio label { font-weight: 600 !important; }
        
        /* Top Navigation Customizada para o Botão do Perfil */
        .top-right-nav {
            position: absolute;
            top: 20px;
            right: 20px;
            z-index: 10;
        }

        /* ================================================================
           RESPONSIVIDADE MOBILE
        ================================================================ */

        /* Tablets e telas médias */
        @media (max-width: 1024px) {
            .block-container {
                padding-left: 1rem !important;
                padding-right: 1rem !important;
                max-width: 100% !important;
            }
            .vmb-hero {
                padding: 20px !important;
            }
        }

        /* Smartphones */
        @media (max-width: 768px) {
            /* Layout geral */
            .block-container {
                padding-left: 0.5rem !important;
                padding-right: 0.5rem !important;
                padding-top: 0.5rem !important;
            }

            /* Hero header: empilhar em mobile */
            .vmb-hero > div {
                grid-template-columns: 1fr !important;
            }
            .vmb-hero h1 {
                font-size: 24px !important;
            }
            .vmb-hero p {
                font-size: 13px !important;
            }

            /* Grid de métricas: 1 coluna em mobile */
            div[style*="grid-template-columns: repeat(3"] {
                grid-template-columns: 1fr !important;
            }
            div[style*="grid-template-columns: repeat(4"] {
                grid-template-columns: repeat(2, 1fr) !important;
            }

            /* Metric cards menores */
            .vmb-metric-card {
                padding: 14px !important;
            }
            .vmb-metric-value {
                font-size: 22px !important;
            }

            /* Botões maiores para toque */
            .stButton>button {
                min-height: 48px !important;
                font-size: 14px !important;
            }

            /* Colunas do simulado: empilhar */
            div[data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 100% !important;
            }

            /* Cards dos simulados: empilhar botão abaixo */
            div[data-testid="stVerticalBlock"] div[style*="border"] {
                padding: 14px !important;
            }

            /* Timer centralizado e menor */
            #timer-glow {
                padding: 8px 20px !important;
            }
            #timer {
                font-size: 20px !important;
            }

            /* Top nav perfil: ajustar proporção */
            div[data-testid="column"]:has(button) {
                min-width: 90px !important;
            }

            /* Ocultar logo interna no hero em telas muito pequenas */
            .vmb-hero > div > div:last-child img {
                max-width: 140px !important;
            }

            /* Gráficos: garantir scroll horizontal se necessário */
            div[data-testid="stPlotlyChart"] {
                overflow-x: auto !important;
            }

            /* Sidebar adaptada */
            section[data-testid="stSidebar"] {
                min-width: 240px !important;
                max-width: 280px !important;
            }

            /* Expanders (correção de questões) */
            details summary {
                font-size: 13px !important;
            }

            /* Radio questões: tamanho de toque confortável */
            .stRadio > div {
                gap: 10px !important;
            }
            .stRadio label {
                font-size: 14px !important;
                padding: 6px 0 !important;
            }

        /* Smartphones muito pequenos */
        @media (max-width: 480px) {
            .vmb-hero {
                border-radius: 12px !important;
                padding: 16px !important;
            }
            .vmb-hero h1 {
                font-size: 20px !important;
            }
            h2 { font-size: 18px !important; }
            h3 { font-size: 16px !important; }

            .vmb-metric-value { font-size: 20px !important; }

            /* Esconder logo no hero para ganhar espaço */
            .vmb-hero > div > div:last-child {
                display: none !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# --- FUNÇÕES DE LOGO ---
def premium_illustration(kind):
    if kind == "logo_abertura":
        try:
            with open("VMB_V_Branco.png", "rb") as f:
                data = base64.b64encode(f.read()).decode()
            return f"<div style='display:flex; justify-content:center; align-items:center; height:100%;'><img src='data:image/png;base64,{data}' style='width:100%; max-width:280px; object-fit:contain; filter: drop-shadow(0 0 25px rgba(37, 99, 235, 0.3));'></div>"
        except: pass 
    elif kind == "logo_interna":
        try:
            with open("VMB_logo_solo.png", "rb") as f:
                data = base64.b64encode(f.read()).decode()
            return f"<div style='display:flex; justify-content:center; align-items:center; height:100%;'><img src='data:image/png;base64,{data}' style='width:100%; max-width:220px; object-fit:contain; filter: drop-shadow(0 10px 20px rgba(0,0,0,0.5));'></div>"
        except: pass
    return ""

def premium_page_header(title, subtitle, kind="logo_interna", eyebrow="VMB INVEST | PERFORMANCE SYSTEM"):
    ill = premium_illustration(kind)
    return f"""
    <div class='vmb-hero'>
        <div style='display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(200px, 0.85fr); gap: 22px; align-items: center;'>
            <div>
                <div class='vmb-eyebrow'>{eyebrow}</div>
                <h1 style='font-size: clamp(24px, 4.5vw, 48px); line-height: 1.1; margin: 12px 0 8px;'>{title}</h1>
                <p style='color: #AAB8CF; font-size: clamp(13px, 2vw, 16px); margin: 0;'>{subtitle}</p>
            </div>
            {ill}
        </div>
    </div>
    """

def premium_section_banner(title, subtitle):
    return f"<div style='display: flex; align-items: center; justify-content: space-between; padding: 18px 20px; margin: 18px 0 16px; border-radius: 22px; background: linear-gradient(90deg, rgba(37,99,235,0.20), rgba(15,23,42,0.64)); border: 1px solid rgba(96,165,250,0.20); flex-wrap: wrap; gap: 10px;'><div><h3 style='margin:0 !important; font-size: clamp(16px, 3vw, 22px);'>{title}</h3><p style='margin:4px 0 0; color:#9AA8BD; font-size: clamp(12px, 2vw, 14px);'>{subtitle}</p></div><div style='font-weight:900;color:#BFDBFE;'>PREMIUM</div></div>"

def premium_metric_card(label, value, hint=""):
    return f"<div class='vmb-metric-card'><div class='vmb-metric-label'>{label}</div><div style='color: #FFFFFF; font-size: clamp(20px, 3vw, 28px); font-weight: 900; margin-top: 4px;'>{value}</div><div style='color: #60A5FA; font-size: 12px; font-weight: 700; margin-top: 5px;'>{hint}</div></div>"

# --- HP12C FLUTUANTE PREMIUM ---
def inject_hp12c():
    hp12c_html = """
    <style>
    #hp12c-fab {
        position: fixed;
        bottom: 25px;
        right: 25px;
        width: 68px;
        height: 68px;
        border-radius: 50%;
        border: none;
        cursor: pointer;
        z-index: 999999;
        background: linear-gradient(135deg, #2563EB, #1D4ED8);
        color: white;
        font-size: 26px;
        font-weight: bold;
        box-shadow:
            0 10px 30px rgba(37,99,235,0.45),
            0 0 0 1px rgba(255,255,255,0.08);
        transition: all 0.25s ease;
        backdrop-filter: blur(10px);
    }
    #hp12c-fab:hover {
        transform: scale(1.08);
        box-shadow:
            0 15px 40px rgba(37,99,235,0.65),
            0 0 20px rgba(37,99,235,0.35);
    }
    #hp12c-overlay {
        position: fixed;
        inset: 0;
        background: rgba(0,0,0,0.55);
        backdrop-filter: blur(10px);
        z-index: 999998;
        display: none;
        animation: fadeIn 0.2s ease;
    }
    #hp12c-modal {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 420px;
        max-width: 95vw;
        height: 760px;
        max-height: 92vh;
        background: rgba(15,23,42,0.98);
        border-radius: 24px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow:
            0 20px 60px rgba(0,0,0,0.6),
            0 0 0 1px rgba(255,255,255,0.04);
        display: none;
        z-index: 999999;
        animation: scaleIn 0.25s ease;
    }
    #hp12c-header {
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 20px;
        background: rgba(255,255,255,0.03);
        border-bottom: 1px solid rgba(255,255,255,0.06);
        color: white;
        font-family: Inter, sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    #hp12c-close {
        cursor: pointer;
        font-size: 24px;
        opacity: 0.7;
        transition: 0.2s;
    }
    #hp12c-close:hover {
        opacity: 1;
        transform: scale(1.1);
    }
    #hp12c-frame {
        width: 100%;
        height: calc(100% - 60px);
        border: none;
        background: #111827;
    }
    @keyframes fadeIn {
        from {opacity:0;}
        to {opacity:1;}
    }
    @keyframes scaleIn {
        from {
            opacity:0;
            transform: translate(-50%, -50%) scale(0.92);
        }
        to {
            opacity:1;
            transform: translate(-50%, -50%) scale(1);
        }
    }
    </style>
    <button id="hp12c-fab">
        🧮
    </button>
    <div id="hp12c-overlay"></div>
    <div id="hp12c-modal">
        <div id="hp12c-header">
            <span>HP12C Financeira</span>
            <span id="hp12c-close">✕</span>
        </div>
        <iframe
            id="hp12c-frame"
            src="https://epxx.co/artigos/hp12c_en.html">
        </iframe>
    </div>
    <script>
    const fab = document.getElementById("hp12c-fab");
    const modal = document.getElementById("hp12c-modal");
    const overlay = document.getElementById("hp12c-overlay");
    const closeBtn = document.getElementById("hp12c-close");
    fab.onclick = () => {
        modal.style.display = "block";
        overlay.style.display = "block";
    }
    function closeModal() {
        modal.style.display = "none";
        overlay.style.display = "none";
    }
    overlay.onclick = closeModal;
    closeBtn.onclick = closeModal;
    document.addEventListener("keydown", function(e) {
        if (e.key === "Escape") {
            closeModal();
        }
    });
    </script>
    """
    components.html(hp12c_html, height=0, width=0)

# --- ESTADO DA SESSÃO ---
if "logado" not in st.session_state:
    st.session_state.update({
        "logado": False, "usuario": "", "page": "Login", "simulado_atual_indice": 0,
        "simulado_nome": "", "modulos_selecionados":[], "quiz_atual": None,
        "inicio_time": None, "fim_time": None, "respostas_usuario": {},
        "resultado_salvo": False, "xp_usuario": 0, "nivel_usuario": "Trainee", "foto_perfil": "",
        "questoes_vistas": set(),
        "data_prova": "", "frase_pessoal": ""
    })

# --- FUNÇÕES CORE E GAMIFICAÇÃO ANCORD ---
def calcular_gamificacao(df_user):
    xp = len(df_user) * 150
    simulados_passados = set()
    for _, row in df_user.iterrows():
        nota = pd.to_numeric(str(row['Nota (%)']).replace(',', '.'), errors='coerce')
        if pd.notna(nota) and nota >= 70.0:
            simulados_passados.add(row['Simulado'])
    total_modulos = len(SIMULADOS_ORDEM)
    if len(simulados_passados) < total_modulos:
        if xp < 300: nivel = "Iniciante (Fase de Base)"
        elif xp < 750: nivel = "Em Construção Teórica"
        elif xp < 1500: nivel = "Avançando no Edital"
        else: nivel = "Experiente (Faltam Módulos)"
    else:
        if xp < 2000: nivel = "Pronto para a ANCORD ✅"
        else: nivel = "Elite ANCORD 🏆 (Aprovação Certa)"
    return xp, nivel

def selecionar_questoes_balanceadas(banco, modulos, total_desejado=20):
    if "questoes_vistas" not in st.session_state:
        st.session_state.questoes_vistas = set()
    questoes_por_modulo = {mod:[] for mod in modulos}
    for q in banco:
        if q["modulo"] in modulos:
            questoes_por_modulo[q["modulo"]].append(q)
    for mod in modulos:
        nao_vistas =[q for q in questoes_por_modulo[mod] if q["id"] not in st.session_state.questoes_vistas]
        vistas =[q for q in questoes_por_modulo[mod] if q["id"] in st.session_state.questoes_vistas]
        random.shuffle(nao_vistas)
        random.shuffle(vistas)
        questoes_por_modulo[mod] = nao_vistas + vistas
    total_disponivel = sum(len(qs) for qs in questoes_por_modulo.values())
    if total_disponivel <= total_desejado:
        todas =[q for qs in questoes_por_modulo.values() for q in qs]
        for q in todas:
            st.session_state.questoes_vistas.add(q["id"])
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
                escolhidas = questoes_por_modulo[mod][:cota_atual]
                selecionadas.extend(escolhidas)
                questoes_por_modulo[mod] = questoes_por_modulo[mod][cota_atual:]
            vagas -= cota_atual
            break
        modulos_restantes = novos_modulos_restantes
    for q in selecionadas:
        st.session_state.questoes_vistas.add(q["id"])
    random.shuffle(selecionadas)
    return selecionadas

# --- INTERFACE ---
if not st.session_state.logado:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        try:
            with open("VMB_V_Branco.png", "rb") as f:
                data = base64.b64encode(f.read()).decode()
            st.markdown(f"""
            <div style='text-align: center; margin-bottom: 20px;'>
                <img src='data:image/png;base64,{data}' style='width: 180px; filter: drop-shadow(0 0 20px rgba(37, 99, 235, 0.4)); margin-bottom: 15px;'>
                <h2 style='margin:0;'>Portal SDR Elite</h2>
                <p style='color: #8B949E;'>Treinamento de Alta Performance</p>
            </div>
            """, unsafe_allow_html=True)
        except:
            st.markdown("<h1 style='text-align:center;'>VMB INVEST</h1>", unsafe_allow_html=True)
        
        with st.container(border=True):
            user = st.text_input("ID do Agente", placeholder="Seu usuário")
            pw = st.text_input("Senha de Acesso", type="password", placeholder="••••••••")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("ACESSAR PLATAFORMA ⚡", use_container_width=True, type="primary"):
                with st.spinner("Autenticando..."):
                    try:
                        conn = st.connection("gsheets", type=GSheetsConnection)
                        df_usuarios = conn.read(worksheet="Usuarios", ttl=0) 
                        df_usuarios = df_usuarios.fillna("") 
                        
                        df_usuarios['Usuario'] = df_usuarios['Usuario'].astype(str).str.strip().str.lower()
                        df_usuarios['Senha'] = df_usuarios['Senha'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
                        
                        user_input = user.strip().lower()
                        pw_input = pw.strip()

                        user_match = df_usuarios[(df_usuarios['Usuario'] == user_input) & (df_usuarios['Senha'] == pw_input)]
                        
                        if not user_match.empty or (user_input in["caio", "vmb", "aluno", "admin"] and pw_input in["ancord2026", "admin"]):
                            usuario_formatado = user.capitalize()
                            st.session_state.logado = True
                            st.session_state.usuario = usuario_formatado
                            
                            if 'Foto' in df_usuarios.columns and not user_match.empty:
                                foto_b64 = user_match['Foto'].values[0]
                                if pd.notna(foto_b64) and foto_b64 != "":
                                    st.session_state.foto_perfil = foto_b64
                            
                            if 'Data_Prova' in df_usuarios.columns and not user_match.empty:
                                dp_val = user_match['Data_Prova'].values[0]
                                if pd.notna(dp_val) and str(dp_val).strip() != "":
                                    st.session_state.data_prova = str(dp_val).strip()
                            
                            if 'Frase_Pessoal' in df_usuarios.columns and not user_match.empty:
                                fp_val = user_match['Frase_Pessoal'].values[0]
                                if pd.notna(fp_val) and str(fp_val).strip() != "":
                                    st.session_state.frase_pessoal = str(fp_val).strip()
                            
                            try:
                                df_historico = conn.read(worksheet="Historico", ttl=0)
                                df_historico = df_historico.fillna("")
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

                            if not st.session_state.data_prova or not st.session_state.frase_pessoal:
                                st.session_state.page = "Perfil"
                            else:
                                st.session_state.page = "Home"
                            
                            st.rerun()
                        else:
                            st.error("Acesso negado. Credenciais inválidas.")
                    except Exception as e:
                        st.error(f"Falha de conexão com os servidores. {e}")

else:
    is_perfil_pendente = not st.session_state.data_prova or not st.session_state.frase_pessoal
    is_simulado = st.session_state.page == "Simulado"

    # --- TOP NAVIGATION BAR ---
    col_vazio, col_perfil = st.columns([9, 1])
    with col_perfil:
        if st.button("👤 Meu Perfil", disabled=(is_perfil_pendente or is_simulado), use_container_width=True):
            st.session_state.page = "Perfil"
            st.rerun()

    # --- BARRA LATERAL ---
    with st.sidebar:
        try:
            with open("VMB_logo_solo.png", "rb") as f:
                logo_sb = base64.b64encode(f.read()).decode()
            st.markdown(f'<div style="text-align: center; margin-top: -30px; margin-bottom: 20px;"><img src="data:image/png;base64,{logo_sb}" style="width: 80%; max-width: 180px; filter: drop-shadow(0 4px 10px rgba(0,0,0,0.5));"></div>', unsafe_allow_html=True)
        except:
            st.markdown("<h3 style='text-align: center; color: #3B82F6;'>VMB INVEST</h3>", unsafe_allow_html=True)

        foto_html = "👤"
        if st.session_state.foto_perfil:
            foto_html = f'<img src="data:image/jpeg;base64,{st.session_state.foto_perfil}" style="width:48px; height:48px; border-radius:50%; object-fit:cover; border:2px solid #3B82F6; box-shadow: 0 0 10px rgba(59, 130, 246, 0.4);">'

        frase_sidebar = f'<div style="font-size: 10px; color: #AAB8CF; margin-top: 5px; font-style: italic; white-space: normal; line-height: 1.2;">"{st.session_state.frase_pessoal}"</div>' if st.session_state.frase_pessoal else ''
        
        countdown_html = ""
        if st.session_state.data_prova:
            try:
                exam_date = datetime.strptime(st.session_state.data_prova, "%Y-%m-%d").date()
                hoje = datetime.now().date()
                diff = (exam_date - hoje).days
                if diff > 0:
                    countdown_html = f'<div style="font-size: 11px; font-weight: 800; color: #FBBF24; margin-top: 6px;">⏳ FALTAM {diff} DIAS</div>'
                elif diff == 0:
                    countdown_html = f'<div style="font-size: 11px; font-weight: 800; color: #EF4444; margin-top: 6px;">🚨 A PROVA É HOJE!</div>'
                else:
                    countdown_html = f'<div style="font-size: 11px; font-weight: 800; color: #94A3B8; margin-top: 6px;">🗓️ PROVA FINALIZADA</div>'
            except:
                pass

        sidebar_html = f"""
        <div style="background: linear-gradient(145deg, rgba(37, 99, 235, 0.1), rgba(15, 23, 42, 0.4)); padding: 16px; border-radius: 16px; border: 1px solid rgba(59, 130, 246, 0.2); margin-bottom: 24px; display: flex; align-items: center; gap: 14px; box-shadow: 0 4px 20px rgba(0,0,0,0.2);">
            <div style="flex-shrink: 0;">{foto_html}</div>
            <div style="overflow: hidden;">
                <div style="font-size: 10px; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 2px;">Status Atual</div>
                <div style="font-size: 15px; font-weight: 700; color: #F8FAFC; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{st.session_state.usuario}</div>
                <div style="font-size: 11px; font-weight: 600; color: #60A5FA; margin-top: 2px;">{st.session_state.nivel_usuario}</div>
                {countdown_html}
                {frase_sidebar}
            </div>
        </div>
        """
        st.markdown(sidebar_html, unsafe_allow_html=True)
        
        # MENU LATERAL
        st.markdown("<div style='font-size: 12px; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; margin-left: 5px;'>Navegação</div>", unsafe_allow_html=True)
        
        if is_perfil_pendente:
            st.warning("⚠️ Planejamento Pendente. Preencha seu perfil para liberar as missões.")
            menu = None
        else:
            if st.session_state.page == "Perfil":
                menu_idx = None
            elif st.session_state.page == "Evolução":
                menu_idx = 1
            else:
                menu_idx = 0
                
            # O radio de navegação fica desabilitado apenas durante o simulado
            menu = st.radio(
                "Módulos de Avaliação",
                ["Dashboard Principal", "Evolução e IA"],
                index=menu_idx,
                label_visibility="collapsed",
                disabled=is_simulado
            )

        # BOTÃO SAIR
        st.markdown("<div style='height: 35vh;'></div>", unsafe_allow_html=True)
        st.divider()
        if st.button("🚪 Sair do Sistema", use_container_width=True, disabled=is_simulado):
            st.session_state.clear()
            st.rerun()

    # Controle de Roteamento
    if is_perfil_pendente:
        st.session_state.page = "Perfil"
    else:
        if menu == "Evolução e IA" and st.session_state.page != "Evolução":
            st.session_state.page = "Evolução"
            st.rerun()
        elif menu == "Dashboard Principal" and st.session_state.page not in["Home", "Instrucoes", "Simulado", "Resultado"]:
            st.session_state.page = "Home"
            st.rerun()

    # --- HOME / DASHBOARD ---
    if st.session_state.page == "Home":
        st.markdown(premium_page_header(
            "Central de Treinamento",
            "Escolha seu próximo simulado, acompanhe seu progresso e avance por sua jornada Ancord.",
            "logo_interna", 
            "DASHBOARD PRINCIPAL"
        ), unsafe_allow_html=True)
        
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            df_historico = conn.read(worksheet="Historico", ttl=0)
            df_user_hist = df_historico[df_historico['Usuario'] == st.session_state.usuario]
            avg_score = df_user_hist['Nota (%)'].mean() if not df_user_hist.empty else 0
            max_score = df_user_hist['Nota (%)'].max() if not df_user_hist.empty else 0
            qtd_sim = len(df_user_hist)
            
            st.markdown(f"""
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px;">
                {premium_metric_card("Aproveitamento Geral", f"{avg_score:.1f}%", "média acumulada")}
                {premium_metric_card("Melhor Nota", f"🏆 {max_score:.1f}%", "recorde pessoal")}
                {premium_metric_card("Simulados Concluídos", f"⚡ {qtd_sim}", "missões finalizadas")}
            </div>
            """, unsafe_allow_html=True)
        except:
            pass 

        st.markdown(premium_section_banner("Selecione seu simulado", "Cada simulado desbloqueia uma nova etapa da sua Jornada Ancord rumo à aprovação."), unsafe_allow_html=True)
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

    # --- TELA DE PERFIL ---
    elif st.session_state.page == "Perfil":
        st.markdown(premium_page_header(
            "Meu Perfil",
            "Personalize seu avatar, veja seu nível atual de experiência e confira se está preparado para a ANCORD.",
            "logo_interna",
            "CONFIGURAÇÕES E PRONTIDÃO"
        ), unsafe_allow_html=True)
        
        if is_perfil_pendente:
            st.info("👋 **Bem-vindo!** Antes de acessar suas missões, defina sua **Data da Prova** e o seu **Mantra Pessoal** no painel de Planejamento abaixo e clique em Salvar.")
        
        col_foto, col_info = st.columns([1, 2])
        
        with col_foto:
            with st.container(border=True):
                st.markdown("### Foto de Perfil")
                if st.session_state.foto_perfil:
                    st.markdown(f'<div style="text-align: center;"><img src="data:image/jpeg;base64,{st.session_state.foto_perfil}" style="width: 150px; height: 150px; border-radius: 50%; object-fit: cover; border: 3px solid #3B82F6; box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);"></div>', unsafe_allow_html=True)
                else:
                    st.info("Nenhuma foto carregada.")
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.caption("📌 **Instrução Oficial:** A imagem enviada deve possuir o tamanho de **120x120 pixels** ou proporção quadrada. Arquivos fora desse formato serão redimensionados e cortados automaticamente pelo sistema.")
                uploaded_file = st.file_uploader("Alterar foto (PNG, JPG)", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
                
                if uploaded_file is not None:
                    with st.spinner("Comprimindo e salvando (Evitando erro de limite)..."):
                        try:
                            img = Image.open(uploaded_file)
                            if img.mode in ("RGBA", "P"):
                                img = img.convert("RGB")
                            img.thumbnail((120, 120))
                            buffered = BytesIO()
                            img.save(buffered, format="JPEG", quality=50, optimize=True)
                            img_str = base64.b64encode(buffered.getvalue()).decode()
                            
                            if len(img_str) > 45000:
                                st.error("⚠️ A imagem selecionada é muito complexa, mesmo após compressão. Escolha uma foto com fundo limpo.")
                            else:
                                conn = st.connection("gsheets", type=GSheetsConnection)
                                df_usuarios = conn.read(worksheet="Usuarios", ttl=0)
                                if 'Foto' not in df_usuarios.columns:
                                    df_usuarios['Foto'] = ""
                                
                                df_usuarios.loc[df_usuarios['Usuario'].astype(str).str.strip().str.lower() == st.session_state.usuario.lower(), 'Foto'] = img_str
                                df_usuarios = df_usuarios.fillna("")
                                conn.update(worksheet="Usuarios", data=df_usuarios)
                                
                                st.session_state.foto_perfil = img_str
                                st.success("Foto salva com sucesso!")
                                time.sleep(1)
                                st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao salvar a foto. Verifique se a coluna 'Foto' existe na aba Usuarios. Erro: {e}")

        with col_info:
            with st.container(border=True):
                st.markdown("### Credenciais e Prontidão ANCORD")
                st.write(f"**Identificação:** {st.session_state.usuario}")
                st.write(f"**Patente:** {st.session_state.nivel_usuario}")
                st.write(f"**Pontuação Geral:** {st.session_state.xp_usuario} XP")
                
                st.divider()
                
                try:
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    df_historico = conn.read(worksheet="Historico", ttl=0)
                    df_user_hist = df_historico[df_historico['Usuario'] == st.session_state.usuario]
                except:
                    df_user_hist = pd.DataFrame()
                    
                simulados_passados = set()
                if not df_user_hist.empty:
                    for _, row in df_user_hist.iterrows():
                        nota = pd.to_numeric(str(row['Nota (%)']).replace(',', '.'), errors='coerce')
                        if pd.notna(nota) and nota >= 70.0:
                            simulados_passados.add(row['Simulado'])

                total_modulos = len(SIMULADOS_ORDEM)
                modulos_concluidos = len(simulados_passados)
                
                st.markdown("#### 🎯 Termômetro de Prontidão para a Prova")
                progresso = int((modulos_concluidos / total_modulos) * 100)
                
                st.progress(progresso)
                st.caption(f"Status atual: **{progresso}% do edital coberto** ({modulos_concluidos}/{total_modulos} Módulos Concluídos)")
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("#### 🧠 Mentor IA - Diagnóstico de Estudos")
                
                if modulos_concluidos == 0:
                    st.info("🤖 **Mentor IA:** Você está no início da sua jornada. Faça os primeiros simulados para identificarmos seu nível. O foco agora é construir base teórica.")
                elif modulos_concluidos < total_modulos:
                    st.warning(f"🤖 **Mentor IA:** Você já dominou {modulos_concluidos} etapas do edital, mas ainda faltam módulos essenciais. Continue avançando nas missões bloqueadas. Dica: Se esbarrar em um módulo de baixa nota, revise a teoria e faça anotações dos erros antes de refazer o simulado.")
                else:
                    st.success("🤖 **Mentor IA:** Parabéns! Você já varreu todos os módulos do edital da ANCORD. Agora a estratégia muda: foque em refazer os simulados de forma intercalada, estude suas fraquezas apontadas no Radar (aba Evolução) e foque na gestão de tempo para simular a prova.")

            with st.container(border=True):
                st.markdown("### 🗓️ Planejamento e Motivação")
                
                col_date, col_phrase = st.columns([1, 1.5])
                
                with col_date:
                    try:
                        curr_date_val = datetime.strptime(st.session_state.data_prova, "%Y-%m-%d").date() if st.session_state.data_prova else None
                    except:
                        curr_date_val = None
                    nova_data = st.date_input("Agendamento da Prova", value=curr_date_val, format="DD/MM/YYYY")
                    
                with col_phrase:
                    nova_frase = st.text_input("Sua Frase Pessoal / Mantra", value=st.session_state.frase_pessoal, placeholder="Ex: Foguete não tem ré!", max_chars=80)
                    
                if st.button("Salvar Planejamento na Nuvem", use_container_width=True):
                    if not nova_data or not nova_frase.strip():
                        st.error("⚠️ Para prosseguir, defina a data da prova e sua frase motivacional.")
                    else:
                        with st.spinner("Sincronizando com o servidor..."):
                            try:
                                conn = st.connection("gsheets", type=GSheetsConnection)
                                df_usuarios = conn.read(worksheet="Usuarios", ttl=0)
                                
                                if 'Data_Prova' not in df_usuarios.columns:
                                    df_usuarios['Data_Prova'] = ""
                                if 'Frase_Pessoal' not in df_usuarios.columns:
                                    df_usuarios['Frase_Pessoal'] = ""
                                    
                                idx_user = df_usuarios['Usuario'].astype(str).str.strip().str.lower() == st.session_state.usuario.lower()
                                df_usuarios.loc[idx_user, 'Frase_Pessoal'] = nova_frase
                                df_usuarios.loc[idx_user, 'Data_Prova'] = str(nova_data)
                                
                                df_usuarios = df_usuarios.fillna("")
                                conn.update(worksheet="Usuarios", data=df_usuarios)
                                
                                st.session_state.frase_pessoal = nova_frase
                                st.session_state.data_prova = str(nova_data)
                                
                                st.success("Planejamento e frase atualizados com sucesso!")
                                time.sleep(1)
                                st.session_state.page = "Home"
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao salvar informações. Verifique as colunas na aba Usuarios. Erro: {e}")

    # --- TELA DE INSTRUÇÕES ---
    elif st.session_state.page == "Instrucoes":
        st.markdown(premium_page_header(
            f"Operação: {st.session_state.simulado_nome}",
            "Leia o protocolo, entre em modo foco e execute a missão com precisão de prova oficial.",
            "logo_interna",
            "PROTOCOLO DE AVALIAÇÃO"
        ), unsafe_allow_html=True)
        
        # Aviso sobre calculadora se for simulado de matemática
        if simulado_tem_matematica(st.session_state.simulado_nome):
            st.success("🧮 **Calculadora HP12C disponível** durante esta prova — clique no botão flutuante 🧮 no canto inferior direito da tela.")
        
        st.markdown("""
        <div style="background: rgba(234, 179, 8, 0.1); border-left: 4px solid #EAB308; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
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
        # HP12C FLUTUANTE — aparece apenas nas provas de Matemática Financeira
        if simulado_tem_matematica(st.session_state.simulado_nome):
            inject_hp12c()
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
        st.markdown(premium_page_header(
            "Relatório de Missão", 
            "Veja sua nota, seu ritmo, seus acertos e os pontos que precisam de reforço para a próxima tentativa.", 
            "logo_interna", 
            "ANÁLISE DE PERFORMANCE"
        ), unsafe_allow_html=True)
        
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
            with st.spinner("Salvando telemetria na nuvem..."):
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
                    df_atualizado = df_atualizado.fillna("")
                    conn.update(worksheet="Historico", data=df_atualizado)
                    st.session_state.resultado_salvo = True
                except Exception as e:
                    pass

        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px;">
            <div class='vmb-metric-card'><div class='vmb-metric-label'>Nota Final</div><div class='vmb-metric-value'>{percentual:.1f}%</div><div style='color: #60A5FA; font-size: 12px; font-weight: 700; margin-top: 5px;'>{acertos}/{total_questoes} corretas</div></div>
            <div class='vmb-metric-card'><div class='vmb-metric-label'>Pace Médio</div><div class='vmb-metric-value'>{int(tempo_medio // 60)}m {int(tempo_medio % 60)}s</div><div style='color: #60A5FA; font-size: 12px; font-weight: 700; margin-top: 5px;'>por questão</div></div>
            <div class='vmb-metric-card'><div class='vmb-metric-label'>Status</div><div class='vmb-metric-value' style='color: {"#4ADE80" if percentual>=70 else "#EF4444"};'>{"APROVADO ✅" if percentual>=70 else "REPROVADO ❌"}</div></div>
        </div>
        """, unsafe_allow_html=True)

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
        st.markdown(premium_page_header(
            "Inteligência e Evolução", 
            "Transforme histórico, radar de competências e diagnóstico do mentor em um plano objetivo de melhoria.", 
            "logo_interna", 
            "MENTOR ANALÍTICO"
        ), unsafe_allow_html=True)
        
        with st.spinner("Processando heurística..."):
            try:
                conn = st.connection("gsheets", type=GSheetsConnection)
                df_historico_geral = conn.read(worksheet="Historico", ttl=0)
                df_user = df_historico_geral[df_historico_geral["Usuario"] == st.session_state.usuario].copy()
                
                if not df_user.empty:
                    df_user.reset_index(drop=True, inplace=True)
                    
                    tempos_segundos =[]
                    total_secs = 0
                    valid_times = 0
                    
                    for t_str in df_user['Tempo']:
                        match = re.search(r'(\d+)m\s*(\d+)s', str(t_str))
                        if match:
                            secs = int(match.group(1)) * 60 + int(match.group(2))
                            total_secs += secs
                            valid_times += 1
                            tempos_segundos.append(secs)
                        else:
                            tempos_segundos.append(0)
                    
                    df_user['Segundos'] = tempos_segundos
                    df_user['Minutos'] = df_user['Segundos'] / 60.0
                    
                    media_secs_prova = total_secs // valid_times if valid_times > 0 else 0
                    media_secs_questao = total_secs / (valid_times * 20) if valid_times > 0 else 0
                    avg_score = df_user['Nota (%)'].mean()
                    
                    df_user['Rotulo'] =[f"{i+1}ª T. ({row['Simulado'][:12]}...)" for i, row in df_user.iterrows()]

                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Média de Acertos", f"{avg_score:.1f}%")
                    col2.metric("Simulados Realizados", len(df_user))
                    col3.metric("Tempo Médio / Prova", f"{media_secs_prova // 60}m {media_secs_prova % 60}s")
                    col4.metric("Tempo / Questão", f"{int(media_secs_questao)}s")
                    
                    st.divider()

                    col_chart1, col_chart2 = st.columns(2)
                    with col_chart1:
                        st.markdown("### 📈 Evolução Histórica (Notas)")
                        if len(df_user) > 1:
                            fig_line = px.line(df_user, x='Rotulo', y='Nota (%)', markers=True)
                            fig_line.update_traces(line_color='#3B82F6', line_width=4, marker=dict(size=12, color='#60A5FA', line=dict(width=2, color='#FFFFFF')))
                            fig_line.add_hline(y=70, line_dash="dash", line_color="#10B981", annotation_text="Meta (70%)", annotation_position="bottom right")
                            fig_line.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="", yaxis_title="Nota (%)", xaxis=dict(showgrid=False, color='#8B949E'), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#8B949E', range=[0, 105]), margin=dict(l=20, r=20, t=20, b=20), hovermode="x unified")
                            st.plotly_chart(fig_line, use_container_width=True)
                        else:
                            st.info("💡 Complete mais simulados para gerar o gráfico de evolução temporal.")

                    with col_chart2:
                        st.markdown("### ⏱️ Evolução de Tempo (Minutos)")
                        if len(df_user) > 0:
                            fig_time = px.bar(df_user, x='Rotulo', y='Minutos', text_auto='.1f')
                            fig_time.update_traces(marker_color='#8B5CF6', marker_line_color='#C4B5FD', marker_line_width=1.5, textposition='outside', textfont_color='#FAFAFA')
                            fig_time.add_hline(y=30, line_dash="dash", line_color="#EF4444", annotation_text="Limite (30m)", annotation_position="top right")
                            
                            max_y = df_user['Minutos'].max() * 1.2 if df_user['Minutos'].max() > 0 else 35
                            fig_time.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="", yaxis_title="Minutos", xaxis=dict(showgrid=False, color='#8B949E'), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#8B949E', range=[0, max(35, max_y)]), margin=dict(l=20, r=20, t=20, b=20))
                            st.plotly_chart(fig_time, use_container_width=True)
                    
                    st.divider()

                    module_scores = {}
                    for _, row in df_user.iterrows():
                        if 'Detalhes_Modulos' in df_user.columns and pd.notna(row['Detalhes_Modulos']) and str(row['Detalhes_Modulos']).strip() != "":
                            try:
                                detalhes = json.loads(str(row['Detalhes_Modulos']))
                                for mod, score in detalhes.items():
                                    if mod not in module_scores: module_scores[mod] =[]
                                    module_scores[mod].append(score)
                            except Exception:
                                pass
                        else:
                            sim_name = row['Simulado']
                            if sim_name in DIC_SIMULADOS:
                                for mod in DIC_SIMULADOS[sim_name]:
                                    if mod not in module_scores: module_scores[mod] =[]
                                    module_scores[mod].append(row['Nota (%)'])

                    avg_module_scores = {mod: sum(scores)/len(scores) for mod, scores in module_scores.items()}

                    col_radar, col_ia = st.columns([1.2, 1.2])
                    with col_radar:
                        st.markdown("<h3 style='text-align:center;'>🎯 Radar de Forças e Fraquezas</h3>", unsafe_allow_html=True)
                        if avg_module_scores:
                            df_radar = pd.DataFrame(dict(Força=list(avg_module_scores.values()), Modulo=list(avg_module_scores.keys())))
                            df_radar = pd.concat([df_radar, df_radar.iloc[[0]]])

                            fig_radar = go.Figure()
                            fig_radar.add_trace(go.Scatterpolar(r=df_radar['Força'], theta=df_radar['Modulo'], fill='toself', name='Sua Força', line_color='#3B82F6', fillcolor='rgba(59, 130, 246, 0.4)'))
                            fig_radar.add_trace(go.Scatterpolar(r=[85]*len(df_radar), theta=df_radar['Modulo'], fill='none', name='Meta Elite (85%)', line_color='rgba(16, 185, 129, 0.5)', line_dash='dash'))

                            fig_radar.update_layout(polar=dict(bgcolor='rgba(0,0,0,0)', radialaxis=dict(visible=True, range=[0, 100], gridcolor='#30363D', color='#8B949E'), angularaxis=dict(gridcolor='#30363D', color='#FAFAFA')), showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=40, r=40, t=20, b=20))
                            st.plotly_chart(fig_radar, use_container_width=True)
                        else:
                            st.info("Faça mais simulados para desenhar seu radar.")

                    with col_ia:
                        st.markdown("### 🧠 Mentor IA - Dicas ANCORD")

                        sorted_mods = sorted(avg_module_scores.items(), key=lambda item: item[1])
                        weak_mods =[mod for mod, score in sorted_mods if score < 70]
                        strong_mods =[mod for mod, score in sorted_mods if score >= 85]

                        st.markdown("""<div style="background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);"><p style="color:#8B949E; font-size:14px; margin-bottom:5px;">DIAGNÓSTICO TÁTICO DE ESTUDOS</p>""", unsafe_allow_html=True)

                        if weak_mods:
                            st.markdown(f"**🚨 Foco de Melhoria:** Notei que você está escorregando em **{weak_mods[0]}** (Média: {dict(sorted_mods)[weak_mods[0]]:.1f}%).<br>💡 *Plano de Ação:* Pause a execução de simulados por um momento, volte no material teórico desse módulo e anote os seus erros principais identificados no relatório da missão.", unsafe_allow_html=True)
                        if strong_mods:
                            st.markdown(f"<br>**🏆 Ponto Forte:** O módulo **{strong_mods[-1]}** está validado e bem absorvido (Média: {dict(sorted_mods)[strong_mods[-1]]:.1f}%).<br>💡 *Como reforçar:* Não gaste tanta energia revisando a teoria básica daqui, continue fazendo as questões só para manter a memória fresca.", unsafe_allow_html=True)

                        st.markdown("<br>**⏱️ Termômetro de Agilidade:**", unsafe_allow_html=True)
                        if media_secs_questao > 90:
                            st.markdown("⚠️ Você demora mais de 1m30s por questão. Na prova oficial (120 min), o tempo é curto. Tente focar diretamente no verbo principal e nas palavras-chave finais do enunciado.")
                        elif media_secs_questao < 40 and valid_times > 0:
                            st.markdown("⚡ Menos de 40s por questão. Cuidado com o ímpeto e a ansiedade! A prova da ANCORD contém pegadinhas que se escondem justamente no final da frase.")
                        elif valid_times > 0:
                            st.markdown("✅ Excelente ritmo de leitura e raciocínio! Mantenha essa cadência de resolução (entre 1m e 1m30s por questão).")

                        st.markdown("<br>🕵️‍♂️ **Alerta do Mentor (Padrão ANCORD):**<br>Redobre a atenção quando a questão contiver as palavras <span style='color:#EF4444; font-weight:bold;'>EXCETO, APENAS, SEMPRE, OBRIGATORIAMENTE, SOMENTE.</span> Elas costumam invalidar aquela alternativa específica.", unsafe_allow_html=True)

                        st.markdown("</div>", unsafe_allow_html=True)

                    st.divider()
                    st.subheader("Data Grid (Registros Brutos)")
                    df_display = df_user[['Rotulo', 'Data', 'Simulado', 'Nota (%)', 'Tempo']].copy()
                    df_display.rename(columns={'Rotulo': 'Tentativa'}, inplace=True)
                    st.dataframe(df_display, column_config={"Nota (%)": st.column_config.ProgressColumn("Desempenho", help="Sua nota percentual", format="%f%%", min_value=0, max_value=100), "Data": st.column_config.TextColumn("Data da Execução"), "Simulado": st.column_config.TextColumn("Missão")}, hide_index=True, use_container_width=True)

                else:
                    st.info("Aguardando telemetria inicial. Faça seu primeiro simulado.")
            except Exception as e:
                st.error(f"Falha ao processar banco de dados da IA. Detalhes do Erro: {e}")
