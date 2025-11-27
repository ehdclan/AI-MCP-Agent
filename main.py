import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents.mrkl.base import ZeroShotAgent
from tools import tools

load_dotenv()

accounts = {
        "001": {
            "name": "Ini",
            "balance": 200000
        },

        "002": {
            "name": "Bolu",
            "balance": 420000
        },

        "003": {
            "name": "Ebuka",
            "balance": 30000000
        },

        "004": {
            "name": "Daniel",
            "balance": 250000
        }
    }


def azure_llm():
    llm = AzureChatOpenAI(
        azure_endpoint = os.getenv("azure_resource_endpoint"),
        api_key = os.getenv("azure_resource_key"),
        api_version = "2024-12-01-preview",
        max_tokens = 4096,
        temperature = 0,
        azure_deployment = "gpt-4o-mini",
    )
    return llm

def banking_agent():
    llm = azure_llm()
    prompt_template = '''You are a helpful banking assistant for a Nigerian bank.

CRITICAL RULES:
1. ALWAYS use the IntentClassifier tool first to understand what the user wants
2. If the user asks about balance but doesn't provide an account number, politely ask for it
3. Only use CheckBalance when you have a valid 3-digit account number (001-004)
4. Be polite, professional, and use Nigerian Naira (₦) for currency

AVAILABLE TOOLS:
- IntentClassifier: Understands what the user wants
- CheckBalance: Gets account balance (needs account number)
- ReportCardIssues: Blocks cards for security
- Unsupported: For requests you can't handle

User query: {input}

Think step by step and use the right tools.

{agent_scratchpad}'''

    agent = ZeroShotAgent.from_llm_and_tools(
        llm=llm,
        tools=tools,
        prefix=prompt_template
    )
    
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5
    )
    return agent_executor

if __name__ == "__main__":
    print("Banking Assistant Started...")

    agent = banking_agent()
    test_queries = [
        "What is my account balance?",
        "My account number is 001, what's my balance?",
        "I lost my card, please block it. Account 002",
    ]
    
    print("\n Running test queries...\n")
    
    for query in test_queries:
        print(f"USER: {query}")
        try:
            result = agent.invoke({"input": query})
            print(f"\n ASSISTANT: {result['output']}")
        except Exception as e:
            print(f"\n ERROR: {str(e)}")
        
        print("\n")