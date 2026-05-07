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
            font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
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

        .stApp::after {
            content: "";
            position: fixed;
            width: 420px;
            height: 420px;
            right: -100px;
            top: 100px;
            pointer-events: none;
            z-index: 0;
            background: radial-gradient(circle, rgba(37,99,235,0.08), transparent 70%);
            filter: blur(60px);
            opacity: 0.5;
        }

        .block-container {
            position: relative;
            z-index: 1;
            padding-top: 2.2rem !important;
            padding-bottom: 4rem !important;
            max-width: 1220px !important;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {background-color: transparent !important;}

        h1, h2, h3, h4 {
            color: var(--vmb-white) !important;
            font-family: 'Inter', sans-serif !important;
            letter-spacing: -0.02em !important;
            text-shadow: none !important;
        }

        p, li, label, span, div { font-family: 'Inter', sans-serif !important; }

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
            background: none;
            -webkit-text-fill-color: initial;
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

        .vmb-illustration svg {
            width: min(100%, 320px);
            height: auto;
            filter: drop-shadow(0 15px 30px rgba(0,0,0,0.3));
            opacity: 0.9;
        }

        section[data-testid="stSidebar"] .vmb-illustration {
            min-height: 120px;
            margin: 4px 0 12px;
        }

        section[data-testid="stSidebar"] .vmb-illustration svg {
            width: min(100%, 210px);
        }

        .vmb-premium-card,
        div[data-testid="stVerticalBlock"] div[style*="border"] {
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
            position: relative;
            overflow: hidden;
            border-radius: 20px;
            padding: 24px;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(148, 163, 184, 0.12);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(8px);
        }

        .vmb-metric-card::after {
            content: "";
            position: absolute;
            width: 100px;
            height: 100px;
            right: -40px;
            top: -40px;
            background: radial-gradient(circle, rgba(59,130,246,0.15), transparent 70%);
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

        .vmb-section-banner h3 { margin: 0 !important; font-size: 22px; }
        .vmb-section-banner p { margin: 4px 0 0; color: #9AA8BD; }

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

        button[kind="secondary"]:hover {
            border-color: #EF4444 !important;
            color: #FCA5A5 !important;
        }

        .stTextInput input {
            border-radius: 14px !important;
            background-color: rgba(2, 6, 23, 0.58) !important;
            border: 1px solid rgba(148, 163, 184, 0.18) !important;
            color: white !important;
            min-height: 46px !important;
        }

        .stTextInput input:focus {
            border-color: #60A5FA !important;
            box-shadow: 0 0 0 3px rgba(59,130,246,0.18) !important;
        }

        .stRadio [role="radiogroup"] {
            gap: 8px;
        }

        .stRadio label {
            border-radius: 14px !important;
            padding: 10px 12px !important;
            background: rgba(15,23,42,0.42) !important;
            border: 1px solid rgba(148,163,184,0.12) !important;
        }

        [data-testid="stMetric"] {
            border-radius: 22px;
            padding: 18px;
            background: linear-gradient(145deg, rgba(15,23,42,0.86), rgba(2,6,23,0.74));
            border: 1px solid rgba(148,163,184,0.16);
            box-shadow: 0 18px 48px rgba(0,0,0,0.30);
        }

        section[data-testid="stSidebar"] {
            background:
                radial-gradient(circle at 50% 0%, rgba(37,99,235,0.24), transparent 32%),
                linear-gradient(180deg, rgba(2,6,23,0.96), rgba(8,13,28,0.96)) !important;
            border-right: 1px solid rgba(148,163,184,0.14) !important;
            backdrop-filter: blur(20px) !important;
        }

        [data-testid="stDataFrame"], .stAlert, .stExpander {
            border-radius: 18px !important;
            overflow: hidden !important;
        }

        hr { border-color: rgba(148,163,184,0.14) !important; }

        @media (max-width: 900px) {
            .vmb-hero-grid, .vmb-metrics-grid { grid-template-columns: 1fr; }
            .vmb-illustration { min-height: 160px; }
        }
    </style>
    """, unsafe_allow_html=True)


def premium_illustration(kind="rocket"):
    illustrations = {
        "rocket": """
        <svg viewBox='0 0 420 300' fill='none' xmlns='http://www.w3.org/2000/svg'>
          <defs><linearGradient id='g1' x1='80' y1='240' x2='310' y2='35' gradientUnits='userSpaceOnUse'><stop stop-color='#1D4ED8'/><stop offset='.55' stop-color='#60A5FA'/><stop offset='1' stop-color='#FFFFFF'/></linearGradient><filter id='blur1'><feGaussianBlur stdDeviation='18'/></filter></defs>
          <circle cx='296' cy='68' r='42' fill='#2563EB' opacity='.18'/><circle cx='110' cy='220' r='64' fill='#60A5FA' opacity='.10'/>
          <path d='M62 222C130 172 192 156 306 154' stroke='#60A5FA' stroke-opacity='.35' stroke-width='2' stroke-dasharray='8 10'/>
          <path d='M232 74C276 56 324 66 350 86C346 126 319 169 282 194L232 74Z' fill='url(#g1)'/>
          <path d='M217 92L161 116L202 135L217 92Z' fill='#1E40AF'/><path d='M265 207L250 252L226 205L265 207Z' fill='#1E40AF'/>
          <path d='M187 128L274 215L220 222L153 155L187 128Z' fill='#EAF2FF'/><circle cx='273' cy='125' r='21' fill='#0B1220' stroke='#BFDBFE' stroke-width='7'/>
          <path d='M161 173C130 184 105 207 89 240C123 224 148 221 174 226L161 173Z' fill='#2563EB'/><path d='M155 184C134 198 120 215 109 234' stroke='#FFFFFF' stroke-opacity='.42' stroke-width='5' stroke-linecap='round'/>
          <path d='M153 156L221 224' stroke='#0F172A' stroke-opacity='.22' stroke-width='4'/>
        </svg>""",
        "growth": """
        <svg viewBox='0 0 420 300' fill='none' xmlns='http://www.w3.org/2000/svg'>
          <defs><linearGradient id='g2' x1='66' y1='238' x2='338' y2='72'><stop stop-color='#1D4ED8'/><stop offset='1' stop-color='#93C5FD'/></linearGradient></defs>
          <rect x='54' y='205' width='44' height='48' rx='12' fill='#1D4ED8'/><rect x='124' y='170' width='44' height='83' rx='12' fill='#2563EB'/><rect x='194' y='128' width='44' height='125' rx='12' fill='#3B82F6'/><rect x='264' y='82' width='44' height='171' rx='12' fill='#60A5FA'/>
          <path d='M70 172C122 156 154 133 194 108C232 84 266 68 335 54' stroke='url(#g2)' stroke-width='10' stroke-linecap='round'/><path d='M310 43L344 52L318 77' stroke='#EAF2FF' stroke-width='8' stroke-linecap='round' stroke-linejoin='round'/>
          <circle cx='83' cy='76' r='32' fill='#60A5FA' opacity='.14'/><circle cx='338' cy='211' r='48' fill='#2563EB' opacity='.10'/><path d='M56 254H346' stroke='#94A3B8' stroke-opacity='.25' stroke-width='2'/>
        </svg>""",
        "dashboard": """
        <svg viewBox='0 0 420 300' fill='none' xmlns='http://www.w3.org/2000/svg'>
          <rect x='54' y='45' width='312' height='210' rx='26' fill='rgba(15,23,42,.9)' stroke='rgba(147,197,253,.35)' stroke-width='2'/><rect x='78' y='72' width='118' height='76' rx='18' fill='rgba(37,99,235,.28)'/><rect x='214' y='72' width='128' height='76' rx='18' fill='rgba(255,255,255,.06)'/>
          <path d='M94 130L119 106L145 119L176 88' stroke='#93C5FD' stroke-width='7' stroke-linecap='round' stroke-linejoin='round'/><circle cx='292' cy='110' r='32' stroke='#60A5FA' stroke-width='12'/><path d='M292 78A32 32 0 0 1 324 110' stroke='#FFFFFF' stroke-width='12' stroke-linecap='round'/>
          <rect x='78' y='169' width='264' height='14' rx='7' fill='rgba(148,163,184,.16)'/><rect x='78' y='169' width='184' height='14' rx='7' fill='#2563EB'/><rect x='78' y='200' width='264' height='14' rx='7' fill='rgba(148,163,184,.16)'/><rect x='78' y='200' width='222' height='14' rx='7' fill='#60A5FA'/>
          <circle cx='354' cy='54' r='32' fill='#2563EB' opacity='.20'/><circle cx='62' cy='244' r='40' fill='#60A5FA' opacity='.10'/>
        </svg>""",
        "ai": """
        <svg viewBox='0 0 420 300' fill='none' xmlns='http://www.w3.org/2000/svg'>
          <rect x='134' y='58' width='152' height='152' rx='38' fill='rgba(37,99,235,.22)' stroke='rgba(147,197,253,.45)' stroke-width='3'/><circle cx='184' cy='129' r='13' fill='#EAF2FF'/><circle cx='236' cy='129' r='13' fill='#EAF2FF'/><path d='M178 166C194 181 226 181 242 166' stroke='#60A5FA' stroke-width='7' stroke-linecap='round'/>
          <path d='M210 33V58M210 210V238M109 134H134M286 134H314M130 72L148 90M290 72L272 90M130 196L148 178M290 196L272 178' stroke='#60A5FA' stroke-width='7' stroke-linecap='round'/>
          <path d='M76 226C135 246 217 254 343 225' stroke='#2563EB' stroke-opacity='.35' stroke-width='3' stroke-dasharray='7 9'/><circle cx='79' cy='225' r='8' fill='#60A5FA'/><circle cx='343' cy='225' r='8' fill='#60A5FA'/><circle cx='210' cy='33' r='7' fill='#93C5FD'/>
        </svg>""",
        "performance": """
        <svg viewBox='0 0 420 300' fill='none' xmlns='http://www.w3.org/2000/svg'>
          <circle cx='210' cy='150' r='94' fill='rgba(37,99,235,.12)' stroke='rgba(147,197,253,.26)' stroke-width='3'/><path d='M210 72V150L266 106' stroke='#60A5FA' stroke-width='10' stroke-linecap='round' stroke-linejoin='round'/><path d='M128 150A82 82 0 0 1 293 150' stroke='#2563EB' stroke-width='16' stroke-linecap='round'/><path d='M152 209C183 238 236 238 268 209' stroke='#EAF2FF' stroke-width='10' stroke-linecap='round'/>
          <rect x='54' y='196' width='70' height='38' rx='15' fill='rgba(255,255,255,.08)' stroke='rgba(147,197,253,.25)'/><rect x='296' y='196' width='70' height='38' rx='15' fill='rgba(37,99,235,.26)' stroke='rgba(147,197,253,.25)'/><circle cx='76' cy='214' r='8' fill='#60A5FA'/><circle cx='318' cy='214' r='8' fill='#EAF2FF'/>
          <path d='M83 84C121 55 154 45 199 44' stroke='#60A5FA' stroke-opacity='.28' stroke-width='3' stroke-dasharray='8 10'/><path d='M220 45C264 50 298 67 331 100' stroke='#60A5FA' stroke-opacity='.28' stroke-width='3' stroke-dasharray='8 10'/>
        </svg>"""
    }
    return f"<div class='vmb-illustration'>{illustrations.get(kind, illustrations['rocket'])}</div>"


def premium_page_header(title, subtitle, kind="dashboard", eyebrow="VMB INVEST | PERFORMANCE SYSTEM"):
    return f"""
    <div class='vmb-hero'>
        <div class='vmb-hero-grid'>
            <div>
                <div class='vmb-eyebrow'>{eyebrow}</div>
                <div class='vmb-title'>{title}</div>
                <p class='vmb-subtitle'>{subtitle}</p>
            </div>
            {premium_illustration(kind)}
        </div>
    </div>
    """


def premium_section_banner(title, subtitle):
    return f"""
    <div class='vmb-section-banner'>
        <div>
            <h3>{title}</h3>
            <p>{subtitle}</p>
        </div>
        <div style='font-weight:900;color:#BFDBFE;'>PREMIUM</div>
    </div>
    """


def premium_metric_card(label, value, hint=""):
    return f"""
    <div class='vmb-metric-card'>
        <div class='vmb-metric-label'>{label}</div>
        <div class='vmb-metric-value'>{value}</div>
        <div class='vmb-metric-hint'>{hint}</div>
    </div>
    """

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
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([0.8, 2.4, 0.8])
    
    with col2:
        st.markdown(premium_page_header(
            "VMB INVEST",
            "Treinamento de alta performance para assessores que querem evoluir com método, dados e mentalidade de elite.",
            "rocket",
            "SIMULADO DE ELITE"
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
        
        st.markdown(premium_illustration("growth"), unsafe_allow_html=True)
        menu = st.radio("Módulos da Plataforma", ["Dashboard Principal", "Evolução e IA"])
        
        # Botão de SAIR no final da Sidebar
        st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
        st.divider()
        if st.button("🚪 Sair do Sistema", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    # Redirecionamento lógico do menu
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
            "Escolha sua próxima missão, acompanhe seu progresso e avance por uma jornada de evolução orientada por performance.",
            "dashboard",
            "DASHBOARD PRINCIPAL"
        ), unsafe_allow_html=True)
        
        # BURACO PARA AS MÉTRICAS INICIAIS
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            df_historico = conn.read(worksheet="Historico", ttl=0)
            df_user_hist = df_historico[df_historico['Usuario'] == st.session_state.usuario]
            
            avg_score = df_user_hist['Nota (%)'].mean() if not df_user_hist.empty else 0
            max_score = df_user_hist['Nota (%)'].max() if not df_user_hist.empty else 0
            qtd_sim = len(df_user_hist)
            
            st.markdown(f"""
            <div class='vmb-metrics-grid'>
                {premium_metric_card("Aproveitamento Geral", f"{avg_score:.1f}%", "média acumulada")}
                {premium_metric_card("Melhor Nota", f"{max_score:.1f}%", "recorde pessoal")}
                {premium_metric_card("Simulados Concluídos", f"{qtd_sim}", "missões finalizadas")}
            </div>
            """, unsafe_allow_html=True)
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
            "performance",
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
            "growth",
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
        col3.metric("Status", "APROVADO" if percentual >= 70 else "REPROVADO")

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
            "Inteligência de Dados e Evolução",
            "Transforme histórico, radar de competências e diagnóstico do mentor em um plano objetivo de melhoria.",
            "ai",
            "MENTOR ANALÍTICO"
        ), unsafe_allow_html=True)
        
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
