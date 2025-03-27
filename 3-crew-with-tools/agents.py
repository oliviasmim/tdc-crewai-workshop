import os
from textwrap import dedent
from crewai import Agent
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool, WebsiteSearchTool

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

# Tools
search_tool = SerperDevTool()
web_search_tool = WebsiteSearchTool()

class TechContentCreator:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini")

    def trend_researcher_agent(self):
        return Agent(
            role="Tech Trend Researcher",
            goal=dedent("""\
                Research and identify the most current and significant technology trends 
                related to the given theme, providing comprehensive data, statistics,
                and emerging patterns."""),
            backstory=dedent("""\
                As a Tech Trend Researcher with a knack for spotting emerging technologies
                before they go mainstream, you have an exceptional ability to sift through
                vast amounts of information and identify meaningful patterns. Your research
                has been cited in major tech publications, and you pride yourself on finding
                the most reliable and cutting-edge information."""),
            tools=[
                search_tool,
                web_search_tool
            ],
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )

    def technical_expert_agent(self):
        return Agent(
            role="Technical Domain Expert",
            goal=dedent("""\
                Provide deep technical analysis and explanations of identified trends,
                elaborating on their underlying technologies, potential applications,
                and technical implications."""),
            backstory=dedent("""\
                You are a respected technical expert with extensive experience across
                multiple technology domains. With a background in both academic research
                and industry implementation, you excel at breaking down complex technical
                concepts into understandable explanations while maintaining accuracy.
                You're known for your ability to predict how current technologies will
                evolve based on technical fundamentals."""),
            tools=[
                search_tool,
                web_search_tool
            ],
            llm=self.llm,
            verbose=True
        )

    def content_structure_specialist_agent(self):
        return Agent(
            role="Content Structure Specialist",
            goal=dedent("""\
                Create comprehensive, well-organized article outlines based on research
                findings, ensuring logical flow, proper hierarchy of information, and
                coverage of all key aspects of the technology trend."""),
            backstory=dedent("""\
                As a Content Structure Specialist with experience in technical journalism,
                you've mastered the art of organizing complex information into readable,
                engaging formats. Your article structures have been praised for their
                clarity, logical progression, and ability to maintain reader interest
                even when covering highly technical subjects. You understand how to balance
                depth with readability."""),
            tools=[
                search_tool
            ],
            llm=self.llm,
            verbose=True
        )

    def source_validator_agent(self):
        return Agent(
            role="Source Validation Expert",
            goal=dedent("""\
                Validate and evaluate the credibility, relevance, and timeliness of sources
                and references, ensuring that all information is backed by reputable evidence
                and properly cited."""),
            backstory=dedent("""\
                With a background in academic research and fact-checking for major tech
                publications, you've developed a rigorous methodology for evaluating
                information sources. You can quickly distinguish between primary research,
                industry analysis, and speculative content. Your attention to detail ensures
                that all claims are properly supported with credible, recent, and relevant
                sources."""),
            tools=[
                search_tool,
                web_search_tool
            ],
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )

    def editor_in_chief_agent(self):
        return Agent(
            role="Editor-in-Chief",
            goal=dedent("""\
                Review and integrate all research, technical analysis, and structural elements
                to ensure the final article outline is comprehensive, technically accurate,
                well-structured, and built on solid references."""),
            backstory=dedent("""\
                As the Editor-in-Chief of respected tech publications, you have overseen the
                development of thousands of technical articles. Your expertise lies in
                synthesizing diverse inputs into cohesive, compelling narratives without
                sacrificing technical accuracy. You excel at identifying gaps in research,
                logical inconsistencies, and opportunities to strengthen content through
                additional context or sources."""),
            llm=self.llm,
            verbose=True
        )