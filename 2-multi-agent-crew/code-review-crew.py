import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


from utils.disable_telemetry import disable_telemetry
disable_telemetry()

# Import required libraries
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
import datetime

# Load environment variables
load_dotenv()

# Set OpenAI API key and model
os.environ['OPENAI_MODEL_NAME'] = "gpt-3.5-turbo"
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

# Define the agents
# 1. CodeQualityAgent - Analisa a qualidade do código
code_quality_agent = Agent(
    role="Especialista em Qualidade de Código",
    goal="Analisar o código para identificar problemas de qualidade e sugerir melhorias",
    backstory="""Você é um desenvolvedor sênior com vasta experiência em análise de código.
    Sua expertise está em identificar código duplicado, funções muito longas, 
    complexidade excessiva, e outros problemas que afetam a qualidade e manutenibilidade.
    Você é conhecido por fornecer sugestões práticas e objetivas para melhorar a qualidade do código.
    """,
    allow_delegation=False,
    verbose=True,
)

# 2. SecurityAgent - Analisa vulnerabilidades de segurança
security_agent = Agent(
    role="Especialista em Segurança",
    goal="Identificar vulnerabilidades de segurança no código e sugerir correções",
    backstory="""Você é um especialista em segurança de aplicações com experiência em 
    identificar vulnerabilidades como injeção, XSS, problemas de autenticação, 
    e outras falhas de segurança comuns.
    Sua análise é minuciosa e você fornece recomendações específicas 
    sobre como corrigir problemas de segurança encontrados.
    """,
    allow_delegation=False,
    verbose=True,
)

# 3. StyleAgent - Analisa aderência a padrões de código
style_agent = Agent(
    role="Especialista em Padrões de Código",
    goal="Verificar a aderência do código aos padrões de estilo e melhores práticas",
    backstory="""Você é um especialista em estilo de código e convenções de programação.
    Sua atenção a detalhes permite identificar inconsistências na formatação, nomenclatura, 
    e organização do código. Você é apaixonado por código limpo e bem estruturado, seguindo 
    as melhores práticas da indústria e padrões específicos da linguagem.
    """,
    allow_delegation=False,
    verbose=True,
)

# Define the tasks
quality_review_task = Task(
    description="""Analise o arquivo sample_code.tsx e identifique:
    1. Código duplicado ou redundante
    2. Funções ou métodos que são muito longos ou complexos
    3. Problemas de abstração ou encapsulamento
    4. Oportunidades para melhorar a eficiência do código
    5. Problemas com a estrutura geral do código
    
    Forneça um relatório detalhado com exemplos específicos do código e sugestões
    claras para melhorias, priorizadas por impacto. Para cada sugestão, explique o
    problema e como a solução proposta melhora a manutenibilidade, legibilidade
    ou desempenho do código.
    """,
    expected_output="Um relatório detalhado de problemas de qualidade de código e recomendações específicas de melhorias",
    agent=code_quality_agent,
)

security_review_task = Task(
    description="""Analise o arquivo sample_code.tsx para vulnerabilidades de segurança, incluindo:
    1. Vulnerabilidades a ataques XSS ou injeção
    2. Vazamento de informações sensíveis
    3. Problemas de autenticação ou autorização
    4. Validação inadequada de entrada
    5. Outras vulnerabilidades comuns em aplicações web
    
    Forneça um relatório de segurança que priorize as vulnerabilidades por gravidade,
    explicando cada problema encontrado, seu potencial impacto e recomendações 
    específicas sobre como corrigir cada vulnerabilidade.
    """,
    expected_output="Um relatório de segurança com vulnerabilidades identificadas, classificadas por severidade, e recomendações de correção",
    agent=security_agent,
)

style_review_task = Task(
    description="""Analise o arquivo sample_code.tsx para verificar a aderência a padrões de estilo:
    1. Consistência na nomenclatura de variáveis, funções e componentes
    2. Formatação adequada (indentação, espaçamento, etc.)
    3. Organização de imports e dependências
    4. Comentários adequados e documentação
    5. Aderência a padrões e melhores práticas específicas do React/TypeScript
    
    Forneça um relatório detalhado sobre problemas encontrados, explicando por
    que são considerados desvios de boas práticas e como corrigi-los para melhorar
    a legibilidade e manutenibilidade do código.
    """,
    expected_output="Um relatório sobre problemas de estilo e padronização, com recomendações para alinhar o código às melhores práticas",
    agent=style_agent,
)

# Create the crew
review_crew = Crew(
    agents=[code_quality_agent, security_agent, style_agent],
    tasks=[quality_review_task, security_review_task, style_review_task],
    verbose=True,
)

def main():
    # Read the content of the sample_code.tsx file
    try:
        with open('sample_code.tsx', 'r') as file:
            code_content = file.read()
    except FileNotFoundError:
        print("Error: sample_code.tsx file not found in the current directory.")
        return
    
    print("Iniciando análise de código com a equipe de revisão...")
    
    # Run the crew with the code content as input
    result = review_crew.kickoff(inputs={"code": code_content})
    
    # Generate output file name with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"code_review_report_{timestamp}.md"
    
    # Write results to Markdown file
    with open(output_file, 'w') as f:
        f.write("# Relatório de Revisão de Código\n\n")
        f.write(f"**Data da revisão:** {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        f.write("**Arquivo analisado:** sample_code.tsx\n\n")
        f.write("## Resultados da Análise\n\n")
        f.write(result.raw)
    
    print(f"Análise completa! Relatório salvo em: {output_file}")

if __name__ == "__main__":
    main()