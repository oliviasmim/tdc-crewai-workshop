from crewai import Task
from textwrap import dedent

class TechContentResearchTasks:
    def trend_research_task(self, agent, tech_theme):
        return Task(description=dedent(f"""\
            Research the latest trends related to {tech_theme} in the technology industry.
            
            Your research should focus on identifying:
            1. Current major trends in {tech_theme}
            2. Emerging technologies that are gaining momentum
            3. Key statistics and data points that demonstrate trend importance
            4. Industry leaders and companies driving innovation in this space
            5. Recent developments (last 6-12 months) in this field
            
            Use search tools to gather comprehensive information from reputable sources
            like industry reports, tech publications, research papers, and company announcements.
            
            Your final response MUST include:
            - A comprehensive list of at least 5 significant trends in {tech_theme}
            - Supporting data and statistics for each trend
            - Timeline information showing how these trends have evolved
            - Links to original sources for all information provided
            
            Remember to focus on factual information that can be verified through credible sources.
            It's currently 2024, so ensure your information is up-to-date.
            """),
            agent=agent,
            expected_output="A comprehensive research report identifying at least 5 major trends in the specified technology theme, with supporting data, statistics, timeline information, and credible sources."
        )
    
    def technical_analysis_task(self, agent, tech_theme):
        return Task(description=dedent(f"""\
            Conduct a deep technical analysis of the trends identified in {tech_theme}.
            
            For each trend, provide:
            1. Detailed explanation of the underlying technologies
            2. Technical architecture or frameworks involved
            3. Current technical limitations and challenges
            4. Potential future developments and technical evolution
            5. Cross-industry applications and technical implications
            
            Your analysis should go beyond surface-level explanations to provide
            genuine technical insights that would be valuable to a technical audience.
            
            Your final response MUST include:
            - Technical deep dives for each major trend
            - Comparison of competing technical approaches where relevant
            - Analysis of technical feasibility and implementation challenges
            - References to technical documentation, whitepapers, or research papers
            - Expert opinions from technical leaders in the field
            
            Make sure your technical explanations are accurate and well-supported by
            credible technical sources.
            """),
            agent=agent,
            expected_output="A detailed technical analysis of each major trend, including underlying technologies, architectures, limitations, future developments, and cross-industry applications, supported by technical documentation and expert opinions."
        )
    
    def content_structure_task(self, agent):
        return Task(description=dedent("""\
            Create a comprehensive article outline based on the research findings and
            technical analysis provided.
            
            Your outline should:
            1. Organize information in a logical flow that builds understanding
            2. Include all major trends with appropriate section hierarchy
            3. Balance technical depth with accessibility for the target audience
            4. Allocate appropriate space to each topic based on importance and complexity
            5. Include placeholders for examples, case studies, and expert quotes
            
            Consider how to structure the article to maintain reader interest while
            covering complex technical topics thoroughly.
            
            Your final response MUST include:
            - A complete article outline with main sections and subsections
            - Brief descriptions of what each section will cover
            - Suggestions for visual elements (diagrams, charts, images) where appropriate
            - Estimated word count for each major section
            - Hook and conclusion recommendations
            
            The outline should serve as a comprehensive blueprint that a writer could
            follow to create a technically accurate, well-structured article.
            """),
            agent=agent,
            expected_output="A comprehensive article outline with hierarchical structure, section descriptions, visual element suggestions, word count estimates, and recommendations for hooks and conclusions."
        )
    
    def source_validation_task(self, agent):
        return Task(description=dedent("""\
            Review and validate all sources and references used in the research and
            technical analysis.
            
            For each source, evaluate:
            1. Credibility (author expertise, publication reputation)
            2. Recency (publication date, relevance to current state)
            3. Objectivity (potential bias, commercial interests)
            4. Technical accuracy (peer review, methodological soundness)
            5. Primary vs secondary nature of the source
            
            Identify any claims or information that require additional sources or
            verification, and suggest alternatives where sources are inadequate.
            
            Your final response MUST include:
            - A comprehensive list of validated sources with evaluation notes
            - Identification of any problematic sources with explanation
            - Suggestions for additional high-quality references where needed
            - A properly formatted bibliography in an appropriate citation style
            - Recommendations for expert quotes or interviews that could strengthen the article
            
            Ensure that all key claims are supported by multiple reliable sources
            where possible.
            """),
            agent=agent,
            expected_output="A validated bibliography with evaluation notes for each source, identification of problematic sources, suggestions for additional references, and recommendations for expert quotes or interviews."
        )
    
    def final_review_task(self, agent, tech_theme):
        return Task(description=dedent(f"""\
            Review and integrate all elements (research, technical analysis, outline, and sources)
            into a final comprehensive article blueprint on {tech_theme}.
            
            Your review should:
            1. Identify and resolve any inconsistencies between sections
            2. Ensure technical accuracy throughout all components
            3. Verify that all major trends are adequately covered
            4. Confirm that the structure serves the content effectively
            5. Validate that all claims are properly supported by credible sources
            
            Look for opportunities to strengthen the article by suggesting:
            - Additional connections between trends
            - Strategic use of examples or case studies
            - Areas where deeper technical explanation would be valuable
            - Potential unique insights or perspectives not covered elsewhere
            
            Your final response MUST include:
            - A complete executive summary of the article plan
            - An integrated outline with annotations for technical depth and source requirements
            - A curated list of the most important and reliable sources
            - Specific recommendations for making the article stand out from similar content
            - A publication readiness assessment with suggested next steps
            
            The final blueprint should provide everything needed to produce an exceptional
            technical article on {tech_theme} that would be valuable to both technical and
            business audiences interested in this technology space.
            """),
            agent=agent,
            expected_output="A complete article blueprint with executive summary, integrated outline, curated source list, content recommendations, and publication readiness assessment for the specified technology theme."
        )