import streamlit as st
import pandas as pd
from src.sec_fetcher import fetch_and_process_10k
from src.transcript_fetcher import fetch_and_analyze_transcript
from src.vector_store import get_store
from src.report_generator import ReportGenerator
from src.sec_agent import SECSpecialistAgent
from src.config import TICKER_CIK_MAP

st.set_page_config(page_title="Earnings Pilot", layout="wide")

st.title("🚀 Earnings Pilot: AI-Powered Executive Assistant")

# Sidebar
st.sidebar.header("Configuration")
ticker = st.sidebar.selectbox("Select Ticker", options=list(TICKER_CIK_MAP.keys()))

# Initialize store and agents
store = get_store()
report_gen = ReportGenerator()
sec_agent = SECSpecialistAgent()

# Create Tabs
tab1, tab2 = st.tabs(["🎙️ Earnings Prep", "📄 Filing Assistant"])

with tab1:
    st.header("Earnings Call Preparation")
    fetch_btn = st.button("Fetch Filings & Transcripts", key="fetch_prep")
    generate_btn = st.button("Generate Prep Report", key="gen_prep")

    if fetch_btn:
        with st.spinner(f"Fetching data for {ticker}..."):
            # 1. Fetch 10-K
            st.write("Fetching 10-K from SEC...")
            sections = fetch_and_process_10k(ticker)
            
            # 2. Fetch Transcript
            st.write("Fetching Earnings Transcript...")
            transcript_data = fetch_and_analyze_transcript(ticker)
            
            # 3. Store in ChromaDB
            st.write("Indexing documents in ChromaDB...")
            store.clear_all()
            
            for section_name, content in sections.get('sections', {}).items():
                if content:
                    store.add_documents([content], [{"source": "10-K", "section": section_name}])
                
            transcript_chunks = [transcript_data['full_content'][i:i+1000] for i in range(0, len(transcript_data['full_content']), 1000)]
            store.add_documents(transcript_chunks, [{"source": "Transcript"}] * len(transcript_chunks))
            
            st.session_state['ticker'] = ticker
            st.session_state['sentiment'] = transcript_data['sentiment']
            st.session_state['data_fetched'] = True
            st.success("Data fetched and indexed successfully!")

    if generate_btn:
        if not st.session_state.get('data_fetched'):
            st.error("Please fetch data first!")
        else:
            with st.spinner("Generating Report..."):
                report = report_gen.generate_report()
                st.session_state['report'] = report
                st.success("Report generated!")

    # Main Display for Prep Report
    if st.session_state.get('report'):
        report = st.session_state['report']
        sentiment = st.session_state.get('sentiment', {})
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.header("Executive Summary")
            st.markdown(report.get('summary', "N/A"))
            
        with col2:
            st.header("Key Metrics")
            st.metric("Sentiment", sentiment.get('sentiment', "N/A"))
            st.write(f"Positive Keywords: {sentiment.get('positive_count', 0)}")
            st.write(f"Negative Keywords: {sentiment.get('negative_count', 0)}")

        st.divider()
        st.header("Analyst Questions & Responses")
        st.markdown(report.get('questions', "N/A"))
        
        st.divider()
        st.header("Potential Contradictions")
        st.markdown(report.get('contradictions', "N/A"))

with tab2:
    st.header("SEC Filing Assistant")
    st.write("Draft and audit 10-K, 10-Q, and 8-K filings with legal-grade precision.")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        form_type = st.selectbox("Filing Type", ["10-K", "10-Q", "8-K"])
    with col_f2:
        mode = st.selectbox("Action", ["Audit Existing", "Draft New Section"])
    with col_f3:
        if mode == "Draft New Section":
            section = st.selectbox("Section", ["mda", "risk_factors", "business"])
        else:
            section = "Full Audit"

    exec_btn = st.button("Executive Run", use_container_width=True)

    if exec_btn:
        with st.spinner(f"Running SEC Specialist for {ticker} ({form_type})..."):
            try:
                if mode == "Audit Existing":
                    results = sec_agent.run_audit(ticker, form_type=form_type)
                else:
                    results = sec_agent.run_drafting(ticker, section=section, form_type=form_type)
                
                report_md = sec_agent.format_report(ticker, results)
                st.session_state['sec_report'] = report_md
                st.success("Filing analysis complete!")
            except Exception as e:
                st.error(f"Filing Assistant Error: {e}")

    if st.session_state.get('sec_report'):
        st.markdown(st.session_state['sec_report'])
        st.download_button(
            label="Download SEC Report",
            data=st.session_state['sec_report'],
            file_name=f"{ticker}_{form_type}_{mode.lower().replace(' ', '_')}.md",
            mime="text/markdown"
        )

# Footer
st.divider()
if st.session_state.get('data_fetched'):
    with st.expander("View Data Stats"):
        st.write(f"Ticker: {st.session_state.get('ticker')}")
        st.write(f"CIK: {TICKER_CIK_MAP.get(st.session_state.get('ticker'), 'Unknown')}")
else:
    st.info("Select a ticker and switch to a tab to get started.")
