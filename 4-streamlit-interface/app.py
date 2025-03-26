import sys
import streamlit as st
from pathlib import Path
import traceback

# WORKSHOP: Streamlit basics
# 1. Import streamlit as st - this is the conventional way to import
# 2. Run with: streamlit run app.py
# 3. The app will automatically reload when you save changes

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Import research engine and utilities
from research_engine import run_research

# WORKSHOP: Page Configuration
# Use set_page_config to customize the app appearance
# Must be called as the first Streamlit command in the script
# Arguments:
# - page_title: Title of the app
# - page_icon: Icon to display in the browser tab
# - layout: "centered" or "wide" (default)
# - initial_sidebar_state: "auto" (default), "expanded", or "collapsed"
# Example: st.set_page_config(page_title="My App", page_icon="🧊", layout="wide", initial_sidebar_state="expanded")

# Page configuration
st.set_page_config(
    page_title="Tech Content Research Assistant",
    page_icon="📊",  # You can use emojis or file paths
    layout="wide",   # Options: "centered" or "wide"
    initial_sidebar_state="expanded"  # Options: "expanded" or "collapsed"
)

# WORKSHOP: Basic Text Elements
# st.title() - Main application title
# st.markdown() - For text with markdown formatting

# App title and description
st.title("🔍 Tech Content Research Assistant")
st.markdown("""
Generate comprehensive research on technology trends with AI assistance.
This tool leverages a team of specialized AI agents to research trends,
analyze technical details, structure content, and validate sources.
""")

# Sidebar with options
# Use with st.sidebar: to add elements to the sidebar
# st.header() - Sidebar section header
# st.selectbox() - Dropdown selection
# st.slider() - Slider input
# st.checkbox() - Checkbox input
# st.markdown() - Text with markdown formatting

with st.sidebar:
    st.header("Research Options")
    model_option = st.selectbox(
        "Select Language Model (Decorative)",
        ["gpt-4o-mini"],
        index=0
    )
    
    search_depth = st.slider(
        "Research Depth (Decorative)",
        min_value=1,
        max_value=5,
        value=3,
        help="Higher values generate more comprehensive research but take longer"
    )
    
    show_agent_work = st.checkbox("Show agent work in progress", value=True)
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This app uses CrewAI to orchestrate a team of specialized AI agents.")
 
# IMPORTANT: Main content area    
# Main input area
tech_theme = st.text_input("Enter a technology theme to research:", placeholder="e.g., Quantum Computing, Edge AI, Web3")

# Research parameters
# Use st.columns() to create multiple columns
col1, col2 = st.columns(2)  # Creates two equal-width columns
with col1:
      # WORKSHOP: Multi-select Input
    research_focus = st.multiselect(
        "Research Focus Areas (Decorative)",
        ["Current Trends", "Technical Details", "Industry Applications", "Future Developments", "Market Analysis"],
        default=["Current Trends", "Technical Details", "Future Developments"]
    )
with col2:
    target_audience = st.selectbox(
        "Target Audience (Decorative)",
        ["Technical Professionals", "Business Decision Makers", "General Audience", "Mixed"],
        index=3
    )

# Start research button
start_col, _ = st.columns([1, 3])
with start_col:
    # type="primary" makes it stand out
    start_research = st.button("Start Research", type="primary", use_container_width=True)

# WORKSHOP: Session State
# Use session_state to persist data between reruns
# st.session_state is a dictionary that persists across reruns
# Think about it as a store for your app's state, like in React or Vue

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
if 'agent_messages' not in st.session_state:
    st.session_state.agent_messages = []
if 'current_phase' not in st.session_state:
    st.session_state.current_phase = 0

# Replace the research execution section with this updated version
if start_research and tech_theme:
    st.session_state.research_complete = False
    st.session_state.progress = 0
    st.session_state.agent_messages = []
    st.session_state.current_phase = 0
    
    # Create progress indicators
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Create containers for agent work display
    agent_work_container = st.empty()
    current_task_container = st.container()
    
    # Research phases with weights (total = 100)
    # So each phase contributes a certain percentage to the progress bar
    phases = [
        ("Researching Technology Trends", 25),
        ("Analyzing Technical Details", 25),
        ("Structuring Content Outline", 20),
        ("Validating Sources", 15),
        ("Finalizing Research Report", 15)
    ]
    
    def update_progress(phase_idx, message):
        """Update progress bar and agent work display"""
        # Calculate cumulative progress
        progress = sum([weight for _, weight in phases[:phase_idx]]) 
        phase_name, phase_weight = phases[phase_idx]
        
        # Update session state
        st.session_state.current_phase = phase_idx
        st.session_state.current_task = phase_name
        st.session_state.agent_messages.append(message)
        
        # Update progress bar based on phase weights
        progress_value = progress / 100.0
        progress_bar.progress(progress_value)
        
        # Update status
        status_text.text(f"Current Phase: {phase_name}")

    
    try:
        # Run the research process
        status_text.text(f"Starting research on: {tech_theme}")
        
        result, output_file = run_research(
            tech_theme=tech_theme,
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
        progress_bar.progress(1.0)
        status_text.text("Research complete! 🎉")
        
        # Show final agent work summary if enabled
        if show_agent_work:
            with current_task_container:
                st.success("Research process completed successfully!")
                st.markdown("### Final Agent Work Summary")
                st.markdown(f"Total messages: {len(st.session_state.agent_messages)}")
                with st.expander("View Full Agent Work Log"):
                    for idx, msg in enumerate(st.session_state.agent_messages, 1):
                        st.text(f"{idx}. {msg}")
        
    except Exception as e:
        st.error(f"An error occurred during research: {str(e)}")
        st.expander("Debug Details").write(traceback.format_exc())
        st.session_state.research_complete = False

# Display results if research is complete
if st.session_state.research_complete and st.session_state.research_results:
    st.markdown("---")
    st.header("Research Results")
    
    # Create tabs for different result sections    
    try:
        # Get full content for display
        content = st.session_state.research_results.raw
        st.markdown(content)
        
    except Exception as e:
        st.error(f"Error displaying results: {str(e)}")
        st.write(st.session_state.research_results.raw) 
    # Download options - only Markdown, no PDF
    st.markdown("---")
    
    try:
        with open(st.session_state.output_file, 'r') as f:
            markdown_data = f.read()
            
        st.download_button(
            label="Download Full Report (Markdown)",
            data=markdown_data,
            file_name=f"{tech_theme.replace(' ', '_').lower()}_research.md",
            mime="text/markdown"
        )
    except Exception as e:
        st.error(f"Error preparing download: {str(e)}")

# WORKSHOP: Info Messages
# Different message types: st.info(), st.warning(), st.error(), st.success()
# Use these to provide feedback to users based on app state
if not tech_theme and not st.session_state.research_complete:
    st.info("Enter a technology theme above and click 'Start Research' to begin.")
elif tech_theme and not st.session_state.research_complete and not start_research:
    st.info("Click 'Start Research' to analyze this technology theme.")