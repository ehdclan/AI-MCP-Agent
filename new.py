from utils import classify_intent, check_balance, report_card_issues, unsupported

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

while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    intent = classify_intent(user_input)

    if intent == "transactions":
        response = check_balance(user_input)
    elif intent == "card":
        response = report_card_issues(user_input)
    else:
        response = unsupported(user_input)

    print("Agent:", response)


