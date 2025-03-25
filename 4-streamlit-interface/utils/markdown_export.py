import re
from pathlib import Path
import datetime

def format_markdown(content, tech_theme):
    """Format the raw content into a well-structured markdown document"""
    formatted = f"""# Tech Content Research: {tech_theme}

**Date:** {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

## Table of Contents

- [Executive Summary](#executive-summary)
- [Key Trends](#key-trends)
- [Technical Analysis](#technical-analysis)
- [Content Outline](#content-outline)
- [Sources & References](#sources-references)

"""
    
    # Try to extract and organize sections
    sections = {
        "executive_summary": "",
        "trends": "",
        "technical_analysis": "",
        "content_outline": "",
        "sources": ""
    }
    
    # Extract executive summary
    summary_pattern = r"(?:#{1,3}\s*(?:Executive|EXECUTIVE|Summary|SUMMARY).*?\n)([\s\S]+?)(?=#{1,3})"
    summary_match = re.search(summary_pattern, content)
    if summary_match:
        sections["executive_summary"] = summary_match.group(1).strip()
    else:
        # If no summary found, create a brief one from the beginning of the content
        sections["executive_summary"] = content[:500] + "..."
    
    # Extract other sections using similar pattern matching
    # ...similar to display.py extraction logic...
    
    # Combine all sections into the formatted markdown
    formatted += f"""
## Executive Summary

{sections["executive_summary"]}

## Key Trends

{sections["trends"] or "No trend information extracted."}

## Technical Analysis

{sections["technical_analysis"] or "No technical analysis extracted."}

## Content Outline

{sections["content_outline"] or "No content outline extracted."}

## Sources & References

{sections["sources"] or "No sources extracted."}
"""
    
    return formatted

def save_markdown(content, tech_theme, output_dir=None):
    """Save the formatted markdown content to a file"""
    if output_dir is None:
        output_dir = Path.cwd() / "reports"
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(exist_ok=True)
    
    # Generate filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_theme = tech_theme.replace(" ", "_").lower()
    output_file = Path(output_dir) / f"{sanitized_theme}_research_{timestamp}.md"
    
    # Write content to file
    with open(output_file, 'w') as f:
        f.write(content)
    
    return str(output_file)