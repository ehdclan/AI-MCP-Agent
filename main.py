import os, json, requests
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_classic.agents import AgentExecutor, Tool
from langchain_classic.prompts import PromptTemplate
import azure.cognitiveservices.speech as speech
from langchain_classic.agents.mrkl.base import ZeroShotAgent
from tools import *

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

if __name__ == "__main__":

    llm = azure_llm()

    prompt_agent = '''You are a banking assistant. You must follow these steps:
    1. First, ALWAYS use the intentClassifier tool to understand the user's intent.
    2. Then, based on the classified intent, use the appropriate tool
    3. If the user does not provide an account number, ask them to provide it.
    4. Only use CheckBalance when you have an actual account number
    User query: {input}
    Let's think step by step.'''

    agent = ZeroShotAgent.from_llm_and_tools(
        llm = llm,
        tools = tools,
        prefix = prompt_agent
    )

    agent_executor = AgentExecutor.from_agent_and_tools(
        agent = agent,
        tools = tools,
        verbose = True,
        handle_parsing_errors = True
    )

    result = agent_executor.invoke({"input": "What is my account balance?"})
    print(result["output"])