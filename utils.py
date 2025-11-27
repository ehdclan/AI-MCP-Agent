import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

accounts = {
    "001": {"name": "Ini", "balance": 200000},
    "002": {"name": "Bolu", "balance": 420000},
    "003": {"name": "Ebuka", "balance": 30000000},
    "004": {"name": "Daniel", "balance": 250000}
}

transactions = {
    "001": [
        {"id": "TXN001", "type": "credit", "amount": 50000, "status": "completed", "date": "2025-11-20"},
        {"id": "TXN002", "type": "debit", "amount": 10000, "status": "pending", "date": "2025-11-25"}
    ],
    "002": [
        {"id": "TXN003", "type": "credit", "amount": 100000, "status": "completed", "date": "2025-11-22"},
        {"id": "TXN004", "type": "debit", "amount": 5000, "status": "failed", "date": "2025-11-26", "reason": "Insufficient funds"}
    ],
    "003": [
        {"id": "TXN005", "type": "debit", "amount": 1000000, "status": "completed", "date": "2025-11-24"}
    ],
    "004": []
}


def extract_account_id(text):
    match = re.search(r'\b(\d{3})\b', text)
    return match.group(1) if match else None


def classify_intent(text):
    try:
        model_endpoint = os.getenv("model_endpoint")
        model_key = os.getenv("model_api_key")
        
        if model_endpoint and model_key:
            response = requests.post(
                url=model_endpoint,
                json={"text": text},
                headers={
                    "Authorization": f"Bearer {model_key}",
                    "Content-Type": "application/json"
                },
                timeout=5
            )
            
            data = response.json()
            intent = data.get("prediction", "unsupported")
            print(f"Intent: {intent}")
            return intent
    except:
        pass
    
    return simple_classification(text)


def simple_classification(text):
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['balance', 'how much', 'check account']):
        return 'check_balance'
    
    if any(word in text_lower for word in ['transaction', 'transfer', 'pending', 'failed', 'payment']):
        return 'check_transaction'
    
    if any(word in text_lower for word in ['card', 'lost', 'stolen', 'block', 'damaged', 'activate']):
        return 'report_card'
    
    return 'unsupported'


def check_balance(account_id):
    acc_id = extract_account_id(account_id)
    
    if not acc_id:
        return {
            'error': True,
            'message': "Please provide a 3-digit account number (001-004)."
        }
    
    account = accounts.get(acc_id)
    
    if not account:
        return {
            'error': True,
            'message': f"Account {acc_id} not found. Valid accounts: 001-004."
        }
    
    return {
        'error': False,
        'account_id': acc_id,
        'name': account['name'],
        'balance': account['balance'],
        'message': f"Hello {account['name']}! Your balance is ₦{account['balance']:,}"
    }


def handle_transaction(query):
    acc_id = extract_account_id(query)
    
    if not acc_id:
        return {
            'error': True,
            'message': "Please provide your account number to view transactions."
        }
    
    if acc_id not in accounts:
        return {
            'error': True,
            'message': f"Account {acc_id} not found."
        }
    
    user_txns = transactions.get(acc_id, [])
    
    if not user_txns:
        return {
            'error': False,
            'message': f"No transactions found for account {acc_id}."
        }


def report_card_issues(query):
    acc_id = extract_account_id(query)
    
    if not acc_id:
        return {
            'error': True,
            'message': "Please provide your account number for card issues."
        }
    
    if acc_id not in accounts:
        return {
            'error': True,
            'message': f"Account {acc_id} not found."
        }
    
    query_lower = query.lower()
    
    if 'lost' in query_lower or 'stolen' in query_lower:
        issue = "lost/stolen"
        action = "Your card has been blocked immediately."
    elif 'damaged' in query_lower or 'broken' in query_lower:
        issue = "damaged"
        action = "Your damaged card has been deactivated."
    elif 'not working' in query_lower or 'declined' in query_lower:
        issue = "malfunction"
        action = "Card flagged for technical review."
    elif 'activate' in query_lower:
        issue = "activation"
        action = "Card activation request received."
    else:
        issue = "general"
        action = "Card issue logged."
    
    name = accounts[acc_id]['name']
    
    return {
        'error': False,
        'message': f"Hello {name},\n\n{action}\n\n"
                   f"Next Steps:\n"
                   f"• New card ready in 48 hours\n"
                   f"• Collect at any branch with ID\n"
                   f"• Reference: CARD-{acc_id}-{issue.upper()}\n"
                   f"• Urgent help: 0800-BANK-HELP"
    }

def unsupported(text):
    """Handle unsupported requests"""
    return (
        "I cannot assist with that request. I can help with:\n"
        "• Checking balances\n"
        "• Viewing transactions\n"
        "• Reporting card issues\n\n"
        "For other services, visit a branch or call 0800-BANK-HELP."
    )