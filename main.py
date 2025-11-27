import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents.mrkl.base import ZeroShotAgent
from langchain_classic.memory import ConversationBufferMemory
from tools import tools
from utils import extract_account_id
import getpass

load_dotenv()

memory = ConversationBufferMemory(memory_key="chat_history")
account_id = None

accounts = {
    "001": {"pin": "1234", "name": "Ini", "account_id": "001"},
    "002": {"pin": "5678", "name": "Bolu", "account_id": "002"}, 
    "003": {"pin": "9012", "name": "Ebuka", "account_id": "003"},
    "004": {"pin": "3456", "name": "Daniel", "account_id": "004"}
    }

def login():
    global account_id
    
    print("Welcome. Please login to begin...")
    
    max_attempts = 3
    attempts = 0
    
    while attempts < max_attempts:
        try:
            acc_id = input("Enter your Account ID: ").strip()
            if acc_id.lower() == 'exit':
                print("\n Goodbye!\n")
                break
            
            if acc_id not in accounts:
                print("Account ID not found. Please try again.\n")
                attempts += 1
                continue
                
            pin = getpass.getpass("Enter your PIN: ")
            
            user_data = accounts.get(acc_id)
            if not user_data:
                print(" Error, invalid credentials.\n")
                attempts += 1
                continue
                
            if "pin" not in user_data:
                print(" Invalid Pin.\n")
                attempts += 1
                continue
                
            if pin == user_data["pin"]:
                account_id = acc_id
                user_name = user_data.get("name", "Customer")
                print(f"\n Login successful! Welcome back, {user_name}!")
                return True
            else:
                attempts += 1
                remaining_attempts = max_attempts - attempts
                if remaining_attempts > 0:
                    print(f"Invalid PIN. {remaining_attempts} attempt(s) remaining.\n")
                else:
                    print("Invalid PIN.\n")
                
        except KeyboardInterrupt:
            print("\n\nLogin cancelled.")
            return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            attempts += 1
    
    print("Too many failed attempts. Please try again later.")
    return False


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
    global account_id
    llm = azure_llm()

    account_context = ""

    if account_id:
        account_context = f"\nIMPORTANT: User's account ID is {account_id} - use this automatically!"
    
    prompt_template = '''You are a helpful banking assistant for a Nigerian bank.

1. ALWAYS use IntentClassifier tool FIRST to understand user intent
2. Check if account ID is available before asking for it
3. Use the appropriate tool based on classified intent
4. Be professional and helpful
{account_context}

{{chat_history}}

User query: {{input}}

Let's think step by step.

{{agent_scratchpad}}'''

    prompt = prompt_template.format(account_context=account_context)

    agent = ZeroShotAgent.from_llm_and_tools(
        llm=llm,
        tools=tools,
        prefix=prompt
    )
    
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,
        memory=memory
    )
    return agent_executor

def process_message(user_input):
    global account_id
    
    agent = banking_agent()
    
    try:
        result = agent.invoke({"input": user_input})
        return result["output"]
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    if not login():
        print("Exiting...")
        exit(1)

    print("Banking Assistant Started... \n")

    print("Start chatting! Try: 'My account is 001, what's my balance?'\n")

    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            if user_input.lower() == 'exit':
                print("\n Goodbye!\n")
                break
            if user_input.lower() in ['logout', 'sign out']:
                print("\n Logged out successfully.\n")
                break
            print("\n Assistant: ", end="", flush=True)
            response = process_message(user_input)
            print(response + "\n")
            
        except KeyboardInterrupt:
            print("\n\n Interrupted. Type 'exit' to quit.\n")
            continue
        except Exception as e:
            print(f"\n Error: {str(e)}\n")