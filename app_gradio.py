"""
Interface Visual do Agente Pesquisador - Gradio
Interface moderna e elegante com Gradio
"""
import gradio as gr
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import os
from src.agent import ResearchAgent

# Estado global para histórico
history = []

def get_api_status(api_key):
    """Verifica status da API key"""
    if api_key and api_key.strip():
        return "✓ API Key configurada"
    return "✗ API Key não configurada"

def create_confidence_gauge(confidence):
    """Cria gráfico de confiança tipo gauge"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence * 100,
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
    fig.update_layout(height=400)
    return fig

def create_metrics_bar(search_count, validations, iterations):
    """Cria gráfico de barras com métricas"""
    metrics_data = {
        'Métrica': ['Fontes', 'Validações', 'Iterações'],
        'Valor': [search_count, validations, iterations]
    }
    fig = px.bar(
        metrics_data,
        x='Métrica',
        y='Valor',
        title='Métricas da Pesquisa',
        color='Valor',
        color_continuous_scale='Purples'
    )
    fig.update_layout(height=400, showlegend=False)
    return fig

def format_references(references):
    """Formata referências para exibição"""
    if not references:
        return "Nenhuma referência disponível"

    formatted = "# Fontes Consultadas\n\n"
    for i, ref in enumerate(references, 1):
        title = ref.get('title', 'Sem título')
        url = ref.get('source', ref.get('url', 'N/A'))
        formatted += f"## 📌 Fonte {i}: {title}\n\n"
        formatted += f"**URL:** {url}\n\n"
        if 'relevance_score' in ref:
            score = ref['relevance_score']
            bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
            formatted += f"**Relevância:** {bar} {score:.0%}\n\n"
        formatted += "---\n\n"

    return formatted

def format_logs(result):
    """Formata logs de execução"""
    if 'full_state' not in result or 'messages' not in result['full_state']:
        return "Nenhum log disponível"

    messages = result['full_state']['messages']
    log_text = "# 📋 Log de Execução\n\n"
    log_text += f"**Total de Mensagens:** {len(messages)}\n\n"
    log_text += "---\n\n"

    for msg in messages:
        # Adiciona emojis e formatação
        if msg.startswith("🎯") or msg.startswith("🔍") or msg.startswith("✅") or msg.startswith("📝"):
            log_text += f"## {msg}\n\n"
        elif msg.strip().startswith("✓"):
            log_text += f"✅ {msg.strip()}\n\n"
        elif msg.strip().startswith("⚠️"):
            log_text += f"⚠️ {msg.strip()}\n\n"
        elif msg.strip().startswith("→"):
            log_text += f"ℹ️ {msg.strip()}\n\n"
        else:
            log_text += f"{msg}\n\n"

    return log_text

def format_details(result):
    """Formata detalhes técnicos"""
    details = "# 🔍 Detalhes Técnicos\n\n"

    # Estado completo
    details += "## 🔧 Estado Completo (JSON)\n\n"
    if 'full_state' in result:
        display_state = {k: v for k, v in result['full_state'].items()
                        if k not in ['search_results', 'validations', 'messages']}
        details += f"```json\n{json.dumps(display_state, indent=2, ensure_ascii=False)}\n```\n\n"

    # Validações
    details += "## ✅ Validações Realizadas\n\n"
    if 'full_state' in result and 'validations' in result['full_state']:
        validations = result['full_state']['validations']
        if validations:
            for i, val in enumerate(validations, 1):
                details += f"### Validação {i}\n\n"
                details += f"- **Afirmação:** {val.claim}\n"
                details += f"- **Validada:** {'✅ Sim' if val.is_validated else '❌ Não'}\n"
                details += f"- **Confiança:** {val.confidence:.0%}\n"
                details += f"- **Raciocínio:** {val.reasoning}\n\n"
        else:
            details += "Nenhuma validação registrada\n\n"

    # Queries
    details += "## 🔍 Queries Geradas\n\n"
    if 'full_state' in result and 'search_queries' in result['full_state']:
        queries = result['full_state']['search_queries']
        for i, q in enumerate(queries, 1):
            details += f"{i}. {q}\n"

    return details

def format_history():
    """Formata histórico de pesquisas"""
    if not history:
        return "Nenhuma pesquisa realizada ainda"

    hist_text = "# 📜 Histórico de Pesquisas\n\n"
    for i, item in enumerate(reversed(history[-5:]), 1):
        hist_text += f"## {i}. {item['query'][:50]}...\n\n"
        hist_text += f"- **Data:** {item['timestamp']}\n"
        hist_text += f"- **Confiança:** {item['confidence']:.0%}\n"
        hist_text += f"- **Fontes:** {item['search_results_count']}\n"
        hist_text += f"- **Iterações:** {item['iterations']}\n\n"
        hist_text += "---\n\n"

    return hist_text

def research_query(query, anthropic_key, max_iterations, use_tavily, tavily_key, progress=gr.Progress()):
    """Executa a pesquisa"""
    global history

    # Validações
    if not query or not query.strip():
        return (
            "❌ Por favor, digite uma pergunta",
            "", "", None, None, "",
            "Aguardando pesquisa...",
            "0%", "0", "0", "0", "Não iniciado"
        )

    if not anthropic_key or not anthropic_key.strip():
        return (
            "❌ Por favor, configure sua ANTHROPIC_API_KEY",
            "", "", None, None, "",
            "Aguardando pesquisa...",
            "0%", "0", "0", "0", "Não iniciado"
        )

    try:
        # Progress feedback
        progress(0, desc="🎯 Inicializando agente...")

        # Inicializa o agente
        agent = ResearchAgent(
            anthropic_api_key=anthropic_key,
            tavily_api_key=tavily_key if use_tavily else None,
            max_iterations=max_iterations
        )

        progress(0.2, desc="✅ Agente inicializado")
        progress(0.3, desc="🔍 Executando pesquisa...")

        # Executa a pesquisa
        result = agent.research(query=query, max_iterations=max_iterations)

        progress(0.9, desc="✅ Pesquisa concluída!")

        # Adiciona metadados
        result['query'] = query
        result['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Salva no histórico
        history.append(result)

        # Formata outputs
        report = result['report']
        references = format_references(result.get('references', []))
        logs = format_logs(result)
        details = format_details(result)

        # Gráficos
        confidence_fig = create_confidence_gauge(result['confidence'])
        metrics_fig = create_metrics_bar(
            result['search_results_count'],
            result['validations_count'],
            result['iterations']
        )

        # Status metrics
        confidence = result['confidence']
        if confidence > 0.75:
            confidence_emoji = "🟢"
        elif confidence > 0.5:
            confidence_emoji = "🟡"
        else:
            confidence_emoji = "🔴"

        status_text = f"{confidence_emoji} Confiança: {confidence:.0%}"
        confidence_str = f"{confidence:.0%}"
        sources_str = str(result['search_results_count'])
        validations_str = str(result['validations_count'])
        iterations_str = str(result['iterations'])
        conflicts_str = "⚠️ Conflitos detectados" if result['conflicts_detected'] else "✅ Sem conflitos"

        progress(1.0, desc="✅ Concluído!")

        return (
            report,
            references,
            logs,
            confidence_fig,
            metrics_fig,
            details,
            status_text,
            confidence_str,
            sources_str,
            validations_str,
            iterations_str,
            conflicts_str
        )

    except Exception as e:
        import traceback
        error_msg = f"❌ Erro durante a pesquisa:\n\n{str(e)}\n\n```\n{traceback.format_exc()}\n```"
        return (
            error_msg,
            "", "", None, None, "",
            "Erro na pesquisa",
            "0%", "0", "0", "0", "Erro"
        )

def clear_history():
    """Limpa o histórico"""
    global history
    history = []
    return "Histórico limpo com sucesso!"

# Tema customizado
theme = gr.themes.Soft(
    primary_hue="purple",
    secondary_hue="pink",
    font=gr.themes.GoogleFont("Inter"),
).set(
    button_primary_background_fill="*primary_500",
    button_primary_background_fill_hover="*primary_600",
)

# Interface Gradio
with gr.Blocks(theme=theme, title="Agente Pesquisador IA", css="""
    .gradio-container {
        max-width: 1400px !important;
    }
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
""") as demo:

    # Header
    gr.HTML("""
        <h1 class="main-header">🔬 Agente Pesquisador IA</h1>
        <p class="sub-header">Pesquisa inteligente com validação de fontes e geração de relatórios</p>
    """)

    with gr.Row():
        # Coluna principal (esquerda)
        with gr.Column(scale=3):
            # Input de pesquisa
            gr.Markdown("### 💭 Faça sua pergunta")
            query_input = gr.Textbox(
                placeholder="Ex: Quais são os principais benefícios e riscos da inteligência artificial generativa?",
                lines=3,
                label="Digite sua pergunta de pesquisa",
                show_label=False
            )

            with gr.Row():
                search_btn = gr.Button("🚀 Pesquisar", variant="primary", scale=3)
                clear_btn = gr.Button("🔄 Limpar", scale=1)

            # Tabs de resultados
            gr.Markdown("---")
            gr.Markdown("## 📋 Resultados da Pesquisa")

            with gr.Tabs():
                with gr.Tab("📄 Relatório"):
                    report_output = gr.Markdown(value="Aguardando pesquisa...")
                    download_report_btn = gr.DownloadButton(
                        "⬇️ Baixar Relatório (Markdown)",
                        visible=False
                    )

                with gr.Tab("📚 Referências"):
                    references_output = gr.Markdown(value="Aguardando pesquisa...")

                with gr.Tab("📊 Análise"):
                    with gr.Row():
                        confidence_plot = gr.Plot(label="Nível de Confiança")
                        metrics_plot = gr.Plot(label="Métricas da Pesquisa")

                with gr.Tab("📋 Logs"):
                    logs_output = gr.Markdown(value="Aguardando pesquisa...")

                with gr.Tab("🔍 Detalhes"):
                    details_output = gr.Markdown(value="Aguardando pesquisa...")

        # Sidebar (direita)
        with gr.Column(scale=1):
            gr.Image(
                "https://api.dicebear.com/7.x/shapes/svg?seed=research",
                show_label=False,
                show_download_button=False,
                container=False
            )

            gr.Markdown("### ⚙️ Configurações")

            # API Keys
            anthropic_key = gr.Textbox(
                label="ANTHROPIC_API_KEY",
                type="password",
                value=os.getenv("ANTHROPIC_API_KEY", ""),
                placeholder="sk-ant-..."
            )
            anthropic_status = gr.Textbox(
                value=get_api_status(os.getenv("ANTHROPIC_API_KEY")),
                label="Status",
                interactive=False,
                show_label=False
            )

            gr.Markdown("---")

            # Parâmetros
            gr.Markdown("### 🎛️ Parâmetros")
            max_iterations = gr.Slider(
                minimum=1,
                maximum=3,
                value=1,
                step=1,
                label="Máximo de iterações",
                info="Número máximo de ciclos de busca e validação"
            )

            use_tavily = gr.Checkbox(
                label="Usar Tavily API (busca real)",
                value=False,
                info="Se desativado, usa simulação com LLM"
            )

            tavily_key = gr.Textbox(
                label="Tavily API Key",
                type="password",
                value=os.getenv("TAVILY_API_KEY", ""),
                placeholder="tvly-...",
                visible=False,
                info="Obtenha gratuitamente em https://tavily.com/"
            )

            # Toggle visibility do campo Tavily
            use_tavily.change(
                fn=lambda x: gr.update(visible=x),
                inputs=[use_tavily],
                outputs=[tavily_key]
            )

            # Update status quando mudar API key
            anthropic_key.change(
                fn=get_api_status,
                inputs=[anthropic_key],
                outputs=[anthropic_status]
            )

            gr.Markdown("---")

            # Status
            gr.Markdown("### 📊 Status")
            status_display = gr.Textbox(
                value="Aguardando pesquisa...",
                label="Status Geral",
                interactive=False
            )

            confidence_display = gr.Textbox(
                value="0%",
                label="Confiança",
                interactive=False
            )

            sources_display = gr.Textbox(
                value="0",
                label="Fontes Consultadas",
                interactive=False
            )

            validations_display = gr.Textbox(
                value="0",
                label="Validações",
                interactive=False
            )

            iterations_display = gr.Textbox(
                value="0",
                label="Iterações",
                interactive=False
            )

            conflicts_display = gr.Textbox(
                value="Não iniciado",
                label="Conflitos",
                interactive=False
            )

            gr.Markdown("---")

            # Histórico
            gr.Markdown("### 📜 Histórico")
            history_display = gr.Markdown(value="Nenhuma pesquisa ainda")
            refresh_history_btn = gr.Button("🔄 Atualizar Histórico", size="sm")
            clear_history_btn = gr.Button("🗑️ Limpar Histórico", size="sm")

    # Footer
    gr.Markdown("---")
    with gr.Row():
        gr.Markdown("🤖 **Powered by:** LangGraph + Claude")
        gr.Markdown("💻 **Desenvolvido com:** Gradio")
        gr.Markdown(f"📅 **Última atualização:** {datetime.now().strftime('%Y-%m-%d')}")

    # Event handlers
    search_btn.click(
        fn=research_query,
        inputs=[query_input, anthropic_key, max_iterations, use_tavily, tavily_key],
        outputs=[
            report_output,
            references_output,
            logs_output,
            confidence_plot,
            metrics_plot,
            details_output,
            status_display,
            confidence_display,
            sources_display,
            validations_display,
            iterations_display,
            conflicts_display
        ]
    )

    clear_btn.click(
        fn=lambda: ("", "Aguardando pesquisa...", "Aguardando pesquisa...", "Aguardando pesquisa...",
                   None, None, "Aguardando pesquisa...", "Aguardando pesquisa...",
                   "0%", "0", "0", "0", "Não iniciado"),
        inputs=[],
        outputs=[
            query_input,
            report_output,
            references_output,
            logs_output,
            confidence_plot,
            metrics_plot,
            details_output,
            status_display,
            confidence_display,
            sources_display,
            validations_display,
            iterations_display,
            conflicts_display
        ]
    )

    refresh_history_btn.click(
        fn=format_history,
        inputs=[],
        outputs=[history_display]
    )

    clear_history_btn.click(
        fn=clear_history,
        inputs=[],
        outputs=[history_display]
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
