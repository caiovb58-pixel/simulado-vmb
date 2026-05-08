importar streamlit como st
importar aleatório
import pandas as pd
from datetime import datetime
tempo de importação
importar os
importar json
importar re
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection

# --- MISSÕES ---
tentar:
    from questoes importar BANCO_QUESTOES
exceto ImportError:
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
        botão[título="Ver em tela cheia"] { display: none !important; }
        .stDeployButton { display: none !important; }
        
        :raiz {
            --vmb-preto: #050812;
            --vmb-black-2: #0A1020;
            --cartão vmb: rgba(10, 16, 32, 0,72);
            --vmb-card-forte: rgba(12, 18, 35, 0,92);
            --vmb-blue: #2563EB;
            --vmb-blue-2: #3B82F6;
            --vmb-blue-3: #60A5FA;
            --vmb-white: #F8FAFC;
            --vmb-muted: #9AA8BD;
            --vmb-border: rgba(148, 163, 184, 0,18);
            --vmb-brilho: rgba(37, 99, 235, 0,32);
        }

        html, corpo, [classe*="css"] {
            font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        }

        .stApp {
            cor: var(--vmb-branco);
            fundo:
                gradiente-radial(círculo em 12% 8%, rgba(37, 99, 235, 0.12) 0, transparente 40%),
                gradiente-radial(círculo em 88% 18%, rgba(96, 165, 250, 0.08) 0, transparente 30%),
                gradiente-linear(135 graus, #020617 0%, #050B14 100%) !importante;
            background-attachment: fixed !important;
        }

        .stApp::before {
            contente: "";
            posição: fixa;
            inserção: 0;
            eventos-ponteiro: nenhum;
            Índice z: 0;
            imagem de fundo:
                gradiente-linear(rgba(255,255,255,0.035) 1px, transparente 1px),
                gradiente-linear(90 graus, rgba(255,255,255,0.035) 1px, transparente 1px),
                gradiente radial (círculo a 30% 30%, rgba(59,130,246,0.13), transparente 22%),
                gradiente-radial(círculo em 75% 62%, rgba(255,255,255,0.06), transparente 18%);
            background-size: 56px 56px, 56px 56px, 100% 100%, 100% 100%;
            máscara-imagem: gradiente-linear(para baixo, rgba(0,0,0,0.9), rgba(0,0,0,0.2));
        }

        .stApp::after {
            contente: "";
            posição: fixa;
            largura: 420px;
            altura: 420px;
            direita: -100px;
            topo: 100px;
            eventos-ponteiro: nenhum;
            Índice z: 0;
            fundo: gradiente radial(círculo, rgba(37,99,235,0.08), transparente 70%);
            filtro: desfoque(60px);
            opacidade: 0,5;
        }

        .block-container {
            posição: relativa;
            Índice z: 1;
            padding-top: 2.2rem !important;
            padding-bottom: 4rem !important;
            largura máxima: 1220px !importante;
        }

        #MenuPrincipal {visibilidade: oculta;}
        rodapé {visibilidade: oculto;}
        cabeçalho {cor de fundo: transparente !importante;}

        h1, h2, h3, h4 {
            cor: var(--vmb-white) !importante;
            família-da-fonte: 'Inter', sem serifa !importante;
            espaçamento entre letras: -0,02em !importante;
            text-shadow: none !important;
        }

        p, li, label, span, div { font-family: 'Inter', sans-serif !important; }

        .vmb-hero {
            posição: relativa;
            overflow: oculto;
            borda: 1px sólida rgba(148, 163, 184, 0.14);
            raio da borda: 24px;
            preenchimento: 32px;
            fundo: gradiente-linear(145deg, rgba(15, 23, 42, 0.95), rgba(2, 6, 23, 0.98));
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
            filtro de fundo: desfoque(12px);
            margem-inferior: 24px;
        }

        .vmb-hero::before {
            contente: "";
            posição: absoluta;
            inserção: 0;
            fundo: gradiente-linear(120deg, rgba(255,255,255,0.13), transparente 24%, transparente 74%, rgba(96,165,250,0.12));
            eventos-ponteiro: nenhum;
        }

        .vmb-sobrancelha {
            exibição: inline-flex;
            alinhamento-itens: centro;
            espaço: 8px;
            preenchimento: 8px 12px;
            borda: 1px sólida rgba(96, 165, 250, 0.28);
            raio-da-borda: 999px;
            fundo: rgba(37, 99, 235, 0.12);
            Cor: #BFDBFE;
            peso da fonte: 800;
            tamanho da fonte: 12px;
            espaçamento entre letras: 0,08em;
            text-transform: maiúsculas;
        }

        .vmb-title {
            tamanho da fonte: clamp(32px, 4.5vw, 56px);
            altura da linha: 1,05;
            margem: 12px 0 8px;
            peso da fonte: 800;
            cor: #FFFFFF !importante;
            Contexto: nenhum;
            -webkit-text-fill-color: inicial;
        }

        .vmb-subtitle {
            Cor: #AAB8CF;
            tamanho da fonte: 16px;
            altura da linha: 1,65;
            largura máxima: 680px;
            margem: 0;
        }

        .vmb-hero-grid {
            Exibir: grade;
            grid-template-columns: minmax(0, 1.15fr) minmax(260px, 0.85fr);
            espaço: 22px;
            alinhamento-itens: centro;
        }

        .vmb-ilustração {
            posição: relativa;
            altura mínima: 230px;
            Exibir: flexível;
            alinhamento-itens: centro;
            justificar-conteúdo: centralizado;
        }

        .vmb-ilustração svg {
            largura: min(100%, 320px);
            altura: automática;
            filtro: sombra-projetada(0 15px 30px rgba(0,0,0,0.3));
            opacidade: 0,9;
        }

        seção[data-testid="stSidebar"] .vmb-illustration {
            altura mínima: 120px;
            margem: 4px 0 12px;
        }

        seção[data-testid="stSidebar"] .vmb-illustration svg {
            largura: min(100%, 210px);
        }

        .vmb-premium-card,
        div[data-testid="stVerticalBlock"] div[style*="border"] {
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.82), rgba(2, 6, 23, 0.74)) !important;
            borda: 1px sólido var(--vmb-border) !importante;
            border-radius: 22px !important;
            box-shadow: 0 20px 60px rgba(2,6,23,0.42), inset 0 1px 0 rgba(255,255,255,0.05) !important;
            preenchimento: 22px !importante;
            transição: transformar 0,25s suavizar, cor da borda 0,25s suavizar, sombra da caixa 0,25s suavizar !importante;
            backdrop-filter: blur(18px) !important;
        }

        div[data-testid="stVerticalBlock"] div[style*="border"]:hover {
            transformar: translateY(-4px) !importante;
            cor da borda: rgba(96, 165, 250, 0.56) !importante;
            box-shadow: 0 26px 78px rgba(37, 99, 235, 0.20), inset 0 1px 0 rgba(255,255,255,0.08) !important;
        }

        .vmb-metrics-grid {
            Exibir: grade;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            espaçamento: 16px;
            margem: 18px 0 28px;
        }

        .vmb-metric-card {
            posição: relativa;
            overflow: oculto;
            raio da borda: 20px;
            preenchimento: 24px;
            fundo: rgba(15, 23, 42, 0.6);
            borda: 1px sólida rgba(148, 163, 184, 0.12);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            filtro de fundo: desfoque(8px);
        }

        .vmb-metric-card::after {
            contente: "";
            posição: absoluta;
            largura: 100px;
            altura: 100px;
            direita: -40px;
            topo: -40px;
            fundo: gradiente radial(círculo, rgba(59,130,246,0.15), transparente 70%);
        }

        .vmb-metric-label { color: #94A3B8; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; }
        .vmb-metric-value { color: #FFFFFF; font-size: 30px; font-weight: 900; margin-top: 8px; letter-spacing: -0.04em; }
        .vmb-metric-hint { color: #60A5FA; font-size: 12px; font-weight: 700; margin-top: 5px; }

        .vmb-section-banner {
            Exibir: flexível;
            alinhamento-itens: centro;
            justify-content: espaço-entre;
            espaçamento: 18px;
            preenchimento: 18px 20px;
            margem: 18px 0 16px;
            raio da borda: 22px;
            fundo: gradiente-linear(90deg, rgba(37,99,235,0.20), rgba(15,23,42,0.64));
            borda: 1px sólida rgba(96,165,250,0.20);
        }

        .vmb-section-banner h3 { margin: 0 !important; font-size: 22px; }
        .vmb-section-banner p { margin: 4px 0 0; color: #9AA8BD; }

        .stButton>botão {
            border-radius: 12px !important;
            peso da fonte: 800 !importante;
            espaçamento entre letras: 0,01em !importante;
            transição: todos os 0,25s de facilidade !importante;
            altura mínima: 44px !importante;
            borda: 1px sólida rgba(148,163,184,0.18) !importante;
            fundo: rgba(15,23,42,0.78) !importante;
            cor: #F8FAFC !importante;
        }

        .stButton>button[kind="primary"] {
            background: linear-gradient(92deg, #1D4ED8, #2563EB 48%, #60A5FA) !important;
            borda: 1px sólida rgba(191,219,254,0.25) !importante;
            box-shadow: 0 12px 30px rgba(37, 99, 235, 0.42) !important;
        }

        .stButton>button:hover {
            transform: translateY(-2px) scale(1.01) !important;
            cor da borda: rgba(96,165,250,0.62) !importante;
            box-shadow: 0 16px 40px rgba(37,99,235,0.28) !important;
        }

        botão[tipo="secundário"]:hover {
            cor da borda: #EF4444 !importante;
            cor: #FCA5A5 !importante;
        }

        .stTextInput input {
            border-radius: 14px !important;
            cor de fundo: rgba(2, 6, 23, 0.58) !importante;
            borda: 1px sólida rgba(148, 163, 184, 0.18) !importante;
            cor: branco !importante;
            altura mínima: 46px !importante;
        }

        .stTextInput input:focus {
            cor da borda: #60A5FA !importante;
            box-shadow: 0 0 0 3px rgba(59,130,246,0.18) !important;
        }

        .stRadio [role="radiogroup"] {
            espaço: 8px;
        }

        .stRadio label {
            border-radius: 14px !important;
            preenchimento: 10px 12px !importante;
            fundo: rgba(15,23,42,0.42) !importante;
            borda: 1px sólida rgba(148,163,184,0.12) !importante;
        }

        [data-testid="stMetric"] {
            raio da borda: 22px;
            preenchimento: 18px;
            fundo: gradiente-linear(145deg, rgba(15,23,42,0.86), rgba(2,6,23,0.74));
            borda: 1px sólida rgba(148,163,184,0.16);
            box-shadow: 0 18px 48px rgba(0,0,0,0.30);
        }

        seção[data-testid="stSidebar"] {
            fundo:
                gradiente-radial(círculo a 50% 0%, rgba(37,99,235,0.24), transparente 32%),
                gradiente-linear(180 graus, rgba(2,6,23,0.96), rgba(8,13,28,0.96)) !importante;
            borda-direita: 1px sólida rgba(148,163,184,0.14) !importante;
            backdrop-filter: blur(20px) !important;
        }

        [data-testid="stDataFrame"], .stAlert, .stExpander {
            border-radius: 18px !important;
            overflow: oculto !importante;
        }

        hr { border-color: rgba(148,163,184,0.14) !important; }

        @media (max-width: 900px) {
            .vmb-hero-grid, .vmb-metrics-grid { grid-template-columns: 1fr; }
            .vmb-illustration { min-height: 160px; }
        }
    </style>
    "", unsafe_allow_html=True)


def premium_illustration(kind):
    se tipo == "logotipo":
        importar base64
        tentar:
            com open("Logo_VMB_V.png", "rb") as f:
                dados = base64.b64encode(f.read()).decode()
            # Aplicando um brilho suave atrás do logo para que o preto não suma no fundo
            return f"<div class='vmb-illustration'><img src='data:image/png;base64,{data}' style='width:100%; max-width:280px; filter: drop-shadow(0 0 15px rgba(255,255,255,0.15)) drop-shadow(0 10px 20px rgba(0,0,0,0.4)); background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%); border-radius: 50%; padding: 20px;'></div>"
        exceto:
            kind = "rocket" # Fallback se o arquivo não existir

    ilustrações = {
        "foguete": """
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
        "crescimento": """
        <svg viewBox='0 0 420 300' fill='none' xmlns='http://www.w3.org/2000/svg'>
          <defs><linearGradient id='g2' x1='66' y1='238' x2='338' y2='72'><stop stop-color='#1D4ED8'/><stop offset='1' stop-color='#93C5FD'/></linearGradient></defs>
          <rect x='54' y='205' width='44' height='48' rx='12' fill='#1D4ED8'/><rect x='124' y='170' width='44' height='83' rx='12' fill='#2563EB'/><rect x='194' y='128' width='44' height='125' rx='12' fill='#3B82F6'/><rect x='264' y='82' width='44' height='171' rx='12' fill='#60A5FA'/>
          <path d='M70 172C122 156 154 133 194 108C232 84 266 68 335 54' stroke='url(#g2)' stroke-width='10' stroke-linecap='round'/><path d='M310 43L344 52L318 77' stroke='#EAF2FF' stroke-width='8' stroke-linecap='round' stroke-linejoin='round'/>
          <circle cx='83' cy='76' r='32' fill='#60A5FA' opacity='.14'/><circle cx='338' cy='211' r='48' fill='#2563EB' opacity='.10'/><path d='M56 254H346' stroke='#94A3B8' stroke-opacity='.25' stroke-width='2'/>
        </svg>""",
        "painel": """
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
        "desempenho": """
        <svg viewBox='0 0 420 300' fill='none' xmlns='http://www.w3.org/2000/svg'>
          <circle cx='210' cy='150' r='94' fill='rgba(37,99,235,.12)' stroke='rgba(147,197,253,.26)' stroke-width='3'/><path d='M210 72V150L266 106' stroke='#60A5FA' stroke-width='10' stroke-linecap='round' stroke-linejoin='round'/><path d='M128 150A82 82 0 0 1 293 150' stroke='#2563EB' stroke-width='16' stroke-linecap='round'/><path d='M152 209C183 238 236 238 268 209' traço='#EAF2FF' largura-do-traço='10' limite-da-linha-do-traço='arredondado'/>
          <rect x='54' y='196' width='70' height='38' rx='15' fill='rgba(255,255,255,.08)' stroke='rgba(147,197,253,.25)'/><rect x='296' y='196' width='70' height='38' rx='15' fill='rgba(37,99,235,.26)' stroke='rgba(147,197,253,.25)'/><circle cx='76' cy='214' r='8' fill='#60A5FA'/><circle cx='318' cy='214' r='8' fill='#EAF2FF'/>
          <path d='M83 84C121 55 154 45 199 44' stroke='#60A5FA' stroke-opacity='.28' stroke-width='3' stroke-dasharray='8 10'/><path d='M220 45C264 50 298 67 331 100' stroke='#60A5FA' stroke-opacity='.28' stroke-width='3' stroke-dasharray='8 10'/>
        </svg>"""
    }
    retornar f"<div class='vmb-illustration'>{illustrations.get(kind, illustrations['rocket'])}</div>"


def premium_page_header(title, subtitle, kind="dashboard", eyebrow="VMB INVEST | SISTEMA DE DESEMPENHO"):
    retornar f"""
    <div class='vmb-hero'>
        <div class='vmb-hero-grid'>
            <div>
                <div class='vmb-eyebrow'>{eyebrow div>
                <div class='vmb-title'>{title div>
                <p class='vmb-subtitle'>{subtitle clep>
            </div>
            {premium_illustration(kind)}
        </div>
    </div>
    """


def banner_seção_premium(título, subtítulo):
    retornar f"""
    <div class='vmb-section-banner'>
        <div>
            <h3>{title>
            <p>{subtitle>
        </div>
        <div style='font-weight:900;color:#BFDBFE;'>PREMIUM</div>
    </div>
    """


def premium_metric_card(label, value, hint=""):
    retornar f"""
    <div class='vmb-metric-card'>
        <div class='vmb-metric-label'>{label div>
        <div class='vmb-metric-value'>{value div>
        <div class='vmb-metric-hint'>{hint div>
    </div>
    """

inject_custom_css()

# braços por simulado
DIC_SIMULADOS = {
    "Simulado 1 (Semanas 1 e 2)":["Atividade do Assessor de Investimentos (AI)", "Lavagem de Dinheiro"],
    "Simulado 2 (Semanas 3 e 4)":["Mercado de Capitais", "Securitização de Recebíveis", "Derivativos"],
    "Simulado 3 (Semanas 5 e 6)":["Fundos de Investimentos", "Outros Fundos de Investimentos", "Clubes de Investimentos"],
    "Simulado 4 (Semanas 7 e 8)":["Mercado Financeiro", "Sistema Financeiro Nacional"],
    "Simulado 5 (Semanas 9 e 10)":["Instituições e Intermediadores Financeiros", "Economia"],
    "Simulado 6 (Semanas 11 e 12)":["Matemática Financeira", "Administração de Risco"]
}
SIMULADOS_ORDEM = lista(DIC_SIMULADOS.keys())

# --- ESTADO DA SESSÃO ---
se "logado" não estiver em st.session_state:
    st.session_state.update({
        "logado": Falso,
        "usuário": "",
        "página": "Entrar",
        "índice_simulado_atual": 0,
        "simulado_nome": "",
        "módulos_selecionados":[],
        "quiz_atual": Nenhum,
        "inicio_time": Nenhum,
        "fim_time": Nenhum,
        "respostas_usuario": {},
        "resultado_salvo": Falso,
        "xp_usuario": 0,
        "nivel_usuario": "Estagiário",
        "foto_perfil": Nenhum
    })

# --- FUNÇÕES CORE ---
def ginficacao_cotdin(df_user):
    """Cálculo XP e Nível baseado no histórico"""
    simulados_feitos = len(df_user)
    xp = simulados_feitos * 150 # 150 XP por simulado concluído
    
    se xp < 300: nível = "Estagiário SDR"
    elif xp < 750: nível = "SDR Júnior"
    elif xp < 1200: nível = "SDR Pleno"
    elif xp < 2000: nível = "SDR Sênior"
    senão: nível = "SDR Elite 🏆"
    
    retorno xp, nível

def selecionar_questoes_balanceadas(banco, módulos, total_desejado=20):
    questoes_por_modulo = {mod:[] para mod em módulos}
    para q em banco:
        se q["módulo"] em módulos:
            questoes_por_modulo[q["módulo"]].append(q)
            
    total_disponivel = soma(len(qs) para qs em questoes_por_modulo.values())
    if total_disponivel <= total_desejado:
        todas = [q para qs em questoes_por_modulo.values() para q em qs]
        embaralhar aleatório(todos)
        retornar todas
        
    sep =[]
    modulos_restantes =[mod para mod em módulos if len(questoes_por_modulo[mod]) > 0]
    filho = total_desejado
    
    enquanto vagas > 0 e módulos_restantes:
        cota = vagas // len(módulos_restantes)
        resto = vagas % len(módulos_restantes)
        novos_módulos_restantes =[]
        
        para i, mod em enumerar(modulos_restantes):
            cota_atual = cota + (1 se eu < resto else 0)
            disponível = len(questoes_por_modulo[mod])
            
            se disponivel <= cota_atual:
                selecionados.extend(questoes_por_modulo[mod])
                jovem -= disponivel
                questoes_por_modulo[mod] =[]
            outro:
                novos_modulos_restantes.append(mod)
                
        if len(novos_módulos_restantes) == len(módulos_restantes):
            para i, mod em enumerar(novos_modulos_restantes):
                cota_atual = cota + (1 se eu < resto else 0)
                escolhidas = random.sample(questoes_por_modulo[mod], cota_atual)
                selecionados.extend(escolhidas)
                jovem -= cota_atual
            quebrar
            
        módulos_restantes = novos_módulos_restantes
        
    random.shuffle(selecionadas)
    retornars

# --- INTERFACE ---
se não st.session_state.logado:
    # --- TELA DE LOGIN PREMIUM ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([0.8, 2.4, 0.8])
    
    com col2:
        st.markdown(premium_page_header(
            "VMB INVEST",
            "Treinamento de alta performance para avaliadores que desejam evoluir com método, dados e mentalidade de elite.",
            "logotipo",
            "SIMULADO DE ELITE"
        ), unsafe_allow_html=True)
        
        com st.container(border=True):
            user = st.text_input("Usuário", placeholder="ID do Agente")
            pw = st.text_input("Senha", type="password", placeholder="••••••••")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("ACESSAR PLATAFORMA ⚡", use_container_width=True, type="primary"):
                with st.spinner("Autenticando e sincronizando progresso..."):
                    tentar:
                        conexão = st.connection("gsheets", type=GSheetsConnection)
                        df_usuarios = conn.read(worksheet="Usuarios", ttl=0)
                        correspondência_do_usuário = df_usuários[
                            (df_usuarios['Usuario'].astype(str).str.lower() == user.lower()) &
                            (df_usuarios['Senha'].astype(str) == pw)
                        ]
                        
                        se não user_match.empty ou (user.lower() == "admin" e pw == "admin"):
                            usuario_formatado = user.capitalize()
                            st.session_state.logado = True
                            st.session_state.usuario = usuario_formatado
                            
                            # SINCRONIZAR PROGRESSO
                            tentar:
                                df_historico = conn.read(worksheet="Historico", ttl=0)
                                df_user_hist = df_historico[df_historico['Usuario'] == usuario_formatado]
                                
                                #Gamência
                                xp, nível = calcular_gamificacao(df_user_hist)
                                st.session_state.xp_usuario = xp
                                st.session_state.nivel_usuario = nível

                                max_passed = -1
                                se df_user_hist não estiver vazio:
                                    para _, linha em df_user_hist.iterrows():
                                        nota = pd.to_numeric(str(row['Nota (%)']).replace(',', '.'), errors='coerce')
                                        se pd.notna(nota) e nota >= 70.0:
                                            sim_name = linha['Simulado']
                                            se nome_sim em SIMULADOS_ORDEM:
                                                idx = SIMULADOS_ORDEM.index(nome_sim)
                                                Se idx > max_passed: max_passed = idx
                                
                                índice_prox = min(max_passado + 1, len(SIMULADOS_ORDEM) - 1)
                                st.session_state.simulado_atual_indice = prox_indice
                            exceto Exceção:
                                st.session_state.simulado_atual_indice = 0

                            st.session_state.page = "Home"
                            st.rerun()
                        outro:
                            st.error("Acesso negado. Credenciais inválidos.")
                    exceto Exception como e:
                        st.error("Falha de conexão com os servidores.")

outro:
    # --- BARRA LATERAL GAMIFICADA ---
    com st.sidebar:
        importar base64
        foto_html = "👤"
        se "foto_perfil" em st.session_state e st.session_state.foto_perfil:
            tentar:
                foto_base64 = base64.b64encode(st.session_state.foto_perfil).decode()
                foto_html = f'<img src="data:image/png;base64,{foto_base64}" style="width:45px; height:45px; border-radius:50%; object-fit:cover; border:2px solid #3B82F6;">'
            exceto: passar

        barra_lateral_html = """
        <div style="background: rgba(37, 99, 235, 0.08); padding: 20px; border-radius: 20px; border: 1px solid rgba(37, 99, 235, 0.15); margin-bottom: 20px; display: flex; align-items: center; gap: 15px;">
            <div style="flex-shrink: 0;">{0}</div>
            <div style="overflow: hidden;">
                <div style="font-size: 12px; color: #8B949E; text-transform: uppercase; letter-spacing: 0.05em;">Agente</div>
                <div style="font-size: 18px; font-weight: 800; color: white; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{1}</div>
                <div style="font-size: 12px; font-weight: 700; color: #3B82F6; margin-top: 2px;">{2}</div>
            </div>
        </div>
        <div style="padding: 0 10px 20px;">
            <div style="background: rgba(255,255,255,0.05); border-radius: 10px; height: 6px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #3B82F6, #60A5FA); width: {3}%; height: 100%;"></div>
            </div>
            <div style="font-size: 10px; color: #8B949E; margin-top: 6px; text-align: right; font-weight: 600;">{4} XP</div>
        </div>
        """.formatar(
            foto_html,
            st.session_state.usuario,
            st.session_state.nivel_usuario,
            (st.session_state.xp_usuario % 1000) / 10,
            st.session_state.xp_usuario
        )
        st.markdown(sidebar_html, unsafe_allow_html=True)
        
        menu = st.radio("Módulos da Plataforma", ["Dashboard Principal", "Evolução e IA", "Meu Perfil"])
        
        # Botão de SAIR no final da barra lateral
        st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
        st.divider()
        if st.button("🚪 Sair do Sistema", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    # Redirecionamento lógico do menu
    if menu == "Evolução e IA" e st.session_state.page != "Evolução":
        st.session_state.page = "Evolução"
        st.rerun()
    menu elif == "Meu Perfil" e st.session_state.page != "Perfil":
        st.session_state.page = "Perfil"
        st.rerun()
    elif menu == "Dashboard Principal" e st.session_state.page não está em["Home", "Instrucoes", "Simulado", "Resultado"]:
        st.session_state.page = "Home"
        st.rerun()

    # --- INÍCIO / PAINEL DE CONTROLE ---
    se st.session_state.page == "Home":
        st.markdown(premium_page_header(
            "Central de Treinamento",
            "Escolha sua próxima missão, acompanhe seu progresso e avance por uma jornada de evolução orientada por performance.",
            "painel",
            "PRINCIPAL DO PAINEL DE CONTROLE"
        ), unsafe_allow_html=True)
        
        # BURACO PARA AS MÉTRICAS INICIAIS
        tentar:
            conexão = st.connection("gsheets", type=GSheetsConnection)
            df_historico = conn.read(worksheet="Historico", ttl=0)
            df_user_hist = df_historico[df_historico['Usuario'] == st.session_state.usuario]
            
            avg_score = df_user_hist['Nota (%)'].mean() if not df_user_hist.empty else 0
            max_score = df_user_hist['Nota (%)'].max() se não df_user_hist.empty senão 0
            qtd_sim = len(df_user_hist)
            
            metrics_html = """
            <div class='vmb-metrics-grid'>
                {0}
                {1}
                {2}
            </div>
            """.formatar(
                premium_metric_card("Aproveitamento Geral", "{0:.1f}%".format(avg_score), "média acumulada"),
                premium_metric_card("Melhor Nota", "{0:.1f}%".format(max_score), "registro pessoal"),
                premium_metric_card("Simulados Concluídos", str(qtd_sim), "missões finalizadas")
            )
            st.markdown(metrics_html, unsafe_allow_html=True)
        exceto:
            passar

        st.markdown(premium_section_banner("Selecione sua missão", "Cada simulado desbloqueia uma nova etapa da trilha de evolução comercial e técnica."), unsafe_allow_html=True)
        para i, nome_sim em enumerar(SIMULADOS_ORDEM):
            com st.container(border=True):
                col_txt, col_btn = st.columns([4, 1])
                com col_txt:
                    st.markdown(f"<h4 style='margin:0; padding:0;'>{nome_sim}</h4>", unsafe_allow_html=True)
                    st.caption(f"{', '.join(DIC_SIMULADOS[nome_sim])}")
                
                com col_btn:
                    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
                    liberado = i <= st.session_state.simulado_atual_indice
                    se liberado:
                        if st.button("Iniciar", key=f"btn_{i}", use_container_width=True, type="primary"):
                            st.session_state.simulado_nome = nome_sim
                            st.session_state.modulos_selecionados = DIC_SIMULADOS[nome_sim]
                            st.session_state.page = "Instruções"
                            st.rerun()
                    outro:
                        st.button("Bloqueado", key=f"btn_{i}", disabled=True, use_container_width=True)

    # --- TELA DE INSTRUÇÕES ---
    elif st.session_state.page == "Instruções":
        st.markdown(premium_page_header(
            f"Operação: {st.session_state.simulado_nome}",
            "Leia o protocolo, entre em modo foco e execute a missão com resultados de prova oficial.",
            "desempenho",
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
        "", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        com col1:
            if st.button("Cancelar Missão", use_container_width=True):
                st.session_state.page = "Home"
                st.rerun()
        com col2:
            if st.button("ACEITO OS TERMOS - INICIAR ⚡", type="primary", use_container_width=True):
                quiz = selecionar_questoes_balanceadas(BANCO_QUESTOES, st.session_state.modulos_selecionados, 20)
                se len(quiz) > 0:
                    st.session_state.quiz_atual = quiz
                    st.session_state.inicio_time = time.time()
                    st.session_state.resultado_salvo = Falso
                    st.session_state.page = "Simulado"
                    st.rerun()
                outro:
                    st.error("Banco de dados insuficiente.")

    # --- EXECUÇÃO DO SIMULADO (TIMER PREMIUM) ---
    elif st.session_state.page == "Simulado" e st.session_state.quiz_atual:
        timer_container = st.empty()
        com timer_container:
            js_timer = """
            <script>
            var countDownDate = new Date().getTime() + (30 * 60 * 1000);
            var x = setInterval(function() {
              var now = new Date().getTime();
              var distância = dataRegressiva - agora;
              
              var minutos = Math.floor((distância % (1000 * 60 * 60)) / (1000 * 60));
              var segundos = Math.floor((distância % (1000 * 60)) / 1000);
              minutos = minutos < 10 ? "0" + minutos : minutos;
              segundos = segundos < 10 ? "0" + segundos : segundos;
              
              var timerDiv = document.getElementById("timer");
              var glowDiv = document.getElementById("timer-glow");
              
              timerDiv.innerHTML = "⏳ " + minutos + ":" + segundos;
              
              se (minutos < 5) {
                  timerDiv.style.color = "#FF4B4B";
                  glowDiv.style.boxShadow = "0 0 20px rgba(255, 75, 75, 0.6)";
                  glowDiv.style.border = "1px solid #FF4B4B";
              }
              
              se (distância < 0) {
                clearInterval(x);
                timerDiv.innerHTML = "🚨 TEMPO ESGOTADO";
              }
            }, 1000);
            </script>
            <div id="timer-glow" style="position: sticky; top: 10px; z-index: 999; background: rgba(14, 17, 23, 0.8); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); padding: 10px 30px; border-radius: 50px; width: fit-content; margin: 0 auto; box-shadow: 0 4px 15px rgba(0,0,0,0.5); transition: all 0.3s ease;">
                <h2 id="timer" style="color: #60A5FA; margin: 0; font-family: monospace; font-size: 26px;">Carregando...</h2>
            </div>
            """
            components.html(js_timer, altura=80)
        
        st.write("")
        com st.form("form_simulado"):
            respostas_locais = {}
            para idx, q em enumerate(st.session_state.quiz_atual):
                st.markdown(f"#### Questão {idx+1}")
                st.markdown(f"<span style='color: #8B949E; font-size: 12px;'>MÓDULO: {q['modulo'].upper()}</span>", unsafe_allow_html=True)
                st.write(q['pergunta'])
                opcoes =[f"{k}) {v}" para k, v em q.get("opcoes", {}).items()]
                
                chave_unica = f"rad_{st.session_state.simulado_atual_indice}_{q['id']}_{idx}"
                respostas_locais[idx] = st.radio("Seleção:", opcoes, key=chave_unica, index=None, label_visibility="collapsed")
                st.markdown("<hr style='opacity: 0.2;'>", unsafe_allow_html=True)
            
            submitted = st.form_submit_button("ENVIAR RESPOSTAS", use_container_width=True, type="primary")
            se submetido:
                st.session_state.fim_time = time.time()
                st.session_state.respostas_usuario = respostas_locais
                st.session_state.page = "Resultado"
                tempo.dormir(0.2)
                st.rerun()

    # --- RESULTADOS ---
    elif st.session_state.page == "Resultado":
        st.markdown(premium_page_header(
            "Relatório de pie",
            "Veja sua nota, seu ritmo, seus acertos e os pontos que precisam de reforço para a próxima tentativa.",
            "crescimento",
            "ANÁLISE DE PERFORMANCE"
        ), unsafe_allow_html=True)
        
        tempo_total_segundos = st.session_state.fim_time - st.session_state.inicio_time
        minutos = int(tempo_total_segundos // 60)
        segundos = int(tempo_total_segundos % 60)
        
        acertos = 0
        total_questoes = len(st.session_state.quiz_atual)
        tempo_medio = tempo_total_segundos / total_questoes if total_questoes > 0 else 0
        
        desempenho_módulos = {}
        para idx, q em enumerate(st.session_state.quiz_atual):
            mod = q['módulo']
            se o mod não estiver em desempenho_modulos:
                desempenho_módulos[mod] = {"total": 0, "acertos": 0}
            
            desempenho_módulos[mod]["total"] += 1
            resp = st.session_state.respostas_usuario.get(idx)
            if resp e resp.startswith(q['resposta_correta']):
                acertos += 1
                desempenho_módulos[mod]["acertos"] += 1

        percentual = (acertos / total_questoes) * 100 if total_questoes > 0 else 0

        # SALVAMENTO
        se não st.session_state.resultado_salvo:
            with st.spinner("Salvando telemetria..."):
                tentar:
                    conexão = st.connection("gsheets", type=GSheetsConnection)
                    df_historico = conn.read(worksheet="Historico", ttl=0)
                    detalhes_mod = {mod: round((dados['acertos'] / dados['total']) * 100, 1) for mod, dados em desempenho_modulos.items()}
                    
                    novo_registro = pd.DataFrame([{
                        "Dados": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "Usuario": st.session_state.usuario,
                        "Simulado": st.session_state.simulado_nome,
                        "Nota (%)": redondo(percentual, 1),
                        "Tempo": f"{minutos}m {segundos}s",
                        "Detalhes_Módulos": json.dumps(detalhes_mod)
                    }])
                    
                    df_atualizado = pd.concat([df_historico, novo_registro], ignore_index=True)
                    conn.update(worksheet="Histórico", data=df_atualizado)
                    st.session_state.resultado_salvo = True
                exceto Exception como e:
                    passar

        col1, col2, col3 = st.columns(3)
        col1.metric("Nota Final", f"{percentual:.1f}%", f"{acertos}/{total_questoes}")
        col2.metric("Ritmo (Tempo Médio)", f"{int(tempo_medio // 60)}m {int(tempo_medio % 60)}s")
        col3.metric("Status", "APROVADO" if percentual >= 70 else "REPROVADO")

        st.divider()
        st.markdown("### Correção Analítica")
        para idx, q em enumerate(st.session_state.quiz_atual):
            resp_usuario = st.session_state.respostas_usuario.get(idx)
            acertou = resp_usuario e resp_usuario.startswith(q['resposta_correta'])
            letra_correta = q['resposta_correta']
            texto_correto = q['opcoes'].get(letra_correta, "")

            status_color = "#10B981" if acertou else "#EF4444"
            status_text = "Acertou" if acertou else "Errou"
            
            com st.expander(f"Q{idx+1} - {status_text} | {q['modulo']}"):
                st.write(f"**{q['pergunta']}**")
                st.markdown(f"<span style='color:{status_color}; font-weight:bold;'>Sua marcação:</span> {resp_usuario if resp_usuario else 'Em branco'}", unsafe_allow_html=True)
                se não acertou:
                    st.markdown(f"<span style='color:#10B981; font-weight:bold;'>Correta:</span> {letra_correta}) {texto_correto}", unsafe_allow_html=True)
                st.info(f"💡 **Insights:** {q.get('explicacao', '')}")

        st.write("")
        if st.button("Finalizar Análise e Voltar", type="primary", use_container_width=True):
            se percentual >= 70 e st.session_state.simulado_nome == SIMULADOS_ORDEM[st.session_state.simulado_atual_indice]:
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
            tentar:
                conexão = st.connection("gsheets", type=GSheetsConnection)
                df_historico_geral = conn.read(worksheet="Historico", ttl=0)
                df_user = df_historico_geral[df_historico_geral["Usuario"] == st.session_state.usuario].copy()
                
                se df_user não estiver vazio:
                    df_user.reset_index(drop=True, inplace=True)
                    
                    # Cálculo de Tempo
                    total_segundos = 0
                    tempos_válidos = 0
                    para t_str em df_user['Tempo']:
                        correspondência = re.search(r'(\d+)m\s*(\d+)s', str(t_str))
                        se houver correspondência:
                            total_secs += int(match.group(1)) * 60 + int(match.group(2))
                            tempos_válidos += 1
                    
                    media_secs = total_secs // tempos_válidos se tempos_válidos > 0 senão 0
                    
                    # Processamento JSON
                    module_scores = {}
                    para _, linha em df_user.iterrows():
                        se 'Detalhes_Modulos' em df_user.columns e pd.notna(row['Detalhes_Modulos']):
                            tentar:
                                detalhes = json.loads(row['Detalhes_Módulos'])
                                para mod, pontuação em detalhes.items():
                                    se mod não estiver em module_scores: module_scores[mod] =[]
                                    module_scores[mod].append(score)
                                continuar
                            exceto: passar
                        
                        sim_name = linha['Simulado']
                        se sim_name em DIC_SIMULADOS:
                            para mod em DIC_SIMULADOS[sim_name]:
                                se mod não estiver em module_scores: module_scores[mod] = []
                                module_scores[mod].append(row['Nota (%)'])
                                
                    avg_module_scores = {mod: sum(scores)/len(scores) for mod, scores in module_scores.items()}

                    col_radar, col_ia = st.columns([1.2, 1])

                    com col_radar:
                        st.markdown("<h3 style='text-align:center;'>Radar de Competências</h3>", unsafe_allow_html=True)
                        se avg_module_scores:
                            df_radar = pd.DataFrame(dict(
                                Força=list(avg_module_scores.values()),
                                Módulo=lista(média_de_pontuações_do_módulo.chaves())
                            ))
                            df_radar = pd.concat([df_radar, df_radar.iloc[[0]]])
                            
                            fig = go.Figure()
                            
                            # O Seu radar
                            fig.add_trace(go.Scatterpolar(
                                r=df_radar['Força'],
                                theta=df_radar['Módulo'],
                                preencher='para si mesmo',
                                nome='Sua',
                                cor_da_linha='#3B82F6',
                                cor de preenchimento='rgba(59, 130, 246, 0.4)'
                            ))
                            
                            # Radar Elite (Top 10% Ficção de meta)
                            fig.add_trace(go.Scatterpolar(
                                r=[85]*len(df_radar),
                                theta=df_radar['Módulo'],
                                preencher='nenhum',
                                nome='Top 10% Elite',
                                cor_da_linha='rgba(16, 185, 129, 0.5)',
                                traço_linha='traço'
                            ))

                            fig.atualizar_layout(
                                polar=dict(
                                    bgcolor='rgba(0,0,0,0)',
                                    radialaxis=dict(visible=True, range=[0, 100], gridcolor='#30363D', color='#8B949E'),
                                    eixo angular=dict(gridcolor='#30363D', color='#FAFAFA')
                                ),
                                mostrarlegenda=Verdadeiro,
                                legenda=dict(orientação="h", âncora="inferior", y=-0.2, âncora="centro", x=0.5),
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                margem=dict(l=40, r=40, t=20, b=20)
                            )
                            st.plotly_chart(fig, use_container_width=True)

                    com col_ia:
                        st.markdown("### 🧠 Diagnóstico do Mentor")
                        
                        sorted_mods = sorted(avg_module_scores.items(), key=lambda item: item[1])
                        weak_mods = [mod para mod, pontuação em sorted_mods se pontuação < 70]
                        strong_mods = [mod para mod, pontuação em sorted_mods se pontuação >= 85]
                        
                        st.markdown("""
                        <div style="background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                            <p style="color:#8B949E; font-size:14px; margin-bottom:5px;">ANÁLISE HEURÍSTICA CONCLUÍDA</p>
                        "", unsafe_allow_html=True)
                        
                        se weak_mods:
                            st.markdown(f"**🚨 Atenção Crítica:**<br>Detectei falhas estruturais em **{weak_mods[0]}**. Redirecione 80% do seu próximo ciclo de estudos para a teoria base deste módulo.", unsafe_allow_html=True)
                        se strong_mods:
                            st.markdown(f"<br>**🏆 Dominância:**<br>O módulo de **{strong_mods[-1]}** atingiu padrão de excelência. Modo manutenção ativada.", unsafe_allow_html=True)

                        st.markdown("<br>**⏱️ Pacing de Prova:**", unsafe_allow_html=True)
                        se media_secs > 1500:
                            st.markdown("⚠️ *Velocidade de risco:* Você está usando quase todo o tempo limite. Na prova oficial, você não terá fôlego para revisar. Pratique leitura dinâmica.")
                        senão, se media_secs > 0 e media_secs < 600:
                            st.markdown("⚡ *Impulsividade:* Seu tempo de resposta é muito rápido. Isso levanta suspeitas de desatenção a palavras como 'EXCETO' ou dupla negação.")
                        elif media_secs > 0:
                            st.markdown("✅ *Ritmo Cadenciado:* Seu controle de tempo está perfeitamente alinhado com os candidatos aprovados.")
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.divider()
                    st.subheader("Data Grid (Registros Brutos)")
                    
                    df_display = df_user[['Dados', 'Simulado', 'Nota (%)', 'Tempo']].copy()
                    
                    st.dataframe(
                        df_display,
                        configuração_coluna={
                            "Nota (%)": st.column_config.ProgressColumn(
                                "Desempenho",
                                ajuda="Sua nota percentual",
                                formato="%f%%",
                                valor_mínimo=0,
                                valor_máximo=100,
                            ),
                            "Dados": st.column_config.TextColumn("Dados da Execução"),
                            "Simulado": st.column_config.TextColumn("Missão")
                        },
                        ocultar_índice=Verdadeiro,
                        use_container_width=True
                    )

                outro:
                    st.info("Aguardando telemetria inicial. Faça seu primeiro simulado.")
            exceto Exception como e:
                st.error("Falha ao processar banco de dados da IA.")

    # --- TELA DE PERFIL ---
    elif st.session_state.page == "Perfil":
        st.markdown(premium_page_header(
            "Meu Perfil",
            "Gerencie suas informações, personalize seu avatar e acompanhe suas conquistas na plataforma.",
            "desempenho",
            "CONFIGURAÇÕES DE AGENTE"
        ), unsafe_allow_html=True)

        col_foto, col_info = st.columns([1, 2])
        
        com col_foto:
            com st.container(border=True):
                st.markdown("### Foto do Perfil")
                se st.session_state.foto_perfil:
                    st.image(st.session_state.foto_perfil, use_container_width=True)
                outro:
                    st.info("Nenhuma foto compartilhada.")
                
                arquivo_enviado = st.file_uploader("Alterar foto", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
                Se o arquivo enviado não for None:
                    st.session_state.foto_perfil = uploaded_file.getvalue()
                    st.success("Foto atualizada com sucesso!")
                    tempo.dormir(1)
                    st.rerun()

        com col_info:
            com st.container(border=True):
                st.markdown("### Informações da Conta")
                st.write(f"**Usuário:** {st.session_state.usuario}")
                st.write(f"**Nível Atual:** {st.session_state.nivel_usuario}")
                st.write(f"**Total de XP:** {st.session_state.xp_usuario}")
                st.divider()
                st.markdown("#### Conquistas")
                se st.session_state.xp_usuario >= 2000:
                    st.markdown("🏆 **Agente Elite:** Você atingiu o topo da performance.")
                elif st.session_state.xp_usuario >= 1200:
                    st.markdown("🥇 **Agente Sênior:** Experiência comprovada em simulados.")
                outro:
                    st.markdown("🎯 **Em Evolução:** Continue completando missões para desbloquear insígnias.")
