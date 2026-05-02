def salvar_resultado(nome, materias, acertos, total):
    try:
        # Puxamos a chave e removemos espaços extras que causam o erro de Padding
        p_key = st.secrets["connections"]["gsheets"]["private_key"].strip()
        
        # Se você colou com \n literais, isso resolve. 
        # Se colou com quebras de linha reais, não afeta.
        p_key = p_key.replace("\\n", "\n")

        conn = st.connection(
            "gsheets", 
            type=GSheetsConnection, 
            ttl=0, 
            private_key=p_key
        )
        
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
        st.success("✅ Desempenho registrado na planilha com sucesso!")
        
    except Exception as e:
        st.error(f"Erro ao salvar dados: {e}")
