import streamlit as st
import KisaluAI.Kisalu.Lixo_que_a_IA_GEROU_ME_ARREPENDO.services as services

# Configuração Base
st.set_page_config(
    page_title="Kisalu.IA | Inteligência em Recrutamento",
    page_icon="K",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- FOLHA DE ESTILOS PROFISSIONAL (CSS) -----------------
st.markdown("""
<style>
    /* Tipografia e Variáveis Base */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Identidade Visual no Topo da Sidebar */
    .brand-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 4px 0 16px 0;
    }
    .brand-avatar {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 42px;
        height: 42px;
        border-radius: 10px;
        background: linear-gradient(135deg, #1e3a8a, #3b82f6);
        color: #ffffff;
        font-size: 1.25rem;
        font-weight: 700;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2);
    }
    .brand-text-title {
        font-size: 1.15rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    .brand-text-sub {
        font-size: 0.75rem;
        color: #64748b;
        letter-spacing: 0.01em;
        text-transform: uppercase;
        font-weight: 500;
    }

    /* Transformação do Radio em Menu de Botões com Animação */
    div[data-testid="stRadio"] > div {
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    div[data-testid="stRadio"] label {
        background: rgba(148, 163, 184, 0.06);
        border: 1px solid rgba(148, 163, 184, 0.16);
        padding: 9px 14px !important;
        border-radius: 8px !important;
        cursor: pointer;
        width: 100%;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        align-items: center;
    }
    /* Oculta o círculo de seleção do rádio */
    div[data-testid="stRadio"] label > div:first-child {
        display: none !important;
    }
    /* Texto do menu */
    div[data-testid="stRadio"] label p {
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        margin: 0 !important;
    }
    /* Efeito de hover com animação de slide */
    div[data-testid="stRadio"] label:hover {
        background: rgba(59, 130, 246, 0.08);
        border-color: rgba(59, 130, 246, 0.35);
        transform: translateX(4px);
    }
    /* Estado Ativo / Selecionado */
    div[data-testid="stRadio"] label:has(input:checked) {
        background: #1e40af !important;
        border-color: #1e40af !important;
        box-shadow: 0 3px 8px rgba(30, 64, 175, 0.25);
    }
    div[data-testid="stRadio"] label:has(input:checked) p {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* Títulos de Secção na Sidebar */
    .section-header {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #64748b;
        font-weight: 700;
        margin: 18px 0 8px 0;
    }

    /* Cartão de Telemetria / Definições */
    .metric-card {
        background: rgba(148, 163, 184, 0.08);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 8px;
        padding: 10px 14px;
        margin-top: 6px;
    }
    .metric-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.82rem;
        padding: 4px 0;
    }
    .metric-label {
        color: #64748b;
    }
    .metric-value {
        font-weight: 600;
    }

    /* Cartão de Vagas no Painel */
    .job-card {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 290px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .company-avatar-small {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 44px;
        height: 44px;
        border-radius: 8px;
        background: rgba(30, 64, 175, 0.1);
        color: #1e40af;
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- ESTADOS DA SESSÃO -----------------
if "dados_vagas" not in st.session_state:
    st.session_state.dados_vagas = services.carregar_dados_locais()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ----------------- BARRA LATERAL (SIDEBAR) -----------------
with st.sidebar:
    # 1. Identidade e Logótipo ao Lado do Nome
    st.markdown("""
    <div class="brand-container">
        <div class="brand-avatar">K</div>
        <div>
            <div class="brand-text-title">Kisalu.IA</div>
            <div class="brand-text-sub">Mercado & Recrutamento</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Navegação em Formato Menu
    st.markdown('<div class="section-header">Módulos</div>', unsafe_allow_html=True)
    
    view_mode = st.radio(
        label="Navegação Principal",
        options=["Painel de Oportunidades", "Assistente de Consulta", "Publicações da Rede"],
        index=0,
        label_visibility="collapsed"
    )

    # 3. Filtros Estruturados
    st.markdown('<div class="section-header">Critérios de Busca</div>', unsafe_allow_html=True)

    filtro_localizacao = st.selectbox(
        "Território",
        ["Angola", "Luanda, Angola", "Benguela, Angola", "Huambo, Angola"],
        index=0
    )

    filtro_ramo = st.selectbox(
        "Setor de Atividade",
        list(services.TERMOS_POR_RAMO.keys()),
        index=0
    )

    filtro_limite = st.slider(
        "Amostragem por cargo",
        min_value=2,
        max_value=25,
        value=5,
        step=1
    )

    # 4. Painel de Estado & Telemetria
    st.markdown('<div class="section-header">Sistema & Métricas</div>', unsafe_allow_html=True)

    total_empresas = len(st.session_state.dados_vagas)
    total_vagas = sum(len(vagas) for vagas in st.session_state.dados_vagas.values())

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-row">
            <span class="metric-label">Vagas em Base</span>
            <span class="metric-value">{total_vagas}</span>
        </div>
        <div class="metric-row">
            <span class="metric-label">Entidades Mapeadas</span>
            <span class="metric-value">{total_empresas}</span>
        </div>
        <div class="metric-row">
            <span class="metric-label">Status do Agente</span>
            <span class="metric-value" style="color: #16a34a;">Ativo</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ----------------- VISTA 1: PAINEL DE OPORTUNIDADES -----------------
if view_mode == "Painel de Oportunidades":
    col_topo_esq, col_topo_dir = st.columns([3, 1])
    with col_topo_esq:
        st.subheader("Oportunidades de Emprego Consolidadas")
        st.caption(f"Filtro ativo: {filtro_ramo} | Território: {filtro_localizacao}")

    with col_topo_dir:
        st.write("")
        if st.button("Atualizar Dados (Scrape)", use_container_width=True, type="primary"):
            barra_progresso = st.progress(0, text="A sincronizar índices de emprego...")
            
            def atualizar_status(pct, texto):
                barra_progresso.progress(pct, text=texto)

            try:
                novos_dados = services.executar_pipeline_completo(
                    localizacao=filtro_localizacao,
                    ramo=filtro_ramo,
                    limite=filtro_limite,
                    progress_callback=atualizar_status
                )
                st.session_state.dados_vagas = novos_dados
                st.success("Dados atualizados com sucesso.")
                st.rerun()
            except Exception as e:
                st.error(f"Falha na sincronização: {e}")

    dados = st.session_state.dados_vagas

    if not dados:
        st.info("Nenhuma oportunidade registada de momento. Execute uma sincronização pelo botão acima.")
    else:
        # Aplanar lista para os cartões
        vagas_cards = []
        for emp, lista in dados.items():
            for v in lista:
                item = v.copy()
                item['empresa_nome'] = emp
                vagas_cards.append(item)

        colunas = st.columns(3)
        for idx, vaga in enumerate(vagas_cards):
            col = colunas[idx % 3]
            iniciais = "".join([p[0] for p in vaga['empresa_nome'].split()[:2]]).upper()

            with col:
                st.markdown(f"""
                <div class="job-card">
                    <div>
                        <div class="company-avatar-small">{iniciais if iniciais else 'RH'}</div>
                        <div style="font-size: 0.85rem; color: #64748b; font-weight: 600;">{vaga['empresa_nome']}</div>
                        <div style="font-size: 1.05rem; font-weight: 700; margin: 4px 0;">{vaga['cargo_limpo']}</div>
                        <div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 8px;">{vaga.get('localizacao', 'Angola')}</div>
                        <p style="font-size: 0.85rem; line-height: 1.45; color: var(--text-color);">
                            {vaga.get('resumo', 'Sem resumo disponível.')}
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("Requisitos Mapeados"):
                    reqs = vaga.get("requisitos", [])
                    if reqs:
                        for r in reqs:
                            st.markdown(f"- {r}")
                    else:
                        st.caption("Requisitos não detalhados na publicação original.")

                if vaga.get("link") and vaga["link"] != "#":
                    st.link_button("Aceder à Publicação Original", vaga["link"], use_container_width=True)
                
                st.write("")


# ----------------- VISTA 2: ASSISTENTE DE CONSULTA -----------------
elif view_mode == "Assistente de Consulta":
    if len(st.session_state.chat_history) == 0:
        st.markdown("""
        <div style="text-align: center; margin-top: 6vh; margin-bottom: 4vh;">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 68px; height: 68px; border-radius: 16px; background: rgba(30, 64, 175, 0.08); color: #1e40af; font-size: 1.8rem; font-weight: 700; margin-bottom: 12px;">K</div>
            <h2 style="font-weight: 700; margin-bottom: 6px;">Consultoria de Mercado Kisalu.IA</h2>
            <p style="color: #64748b; max-width: 540px; margin: 0 auto; font-size: 0.95rem;">
                Consulte informações específicas sobre as vagas em aberto, qualificações exigidas e tendências de contratação em território angolano.
            </p>
        </div>
        """, unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    pergunta = st.chat_input("Introduza a sua questão sobre vagas, empresas ou competências...")

    if pergunta:
        st.session_state.chat_history.append({"role": "user", "content": pergunta})
        with st.chat_message("user"):
            st.markdown(pergunta)

        with st.chat_message("assistant"):
            with st.spinner("A analisar registos..."):
                resposta = services.responder_duvida_rh(
                    pergunta=pergunta,
                    historico_chat=st.session_state.chat_history[:-1],
                    dados_vagas=st.session_state.dados_vagas
                )
                st.markdown(resposta)

        st.session_state.chat_history.append({"role": "assistant", "content": resposta})


# ----------------- VISTA 3: PUBLICAÇÕES DA REDE -----------------
# ----------------- VISTA 3: PUBLICAÇÕES DA REDE -----------------
elif view_mode == "Publicações da Rede":
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        st.subheader("Radar de Publicações & Anúncios Informais")
        st.caption("Oportunidades partilhadas em comunidades e feeds nos últimos 7 dias")
    with col_t2:
        st.write("")
        if st.button("Capturar Publicações (7 dias)", use_container_width=True, type="primary"):
            p_bar = st.progress(0.0, text="A iniciar monitorização...")
            try:
                novos_posts = services.executar_pipeline_publicacoes(
                    localizacao=filtro_localizacao,
                    progress_callback=lambda pct, txt: p_bar.progress(min(max(float(pct), 0.0), 1.0), text=txt)
                )
                st.session_state.publicacoes = novos_posts
                st.success("Publicações da rede atualizadas!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao capturar publicações: {e}")

    posts = services.carregar_publicacoes()

    if not posts:
        st.info("Nenhuma publicação informal registada. Clica no botão acima para o Agente capturar anúncios dos últimos 7 dias.")
    else:
        cols_posts = st.columns(2)
        for i, post in enumerate(posts):
            c = cols_posts[i % 2]
            with c:
                st.markdown(f"""
                <div class="job-card">
                    <div>
                        <div class="company-avatar-small">POST</div>
                        <div style="font-size: 0.85rem; color: #64748b; font-weight: 600;">{post.get('empresa', 'Não identificada')}</div>
                        <div style="font-size: 1.05rem; font-weight: 700; margin: 4px 0;">{post.get('cargo', 'Vaga')}</div>
                        <div style="font-size: 0.8rem; color: #2563eb; margin-bottom: 8px;">Contacto: {post.get('contacto', 'Consulte a publicação')}</div>
                        <p style="font-size: 0.85rem; line-height: 1.45;">
                            {post.get('resumo', '')}
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if post.get("link") and post["link"] != "#":
                    st.link_button("Ver Publicação Original", post["link"], use_container_width=True)
                st.write("")