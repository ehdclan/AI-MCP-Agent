🏦 AI Banking Assistant
A conversational AI-powered banking assistant that provides secure, intelligent banking services through natural language interactions. Built with LangChain and Azure OpenAI, this system allows customers to check balances, view transactions, and report card issues seamlessly.

🌟 Features
🔐 Secure Login System - Simple PIN-based authentication

💬 Natural Language Processing - Understands banking queries in everyday language

🏦 Banking Operations:

Balance inquiries

Transaction history

Card issue reporting (lost/stolen/damaged cards)

Account management

🧠 AI-Powered - Uses Azure OpenAI GPT-4 for intelligent responses

💾 Conversation Memory - Remains context-aware during conversations

🛡️ Error Handling - Robust error handling and input validation

🚀 Quick Start
Prerequisites
Python 3.8 or higher

Azure OpenAI service access

Basic understanding of Python environments

Installation
Clone or download the project files to your local machine

Create a virtual environment (recommended):

bash
python -m venv banking_env
source banking_env/bin/activate  # On Windows: banking_env\Scripts\activate
Install required dependencies:

bash
pip install -r requirements.txt
Set up environment variables:
Create a .env file in the project root with your Azure OpenAI credentials:

env
azure_resource_endpoint=your_azure_endpoint_here
azure_resource_key=your_azure_api_key_here
model_endpoint=your_intent_classifier_endpoint
model_api_key=your_intent_classifier_api_key
Running the Application
Activate your virtual environment (if not already activated):

bash
source banking_env/bin/activate  # On Windows: banking_env\Scripts\activate
Launch the banking assistant:

bash
python main.py
Login with test credentials:

text
Available test accounts:
------------------------------
Account: 001 | PIN: 1234 | Name: Ini
Account: 002 | PIN: 5678 | Name: Bolu
Account: 003 | PIN: 9012 | Name: Ebuka
Account: 004 | PIN: 3456 | Name: Daniel
------------------------------
Start interacting with the assistant using natural language!

💬 Example Conversations
Once logged in, try these examples:

text
You: What's my balance?
Assistant: Hello Ini! Your balance is ₦200,000

You: I lost my card
Assistant: Hello Ini!
Your card has been blocked immediately.

Next Steps:
• New card ready in 48 hours
• Collect at any branch with ID
• Reference: CARD-001-LOST/STOLEN
• Urgent help: 0800-BANK-HELP

You: Show my recent transactions
Assistant: Here are your recent transactions...
🗂️ Project Structure
text
banking-assistant/
├── main.py                 # Main application and login system
├── utils.py               # Utility functions and banking operations
├── tools.py               # LangChain tool definitions
├── requirements.txt       # Python dependencies
└── .env                  # Environment variables (create this)
File Descriptions
main.py - Core application with login system, agent initialization, and chat interface

utils.py - Contains banking logic: balance checks, transaction handling, card issues

tools.py - Defines AI tools for intent classification and banking operations

requirements.txt - Lists all Python package dependencies

🔧 Configuration
Azure OpenAI Setup
Obtain Azure OpenAI credentials from the Azure Portal

Ensure you have a deployed GPT-4 model (gpt-4o-mini recommended)

Update the .env file with your specific endpoints and keys

Test Accounts
The system comes with four pre-configured test accounts:

Account	PIN	Name	Balance
001	1234	Ini	₦200,000
002	5678	Bolu	₦420,000
003	9012	Ebuka	₦30,000,000
004	3456	Daniel	₦250,000
🛠️ Development
Adding New Banking Features
Add new intent classification in utils.py:

python
def simple_classification(text):
    # Add new condition
    if any(word in text_lower for word in ['loan', 'apply']):
        return 'loan_application'
Create corresponding tool in tools.py:

python
loan_tool = Tool(
    name="LoanApplication",
    func=handle_loan_application,
    description="Process loan applications and eligibility checks",
)
Implement the handler in utils.py:

python
def handle_loan_application(query):
    # Your loan application logic here
Customization Options
Modify account data in utils.py accounts dictionary

Adjust AI parameters in azure_llm() function in main.py

Extend conversation memory by modifying LangChain memory settings

Add new banking tools by following the existing pattern

🐛 Troubleshooting
Common Issues
ModuleNotFoundError: No module named 'langchain'

Solution: Run pip install -r requirements.txt to install all dependencies

Azure API authentication errors

Verify your .env file contains correct endpoints and keys

Check that your Azure OpenAI resource is active and properly configured

Login failures

Use the exact test account IDs and PINs provided

Ensure you're entering numeric values without spaces

Agent execution errors

Check that all required tools are properly defined in tools.py

Verify the intent classification system is functioning

Getting Help
If you encounter issues:

Check that all environment variables are set correctly

Verify your Python version is 3.8 or higher

Ensure all dependencies are installed from requirements.txt

Check the Azure OpenAI service status

🔒 Security Notes
⚠️ Important Security Considerations

This is a demonstration system with simple PIN-based authentication

In production, implement proper password hashing and secure authentication

Never store real credentials in plain text

Use HTTPS in production environments

Consider implementing session timeouts and additional security measures

📝 License
This project is for educational and demonstration purposes. Please ensure compliance with your organization's security policies before deploying in production environments.

🎯 Next Steps
Potential enhancements for production use:

Database integration for account storage

SMS/Email verification for transactions

Multi-factor authentication

Transaction processing capabilities

Integration with real banking APIs

Web interface or mobile app frontend