import streamlit as st
import random
import pandas as pd
from datetime import datetime
import time
import os
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection

# --- QUESTÕES ---
try:
    from questoes import BANCO_QUESTOES
except ImportError:
    st.error("Arquivo 'questoes.py' não encontrado no repositório.")
    st.stop()

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="VMB - Simulado de Elite", layout="wide", page_icon="🎓")

# Módulos por simulado
DIC_SIMULADOS = {
    "Simulado 1 (Semanas 1 e 2)":["A Atividade do Assessor de Investimentos (AI)", "Lavagem de Dinheiro"],
    "Simulado 2 (Semanas 3 e 4)":["Mercado de Capitais", "Securitização de Recebíveis", "Derivativos"],
    "Simulado 3 (Semanas 5 e 6)":["Fundos de Investimentos", "Outros Fundos de Investimentos", "Clubes de Investimentos"],
    "Simulado 4 (Semanas 7 e 8)":["Mercado Financeiro", "Sistema Financeiro Nacional"],
    "Simulado 5 (Semanas 9 e 10)": ["Instituições e Intermediadores Financeiros", "Economia"],
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
        "resultado_salvo": False
    })

# --- FUNÇÕES ---
def mostrar_logo(tamanho_maximo=False):
    if os.path.exists("vmb_logo_fundo_preto.png"):
        if tamanho_maximo:
            st.image("vmb_logo_fundo_preto.png", use_container_width=True)
        else:
            st.image("vmb_logo_fundo_preto.png", width=200)
    else:
        st.markdown("<h1 style='text-align: center; color: #1D3557;'>🏛️ VMB INVEST</h1>", unsafe_allow_html=True)

# --- INTERFACE ---
if not st.session_state.logado:
    # --- TELA DE LOGIN ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        mostrar_logo(tamanho_maximo=True)
        st.markdown("<h3 style='text-align: center; color: #457B9D;'>Portal SDR - Acesso Restrito</h3>", unsafe_allow_html=True)
        st.markdown("---")
        
        with st.container(border=True):
            user = st.text_input("Usuário", placeholder="Digite seu usuário")
            pw = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("ENTRAR NO PORTAL 🚀", use_container_width=True, type="primary"):
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
                            
                            # =====================================================
                            # LÓGICA DE RECUPERAÇÃO DE PROGRESSO (O SEGREDO ESTÁ AQUI)
                            # =====================================================
                            try:
                                df_historico = conn.read(worksheet="Historico", ttl=0)
                                df_user_hist = df_historico[df_historico['Usuario'] == usuario_formatado]
                                
                                max_passed = -1
                                if not df_user_hist.empty:
                                    for _, row in df_user_hist.iterrows():
                                        # Converte a nota da planilha para número
                                        nota_str = str(row['Nota (%)']).replace(',', '.')
                                        nota = pd.to_numeric(nota_str, errors='coerce')
                                        
                                        # Se tirou 70 ou mais, considera o módulo como "passado"
                                        if pd.notna(nota) and nota >= 70.0:
                                            sim_name = row['Simulado']
                                            if sim_name in SIMULADOS_ORDEM:
                                                idx = SIMULADOS_ORDEM.index(sim_name)
                                                if idx > max_passed:
                                                    max_passed = idx
                                
                                # O índice atual será o maior que ele passou + 1 (Avança de fase)
                                prox_indice = max_passed + 1
                                # Não deixa ultrapassar o limite total de simulados
                                if prox_indice >= len(SIMULADOS_ORDEM):
                                    prox_indice = len(SIMULADOS_ORDEM) - 1
                                    
                                st.session_state.simulado_atual_indice = prox_indice
                                
                            except Exception:
                                # Se for o primeiro acesso ou não tiver aba de histórico ainda
                                st.session_state.simulado_atual_indice = 0
                            # =====================================================

                            st.session_state.page = "Home"
                            st.rerun()
                        else:
                            st.error("⚠️ Usuário ou senha incorretos. Acesso negado.")
                    except Exception as e:
                        st.error(f"⚠️ Erro ao conectar na planilha de usuários. Erro: {e}")

