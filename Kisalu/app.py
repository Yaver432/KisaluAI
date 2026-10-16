import streamlit as st
import pandas as pd
import json
import os

# Configuração da página (Tema e Layout)
st.set_page_config(
    page_title="Kisalu.IA - Agente de Vagas",
    page_icon="🤖",
    layout="wide"
)

# --- BARRA LATERAL (Filtros e Navegação) ---
st.sidebar.title("Kisalu.IA")
pagina = st.sidebar.radio("Navegação", ["Overview / Painel de Vagas", "ChatBot Inteligente"])

st.sidebar.markdown("---")
st.sidebar.subheader("Filtros de Pesquisa")
localizacao = st.sidebar.selectbox("Localização", ["Angola", "Luanda", "Benguela", "Outra"])
ramo = st.sidebar.selectbox("Ramo", ["IT / Tecnologia", "Finanças", "Engenharia", "Geral"])
resultados_desejados = st.sidebar.slider("Resultados Desejados por Site", 5, 20, 10)

if st.sidebar.button("🔄 Reload (Executar Scraping)"):
    with st.spinner("A executar o scraper e a processar com a IA..."):
        # Aqui chamas o teu script de scraping e processamento (ex: import main; main.rodar_fluxo())
        st.success("Dados atualizados com sucesso!")

# --- CARREGAR DADOS PROCESSADOS ---
json_path = "relatorio_rh_final.json"
dados_vagas = {}
if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        dados_vagas = json.load(f)

# --- PÁGINA 1: OVERVIEW / PAINEL DE VAGAS (Em formato de Cartões) ---
if pagina == "Overview / Painel de Vagas":
    st.title("Painel de Vagas - Angola")
    st.markdown("Aqui encontras todas as oportunidades agregadas e tratadas pela IA para os RHs.")

    if not dados_vagas:
        st.warning("Nenhum dado encontrado. Clica em 'Reload (Executar Scraping)' na barra lateral para recolher vagas.")
    else:
        # Iterar pelas empresas do JSON
        for empresa, vagas in dados_vagas.items():
            st.markdown(f"### 🏢 {empresa.upper()}")
            
            # Criar colunas para os cartões (estilo grid do teu wireframe)
            cols = st.columns(3)
            for i, vaga in enumerate(vagas):
                col = cols[i % 3]
                with col:
                    with st.container(border=True):
                        st.markdown(f"**Cargo:** {vaga['cargo_limpo']}")
                        st.markdown(f"📍 **Local:** {vaga['localizacao']}")
                        st.markdown(f"📝 {vaga['resumo']}")
                        st.markdown(f"🔗 [Aceder à Vaga]({vaga['link']})")
            st.markdown("---")

# --- PÁGINA 2: CHATBOT INTERACTIVO ---
elif pagina == "ChatBot Inteligente":
    st.title("Assistente de RH - Kisalu.IA")
    st.markdown("Tira dúvidas sobre as vagas disponíveis na região, requisitos ou tecnologias exigidas.")

    # Histórico de mensagens do chat no Streamlit
    if "mensagens" not in st.session_state:
        st.session_state.mensagens = []

    for msg in st.session_state.mensagens:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input do chat na parte inferior (igualzinho ao teu wireframe)
    if prompt := st.chat_input("Pergunte sobre as vagas disponíveis (ex: 'Quais vagas exigem suporte técnico?')..."):
        st.session_state.mensagens.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Resposta simulada da IA com base no JSON carregado
        with st.chat_message("assistant"):
            resposta_ia = f"Com base nas vagas atuais em Angola, encontrei várias opções relevantes no teu relatório. (Aqui o Gemini/Groq responde à tua pergunta usando o contexto das vagas)."
            st.markdown(resposta_ia)
            st.session_state.mensagens.append({"role": "assistant", "content": resposta_ia})