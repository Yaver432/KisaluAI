import streamlit as st
import json
import os
from groq import Groq

api_key = st.secrets["GROQ_API_KEY"]

# --- CONFIGURAÇÃO VISUAL & MINIMALISTA ---
st.set_page_config(
    page_title="Kisalu — Intelligence & Jobs",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização sutil: visual bold, preto/cinzento/branco, sem aspeto genérico de IA
st.markdown("""
<style>
    /* Estilo global minimalista */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Remove decorações e torna títulos mais bold */
    h1, h2, h3 {
        letter-spacing: -0.03em;
        font-weight: 700;
        color: #111111;
    }
    
    /* Links minimalistas */
    a {
        color: #000000 !important;
        text-decoration: underline !important;
        font-weight: 500;
    }
    a:hover {
        color: #555555 !important;
    }
    
    /* Cartões compactos e sem excessos */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff;
        border-color: #e5e5e5;
        border-radius: 4px;
        transition: border-color 0.2s ease;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #111111;
    }
</style>
""", unsafe_allow_html=True)

# --- CLIENTE GROQ ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", None)

def get_groq_client():
    if not GROQ_API_KEY:
        st.sidebar.error("Chave GROQ_API_KEY não detetada nas variáveis de ambiente.")
        return None
    return Groq(api_key=GROQ_API_KEY)

# --- CARREGAR DADOS COM CACHE ---
@st.cache_data
def carregar_dados():
    json_path = "relatorio_rh_final.json"
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

dados_vagas = carregar_dados()

# --- BARRA LATERAL ---
st.sidebar.markdown("### **KISALU**")
st.sidebar.caption("Job Market Intelligence | Angola")
st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "Navegação", 
    ["Painel de Vagas", "Assistente de Consulta"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Filtros de Mercado**")
localizacao = st.sidebar.selectbox("Região", ["Todas", "Luanda", "Benguela", "Outra"])
ramo = st.sidebar.selectbox("Setor", ["Todos", "IT / Tecnologia", "Finanças", "Engenharia"])

if st.sidebar.button("Atualizar Base de Dados"):
    with st.spinner("A indexar novas vagas..."):
        # Executar rotina de scraping aqui (ex: main.rodar_fluxo())
        st.cache_data.clear()
        st.rerun()

# --- PÁGINA 1: PAINEL DE VAGAS ---
if pagina == "Painel de Vagas":
    st.title("Oportunidades em Aberto")
    st.caption("Visão estruturada de inteligência de recrutamento.")

    if not dados_vagas:
        st.info("Nenhuma oportunidade registada de momento. Atualize a base de dados.")
    else:
        for empresa, vagas in dados_vagas.items():
            st.markdown(f"#### {empresa.upper()}")
            
            # Grid de 3 colunas
            cols = st.columns(3)
            for i, vaga in enumerate(vagas):
                col = cols[i % 3]
                with col:
                    with st.container(border=True):
                        # Tipografia bold e neutra, sem emojis
                        st.markdown(f"**{vaga.get('cargo_limpo', 'Posição não informada')}**")
                        st.caption(f"Local: {vaga.get('localizacao', 'Angola')}")
                        st.markdown(
                            f"<p style='font-size: 0.88rem; color: #444; margin: 8px 0;'>"
                            f"{vaga.get('resumo', vaga.get('resumo_executivo', ''))}"
                            f"</p>", 
                            unsafe_allow_html=True
                        )
                        
                        link = vaga.get('link', '#')
                        st.markdown(f"[Aceder à vaga →]({link})")
            
            st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

# --- PÁGINA 2: CHATBOT GROQ ---
elif pagina == "Assistente de Consulta":
    st.title("Consulta de Mercado & Requisitos")
    st.caption("Pergunte diretamente sobre perfis, stacks tecnológicas e exigências.")

    client = get_groq_client()

    # Histórico de sessão
    if "mensagens" not in st.session_state:
        st.session_state.mensagens = []

    # Renderizar histórico existente
    for msg in st.session_state.mensagens:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input do Utilizador
    if prompt := st.chat_input("Ex: Quais são as vagas para tecnologia e quais os requisitos principais?"):
        # Registar pergunta
        st.session_state.mensagens.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Preparar chamada ao Groq
        with st.chat_message("assistant"):
            if not client:
                st.error("Configuração de API da Groq ausente.")
            else:
                # Contexto técnico puro, objetivo e sem rodeios de chatbot genérico
                contexto_vagas = json.dumps(dados_vagas, ensure_ascii=False)
                
                system_prompt = f"""
                És um analista sénior de Inteligência de Mercado de RH em Angola.
                O teu objetivo é analisar e responder sobre as vagas fornecidas na base de contexto.
                
                Diretrizes de resposta:
                - Responde de forma direta, clara, técnica e profissional.
                - Não uses emojis.
                - Não inventes vagas; fundamenta-te exclusivamente nos dados fornecidos abaixo, e em casos de necessidade podes pesquisar apenas em fontes confiaveis como o linkedin.
                - Se a vaga requer certos requisitos ou tecnologias, lista-os em formato de tópicos concisos.
                - Se a informação pedida não constar nos dados, diga que a informação nao consta nos dados, mas com base a pesquisas  de fontes confiaveis como o linkedin voce pode basear a sua resposta, tente sempre validar tambem sobre o status da vaga, em casos de duvida diga que nao tem como responder sobre pois nao consta nos dados fornecidos.

                Base de vagas disponíveis (JSON):
                {contexto_vagas}
                """

                # Estruturar histórico para a chamada
                mensagens_payload = [{"role": "system", "content": system_prompt}]
                for m in st.session_state.mensagens:
                    mensagens_payload.append({"role": m["role"], "content": m["content"]})

                # Streaming da resposta
                try:
                    stream = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=mensagens_payload,
                        temperature=0.2,
                        stream=True
                    )
                    
                    # Gerador para o st.write_stream
                    def gerar_resposta():
                        for chunk in stream:
                            if chunk.choices[0].delta.content:
                                yield chunk.choices[0].delta.content

                    resposta_completa = st.write_stream(gerar_resposta)
                    st.session_state.mensagens.append({"role": "assistant", "content": resposta_completa})
                    
                except Exception as e:
                    st.error(f"Erro ao consultar a API Groq: {e}")