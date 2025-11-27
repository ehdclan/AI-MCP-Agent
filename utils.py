import os, json, requests
from dotenv import load_dotenv
from langchain_classic.agents.mrkl.base import ZeroShotAgent

load_dotenv()

accounts = {
    "001": {"name": "Ini", "balance": 200000},
    "002": {"name": "Bolu", "balance": 420000},
    "003": {"name": "Ebuka", "balance": 30000000},
    "004": {"name": "Daniel", "balance": 250000}
}


def classify_intent(text: str):
    model_api_endpoint = os.getenv("model_endpoint")
    model_api_key = os.getenv("model_api_key")
    response = requests.post(
        url=model_api_endpoint,
        json={"text": text},
        headers={
            "Authorization": f"Bearer {model_api_key}",
            "Content-Type": "application/json"
        },
    )

    data = dict(response.json())
    print(data["prediction"])
    return data["prediction"]

def extract_account_id(text: str):
    import re
    match = re.search(r'\b(\d{3})\b', text)
    return match.group(1) if match else None

def check_balance(account_id: str):
    extracted_id = extract_account_id(account_id)
    acct = accounts.get(extracted_id)
    if not acct:
        return {'error': "Account not found. Please provide a valid 3-digit account number."}

    return {
        'account_id': extracted_id,
        'name': acct['name'],
        'balance': acct['balance'],
        'message': f"Account holder: {acct['name']}, Balance: ₦{acct['balance']:,}"
    }
    
def report_card_issues(account_id: str):
    #simulate blocking card
    extracted_id = extract_account_id(account_id)
    return {"status": "blocked",
            "account_id": extracted_id, 
            "next_step": "Collect new card in 48 hours"
            }

def unsupported(text: str):
    return "Sorry, I cannot assist with that request."