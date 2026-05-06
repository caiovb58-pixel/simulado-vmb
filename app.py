import streamlit as st
import random
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Simulado ANCORD · VMB Invest",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# ESTILO VISUAL  (VMB — dark, profissional)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Fundo geral */
.stApp {
    background: #0a0e1a;
    color: #e8e9ef;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f1526 !important;
    border-right: 1px solid #1e2640;
}
[data-testid="stSidebar"] * {
    color: #c8cbd8 !important;
}

/* Títulos com fonte display */
h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    letter-spacing: -0.02em;
}

/* Cards */
.vmb-card {
    background: #131929;
    border: 1px solid #1e2a45;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

/* Questão card */
.questao-card {
    background: #131929;
    border: 1px solid #1e2a45;
    border-left: 4px solid #3d6ef5;
    border-radius: 0 12px 12px 0;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.8rem;
}
.questao-card.correta {
    border-left-color: #22c55e;
    background: #0d1f14;
}
.questao-card.errada {
    border-left-color: #ef4444;
    background: #1f0d0d;
}

/* Badges */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.badge-blue  { background: #1a2f6e; color: #7cabff; }
.badge-green { background: #0d2e1a; color: #4ade80; }
.badge-red   { background: #2e0d0d; color: #f87171; }
.badge-amber { background: #2e1f0d; color: #fbbf24; }

/* Timer */
.timer-box {
    background: #131929;
    border: 1px solid #1e2a45;
    border-radius: 12px;
    padding: 0.6rem 1.2rem;
    text-align: center;
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: #7cabff;
}
.timer-box.urgente { color: #f87171; border-color: #4a1a1a; }

/* Barra de progresso customizada */
.prog-bar-outer {
    background: #1e2640;
    border-radius: 8px;
    height: 8px;
    width: 100%;
    margin: 6px 0 12px;
}
.prog-bar-inner {
    background: linear-gradient(90deg, #3d6ef5, #7cabff);
    height: 8px;
    border-radius: 8px;
    transition: width 0.4s ease;
}

/* Botão primário */
.stButton > button {
    background: #3d6ef5 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.18s ease !important;
}
.stButton > button:hover {
    background: #5585ff !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 18px rgba(61,110,245,0.35) !important;
}

/* Radio options */
.stRadio > div { gap: 6px; }
.stRadio label {
    background: #1a2035 !important;
    border: 1px solid #1e2a45 !important;
    border-radius: 10px !important;
    padding: 0.5rem 0.9rem !important;
    transition: border-color 0.15s;
    cursor: pointer;
}
.stRadio label:hover { border-color: #3d6ef5 !important; }

/* Metric cards */
.metric-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
}
.metric-card {
    flex: 1;
    background: #131929;
    border: 1px solid #1e2640;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.metric-val {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #7cabff;
    line-height: 1;
}
.metric-lbl {
    font-size: 0.75rem;
    color: #6b7294;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 4px;
}

/* Forms */
.stTextInput input, .stSelectbox select {
    background: #131929 !important;
    border: 1px solid #1e2a45 !important;
    border-radius: 10px !important;
    color: #e8e9ef !important;
}
input[type="password"] {
    background: #131929 !important;
    color: #e8e9ef !important;
}

/* Divisor */
hr { border-color: #1e2640 !important; }

/* Oculta itens do menu padrão */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────
ADMINS = ["Caio", "Admin"]
TEMPO_PROVA_MIN = 30
QUESTOES_POR_PROVA = 20
NOTA_APROVACAO = 70

from questoes import BANCO_QUESTOES

DIC_SIMULADOS = {
    "Simulado 1 (Semanas 1 e 2)":   ["Atividade do AAI", "Lavagem de Dinheiro"],
    "Simulado 2 (Semanas 3 e 4)":   ["Mercado de Capitais", "Securitização e Recebíveis", "Derivativos"],
    "Simulado 3 (Semanas 5 e 6)":   ["Fundos de Investimentos", "Outros Fundos", "Clube de Investimentos"],
    "Simulado 4 (Semanas 7 e 8)":   ["Mercado Financeiro", "Sistema Financeiro Nacional"],
    "Simulado 5 (Semanas 9 e 10)":  ["Instituições Financeiras", "Economia"],
    "Simulado 6 (Semanas 11 e 12)": ["Matemática Financeira", "Administração de Risco", "Clube de Investimentos"],
}
SIMULADOS_ORDEM = list(DIC_SIMULADOS.keys())


# ─────────────────────────────────────────────
# SESSION STATE — inicialização segura
# ─────────────────────────────────────────────
_defaults = {
    "logado": False,
    "usuario": "",
    "simulado_atual_indice": 0,
    # Prova em andamento
    "prova_ativa": False,
    "prova_simulado_indice": None,
    "questoes": [],
    "respostas": {},          # {idx: letra}
    "tempo_fim": None,
    "inicio_prova": None,
    # Resultado da última prova
    "resultado": None,        # dict com dados do resultado
    # Modo revisão
    "modo_revisao": False,
    "revisao_questoes": [],
    # Tela inicial de boas-vindas (por sessão)
    "mostrou_welcome": False,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────
# CONEXÃO GOOGLE SHEETS
# ─────────────────────────────────────────────
@st.cache_resource
def get_conn():
    return st.connection("gsheets", type=GSheetsConnection)

conn = get_conn()


# ─────────────────────────────────────────────
# HELPERS — SHEETS
# ─────────────────────────────────────────────
def _ler(worksheet: str) -> pd.DataFrame:
    """Lê worksheet com cache curto."""
    return conn.read(worksheet=worksheet, ttl=30)

def _salvar(worksheet: str, df: pd.DataFrame):
    conn.update(worksheet=worksheet, data=df)


def carregar_progresso(usuario: str) -> int:
    try:
        df = _ler("Progresso")
        row = df[df["Usuario"] == usuario]
        return int(row.iloc[0]["Simulado_Atual"]) if not row.empty else 0
    except Exception:
        return 0


def salvar_progresso(usuario: str, indice: int, status: str):
    try:
        df = _ler("Progresso")
        if "Usuario" not in df.columns:
            df = pd.DataFrame(columns=["Usuario", "Simulado_Atual", "Ultimo_Status"])
        if usuario in df["Usuario"].values:
            df.loc[df["Usuario"] == usuario, "Simulado_Atual"] = indice
            df.loc[df["Usuario"] == usuario, "Ultimo_Status"] = status
        else:
            novo = pd.DataFrame([{"Usuario": usuario, "Simulado_Atual": indice, "Ultimo_Status": status}])
            df = pd.concat([df, novo], ignore_index=True)
        _salvar("Progresso", df)
    except Exception as e:
        st.toast(f"⚠️ Progresso não salvo: {e}", icon="⚠️")


def salvar_resultado(usuario: str, simulado: str, nota: float, tempo_medio: float, respostas_por_modulo: dict):
    try:
        df = _ler("Resultados")
        for col in ["Tempo_medio", "Data", "Detalhes_Modulo"]:
            if col not in df.columns:
                df[col] = None

        detalhes = "; ".join(
            f"{m}: {v[0]}/{v[1]}"
            for m, v in respostas_por_modulo.items()
        )
        novo = pd.DataFrame([{
            "Usuario":         usuario,
            "Simulado":        simulado,
            "Nota":            round(nota, 1),
            "Tempo_medio":     round(tempo_medio, 1),
            "Data":            datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Detalhes_Modulo": detalhes,
        }])
        _salvar("Resultados", pd.concat([df, novo], ignore_index=True))
    except Exception as e:
        st.toast(f"⚠️ Resultado não salvo: {e}", icon="⚠️")


def login(usuario: str, senha: str) -> bool:
    try:
        df = _ler("Usuarios")
        return not df[(df["Nome"] == usuario) & (df["Senha"] == senha)].empty
    except Exception:
        return False


# ─────────────────────────────────────────────
# HELPERS — TIMER (sem sleep/rerun no meio da UI)
# ─────────────────────────────────────────────
def segundos_restantes() -> int:
    if st.session_state.tempo_fim is None:
        return 0
    delta = (st.session_state.tempo_fim - datetime.now()).total_seconds()
    return max(0, int(delta))


def formatar_tempo(seg: int) -> str:
    m, s = divmod(seg, 60)
    return f"{m:02d}:{s:02d}"


# ─────────────────────────────────────────────
# HELPERS — UI
# ─────────────────────────────────────────────
def barra_progresso(valor: float, label: str = ""):
    pct = min(100, max(0, valor * 100))
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;font-size:0.78rem;color:#6b7294;margin-bottom:2px">
        <span>{label}</span><span>{pct:.0f}%</span>
    </div>
    <div class="prog-bar-outer">
        <div class="prog-bar-inner" style="width:{pct}%"></div>
    </div>
    """, unsafe_allow_html=True)


def metric_cards(dados: list):
    """dados = [(valor, label), ...]"""
    cols_html = "".join(
        f'<div class="metric-card"><div class="metric-val">{v}</div><div class="metric-lbl">{l}</div></div>'
        for v, l in dados
    )
    st.markdown(f'<div class="metric-row">{cols_html}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TELA DE LOGIN
# ─────────────────────────────────────────────
def tela_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align:center;margin:3rem 0 2rem">
            <div style="font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;
                        background:linear-gradient(90deg,#7cabff,#3d6ef5);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent">
                VMB Invest
            </div>
            <div style="font-family:'Syne',sans-serif;font-size:1rem;color:#6b7294;
                        letter-spacing:0.15em;text-transform:uppercase;margin-top:4px">
                Simulado ANCORD
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            usuario = st.text_input("Usuário", placeholder="Seu nome de acesso")
            senha   = st.text_input("Senha", type="password", placeholder="••••••")
            entrar  = st.form_submit_button("🔑 Entrar", use_container_width=True)

        if entrar:
            if login(usuario, senha):
                st.session_state.logado                = True
                st.session_state.usuario               = usuario
                st.session_state.simulado_atual_indice = carregar_progresso(usuario)
                st.session_state.mostrou_welcome       = False
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")


# ─────────────────────────────────────────────
# TELA DE BOAS-VINDAS (uma vez por sessão)
# ─────────────────────────────────────────────
def tela_boas_vindas():
    progresso = st.session_state.simulado_atual_indice
    total     = len(SIMULADOS_ORDEM)

    st.markdown(f"""
    <div style="margin:2rem 0 1rem">
        <span style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:700">
            Olá, {st.session_state.usuario}! 👋
        </span><br>
        <span style="color:#6b7294">Pronto para mais uma rodada de estudos?</span>
    </div>
    """, unsafe_allow_html=True)

    # Cards de status rápido
    metric_cards([
        (f"{progresso}/{total}", "Simulados concluídos"),
        (f"{int(progresso/total*100)}%", "Progresso geral"),
        (f"{total - progresso}", "Restantes"),
    ])

    st.markdown("---")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class="vmb-card">
            <div style="font-family:'Syne',sans-serif;font-size:1.05rem;font-weight:700;margin-bottom:.6rem">📋 Regras</div>
            <ul style="color:#9ba3bf;font-size:0.88rem;line-height:1.8;padding-left:1rem">
                <li>20 questões por simulado</li>
                <li>30 minutos de duração</li>
                <li>Nota mínima de 70% para aprovação</li>
                <li>Não consulte material durante a prova</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="vmb-card">
            <div style="font-family:'Syne',sans-serif;font-size:1.05rem;font-weight:700;margin-bottom:.6rem">🏆 Dica</div>
            <p style="color:#9ba3bf;font-size:0.88rem;line-height:1.7">
                Foco total durante a prova. Após concluir, você poderá revisar cada questão
                com a explicação completa do gabarito. Use a aba <b>Evolução</b> para acompanhar
                seu desempenho ao longo do tempo.
            </p>
            <p style="color:#7cabff;font-size:0.82rem;font-style:italic">
                "Disciplina hoje, liberdade amanhã."
            </p>
        </div>
        """, unsafe_allow_html=True)

    if st.button("🔥 Ir para os Simulados", use_container_width=True):
        st.session_state.mostrou_welcome = True
        st.rerun()


# ─────────────────────────────────────────────
# TELA DE SIMULADOS (lista)
# ─────────────────────────────────────────────
def tela_simulados():
    progresso = st.session_state.simulado_atual_indice
    total     = len(SIMULADOS_ORDEM)

    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:700;margin-bottom:.4rem">
        📚 Seus Simulados
    </div>
    """, unsafe_allow_html=True)
    barra_progresso(progresso / total, f"Progresso: {progresso}/{total}")

    for i, nome in enumerate(SIMULADOS_ORDEM):
        modulos = ", ".join(DIC_SIMULADOS[nome])
        if i < progresso:
            # Concluído
            with st.expander(f"✅ {nome}", expanded=False):
                st.markdown(f"<span style='color:#4ade80;font-size:.85rem'>Concluído · Módulos: {modulos}</span>", unsafe_allow_html=True)
                if st.button("Refazer / Revisar", key=f"ref_{i}"):
                    _iniciar_prova(i)

        elif i == progresso:
            # Disponível
            st.markdown(f"""
            <div class="vmb-card" style="border-left:4px solid #3d6ef5;border-radius:0 12px 12px 0">
                <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700">{nome}</div>
                <div style="color:#6b7294;font-size:.82rem;margin:.25rem 0 .8rem">{modulos}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"▶ Iniciar {nome.split('(')[0].strip()}", key=f"ini_{i}", use_container_width=True):
                _iniciar_prova(i)

        else:
            # Bloqueado
            st.markdown(f"""
            <div style="background:#0c1120;border:1px solid #1a2035;border-radius:12px;
                        padding:.8rem 1.2rem;margin-bottom:.5rem;opacity:.5">
                🔒 <span style="font-size:.9rem">{nome}</span>
                <span style="float:right;font-size:.75rem;color:#3d5080">Bloqueado</span>
            </div>
            """, unsafe_allow_html=True)


def _iniciar_prova(indice: int):
    nome    = SIMULADOS_ORDEM[indice]
    materias = DIC_SIMULADOS[nome]
    pool    = [q for q in BANCO_QUESTOES if q["modulo"] in materias]
    qtd     = min(QUESTOES_POR_PROVA, len(pool))

    st.session_state.prova_ativa           = True
    st.session_state.prova_simulado_indice = indice
    st.session_state.questoes              = random.sample(pool, qtd)
    st.session_state.respostas             = {}
    st.session_state.tempo_fim             = datetime.now() + timedelta(minutes=TEMPO_PROVA_MIN)
    st.session_state.inicio_prova          = datetime.now()
    st.session_state.resultado             = None
    st.session_state.modo_revisao          = False
    st.rerun()


# ─────────────────────────────────────────────
# TELA DA PROVA
# ─────────────────────────────────────────────
def tela_prova():
    restante = segundos_restantes()
    questoes = st.session_state.questoes
    indice   = st.session_state.prova_simulado_indice
    nome_sim = SIMULADOS_ORDEM[indice]

    # ── Cabeçalho ──
    col_tit, col_timer = st.columns([3, 1])
    with col_tit:
        st.markdown(f"""
        <div style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:700">{nome_sim}</div>
        <div style="color:#6b7294;font-size:.82rem">{len(questoes)} questões · {QUESTOES_POR_PROVA} minutos</div>
        """, unsafe_allow_html=True)

    with col_timer:
        cls = "urgente" if restante < 300 else ""
        st.markdown(f"""
        <div class="timer-box {cls}">⏱ {formatar_tempo(restante)}</div>
        """, unsafe_allow_html=True)

    # Progresso de respostas
    respondidas = len(st.session_state.respostas)
    barra_progresso(respondidas / len(questoes), f"{respondidas}/{len(questoes)} respondidas")

    st.markdown("---")

    # ── Auto-submit quando zera (re-render a cada interação) ──
    tempo_esgotado = restante <= 0

    # ── Questões ──
    for i, q in enumerate(questoes):
        resp_atual = st.session_state.respostas.get(i)

        st.markdown(f"""
        <div style="font-size:.75rem;color:#6b7294;margin-bottom:.2rem">
            <span class="badge badge-blue">{q['modulo']}</span>
            &nbsp; Questão {i+1}
        </div>
        <div style="font-size:1rem;font-weight:500;margin-bottom:.6rem">{q['pergunta']}</div>
        """, unsafe_allow_html=True)

        opcoes    = [f"{k}) {v}" for k, v in q["opcoes"].items()]
        opcoes_map = {f"{k}) {v}": k for k, v in q["opcoes"].items()}

        idx_atual = None
        if resp_atual:
            rotulo = f"{resp_atual}) {q['opcoes'][resp_atual]}"
            if rotulo in opcoes:
                idx_atual = opcoes.index(rotulo)

        escolha = st.radio(
            label=f"q_{i}",
            options=opcoes,
            index=idx_atual,
            key=f"radio_{i}",
            label_visibility="collapsed",
            disabled=tempo_esgotado,
        )

        if escolha:
            st.session_state.respostas[i] = opcoes_map[escolha]

        st.markdown("<div style='margin-bottom:1.2rem'></div>", unsafe_allow_html=True)

    st.markdown("---")

    # ── Ações finais ──
    col_fin, col_canc = st.columns([2, 1])
    with col_fin:
        finalizar = st.button("✅ Finalizar Simulado", use_container_width=True)
    with col_canc:
        if st.button("❌ Cancelar", use_container_width=True):
            st.session_state.prova_ativa = False
            st.rerun()

    # ── Processar resultado ──
    if finalizar or tempo_esgotado:
        _processar_resultado()


# ─────────────────────────────────────────────
# PROCESSAR RESULTADO
# ─────────────────────────────────────────────
def _processar_resultado():
    questoes    = st.session_state.questoes
    respostas   = st.session_state.respostas
    indice      = st.session_state.prova_simulado_indice
    nome_sim    = SIMULADOS_ORDEM[indice]
    usuario     = st.session_state.usuario
    inicio      = st.session_state.inicio_prova

    tempo_total = (datetime.now() - inicio).total_seconds()
    tempo_medio = tempo_total / len(questoes) if questoes else 0

    acertos     = 0
    por_modulo  = {}   # {modulo: [acertos, total]}
    detalhes    = []   # [{pergunta, opcoes, correta, respondida, acertou, explicacao}]

    for i, q in enumerate(questoes):
        mod = q["modulo"]
        por_modulo.setdefault(mod, [0, 0])
        por_modulo[mod][1] += 1

        resp = respostas.get(i)
        acertou = resp == q["resposta_correta"]
        if acertou:
            acertos += 1
            por_modulo[mod][0] += 1

        detalhes.append({
            "pergunta":    q["pergunta"],
            "opcoes":      q["opcoes"],
            "modulo":      mod,
            "correta":     q["resposta_correta"],
            "respondida":  resp,
            "acertou":     acertou,
            "explicacao":  q.get("explicacao", ""),
        })

    nota   = (acertos / len(questoes)) * 100 if questoes else 0
    status = "Aprovado" if nota >= NOTA_APROVACAO else "Reprovado"

    # Salvar nos Sheets
    salvar_resultado(usuario, nome_sim, nota, tempo_medio, por_modulo)

    # Atualizar progresso somente se aprovado e era o simulado atual
    progresso_atual = st.session_state.simulado_atual_indice
    novo_idx        = progresso_atual
    if status == "Aprovado" and indice == progresso_atual:
        novo_idx = progresso_atual + 1
    salvar_progresso(usuario, novo_idx, status)
    st.session_state.simulado_atual_indice = novo_idx

    # Guardar resultado na session e limpar prova
    st.session_state.resultado  = {
        "nome_sim":   nome_sim,
        "nota":       nota,
        "status":     status,
        "acertos":    acertos,
        "total":      len(questoes),
        "tempo_medio": tempo_medio,
        "por_modulo": por_modulo,
        "detalhes":   detalhes,
    }
    st.session_state.prova_ativa = False
    st.rerun()


# ─────────────────────────────────────────────
# TELA DE RESULTADO
# ─────────────────────────────────────────────
def tela_resultado():
    r = st.session_state.resultado
    aprovado = r["status"] == "Aprovado"

    cor_status  = "#22c55e" if aprovado else "#ef4444"
    bg_status   = "#0d2e1a" if aprovado else "#2e0d0d"
    emoji_status = "🏆" if aprovado else "📖"

    # ── Banner resultado ──
    st.markdown(f"""
    <div style="background:{bg_status};border:1px solid {cor_status}33;border-radius:14px;
                padding:1.5rem;text-align:center;margin-bottom:1.2rem">
        <div style="font-size:2.5rem">{emoji_status}</div>
        <div style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:{cor_status}">
            {r['nota']:.1f}%
        </div>
        <div style="font-family:'Syne',sans-serif;font-size:1rem;color:{cor_status};
                    text-transform:uppercase;letter-spacing:.12em;margin-top:4px">
            {r['status']}
        </div>
        <div style="color:#6b7294;font-size:.85rem;margin-top:.4rem">{r['nome_sim']}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Métricas ──
    metric_cards([
        (f"{r['acertos']}/{r['total']}", "Acertos"),
        (f"{r['tempo_medio']:.0f}s", "Tempo médio/questão"),
        (f"{r['nota']:.1f}%", "Nota final"),
    ])

    # ── Desempenho por módulo ──
    st.markdown("#### 📊 Desempenho por módulo")
    for mod, (ac, tot) in r["por_modulo"].items():
        pct = (ac / tot * 100) if tot else 0
        cor_barra = "#22c55e" if pct >= 70 else "#ef4444"
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;font-size:.82rem;color:#9ba3bf;margin-bottom:2px">
            <span>{mod}</span><span>{ac}/{tot} ({pct:.0f}%)</span>
        </div>
        <div class="prog-bar-outer">
            <div style="background:{cor_barra};height:8px;border-radius:8px;width:{pct}%"></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Ações ──
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button("🔍 Revisar questões", use_container_width=True):
            st.session_state.modo_revisao     = True
            st.session_state.revisao_questoes = r["detalhes"]
            st.session_state.resultado        = None
            st.rerun()
    with col_b:
        if st.button("📚 Voltar aos simulados", use_container_width=True):
            st.session_state.resultado = None
            st.rerun()
    with col_c:
        if st.button("🔄 Refazer este simulado", use_container_width=True):
            _iniciar_prova(r.get("indice", st.session_state.simulado_atual_indice - 1))


# ─────────────────────────────────────────────
# MODO REVISÃO
# ─────────────────────────────────────────────
def tela_revisao():
    questoes = st.session_state.revisao_questoes

    erradas = [q for q in questoes if not q["acertou"]]
    certas  = [q for q in questoes if q["acertou"]]

    st.markdown(f"""
    <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:700;margin-bottom:.8rem">
        🔍 Revisão — {len(erradas)} erros de {len(questoes)} questões
    </div>
    """, unsafe_allow_html=True)

    filtro = st.radio(
        "Exibir:", ["Todas", "Apenas erradas", "Apenas certas"],
        horizontal=True, index=1
    )

    lista = {"Todas": questoes, "Apenas erradas": erradas, "Apenas certas": certas}[filtro]

    for i, q in enumerate(lista):
        classe = "correta" if q["acertou"] else "errada"
        icon   = "✅" if q["acertou"] else "❌"
        cor_ga = "#22c55e"
        cor_er = "#ef4444"

        with st.expander(f"{icon} Questão {i+1} — {q['modulo']}", expanded=not q["acertou"]):
            st.markdown(f"**{q['pergunta']}**")

            for letra, texto in q["opcoes"].items():
                rotulo = f"{letra}) {texto}"
                if letra == q["correta"]:
                    st.markdown(f"<div style='color:{cor_ga};font-size:.9rem'>✓ {rotulo}</div>", unsafe_allow_html=True)
                elif letra == q["respondida"] and not q["acertou"]:
                    st.markdown(f"<div style='color:{cor_er};font-size:.9rem'>✗ {rotulo} <em>(sua resposta)</em></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='color:#6b7294;font-size:.9rem'>&nbsp;&nbsp; {rotulo}</div>", unsafe_allow_html=True)

            if q["respondida"] is None:
                st.markdown(f"<div style='color:#fbbf24;font-size:.85rem'>⚠ Não respondida</div>", unsafe_allow_html=True)

            if q["explicacao"]:
                st.markdown(f"""
                <div style="background:#0f1a2e;border-left:3px solid #3d6ef5;border-radius:0 8px 8px 0;
                            padding:.8rem 1rem;margin-top:.6rem;font-size:.88rem;color:#9ba3bf">
                    💡 {q['explicacao']}
                </div>
                """, unsafe_allow_html=True)

    if st.button("← Voltar aos simulados", use_container_width=True):
        st.session_state.modo_revisao     = False
        st.session_state.revisao_questoes = []
        st.rerun()


# ─────────────────────────────────────────────
# ABA EVOLUÇÃO
# ─────────────────────────────────────────────
def tela_evolucao():
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:700;margin-bottom:1rem">
        📈 Sua Evolução
    </div>
    """, unsafe_allow_html=True)

    try:
        df = _ler("Resultados")
    except Exception:
        st.warning("Não foi possível carregar os resultados.")
        return

    usuario = st.session_state.usuario
    user_df = df[df["Usuario"] == usuario].copy() if "Usuario" in df.columns else pd.DataFrame()

    if user_df.empty:
        st.info("Você ainda não realizou nenhum simulado. Faça o primeiro para ver sua evolução!")
        return

    # Métricas gerais
    melhor = user_df["Nota"].max()
    media  = user_df["Nota"].mean()
    total  = len(user_df)
    aprov  = len(user_df[user_df["Nota"] >= NOTA_APROVACAO])

    metric_cards([
        (total, "Provas feitas"),
        (f"{aprov}/{total}", "Aprovações"),
        (f"{media:.1f}%", "Média geral"),
        (f"{melhor:.1f}%", "Melhor nota"),
    ])

    st.markdown("#### Notas por simulado")
    st.line_chart(user_df[["Simulado", "Nota"]].set_index("Simulado"), use_container_width=True)

    if "Tempo_medio" in user_df.columns and user_df["Tempo_medio"].notna().any():
        st.markdown("#### Tempo médio por questão (s)")
        st.line_chart(user_df[["Simulado", "Tempo_medio"]].set_index("Simulado"), use_container_width=True)

    st.markdown("#### Histórico completo")
    cols_exib = [c for c in ["Data", "Simulado", "Nota", "Tempo_medio"] if c in user_df.columns]
    st.dataframe(
        user_df[cols_exib].sort_values("Data", ascending=False),
        use_container_width=True,
        hide_index=True,
    )


# ─────────────────────────────────────────────
# ABA ADMIN
# ─────────────────────────────────────────────
def tela_admin():
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:700;margin-bottom:1rem">
        🛡️ Painel Admin
    </div>
    """, unsafe_allow_html=True)

    try:
        df_res  = _ler("Resultados")
        df_prog = _ler("Progresso")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return

    tab1, tab2, tab3 = st.tabs(["📊 Resultados", "🏆 Ranking", "📥 Exportar"])

    with tab1:
        st.dataframe(df_res, use_container_width=True, hide_index=True)

    with tab2:
        if not df_res.empty and "Usuario" in df_res.columns:
            ranking = (
                df_res.groupby("Usuario")["Nota"]
                .agg(["mean", "max", "count"])
                .rename(columns={"mean": "Média", "max": "Melhor", "count": "Provas"})
                .sort_values("Média", ascending=False)
                .reset_index()
            )
            ranking["Média"] = ranking["Média"].round(1)
            ranking["Melhor"] = ranking["Melhor"].round(1)
            ranking.index = ranking.index + 1  # Posição começa em 1
            st.dataframe(ranking, use_container_width=True)

    with tab3:
        st.markdown("Baixe os dados completos em CSV:")
        csv_res  = df_res.to_csv(index=False).encode("utf-8")
        csv_prog = df_prog.to_csv(index=False).encode("utf-8") if not df_prog.empty else b""

        col1, col2 = st.columns(2)
        with col1:
            st.download_button("📥 Resultados CSV", csv_res,  "resultados.csv",  "text/csv")
        with col2:
            if csv_prog:
                st.download_button("📥 Progresso CSV", csv_prog, "progresso.csv", "text/csv")


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
def sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div style="padding:.5rem 0 1rem">
            <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;
                        background:linear-gradient(90deg,#7cabff,#3d6ef5);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent">
                VMB Invest
            </div>
            <div style="font-size:.75rem;color:#6b7294;margin-top:2px">Simulado ANCORD</div>
        </div>
        <div style="font-size:.85rem;color:#9ba3bf;padding:.4rem .6rem;
                    background:#1a2035;border-radius:8px;margin-bottom:1rem">
            👤 {st.session_state.usuario}
        </div>
        """, unsafe_allow_html=True)

        opcoes_menu = ["Simulados", "Evolução"]
        if st.session_state.usuario in ADMINS:
            opcoes_menu.append("Admin")

        menu = st.radio("", opcoes_menu, label_visibility="collapsed")

        st.markdown("<div style='flex:1'></div>", unsafe_allow_html=True)
        st.markdown("---")
        if st.button("🚪 Sair", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    return menu


# ─────────────────────────────────────────────
# ROTEADOR PRINCIPAL
# ─────────────────────────────────────────────
def main():
    # 1. Login
    if not st.session_state.logado:
        tela_login()
        return

    # 2. Sidebar (sempre visível após login)
    menu = sidebar()

    # 3. Prova em andamento → tela da prova (prioridade máxima)
    if st.session_state.prova_ativa:
        tela_prova()
        return

    # 4. Resultado pendente → tela de resultado
    if st.session_state.resultado is not None:
        tela_resultado()
        return

    # 5. Modo revisão
    if st.session_state.modo_revisao:
        tela_revisao()
        return

    # 6. Navegação por menu
    if menu == "Simulados":
        if not st.session_state.mostrou_welcome:
            tela_boas_vindas()
        else:
            tela_simulados()

    elif menu == "Evolução":
        tela_evolucao()

    elif menu == "Admin":
        if st.session_state.usuario in ADMINS:
            tela_admin()
        else:
            st.error("Acesso restrito.")


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__" or True:
    main()
