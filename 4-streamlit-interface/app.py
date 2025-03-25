import os
import sys
import streamlit as st
import time
from pathlib import Path
import datetime

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Import research engine and utilities
from research_engine import run_research
from utils.display import display_results, render_markdown
from utils.markdown_export import format_markdown, save_markdown

# Page configuration
st.set_page_config(
    page_title="Tech Content Research Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title and description
st.title("🔍 Tech Content Research Assistant")
st.markdown("""
Generate comprehensive research on technology trends with AI assistance.
This tool leverages a team of specialized AI agents to research trends,
analyze technical details, structure content, and validate sources.
""")

# Sidebar with options
with st.sidebar:
    st.header("Research Options")
    model_option = st.selectbox(
        "Select Language Model",
        ["GPT-3.5 Turbo", "GPT-4 Turbo"],
        index=1
    )
    
    search_depth = st.slider(
        "Research Depth",
        min_value=1,
        max_value=5,
        value=3,
        help="Higher values generate more comprehensive research but take longer"
    )
    
    show_agent_work = st.checkbox("Show agent work in progress", value=True)
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This app uses CrewAI to orchestrate a team of specialized AI agents.")
    
# Main input area
tech_theme = st.text_input("Enter a technology theme to research:", placeholder="e.g., Quantum Computing, Edge AI, Web3")

# Research parameters
col1, col2 = st.columns(2)
with col1:
    research_focus = st.multiselect(
        "Research Focus Areas (Optional)",
        ["Current Trends", "Technical Details", "Industry Applications", "Future Developments", "Market Analysis"],
        default=["Current Trends", "Technical Details", "Future Developments"]
    )
with col2:
    target_audience = st.selectbox(
        "Target Audience",
        ["Technical Professionals", "Business Decision Makers", "General Audience", "Mixed"],
        index=3
    )

# Start research button
start_col, _ = st.columns([1, 3])
with start_col:
    start_research = st.button("Start Research", type="primary", use_container_width=True)

# Initialize session state to store results
if 'research_complete' not in st.session_state:
    st.session_state.research_complete = False
if 'research_results' not in st.session_state:
    st.session_state.research_results = None
if 'output_file' not in st.session_state:
    st.session_state.output_file = None
if 'progress' not in st.session_state:
    st.session_state.progress = 0
if 'current_task' not in st.session_state:
    st.session_state.current_task = ""

# Run research when button is clicked
if start_research and tech_theme:
    st.session_state.research_complete = False
    st.session_state.progress = 0
    
    # Create progress indicators
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Research phases
    phases = [
        "Researching Technology Trends",
        "Analyzing Technical Details",
        "Structuring Content Outline",
        "Validating Sources",
        "Finalizing Research Report"
    ]
    
    # Run research with progress updates
    status_text.text(f"Starting research on: {tech_theme}")
    
    # Callback for progress updates
    def update_progress(phase_idx, message):
        st.session_state.progress = (phase_idx + 1) * 20
        st.session_state.current_task = message
        progress_bar.progress(st.session_state.progress)
        status_text.text(message)
        if show_agent_work:
            st.text(message)
    
    try:
        # Run the research process
        result, output_file = run_research(
            tech_theme=tech_theme,
            model=model_option,
            research_focus=research_focus,
            target_audience=target_audience,
            depth=search_depth,
            progress_callback=update_progress
        )
        
        # Update session state with results
        st.session_state.research_complete = True
        st.session_state.research_results = result
        st.session_state.output_file = output_file
        
        # Complete the progress bar
        progress_bar.progress(100)
        status_text.text("Research complete! 🎉")
        
    except Exception as e:
        st.error(f"An error occurred during research: {str(e)}")
        st.session_state.research_complete = False

# Display results if research is complete
if st.session_state.research_complete and st.session_state.research_results:
    st.markdown("---")
    st.header("Research Results")
    
    # Create tabs for different result sections
    tabs = st.tabs(["Summary", "Trends", "Technical Analysis", "Content Outline", "Sources"])
    
    with tabs[0]:  # Summary
        st.markdown("## Executive Summary")
        if hasattr(st.session_state.research_results, 'executive_summary'):
            st.markdown(st.session_state.research_results.executive_summary)
        else:
            st.markdown(st.session_state.research_results.raw[:1000] + "...")
    
    # Display full results in other tabs
    display_results(st.session_state.research_results, tabs)
    
    # Download options
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="Download Full Report (Markdown)",
            data=open(st.session_state.output_file, 'r').read(),
            file_name=f"{tech_theme.replace(' ', '_').lower()}_research.md",
            mime="text/markdown"
        )
    
    with col2:
        st.download_button(
            label="Download as PDF",
            data=render_markdown(st.session_state.output_file),
            file_name=f"{tech_theme.replace(' ', '_').lower()}_research.pdf",
            mime="application/pdf"
        )

# Display a message if no research has been done yet
if not tech_theme and not st.session_state.research_complete:
    st.info("Enter a technology theme above and click 'Start Research' to begin.")
elif tech_theme and not st.session_state.research_complete and not start_research:
    st.info("Click 'Start Research' to analyze this technology theme.")