import streamlit as st
import random
import pandas as pd
from datetime import datetime
import time
import os
import streamlit.components.v1 as components

# --- QUESTÕES ---
try:
    from questoes import BANCO_QUESTOES
except ImportError:
    st.error("Arquivo 'questoes.py' não encontrado no repositório. Crie o arquivo com a variável BANCO_QUESTOES.")
    st.stop()

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="VMB - Simulado de Elite", layout="wide", page_icon="🎓")

# Módulos por simulado (Trava Lógica)
DIC_SIMULADOS = {
    "Simulado 1 (Semanas 1 e 2)":["A Atividade do Assessor de Investimentos (AI)", "Lavagem de Dinheiro"],
    "Simulado 2 (Semanas 3 e 4)":["Mercado de Capitais", "Securitização de Recebíveis", "Derivativos"],
    "Simulado 3 (Semanas 5 e 6)":["Fundos de Investimentos", "Outros Fundos de Investimentos", "Clubes de Investimentos"],
    "Simulado 4 (Semanas 7 e 8)":["Mercado Financeiro", "Sistema Financeiro Nacional"],
    "Simulado 5 (Semanas 9 e 10)":["Instituições e Intermediadores Financeiros", "Economia"],
    "Simulado 6 (Semanas 11 e 12)": ["Matemática Financeira", "Administração de Risco"]
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
        st.markdown("<h1 style='text-align: center; color: #1D3557;'>🏛️ VMB INVEST</h1>", unsafe_allow_html=True)

# --- INTERFACE ---
if not st.session_state.logado:
    # --- TELA DE LOGIN ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Imagem grande ocupando a largura da coluna
        mostrar_logo(tamanho_maximo=True)
        
        st.markdown("<h3 style='text-align: center; color: #457B9D;'>Portal SDR - Acesso Restrito</h3>", unsafe_allow_html=True)
        st.markdown("---")
        
        with st.container(border=True):
            user = st.text_input("Usuário", placeholder="Digite seu usuário")
            pw = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("ENTRAR NO PORTAL 🚀", use_container_width=True, type="primary"):
                if user.lower() in ["caio", "vmb", "aluno"] and pw == "ancord2026":
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
    menu = st.sidebar.radio("📍 Navegação",["Home", "Evolução", "Sair"])
    
    # Controle do menu lateral
    if menu == "Sair":
        st.session_state.clear()
        st.rerun()
    elif menu == "Evolução" and st.session_state.page != "Evolução":
        st.session_state.page = "Evolução"
        st.rerun()
    elif menu == "Home" and st.session_state.page not in["Home", "Instrucoes", "Simulado", "Resultado"]:
        st.session_state.page = "Home"
        st.rerun()

    # --- HOME / DASHBOARD ---
    if st.session_state.page == "Home":
        st.title("🚀 Jornada de Certificação de Elite")
        st.markdown("Escolha o módulo que deseja treinar. Lembre-se: a consistência é a chave da aprovação.")
        st.divider()
        
        # Exibição dos Simulados
        for i, nome_sim in enumerate(SIMULADOS_ORDEM):
            with st.container(border=True):
                col_txt, col_btn = st.columns([4, 1])
                with col_txt:
                    st.markdown(f"#### 📚 {nome_sim}")
                    st.caption(f"**Módulos avaliados:** {', '.join(DIC_SIMULADOS[nome_sim])}")
                
                with col_btn:
                    st.markdown("<br>", unsafe_allow_html=True)
                    liberado = i <= st.session_state.simulado_atual_indice
                    if liberado:
                        if st.button("Acessar", key=f"btn_{i}", use_container_width=True, type="primary"):
                            st.session_state.simulado_nome = nome_sim
                            st.session_state.modulos_selecionados = DIC_SIMULADOS[nome_sim]
                            st.session_state.page = "Instrucoes"
                            st.rerun()
                    else:
                        st.button("🔒 Bloqueado", key=f"btn_{i}", disabled=True, use_container_width=True)

    # --- TELA DE INSTRUÇÕES (BOAS-VINDAS) ---
    elif st.session_state.page == "Instrucoes":
        st.title(f"📖 Regras: {st.session_state.simulado_nome}")
        
        st.warning("⚠️ **ATENÇÃO: LEIA AS REGRAS ANTES DE COMEÇAR!**")
        st.markdown("""
        ### Condições do Simulado:
        1. ⏱️ **Duração Limitada:** Você terá **EXATOS 30 MINUTOS** para concluir e enviar o teste.
        2. 🎯 **Formato da Prova:** O simulado possui **20 questões** escolhidas de forma aleatória da sua trilha.
        3. 🚫 **Sem Consultas:** Simule o ambiente real de prova. Feche abas de pesquisa e guarde seu material.
        4. 🤫 **Foco Total:** Não converse e procure um ambiente silencioso.
        5. 🔄 **Cuidado com a página:** **NÃO atualize ou recarregue a página (F5)** durante a prova. Se fizer isso, perderá seu progresso!
        """)
        
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Voltar aos Simulados", use_container_width=True):
                st.session_state.page = "Home"
                st.rerun()
        with col2:
            if st.button("ACEITO AS REGRAS - INICIAR AGORA 🚀", type="primary", use_container_width=True):
                # Filtra questões e garante exatamente 20
                questoes_filtradas = [q for q in BANCO_QUESTOES if q["modulo"] in st.session_state.modulos_selecionados]
                qtd_questoes = min(len(questoes_filtradas), 20) # Pega 20 ou o máximo que tiver
                
                if qtd_questoes > 0:
                    st.session_state.quiz_atual = random.sample(questoes_filtradas, qtd_questoes)
                    st.session_state.inicio_time = time.time()
                    st.session_state.page = "Simulado"
                    st.rerun()
                else:
                    st.error("Nenhuma questão cadastrada para os módulos deste simulado.")

    # --- EXECUÇÃO DO SIMULADO ---
    elif st.session_state.page == "Simulado" and st.session_state.quiz_atual:
        
        # --- CRONÔMETRO VISUAL EM TEMPO REAL (Javascript) ---
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
          
          document.getElementById("timer").innerHTML = "⏱️ Tempo Restante: " + minutes + ":" + seconds;
          
          if (distance < 0) {
            clearInterval(x);
            document.getElementById("timer").innerHTML = "🚨 TEMPO ESGOTADO!";
            document.getElementById("timer").style.color = "white";
            document.getElementById("timer").style.backgroundColor = "#D90429";
          }
        }, 1000);
        </script>
        <div id="timer" style="font-size:24px; font-weight:bold; color:#1D3557; text-align:center; padding:15px; border:3px solid #457B9D; border-radius:10px; background-color:#F1FAEE; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
            ⏱️ Calculando tempo...
        </div>
        """
        components.html(js_timer, height=85)
        
        st.title(f"📝 {st.session_state.simulado_nome}")
        st.info("Responda todas as questões e clique no botão verde 'Finalizar Simulado' no final da página.")
        
        # Usar st.form impede a tela de atualizar/piscar a cada clique na alternativa
        with st.form("form_simulado"):
            respostas_locais = {}
            
            for idx, q in enumerate(st.session_state.quiz_atual):
                st.markdown(f"### Questão {idx+1}")
                st.caption(f"**Módulo:** {q['modulo']}")
                st.write(q['pergunta'])
                
                opcoes =[f"{k}) {v}" for k, v in q.get("opcoes", {}).items()]
                # Usamos o indice do loop (idx) para evitar duplicidade de chaves
                respostas_locais[idx] = st.radio("Sua resposta:", opcoes, key=f"q_{idx}", index=None)
                st.divider()
            
            submitted = st.form_submit_button("🏁 Finalizar Simulado", use_container_width=True)
            
            if submitted:
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
        
        for idx, q in enumerate(st.session_state.quiz_atual):
            mod = q['modulo']
            if mod not in desempenho_modulos:
                desempenho_modulos[mod] = {"total": 0, "acertos": 0}
            
            desempenho_modulos[mod]["total"] += 1
            
            resp = st.session_state.respostas_usuario.get(idx)
            # Verifica se a letra (Ex: "A) ...") bate com a resposta_correta
            if resp and resp.startswith(q['resposta_correta']):
                acertos += 1
                desempenho_modulos[mod]["acertos"] += 1

        percentual = (acertos / total_questoes) * 100 if total_questoes > 0 else 0

        # Exibição do Tempo
        if estourou_tempo:
            st.error(f"⚠️ Você estourou o tempo limite de 30 minutos! Tempo total decorrido: **{minutos}m e {segundos}s**.")
        else:
            st.success(f"⏱️ Tempo total da prova: **{minutos}m e {segundos}s**.")

        # Indicadores em cima (Métricas)
        col1, col2, col3 = st.columns(3)
        col1.metric("Nota Final", f"{percentual:.1f}%", f"{acertos} de {total_questoes} corretas")
        col2.metric("Tempo Médio / Questão", f"{int(tempo_medio // 60)}m {int(tempo_medio % 60)}s")
        
        if percentual >= 70:
            col3.metric("Status", "APROVADO", "✅ Mandou bem!")
        else:
            col3.metric("Status", "REPROVADO", "❌ Precisa revisar")

        st.divider()

        # Diagnóstico de Onde Melhorar
        st.header("🎯 Diagnóstico por Módulo")
        st.markdown("Verifique abaixo os seus pontos fortes e as áreas onde você precisa focar seus estudos:")

        for mod, dados in desempenho_modulos.items():
            perc_mod = (dados['acertos'] / dados['total']) * 100
            
            if perc_mod < 70:
                st.error(f"📉 **{mod}**: {perc_mod:.0f}% ({dados['acertos']}/{dados['total']}) — **Você precisa melhorar urgentemente.**")
            elif perc_mod < 85:
                st.warning(f"🟡 **{mod}**: {perc_mod:.0f}% ({dados['acertos']}/{dados['total']}) — **Bom, mas dá pra lapidar os erros.**")
            else:
                st.success(f"🏆 **{mod}**: {perc_mod:.0f}% ({dados['acertos']}/{dados['total']}) — **Ponto forte! Excelente.**")

        st.divider()
        
        if st.button("🏠 Concluir e Voltar para a Home", use_container_width=True, type="primary"):
            # Lógica para liberar a próxima fase
            if percentual >= 70 and st.session_state.simulado_nome == SIMULADOS_ORDEM[st.session_state.simulado_atual_indice]:
                if st.session_state.simulado_atual_indice < len(SIMULADOS_ORDEM) - 1:
                    st.session_state.simulado_atual_indice += 1
            
            st.session_state.page = "Home"
            st.rerun()

    # --- TELA EVOLUÇÃO ---
    elif st.session_state.page == "Evolução":
        st.title("📈 O seu Desempenho Histórico")
        st.markdown("Acompanhe o seu progresso nos simulados para chegar pronto no dia da certificação!")
        
        # Gráfico estático demonstrativo (Substituir por banco de dados futuro)
        data = pd.DataFrame({
            "Simulado":["Sim 1", "Sim 2", "Sim 3", "Sim 4"], 
            "Nota (%)":[60, 75, 65, 85]
        })
        st.bar_chart(data.set_index("Simulado"), color="#457B9D")
        
        st.info("💡 Dica: O sistema de notas em breve será totalmente integrado à nossa nuvem de dados. Continue treinando!")
