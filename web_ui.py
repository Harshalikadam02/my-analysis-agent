"""web_ui.py
Professional Streamlit entrypoint for the AI Data Analytics Agent.

This file is a thin wrapper around `analytics_core.OllamaAnalyticsAgent` and
defines a small Streamlit interface locally so the module imports cleanly.

Run with:
  streamlit run web_ui.py
"""

import os
import streamlit as st
from analytics_core import OllamaAnalyticsAgent


class StreamlitInterface:
    def __init__(self):
        self.agent = None
        self.data = None

    def run(self):
        st.set_page_config(page_title="AI Data Analytics Agent", page_icon="📊", layout="wide")

        # --- Dark/Red Theme Styling ---
        st.markdown(
            """
            <style>
            /* Main body and background */
            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                max-width: 100%;
            }
            
            /* Dark theme background */
            .stApp {
                background-color: #121212;
                color: #e5e5e5;
            }
            
            /* Header styling */
            .app-header {display:flex;align-items:center;gap:12px}
            .app-title {font-size:28px;font-weight:700;margin:0;color:#e5e5e5}
            .app-sub {color: #a0a0a0; margin:0}
            
            /* Sidebar styling */
            [data-testid="stSidebar"] {
                background-color: #1e1e1e;
                border-right: 1px solid rgba(255, 0, 0, 0.2);
            }
            
            [data-testid="stSidebar"] .stMarkdown {
                color: #e5e5e5;
            }
            
            [data-testid="stSidebar"] .stSelectbox > div > div {
                background-color: #2a2a2a;
                color: #e5e5e5;
                border: 1px solid rgba(255, 0, 0, 0.3);
            }
            
            [data-testid="stSidebar"] .stSelectbox > div > div:hover {
                border-color: rgba(255, 0, 0, 0.5);
            }
            
            /* Button styling */
            .stButton > button {
                background-color: #ff0000;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0.5rem 1rem;
                font-weight: 500;
                transition: all 0.2s ease;
            }
            
            .stButton > button:hover {
                background-color: #e60000;
                box-shadow: 0 2px 8px rgba(255, 0, 0, 0.3);
            }
            
            /* Tabs styling */
            .stTabs [data-baseweb="tab-list"] {
                background-color: #1e1e1e;
                border-bottom: 1px solid rgba(255, 0, 0, 0.1);
            }
            
            .stTabs [data-baseweb="tab"] {
                background-color: transparent;
                color: #a0a0a0;
                border-bottom: 2px solid transparent;
                padding: 0.75rem 1.5rem;
                font-weight: 500;
            }
            
            .stTabs [aria-selected="true"] {
                color: #e5e5e5;
                border-bottom-color: #ff0000;
                background-color: #2a2a2a;
            }
            
            .stTabs [data-baseweb="tab"]:hover {
                color: #e5e5e5;
                background-color: #2a2a2a;
            }
            
            /* Tab content styling */
            .stTabs [data-baseweb="tab-panel"] {
                background-color: #1e1e1e;
                border-radius: 8px;
                padding: 1.5rem;
                margin-top: 1rem;
                border: 1px solid rgba(255, 0, 0, 0.1);
                width: 100% !important;
            }
            
            /* File uploader styling */
            .stFileUploader {
                background-color: #1e1e1e;
                border: 2px dashed rgba(255, 0, 0, 0.3);
                border-radius: 8px;
                padding: 2rem;
                text-align: center;
            }
            
            .stFileUploader:hover {
                border-color: rgba(255, 0, 0, 0.5);
                background-color: #2a2a2a;
            }
            
            .stFileUploader > div > div {
                color: #e5e5e5;
            }
            
            /* Dataframe styling */
            .stDataFrame {
                background-color: #2a2a2a;
                border-radius: 8px;
                overflow: hidden;
                width: 100% !important;
            }
            
            .stDataFrame table {
                background-color: #2a2a2a;
                color: #e5e5e5;
            }
            
            .stDataFrame th {
                background-color: #1e1e1e;
                color: #e5e5e5;
                border-bottom: 1px solid rgba(255, 0, 0, 0.1);
            }
            
            .stDataFrame td {
                border-bottom: 1px solid rgba(255, 0, 0, 0.1);
            }
            
            .stDataFrame tr:hover {
                background-color: rgba(255, 0, 0, 0.1);
            }
            
            /* Text area and input styling */
            .stTextArea > div > div > textarea,
            .stTextInput > div > div > input {
                background-color: #2a2a2a;
                color: #e5e5e5;
                border: 1px solid rgba(255, 0, 0, 0.3);
                border-radius: 6px;
            }
            
            .stTextArea > div > div > textarea:focus,
            .stTextInput > div > div > input:focus {
                border-color: #ff0000;
                box-shadow: 0 0 0 2px rgba(255, 0, 0, 0.2);
            }
            
            /* Expander styling */
            .streamlit-expanderHeader {
                background-color: #1e1e1e;
                color: #e5e5e5;
                border: 1px solid rgba(255, 0, 0, 0.1);
                border-radius: 6px;
            }
            
            .streamlit-expanderContent {
                background-color: #2a2a2a;
                border: 1px solid rgba(255, 0, 0, 0.1);
                border-top: none;
                border-radius: 0 0 6px 6px;
                width: 100% !important;
            }
            
            /* Selectbox styling */
            .stSelectbox > div > div {
                background-color: #2a2a2a;
                color: #e5e5e5;
                border: 1px solid rgba(255, 0, 0, 0.3);
                border-radius: 6px;
            }
            
            .stSelectbox > div > div:hover {
                border-color: rgba(255, 0, 0, 0.5);
            }
            
            /* Markdown text styling */
            .stMarkdown {
                color: #e5e5e5;
            }
            
            .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
                color: #e5e5e5;
            }
            
            /* Spinner styling */
            .stSpinner {
                color: #ff0000;
            }
            
            /* Success/Error/Warning message styling */
            .stSuccess {
                background-color: rgba(0, 255, 0, 0.1);
                border: 1px solid rgba(0, 255, 0, 0.3);
                color: #00ff00;
            }
            
            .stError {
                background-color: rgba(255, 0, 0, 0.1);
                border: 1px solid rgba(255, 0, 0, 0.3);
                color: #ff6666;
            }
            
            .stWarning {
                background-color: rgba(255, 165, 0, 0.1);
                border: 1px solid rgba(255, 165, 0, 0.3);
                color: #ffb366;
            }
            
            .stInfo {
                background-color: rgba(0, 123, 255, 0.1);
                border: 1px solid rgba(0, 123, 255, 0.3);
                color: #66b3ff;
            }
            
            /* Caption styling */
            .stCaption {
                color: #a0a0a0;
            }
            
            /* Card styling for sections */
            .card {
                background: #1e1e1e;
                border-radius: 8px;
                padding: 18px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 0, 0, 0.1);
            }

            /* Ensure charts and json expand to full container width */
            .stPlotlyChart, .stMarkdown, .stJson, .stAlert {
                width: 100% !important;
            }
            .stPlotlyChart > div {
                width: 100% !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Header with dark theme styling
        st.markdown(
            """
            <div style="background-color: #000000; border-bottom: 1px solid rgba(255, 0, 0, 0.2); padding: 1rem 1.5rem; margin-bottom: 2rem;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="width: 32px; height: 32px; background-color: #ff0000; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                        <span style="color: white; font-size: 16px;">🤖</span>
                    </div>
                    <div>
                        <h1 style="font-size: 24px; font-weight: bold; margin: 0; color: #e5e5e5;">AI Data Analytics Agent</h1>
                        <p style="color: #a0a0a0; margin: 0; font-size: 14px;">Professional analytics powered by local Ollama models</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Sidebar configuration
        with st.sidebar:
            st.header("Configuration")
            st.markdown("Choose model and initialize the analytics agent.")
            try:
                available_models = __import__('ollama').list()
                models = []
                if isinstance(available_models, dict) and 'models' in available_models:
                    models = available_models['models']
                elif hasattr(available_models, 'models'):
                    models = available_models.models
                elif isinstance(available_models, list):
                    models = available_models
                model_names = []
                for model in models:
                    if hasattr(model, 'model'):
                        model_names.append(model.model)
                    elif isinstance(model, dict) and 'name' in model:
                        model_names.append(model['name'])
                    elif isinstance(model, str):
                        model_names.append(model)
                if model_names:
                    # Prefer llama3.2 if present
                    # allow override via env var
                    preferred_env = os.environ.get('OLLAMA_PREFERRED_MODEL')
                    preferred = None
                    if preferred_env:
                        for m in model_names:
                            if preferred_env in m:
                                preferred = m
                                break
                    if not preferred:
                        for m in model_names:
                            if 'llama3.2' in m or 'llama3' in m:
                                preferred = m
                                break
                    if preferred:
                        ordered = [preferred] + [x for x in model_names if x != preferred]
                    else:
                        ordered = model_names
                    selected_model = st.selectbox("Select Ollama Model", ordered)
                else:
                    selected_model = None
                    st.warning("No Ollama models found. Pull a model or start Ollama.")
            except Exception as e:
                selected_model = None
                st.error(f"Cannot connect to Ollama: {e}")
                st.info("Make sure Ollama is running: `ollama serve`")

            if st.button("Initialize Agent"):
                if selected_model:
                    st.session_state.agent = OllamaAnalyticsAgent(selected_model)
                    st.success(f"Agent initialized with {selected_model}")
                else:
                    st.error("Cannot initialize agent: No model selected or available.")
            # Auto-initialize if a preferred model is available and agent not yet initialized
            try:
                if 'agent' not in st.session_state and selected_model is not None:
                    # auto-init when a preferred model exists
                    st.session_state.agent = OllamaAnalyticsAgent(selected_model)
                    st.success(f"Agent auto-initialized with {selected_model}")
            except Exception:
                # don't crash UI when auto-init fails
                pass

        # Data upload section with dark theme styling
        st.markdown(
            """
            <div style="background-color: #1e1e1e; border-radius: 12px; border: 1px solid rgba(255, 0, 0, 0.1); padding: 1.5rem; margin-bottom: 2rem; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);">
                <h2 style="color: #e5e5e5; margin-bottom: 1rem; font-size: 20px; font-weight: 600;">📁 Upload Your Data</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
        uploaded_file = st.file_uploader("Choose a data file", type=['csv', 'xlsx', 'json'], help="Supports CSV, Excel, JSON files (Max 100MB)")
        agent = st.session_state.get('agent', None)
        data = st.session_state.get('data', None)

        if uploaded_file and agent:
            # Choose a writable upload directory. In production `./data` may be mounted read-only.
            upload_dir = os.environ.get("APP_UPLOAD_DIR")
            if not upload_dir:
                # Prefer a temp directory inside the container; fall back to ./data only if /tmp isn't usable.
                try:
                    upload_dir = "/tmp/app_uploads"
                    os.makedirs(upload_dir, exist_ok=True)
                except Exception:
                    # Last-resort fallback for local development when ./data is writable.
                    os.makedirs("data", exist_ok=True)
                    upload_dir = "data"
            else:
                os.makedirs(upload_dir, exist_ok=True)

            file_path = os.path.join(upload_dir, f"temp_{uploaded_file.name}")
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            with st.spinner("Loading and analyzing data..."):
                data = agent.load_and_analyze_data(file_path)
                if data is not None:
                    st.session_state.data = data
                    # Intentionally silent on successful load to avoid verbose UI messages
                else:
                    # show loading/parsing errors from the agent if present
                    load_err = agent.data_cache.get('load_error') if hasattr(agent, 'data_cache') else None
                    if load_err:
                        st.error(f"Failed to load file: {load_err}")
                    else:
                        st.error("Failed to load file: unknown error")

        if data is not None and agent is not None:
            # Data preview section with dark theme styling
            st.markdown(
                """
                <div style="background-color: #1e1e1e; border-radius: 12px; border: 1px solid rgba(255, 0, 0, 0.1); padding: 1.5rem; margin-bottom: 2rem; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);">
                    <h2 style="color: #e5e5e5; margin-bottom: 1rem; font-size: 20px; font-weight: 600;">📋 Data Preview</h2>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.dataframe(data.head())

            # Analysis section with dark theme styling
            st.markdown(
                """
                <div style="background-color: #1e1e1e; border-radius: 12px; border: 1px solid rgba(255, 0, 0, 0.1); padding: 1.5rem; margin-bottom: 2rem; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                        <h2 style="color: #e5e5e5; margin: 0; font-size: 20px; font-weight: 600;">Analysis Results</h2>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Main analysis tabs for a cleaner UX
            tabs = st.tabs(["Descriptive", "Predictive", "Cleaning", "Visualizations", "Custom"])

            with tabs[0]:
                st.markdown("### 📈 Descriptive Analytics")
                col1, col2 = st.columns([1, 4])
                result = None
                with col1:
                    if st.button("🚀 Run Analysis", key='desc'):
                        with st.spinner("Running descriptive analytics..."):
                            result = agent.descriptive_analytics(data)
                if result is not None:
                    self._display_result(result)

            with tabs[1]:
                st.markdown("### 🔮 Predictive Analytics")
                numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
                if numeric_cols:
                    target_col = st.selectbox("Select target column", numeric_cols, key='target')
                    col1, col2 = st.columns([1, 4])
                    result = None
                    with col1:
                        if st.button("🚀 Run Analysis", key='pred'):
                            with st.spinner("Running predictive analytics..."):
                                result = agent.predictive_analytics(data, target_col)
                    if result is not None:
                        self._display_result(result)
                else:
                    st.info("No numeric columns found for predictive analytics.")

            with tabs[2]:
                st.markdown("### 🧹 Data Cleaning Suggestions")
                col1, col2 = st.columns([1, 4])
                result = None
                with col1:
                    if st.button("🚀 Get Suggestions", key='clean'):
                        with st.spinner("Assessing data quality..."):
                            result = agent.data_cleaning_suggestions(data)
                if result is not None:
                    self._display_result(result)

            with tabs[3]:
                st.markdown("### 📊 Visualization Suggestions")
                col1, col2 = st.columns([1, 4])
                result = None
                with col1:
                    if st.button("🚀 Get Suggestions", key='viz'):
                        with st.spinner("Preparing visualizations..."):
                            result = agent.visualization_suggestions(data)
                if result is not None:
                    self._display_result(result)

            with tabs[4]:
                st.markdown("### 💬 Custom Analysis")
                custom_query = st.text_area("Ask a custom question about your data:", placeholder="e.g., What are the key trends in this dataset?")
                col1, col2 = st.columns([1, 4])
                result = None
                with col1:
                    if st.button("🚀 Analyze Query", key='custom'):
                        if not custom_query or not custom_query.strip():
                            st.warning("Please enter a query before clicking Analyze.")
                        else:
                            try:
                                with st.spinner("Running custom analysis..."):
                                    result = agent.custom_analysis(data, custom_query)
                            except Exception as e:
                                st.exception(e)
                if result is not None and not isinstance(result, Exception):
                    if isinstance(result.insights, str) and result.insights.startswith("[ERROR]"):
                        st.warning(f"Analysis completed with warning: {result.insights}")
                    self._display_result(result)

    def _display_result(self, result):
        # Results section with dark theme styling
        st.markdown(
            f"""
            <div style="background-color: #2a2a2a; border-radius: 8px; border: 1px solid rgba(255, 0, 0, 0.1); padding: 1.5rem; margin-bottom: 1rem;">
                <h3 style="color: #e5e5e5; margin-bottom: 1rem; font-size: 18px; font-weight: 600;">📊 {result.analysis_type.title()} Analysis Results</h3>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("### 🧠 AI Insights")
        # Render insights as Markdown so paragraphs, lists, and code blocks display correctly.
        try:
            insights_text = result.insights
            if isinstance(insights_text, (dict, list)):
                st.json(insights_text)
            elif isinstance(insights_text, str):
                # If the model returned raw HTML, allow safe rendering; otherwise standard Markdown.
                looks_like_html = insights_text.strip().startswith("<") and ">" in insights_text
                st.markdown(insights_text, unsafe_allow_html=looks_like_html)
            else:
                st.write(insights_text)
        except Exception:
            # Fallback to plain text if anything goes wrong
            st.write(result.insights)
        
        if result.visualizations:
            st.markdown("### 📈 Visualizations")
            for viz in result.visualizations:
                # Ensure charts use the full available width
                st.plotly_chart(viz['figure'], use_container_width=True)
                st.caption(viz.get('description', ''))
        
        with st.expander("📋 Raw Analysis Results"):
            st.json(result.results)


def main():
    interface = StreamlitInterface()
    interface.run()


if __name__ == '__main__':
    main()