else:
    # --- BARRA LATERAL ---
    st.sidebar.title(f"🎓 Olá, {st.session_state.usuario}!")
    st.sidebar.markdown("---")
    menu = st.sidebar.radio("📍 Navegação",["Home", "Evolução", "Sair"])
    
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
        st.markdown("Escolha o módulo que deseja treinar. Seu progresso foi salvo e sincronizado na nuvem! ☁️")
        st.divider()
        
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

    # --- TELA DE INSTRUÇÕES ---
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
                questoes_filtradas =[q for q in BANCO_QUESTOES if q["modulo"] in st.session_state.modulos_selecionados]
                qtd_questoes = min(len(questoes_filtradas), 20)
                
                if qtd_questoes > 0:
                    st.session_state.quiz_atual = random.sample(questoes_filtradas, qtd_questoes)
                    st.session_state.inicio_time = time.time()
                    st.session_state.resultado_salvo = False
                    st.session_state.page = "Simulado"
                    st.rerun()
                else:
                    st.error("Nenhuma questão cadastrada para os módulos deste simulado.")

    # --- EXECUÇÃO DO SIMULADO ---
    elif st.session_state.page == "Simulado" and st.session_state.quiz_atual:
        
        # --- CRONÔMETRO VISUAL (Javascript) ---
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
        
        with st.form("form_simulado"):
            respostas_locais = {}
            
            for idx, q in enumerate(st.session_state.quiz_atual):
                st.markdown(f"### Questão {idx+1}")
                st.caption(f"**Módulo:** {q['modulo']}")
                st.write(q['pergunta'])
                
                opcoes =[f"{k}) {v}" for k, v in q.get("opcoes", {}).items()]
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
        
        tempo_total_segundos = st.session_state.fim_time - st.session_state.inicio_time
        minutos = int(tempo_total_segundos // 60)
        segundos = int(tempo_total_segundos % 60)
        estourou_tempo = tempo_total_segundos > 1800 
        
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

        # --- SALVAR PROGRESSO NO GOOGLE SHEETS ---
        if not st.session_state.resultado_salvo:
            with st.spinner("☁️ Salvando seu resultado no banco de dados..."):
                try:
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    df_historico = conn.read(worksheet="Historico", ttl=0)
                    
                    novo_registro = pd.DataFrame([{
                        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "Usuario": st.session_state.usuario,
                        "Simulado": st.session_state.simulado_nome,
                        "Nota (%)": round(percentual, 1),
                        "Tempo": f"{minutos}m {segundos}s"
                    }])
                    
                    df_atualizado = pd.concat([df_historico, novo_registro], ignore_index=True)
                    conn.update(worksheet="Historico", data=df_atualizado)
                    
                    st.session_state.resultado_salvo = True
                except Exception as e:
                    st.error(f"Erro ao salvar na planilha (Verifique se a aba 'Historico' existe). Erro: {e}")

        # Exibição do Tempo
        if estourou_tempo:
            st.error(f"⚠️ Você estourou o tempo limite de 30 minutos! Tempo total decorrido: **{minutos}m e {segundos}s**.")
        else:
            st.success(f"⏱️ Tempo total da prova: **{minutos}m e {segundos}s**.")

        col1, col2, col3 = st.columns(3)
        col1.metric("Nota Final", f"{percentual:.1f}%", f"{acertos} de {total_questoes} corretas")
        col2.metric("Tempo Médio / Questão", f"{int(tempo_medio // 60)}m {int(tempo_medio % 60)}s")
        
        if percentual >= 70:
            col3.metric("Status", "APROVADO", "✅ Mandou bem!")
        else:
            col3.metric("Status", "REPROVADO", "❌ Precisa revisar")

        st.divider()

        st.header("🎯 Diagnóstico por Módulo")
        st.markdown("Verifique abaixo os seus pontos fortes e as áreas onde você precisa focar seus estudos:")

        for mod, dados in desempenho_modulos.items():
            perc_mod = (dados['acertos'] / dados['total']) * 100
            if perc_mod < 70:
                st.error(f"📉 **{mod}**: {perc_mod:.0f}% ({dados['acertos']}/{dados['total']}) — **Você precisa melhorar.**")
            elif perc_mod < 85:
                st.warning(f"🟡 **{mod}**: {perc_mod:.0f}% ({dados['acertos']}/{dados['total']}) — **Bom, mas dá pra lapidar os erros.**")
            else:
                st.success(f"🏆 **{mod}**: {perc_mod:.0f}% ({dados['acertos']}/{dados['total']}) — **Ponto forte! Excelente.**")

        st.divider()

        st.header("📋 Correção Detalhada (Gabarito)")
        for idx, q in enumerate(st.session_state.quiz_atual):
            resp_usuario = st.session_state.respostas_usuario.get(idx)
            acertou = resp_usuario and resp_usuario.startswith(q['resposta_correta'])
            
            letra_correta = q['resposta_correta']
            texto_correto = q['opcoes'].get(letra_correta, "")

            with st.expander(f"Questão {idx+1} - {q['modulo']} {'(✅ Acertou)' if acertou else '(❌ Errou)'}"):
                st.write(f"**Pergunta:** {q['pergunta']}")
                
                if not acertou:
                    st.write(f"**Sua resposta:** {resp_usuario if resp_usuario else 'Não respondida'}")
                    st.success(f"**Resposta Correta:** {letra_correta}) {texto_correto}")
                else:
                    st.write(f"**Sua resposta:** {resp_usuario}")

                st.info(f"**Explicação / Dica:** {q.get('explicacao', 'Explicação não disponível para esta questão.')}")

        st.divider()
        if st.button("🏠 Concluir e Voltar para a Home", use_container_width=True, type="primary"):
            # Avanço local e temporário só pra não ter que sair (o banco de dados cobre se ele deslogar)
            if percentual >= 70 and st.session_state.simulado_nome == SIMULADOS_ORDEM[st.session_state.simulado_atual_indice]:
                if st.session_state.simulado_atual_indice < len(SIMULADOS_ORDEM) - 1:
                    st.session_state.simulado_atual_indice += 1
            
            st.session_state.page = "Home"
            st.rerun()

    # --- TELA EVOLUÇÃO ---
    elif st.session_state.page == "Evolução":
        st.title("📈 O seu Desempenho Histórico")
        st.markdown("Acompanhe o seu progresso nos simulados puxado diretamente do banco de dados oficial.")
        
        with st.spinner("Carregando dados da nuvem..."):
            try:
                conn = st.connection("gsheets", type=GSheetsConnection)
                df_historico_geral = conn.read(worksheet="Historico", ttl=0)
                
                df_user = df_historico_geral[df_historico_geral["Usuario"] == st.session_state.usuario]
                
                if not df_user.empty:
                    st.subheader("Gráfico de Notas (%)")
                    df_user = df_user.copy()
                    df_user.reset_index(drop=True, inplace=True)
                    df_user['Tentativa'] =[f"{i+1}ª T. ({row['Simulado']})" for i, row in df_user.iterrows()]
                    
                    st.line_chart(df_user.set_index("Tentativa")["Nota (%)"])
                    
                    st.subheader("Registros Detalhados")
                    st.dataframe(df_user.drop(columns=['Tentativa', 'Usuario']), use_container_width=True)
                else:
                    st.info("📊 Nenhum simulado finalizado ainda. Vá até a Home e faça seu primeiro simulado!")
            except Exception as e:
                st.error("⚠️ Ainda não há registros na planilha ou ela não está configurada corretamente.")
