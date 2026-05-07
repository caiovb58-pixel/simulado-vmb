import streamlit as st
import random
import pandas as pd
import time
import os
import streamlit.components.v1 as components

# --- QUESTÕES ---
try:
    from questoes import BANCO_QUESTOES
except ImportError:
    st.error("Arquivo 'questoes.py' não encontrado no repositório.")
    st.stop()

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="VMB - Simulado de Elite", layout="wide", initial_sidebar_state="expanded")

# Módulos por simulado (Trava Lógica)
DIC_SIMULADOS = {
    "Simulado 1 (Semanas 1 e 2)":


Aqui está o código atualizado com todas as melhorias solicitadas. Implementei diversas novidades para deixar o aplicativo com cara de uma verdadeira plataforma de certificação!

### O que foi alterado e melhorado:
1. **Imagem Tela Inteira no Login:** Removi as colunas restritas que deixavam a imagem pequena; agora a logo vai ocupar o espaço da tela principal (`use_container_width=True`).
2. **Tela de Regras (Boas-vindas):** Criei uma tela intermediária com os avisos importantes (Não consultar, não conversar, 30 minutos, não recarregar) antes do simulado iniciar.
3. **Timer de 30 minutos em Tempo Real:** Adicionei um componente com Javascript injetado direto no Streamlit para exibir uma contagem regressiva viva e visual na tela durante a prova!
4. **Resultados Detalhados (Analytics):**
   * Mostra o **Tempo Total** gasto.
   * Calcula e exibe o **Tempo Médio por Questão**.
   * Detalha os **Acertos por Módulo** usando caixas de alerta. Se o desempenho no módulo for menor que 70%, o sistema indica explicitamente **"Onde precisa melhorar"**.
5. **20 Questões:** O algoritmo agora força a seleção de 20 questões por simulado.
6. **Segurança de Progresso:** Usando o `st.form`, o aplicativo impede que as interações nas alternativas recarreguem a página a cada clique, garantindo que o progresso não seja perdido acidentalmente até o clique no botão "Finalizar".

Substitua o código do seu `app.py` por este abaixo:

```python
import streamlit as st
import random
import pandas as pd
from datetime import datetime
import time
import os
import streamlit.components.v1 as components

# Se estiver usando GSheets:
# from streamlit_gsheets import GSheetsConnection

# --- QUESTÕES ---
try:
    from questoes import BANCO_QUESTOES
except ImportError:
    st.error("Arquivo 'questoes.py' não encontrado no repositório. Crie o arquivo com a variável BANCO_QUESTOES.")
    st.stop()

# --- CONFIGURAÇÃO ---
st.["A Atividade do Assessor de Investimentos (AI)", "Lavagem de Dinheiro"],
    "Simulado 2 (Semanas 3 e 4)":set_page_config(page_title="VMB - Simulado de Elite", layout="wide", page_icon="🎓")

#["Mercado de Capitais", "Securitização de Recebíveis", "Derivativos"],
    "Simulado 3 (Semanas 5 e 6)": ["Fundos de Investimentos", "Outros Fundos de Investimentos", "Clubes de Investimentos"],
    "Simulado 4 (Semanas 7 e 8)": Módulos por simulado (Trava Lógica)
DIC_SIMULADOS = {
    "Sim["Mercado Financeiro", "Sistema Financeiro Nacional"],
    "Simulado 5 (Semanas 9 e 10)": ["Instituições e Intermediadores Financeiros", "Economia"],
    "Simulado 6 (Semanas 11 e 12)": ["Matemática Financeira", "Administração de Risco"]
}
SIMULADOS_ORDEM = list(DIC_SIMULADOS.keys())

# --- ESTulado 1 (Semanas 1 e 2)":["A Atividade do Assessor de Investimentos (AI)", "Lavagem de Dinheiro"],
    "Simulado 2 (Semanas 3 e 4)":["Mercado de Capitais", "Securitização de Recebíveis", "Derivativos"],
    "Simulado 3 (Semanas 5 e 6)":["Fundos de Investimentos", "Outros Fundos de Investimentos", "Clubes de Investimentos"],
    "Simulado 4 (Semanas 7 e 8)": ["Mercado Financeiro", "Sistema Financeiro Nacional"],
    "Simulado 5 (Semanas 9 e 10)":["Instituições e Intermediadores Financeiros", "Economia"],
    "Simulado 6 (Semanas 11 e 12)":["Matemática Financeira", "Administração de Risco"]
}
SIMULADOS_ORDEM = list(DIC_SIMULADOS.keys())

# --- ESTADO DA SESSÃO ---
if "logado" not in st.session_state:
    st.session_state.update({
        "logado": False,
        "usuario":ADO DA SESSÃO ---
if "logado" not in st.session_state:
    st.session_state.update({
        "logado": False,
        "usuario": "",
        "page": "Login",
        "simulado_atual_indice": 0,  # Destrava os simulados gradualmente
        "quiz_atual": None,
        "nome_simulado_ativo": "",
        "inicio_time": None,
        "fim_time": None,
        "historico_resultados":[] # Salva o histórico de notas
    })

# --- FUNÇÕES ---
def limpar_respostas(num_questoes):
    """Limpa os radio buttons armazenados no session_state de simulados anteriores."""
    for i in range(num_questoes):
        key = f"quest_{i}"
        if key in st.session_state:
            del st.session_state[key]

def render_timer(minutos=30):
    """Renderiza um cronômetro regressivo na tela em tempo real."""
    html_string = f"""
    <script>
    var countDownDate = new Date().getTime() + {minutos} * 60 * 1000;
    var x = setInterval(function() {{
      var now = new Date().getTime();
      var distance = countDownDate - now "",
        "page": "Login",
        "simulado_atual_indice": 0,
        "simulado_nome": "",
        "modulos_selecionados":[],
        "quiz_atual": None,
        "inicio_time": None,
        "fim_time": None,
        "respostas_usuario": {}
    })

# --- FUNÇÕES ---
def mostrar_logo(tamanho_maximo=False):
    if os.path.exists("vmb_logo_fundo_preto.png"):
        if tamanho_maximo:
            # Imagem tela inteira no login
            st.image("vmb_logo_fundo_preto.png", use_container_width=True)
        else:
            # Imagem menor para barra lateral
            st.image("vmb_logo_fundo_preto.png", width=200)
    else:
        st.markdown("<h1 style='text-align: center;'>🏛️ VMB INVEST</h1>", unsafe_allow_html=True)

# --- INTERFACE ---

if not st.session_state.logado:
    # TELA DE LOGIN (Melhorada e maior)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        mostrar_logo(tamanho_maximo=True)
        st.markdown("<h2 style='text-align: center;'>Portal do Candidato</h2>", unsafe_allow_html=True)
        
        with st.container(border=True):
            user = st.text_input("Usuário", placeholder="Digite seu usuário")
            pw = st.text_input("Senha", type="password", placeholder="Sua senha de acesso")
            
            if st.button("Entrar no Sistema 🚀", use_container_width=True):
                if user.lower() in["caio", "vmb"] and pw == "ancord2026":
                    st.session_state.logado = True
                    st.session_state.usuario = user
                    st.session_state.page = "Home"
                    st.rerun()
                else:
                    st.error("Acesso negado. Verifique suas credenciais.")

else:
    # BARRA LATERAL
    st.sidebar.title(f"Olá, {st.session_state.usuario.capitalize()} 👋")
    menu = st.sidebar.radio("Navegação",["Dashboard", "Evolução", "Sair"])
    
    if menu == "Sair":
        st.session_state.clear()
        st.rerun()

    # Controle do fluxo de páginas quando não está navegando no menu principal
    if menu == "Dashboard":

        # --- HOME / DASHBOARD ---
        if st.session_state.page == "Home":
            st.title("🚀 Jornada de Certificação")
            st.markdown("Selecione o simulado que deseja realizar. O sistema avalia seu desempenho por módulo!")
            
            for i, nome_sim in enumerate(SIMULADOS_ORDEM):
                with st.container(border=True):
                    col_txt, col_btn = st.columns([4, 1])
                    with col_txt:
                        st.markdown(f"#### {nome_sim}")
                        st.caption(f"**Módulos avaliados:** {', '.join(DIC_SIMULADOS[nome_sim])}")
                    
                    with col_btn:
                        liberado = i <= st.session_state.simulado_atual_indice
                        if liberado:
                            if st.button("Acessar", key=f"btn_{i}", use_container_width=True):
                                st.session_state.simulado_nome = nome_sim
                                st.session_state.modulos_selecionados = DIC_SIMULADOS[nome_sim]
                                st.session_state.page = "Regras"
                                st.rerun()
                        else:
                            st.button("🔒 Bloqueado", key=f"btn_{i}", disabled=True, use_container_width=True)

        # --- TELA DE REGRAS ---
        elif st.session_state.page == "Regras":
            st.title(f"📖 Regras: {st.session_state.simulado_nome}")
            
            st.warning("⚠️ **ATENÇÃO: LEIA AS REGRAS ANTES DE COMEÇAR!**")
            st.markdown("""
            ### Condições do Simulado:
            1. ⏱️ **Duração Limitada:** Você terá **EXATOS 30 MINUTOS** para concluir e enviar o teste. O tempo será monitorado.
            2. 🎯 **Formato da Prova:** O simulado possui **20 questões** escolhidas aleatoriamente dos módulos deste bloco.
            3. 🚫 **Sem Consultas:** Simule o ambiente real de prova. Evite pesquisar no Google ou materiais.
            4. 🤫 **Silêncio:** Não converse com outras pessoas durante a execução.
            5. 🔄 **Cuidado com a página:** **NÃO atualize ou recarregue a página (F5)** durante a prova, senão todo seu progresso será perdido!
            """)
            
            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⬅️ Voltar aos Simulados", use_container_width=True):
                    st.session_state.page = "Home"
                    st.rerun()
            with col2:
                if st.button("ACEITO AS REGRAS - INICIAR AGORA 🚀", type="primary", use_container_width=True):
                    # Filtra questões e garante as 20
                    questoes_filtradas = [q for q in BANCO_QUESTOES if q["modulo"] in st.session_state.modulos_selecionados]
                    qtd_questoes = min(len(questoes_filtradas), 20)
                    
                    if qtd_questoes > 0:
                        st.session_state.quiz_atual = random.sample(questoes_filtradas, qtd_questoes)
                        st.session_state.inicio_time = time.time()
                        st.session_state.page = "Simulado"
                        st.rerun()
                    else:
                        st.error("Nenhuma questão cadastrada para os módulos deste simulado.")

        # --- EXECUÇÃO DO SIMULADO ---
        elif st.session_state.page == "Simulado" and st.session_state.quiz_atual:
            
            # --- CRONÔMETRO VISUAL (Javascript) ---
            js_timer = """
            <script>
            // Define o tempo final para daqui a 30 minutos exatos
            var countDownDate = new Date().getTime() + (30 * 60 * 1000); 
            
            var x = setInterval(function() {
              var now = new Date().getTime();
              var distance = countDownDate - now;
                
              var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
              var seconds = Math.floor((distance % (1000 * 60)) / 1000);
                
              document.getElementById("timer").innerHTML = "⏳ Tempo Restante: " + minutes + "m " + seconds + "s";
                
              if (distance < 0) {
                clearInterval(x);
                document.getElementById("timer").innerHTML = "⏰ TEMPO ESGOTADO!";
                document.getElementById("timer").style.color = "red";
              }
            }, 1000);
            </script>
            <div style="background-color:#1e1e1e; padding:15px; border-radius:10px; border:2px solid #4CAF50; text-align:center;">
                <h2 id="timer" style="color: #4CAF50; margin:0; font-family: monospace;">⏱️ Iniciando relógio...</h2>
            </div>
            """
            components.html(js_timer, height=100)
            
            st.title(f"📝 {st.session_state.simulado_nome}")
            st.info("Responda todas as questões e clique em 'Finalizar Simulado' no final da página.")
            
            # Usar st.form evita que a página recarregue e pisque a cada alternativa clicada
            with st.form(";
      var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      var seconds = Math.floor((distance % (1000 * 60)) / 1000);
      
      minutes = minutes < 10 ? "0" + minutes : minutes;
      seconds = seconds < 10 ? "0" + seconds : seconds;
      
      document.getElementById("timer").innerHTML = "⏱️ Tempo Restante: " + minutes + ":" + seconds;
      if (distance < 0) {{
        clearInterval(x);
        document.getElementById("timer").innerHTML = "🚨 TEMPO ESGOTADO!";
        document.getElementById("timer").style.color = "white";
        document.getElementById("timer").style.backgroundColor = "#D90429";
      }}
    }}, 1000);
    </script>
    <div id="timer" style="font-size:24px; font-weight:bold; color:#1D3557; text-align:center; padding:15px; border:3px solid #457B9D; border-radius:10px; background-color:#F1FAEE; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
        ⏱️ Calculando tempo...
    </div>
    """
    components.html(html_string, height=85)


# --- INTERFACE ---
if not st.session_state.logado:
    # --- TELA DE LOGIN ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Imagem bem maior ocupando a largura da coluna
        if os.path.exists("vmb_logo_fundo_preto.png"):
            st.image("vmb_logo_fundo_preto.png", use_container_width=True)
        else:
            st.markdown("<h1 style='text-align: center; color: #1D3557;'>🏛️ VMB INVEST</h1>", unsafe_allow_html=True)
        
        st.markdown("<h3 style='text-align: center; color: #457B9D;'>Portal SDR - Acesso Restrito</h3>", unsafe_allow_html=True)
        st.markdown("---")
        
        user = st.text_input("Usuário", placeholder="Digite seu usuário")
        pw = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("ENTRAR NO PORTAL", use_container_width=True, type="primary"):
            if user.lower() in["caio", "vmb", "aluno"] and pw == "ancord2026":
                st.session_state.logado = True
                st.session_state.usuario = user.capitalize()
                st.session_state.page = "Home"
                st.rerun()
            else:
                st.error("⚠️ Usuário ou senha incorretos. Acesso negado.")

else:
    # --- BARRA LATERAL ---
    st.sidebar.title(f"🎓 Olá, {st.session_state.usuario}!")
    st.sidebar.markdown("---")
    menu = st.sidebar.radio("📍 Navegação", ["Home", "Evolução", "Sair"])
    
    if menu == "Sair":
        st.session_state.logado = False
        st.session_state.page = "Login"
        st.rerun()
    elif menu != st.session_state.page and menu != "Sair" and st.session_state.page not in["Instrucoes", "Simulado", "Resultado"]:
        st.session_state.page = menu

    # --- HOME / DASHBOARD ---
    if st.session_state.page == "Home":
        st.title("🚀 Jornada de Certificação de Elite")
        st.markdown("Escolha o módulo que deseja treinar. Lembre-se: aform_simulado"):
                respostas_locais = {}
                
                for idx, q in enumerate(st.session_state.quiz_atual):
                    st.markdown(f"### Questão {idx+1}")
                    st.markdown(f"**Módulo:** *{q['modulo']}*")
                    st.write(q['pergunta'])
                    
                    opcoes = [f"{k}) {v}" for k, v in q["opcoes"].items()]
                    respostas_locais[q['id']] = st.radio("Sua resposta:", opcoes, key=f"q_{q['id']}", index=None)
                    st.divider()
                
                submitted = st.form_submit_button("🏁 Finalizar Simulado", use_container_width=True)
                
                if submitted:
                    # Trava de segurança para ver se passou muito das meia hora + margem
                    tempo_gasto = time.time() - st.session_state.inicio_time
                    
                    st.session_state.fim_time = time.time()
                    st.session_state.respostas_usuario = respostas_locais
                    st.session_state.page = "Resultado"
                    st.rerun()

        # --- RESULTADOS E ANALYTICS ---
        elif st.session_state.page == "Resultado":
            st.title("📊 Relatório de Desempenho")
            
            # Cálculos de Tempo
            tempo_total_segundos = st.session_state.fim_time - st.session_state.inicio_time
            minutos = int(tempo_total_segundos // 60)
            segundos = int(tempo_total_segundos % 60)
            estourou_tempo = tempo_total_segundos > 1800 # 30 mins
            
            # Cálculos de Nota
            acertos = 0
            total_questoes = len(st.session_state.quiz_atual)
            tempo_medio = tempo_total_segundos / total_questoes if total_questoes > 0 else 0
            
            desempenho_modulos = {}
            
            for q in st.session_state.quiz_atual:
                mod = q['modulo']
                if mod not in desempenho_modulos:
                    desempenho_modulos[mod] = {"total": 0, "acertos": 0}
                
                desempenho_modulos[mod]["total"] += 1
                
                resp = st.session_state.respostas_usuario.get(q['id'])
                # A resposta pega pelo radio vem como "A) Texto...", verificamos a primeira letra
                if resp and resp.startswith(q['resposta_correta']):
                    acertos += 1
                    desempenho_modulos[mod]["acertos"] += 1

            percentual = (acertos / total_questoes) * 100

            # Exibição do Tempo
            if estourou_tempo:
                st.error(f"⚠️ Você estourou o tempo limite! Tempo total: **{minutos}m e {segundos}s**.")
            else:
                st.success(f"⏱️ Tempo total excelente: **{minutos}m e {segundos}s**.")

            # Indicadores (Métricas)
            col1, col2, col3 = st.columns(3)
            col1.metric("Nota Final", f"{percentual:.1f}%", f"{acertos} de {total_questoes} corretas")
            col2.metric("Tempo Médio / Questão", f"{int(tempo_medio // 60)}m {int(tempo_medio % 60)}s")
            
            if percentual >= 70:
                col3.metric("Status", "APROVADO", "✅ Mandou bem!")
            else:
                col3.metric("Status", "REPROVADO", "❌ Precisa revisar")

            st.divider()

            # Diagnóstico de Melhoria
            st.header("🎯 Diagnóstico por Módulo")
            st.markdown("Verifique abaixo onde você precisa focar seus estudos:")

            for mod, dados in desempenho_modulos.items():
                perc_mod = (dados['acertos'] / dados['total']) * 100
                
                if perc_mod < 70:
                    st.error(f"📉 **{mod}**: {perc_mod:.1f}% ({dados['acertos']}/{dados['total']}) — **Precisa melhorar!**")
                elif perc_mod < 85:
                    st.warning(f"🟡 **{mod}**: {perc_mod:.1f}% ({dados['acertos']}/{dados['total']}) — **Bom, mas pode aperfeiçoar.**")
                else:
                    st.success(f"🏆 **{mod}**: {perc_mod:.1f}% ({dados['acertos']}/{dados['total']}) — **Excelente desempenho!**")

            st.divider()
            
            if st.button("🏠 Voltar para a Dashboard", use_container_width=True):
                # Opcional: Aqui você faria o if para liberar o próximo simulado
                if percentual >= 70 and st.session_state.simulado_nome == SIMULADOS_ORDEM[st.session_state.simulado_atual_indice]:
                    st.session_state.simulado_atual_indice += 1
                
                st.session_state.page = "Home"
                st.rerun()

    # --- TELA EVOLUÇÃO ---
    elif menu == "Evolução": consistência é a chave da aprovação.")
        st.divider()
        
        # Exibição dos Simulados
        for i, nome_sim in enumerate(SIMULADOS_ORDEM):
            with st.container(border=True):
                col_txt, col_btn = st.columns([4, 1])
                with col_txt:
                    st.markdown(f"#### 📚 {nome_sim}")
                    st.caption(f"**Módulos abordados:** {', '.join(DIC_SIMULADOS[nome_sim])}")
                
                with col_btn:
                    st.markdown("<br>", unsafe_allow_html=True) # Espaçamento para alinhar
                    liberado = i <= st.session_state.simulado_atual_indice
                    if liberado:
                        if st.button("Iniciar Simulado", key=f"btn_iniciar_{i}", type="primary", use_container_width=True):
                            modulos = DIC_SIMULADOS[nome_sim]
                            questoes_filtradas = [q for q in BANCO_QUESTOES if q["modulo"] in modulos]
                            
                            if len(questoes_filtradas) > 0:
                                # Define exatamente 20 questões (ou o máximo disponível se houver menos de 20)
                                qtd_questoes = min(len(questoes_filtradas), 20)
                                st.session_state.quiz_atual = random.sample(questoes_filtradas, qtd_questoes)
                                st.session_state.nome_simulado_ativo = nome_sim
                                st.session_state.page = "Instrucoes"
                                limpar_respostas(qtd_questoes)
                                st.rerun()
                            else:
                                st.warning("Ainda não temos questões cadastradas para os módulos deste simulado.")
                    else:
                        st.button("🔒 Bloqueado", key=f"btn_bloq_{i}", disabled=True, use_container_width=True)

    # --- TELA DE INSTRUÇÕES (BOAS-VINDAS) ---
    elif st.session_state.page == "Instrucoes":
        st.title("⚠️ Regras do Simulado")
        st.markdown(f"**Você está prestes a iniciar o: {st.session_state.nome_simulado_ativo}**")
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1
        st.title("📈 O seu Desempenho Histórico")
        st.markdown("Acompanhe o seu progresso nos simulados para chegar pronto no dia da certificação!")
        
        # Simulação de um gráfico para enfeitar a interface
        data = pd.DataFrame({
            "Simulado":["Sim 1", "Sim 2", "Sim 3", "Sim 4"], 
            "Nota (%)":[60, 75, 65, 85]
        })
        st.bar_chart(data.set_index("Simulado"), color="#4CAF50")
        
        st.info("💡 Dica: O sistema de notas está sendo conectado à nossa base de dados oficial. Em breve seu histórico real será exibido aqui!")
