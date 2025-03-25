import streamlit as st
import re
import markdown
import base64
from pathlib import Path
import pdfkit

def extract_sections(content):
    """Extract main sections from the research results"""
    # This is a simplified implementation that would need to be adapted
    # based on the actual structure of your results
    sections = {
        "trends": "",
        "technical_analysis": "",
        "content_outline": "",
        "sources": ""
    }
    
    # Extract trends section (look for headers with "trend" in them)
    trends_pattern = r"(?:#{1,3}\s*(?:Trends|TRENDS|trends|Current|Emerging).*?\n)([\s\S]+?)(?=#{1,3})"
    trends_match = re.search(trends_pattern, content)
    if trends_match:
        sections["trends"] = trends_match.group(1).strip()
    
    # Extract technical analysis
    tech_pattern = r"(?:#{1,3}\s*(?:Technical|TECHNICAL|Analysis|ANALYSIS).*?\n)([\s\S]+?)(?=#{1,3})"
    tech_match = re.search(tech_pattern, content)
    if tech_match:
        sections["technical_analysis"] = tech_match.group(1).strip()
    
    # Extract content outline
    outline_pattern = r"(?:#{1,3}\s*(?:Outline|OUTLINE|Structure|STRUCTURE).*?\n)([\s\S]+?)(?=#{1,3})"
    outline_match = re.search(outline_pattern, content)
    if outline_match:
        sections["content_outline"] = outline_match.group(1).strip()
    
    # Extract sources
    sources_pattern = r"(?:#{1,3}\s*(?:Sources|SOURCES|References|REFERENCES|Bibliography).*?\n)([\s\S]+?)(?=#{1,3}|$)"
    sources_match = re.search(sources_pattern, content)
    if sources_match:
        sections["sources"] = sources_match.group(1).strip()
    
    return sections

def display_results(results, tabs):
    """Display the research results in the appropriate tabs"""
    content = results.raw
    sections = extract_sections(content)
    
    # Display trends
    with tabs[1]:
        st.markdown("## Key Trends")
        if sections["trends"]:
            st.markdown(sections["trends"])
        else:
            st.markdown(content)  # Fallback to full content
    
    # Display technical analysis
    with tabs[2]:
        st.markdown("## Technical Analysis")
        if sections["technical_analysis"]:
            st.markdown(sections["technical_analysis"])
        else:
            st.info("Technical analysis section not found in the results.")
    
    # Display content outline
    with tabs[3]:
        st.markdown("## Content Outline")
        if sections["content_outline"]:
            st.markdown(sections["content_outline"])
        else:
            st.info("Content outline section not found in the results.")
    
    # Display sources
    with tabs[4]:
        st.markdown("## Sources & References")
        if sections["sources"]:
            st.markdown(sections["sources"])
        else:
            st.info("Sources section not found in the results.")

def render_markdown(markdown_file):
    """Convert markdown to PDF"""
    try:
        # Read markdown content
        with open(markdown_file, 'r') as f:
            markdown_content = f.read()
        
        # Convert to HTML
        html_content = markdown.markdown(markdown_content)
        
        # Add some basic styling
        styled_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #3498db; margin-top: 30px; }}
                h3 {{ color: #2980b9; }}
                a {{ color: #3498db; }}
                pre {{ background-color: #f8f8f8; padding: 10px; border-radius: 5px; }}
                blockquote {{ border-left: 5px solid #e7e7e7; padding-left: 10px; margin-left: 20px; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Generate PDF using pdfkit
        pdf_bytes = pdfkit.from_string(styled_html, False)
        return pdf_bytes
        
    except Exception as e:
        st.error(f"Error converting to PDF: {str(e)}")
        return None