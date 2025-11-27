from langchain_classic.agents import Tool
from utils import classify_intent, check_balance, report_card_issues, unsupported

classify_tool = Tool(
    name="IntentClassifier",
    func=classify_intent,
    description="Classifies user intent in a banking conversation.",
)

balance_tool = Tool(
    name="CheckBalance",
    func=check_balance,
    description="Returns account balance for a givien account_id.",
)

card_tool = Tool(
    name="ReportCardIssues",
    func=report_card_issues,
    description="Block a acard and return next steps.",
)

unsupported_tool = Tool(
    name="Unsupported",
    func=unsupported,
    description="Use this tool when the user's request cannot be handled by any other tool.",
)

tools = [classify_tool, balance_tool, card_tool, unsupported_tool]