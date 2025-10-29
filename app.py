"""
Interface Visual do Agente Pesquisador
Streamlit App com interface elegante e interativa
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import pandas as pd
from src.agent import ResearchAgent
import os

# Configuração da página
st.set_page_config(
    page_title="Agente Pesquisador IA",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🔬 Agente Pesquisador IA</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Pesquisa inteligente com validação de fontes e geração de relatórios</p>', unsafe_allow_html=True)

# Inicializa session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_result' not in st.session_state:
    st.session_state.current_result = None

# Sidebar
with st.sidebar:
    st.image("https://api.dicebear.com/7.x/shapes/svg?seed=research", width=200)
    st.markdown("### ⚙️ Configurações")

    # Verificar API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        st.success("✓ API Key configurada")
    else:
        st.error("✗ API Key não encontrada")
        api_key = st.text_input("Cole sua ANTHROPIC_API_KEY:", type="password")

    st.markdown("---")

    # Configurações do agente
    st.markdown("### 🎛️ Parâmetros")
    max_iterations = st.slider(
        "Máximo de iterações",
        min_value=1,
        max_value=3,
        value=1,
        help="Número máximo de ciclos de busca e validação"
    )

    use_tavily = st.checkbox(
        "Usar Tavily API (busca real)",
        value=False,
        help="Se desativado, usa simulação com LLM"
    )

    tavily_key = None
    if use_tavily:
        tavily_key = st.text_input(
            "Tavily API Key:",
            type="password",
            value=os.getenv("TAVILY_API_KEY", ""),
            help="Obtenha gratuitamente em https://tavily.com/"
        )
        if tavily_key:
            st.success("✓ Tavily API Key configurada")

    st.markdown("---")

    # Histórico
    st.markdown("### 📜 Histórico")
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history[-5:])):
            with st.expander(f"🔍 {item['query'][:30]}...", expanded=False):
                st.caption(f"⏰ {item['timestamp']}")
                st.caption(f"💯 Confiança: {item['confidence']:.0%}")
                if st.button(f"Recarregar", key=f"reload_{i}"):
                    st.session_state.current_result = item
                    st.rerun()
    else:
        st.info("Nenhuma pesquisa ainda")

    if st.button("🗑️ Limpar Histórico", use_container_width=True):
        st.session_state.history = []
        st.rerun()

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 💭 Faça sua pergunta")

    # Input de pesquisa
    query = st.text_area(
        "Digite sua pergunta de pesquisa:",
        height=100,
        placeholder="Ex: Quais são os principais benefícios e riscos da inteligência artificial generativa?",
        label_visibility="collapsed"
    )

    # Botão de pesquisa
    search_col, clear_col = st.columns([3, 1])
    with search_col:
        search_button = st.button("🚀 Pesquisar", type="primary", use_container_width=True)
    with clear_col:
        if st.button("🔄 Limpar", use_container_width=True):
            st.session_state.current_result = None
            st.rerun()

with col2:
    st.markdown("### 📊 Status")
    if st.session_state.current_result:
        result = st.session_state.current_result

        # Métrica de confiança com indicador visual
        confidence = result['confidence']
        if confidence > 0.75:
            confidence_emoji = "🟢"
        elif confidence > 0.5:
            confidence_emoji = "🟡"
        else:
            confidence_emoji = "🔴"

        st.metric(f"{confidence_emoji} Confiança", f"{confidence:.0%}")

        st.metric("Fontes Consultadas", result['search_results_count'])
        st.metric("Validações", result['validations_count'])
        st.metric("Iterações", result['iterations'])

        if result['conflicts_detected']:
            st.warning("⚠️ Conflitos detectados")
        else:
            st.success("✅ Sem conflitos")
    else:
        st.info("Aguardando pesquisa...")

# Executar pesquisa
if search_button and query:
    if not api_key:
        st.error("❌ Por favor, configure sua ANTHROPIC_API_KEY na sidebar")
    else:
        try:
            # Status container com feedback visual
            with st.status("🔬 Executando pesquisa...", expanded=True) as status_container:
                st.write("🎯 Inicializando agente...")

                # Inicializa o agente
                agent = ResearchAgent(
                    anthropic_api_key=api_key,
                    tavily_api_key=tavily_key if use_tavily else None,
                    max_iterations=max_iterations
                )

                st.write("✅ Agente inicializado")
                st.write("🔍 Executando pesquisa (isso pode levar alguns segundos)...")

                # Executa a pesquisa
                result = agent.research(query=query, max_iterations=max_iterations)

                st.write("✅ Pesquisa concluída!")

                # Exibe log de execução
                if 'full_state' in result and 'messages' in result['full_state']:
                    st.write("---")
                    st.write("📋 **Log de Execução:**")
                    for msg in result['full_state']['messages']:
                        st.text(msg)

                status_container.update(label="✅ Pesquisa concluída!", state="complete", expanded=False)

            # Salva no histórico
            result['query'] = query
            result['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.history.append(result)
            st.session_state.current_result = result

            st.rerun()

        except Exception as e:
            st.error(f"❌ Erro durante a pesquisa: {str(e)}")
            import traceback
            st.code(traceback.format_exc())

# Exibir resultados
if st.session_state.current_result:
    result = st.session_state.current_result

    st.markdown("---")
    st.markdown("## 📋 Resultados da Pesquisa")

    # Tabs para organizar informações
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📄 Relatório", "📚 Referências", "📊 Análise", "📋 Logs", "🔍 Detalhes"])

    with tab1:
        st.markdown("### Relatório Final")
        st.markdown(result['report'])

        # Botão de download
        st.download_button(
            label="⬇️ Baixar Relatório (Markdown)",
            data=result['report'],
            file_name=f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )

    with tab2:
        st.markdown("### Fontes Consultadas")

        if result.get('references'):
            for i, ref in enumerate(result['references'], 1):
                with st.expander(f"📌 Fonte {i}: {ref.get('title', 'Sem título')}", expanded=False):
                    st.write(f"**URL:** {ref.get('source', ref.get('url', 'N/A'))}")
                    if 'relevance_score' in ref:
                        st.progress(ref['relevance_score'], text=f"Relevância: {ref['relevance_score']:.0%}")
        else:
            st.info("Nenhuma referência disponível")

    with tab3:
        st.markdown("### Análise Visual")

        col1, col2 = st.columns(2)

        with col1:
            # Gráfico de confiança
            fig_confidence = go.Figure(go.Indicator(
                mode="gauge+number",
                value=result['confidence'] * 100,
                title={'text': "Nível de Confiança"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#667eea"},
                    'steps': [
                        {'range': [0, 50], 'color': "#ffebee"},
                        {'range': [50, 75], 'color': "#fff9c4"},
                        {'range': [75, 100], 'color': "#c8e6c9"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig_confidence.update_layout(height=300)
            st.plotly_chart(fig_confidence, use_container_width=True)

        with col2:
            # Gráfico de métricas
            metrics_data = {
                'Métrica': ['Fontes', 'Validações', 'Iterações'],
                'Valor': [
                    result['search_results_count'],
                    result['validations_count'],
                    result['iterations']
                ]
            }
            fig_metrics = px.bar(
                metrics_data,
                x='Métrica',
                y='Valor',
                title='Métricas da Pesquisa',
                color='Valor',
                color_continuous_scale='Purples'
            )
            fig_metrics.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig_metrics, use_container_width=True)

    with tab4:
        st.markdown("### 📋 Log de Execução")
        st.markdown("Acompanhe passo a passo o que o agente fez durante a pesquisa:")

        if 'full_state' in result and 'messages' in result['full_state']:
            messages = result['full_state']['messages']

            # Container com scroll para logs longos
            log_container = st.container()
            with log_container:
                # Agrupa mensagens por tipo de operação
                current_section = None

                for msg in messages:
                    # Detecta início de nova seção
                    if msg.startswith("🎯"):
                        current_section = "plan"
                        st.markdown(f"#### {msg}")
                    elif msg.startswith("🔍"):
                        current_section = "search"
                        st.markdown(f"#### {msg}")
                    elif msg.startswith("✅") and "VALIDANDO" in msg:
                        current_section = "validate"
                        st.markdown(f"#### {msg}")
                    elif msg.startswith("📝"):
                        current_section = "synthesize"
                        st.markdown(f"#### {msg}")
                    else:
                        # Mensagens de detalhe
                        if msg.strip().startswith("✓"):
                            st.success(msg.strip())
                        elif msg.strip().startswith("⚠️"):
                            st.warning(msg.strip())
                        elif msg.strip().startswith("→"):
                            st.info(msg.strip())
                        else:
                            st.text(msg)

            # Estatísticas do log
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Mensagens", len(messages))
            with col2:
                success_msgs = len([m for m in messages if "✓" in m])
                st.metric("Operações Bem-sucedidas", success_msgs)
            with col3:
                warning_msgs = len([m for m in messages if "⚠️" in m])
                st.metric("Avisos", warning_msgs)

            # Opção de download dos logs
            log_text = "\n".join(messages)
            st.download_button(
                label="⬇️ Baixar Logs",
                data=log_text,
                file_name=f"logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

        else:
            st.info("Nenhum log disponível para esta pesquisa")

    with tab5:
        st.markdown("### Informações Técnicas")

        # Estado completo
        with st.expander("🔧 Estado Completo (JSON)", expanded=False):
            if 'full_state' in result:
                # Remove campos muito grandes para melhor visualização
                display_state = {k: v for k, v in result['full_state'].items()
                               if k not in ['search_results', 'validations']}
                st.json(display_state)

        # Validações
        with st.expander("✅ Validações Realizadas", expanded=False):
            if 'full_state' in result and 'validations' in result['full_state']:
                validations = result['full_state']['validations']
                if validations:
                    for i, val in enumerate(validations, 1):
                        st.markdown(f"**Validação {i}:**")
                        st.write(f"- **Afirmação:** {val.claim}")
                        st.write(f"- **Validada:** {'✅ Sim' if val.is_validated else '❌ Não'}")
                        st.write(f"- **Confiança:** {val.confidence:.0%}")
                        st.write(f"- **Raciocínio:** {val.reasoning}")
                        st.markdown("---")
                else:
                    st.info("Nenhuma validação registrada")

        # Queries de busca
        with st.expander("🔍 Queries Geradas", expanded=False):
            if 'full_state' in result and 'search_queries' in result['full_state']:
                queries = result['full_state']['search_queries']
                for i, q in enumerate(queries, 1):
                    st.write(f"{i}. {q}")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("🤖 **Powered by:** LangGraph + Claude")
with col2:
    st.markdown("💻 **Desenvolvido com:** Streamlit")
with col3:
    st.markdown(f"📅 **Última atualização:** {datetime.now().strftime('%Y-%m-%d')}")
