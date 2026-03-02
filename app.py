import streamlit as st
import pandas as pd
from src.sec_fetcher import fetch_and_process_10k
from src.transcript_fetcher import fetch_and_analyze_transcript
from src.vector_store import get_store
from src.report_generator import ReportGenerator
from src.config import TICKER_CIK_MAP

st.set_page_config(page_title="Earnings Pilot", layout="wide")

st.title("🚀 Earnings Pilot: AI-Powered Earnings Call Prep")

# Sidebar
st.sidebar.header("Configuration")
ticker = st.sidebar.selectbox("Select Ticker", options=list(TICKER_CIK_MAP.keys()))
fetch_btn = st.sidebar.button("Fetch Filings & Transcripts")
generate_btn = st.sidebar.button("Generate Report")

store = get_store()
report_gen = ReportGenerator()

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
        
        for section_name, chunks in sections.items():
            metadatas = [{"source": "10-K", "section": section_name}] * len(chunks)
            store.add_documents(chunks, metadatas)
            
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
        with st.spinner("Generating Report using Claude 3.5 Sonnet..."):
            report = report_gen.generate_report()
            st.session_state['report'] = report
            st.success("Report generated!")

# Main Display
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
    
    # Download Button
    full_markdown = f"""
# Earnings Pilot Report: {ticker}

## Executive Summary
{report.get('summary')}

## Key Metrics
- Sentiment: {sentiment.get('sentiment')}
- Positive Words: {sentiment.get('positive_count')}
- Negative Words: {sentiment.get('negative_count')}

## Analyst Questions
{report.get('questions')}

## Contradictions
{report.get('contradictions')}
"""
    st.download_button(
        label="Download Full Report (Markdown)",
        data=full_markdown,
        file_name=f"{ticker}_earnings_report.md",
        mime="text/markdown"
    )
else:
    st.info("Select a ticker and click 'Fetch Filings' to get started.")

# Show some raw data stats if available
if st.session_state.get('data_fetched'):
    with st.expander("View Data Stats"):
        st.write(f"Ticker: {st.session_state['ticker']}")
        st.write(f"Source CIK: {TICKER_CIK_MAP[st.session_state['ticker']]}")
