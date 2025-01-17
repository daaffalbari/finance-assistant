from langchain_core.tools.retriever import create_retriever_tool
from langchain_core.tools import Tool, StructuredTool


def monthly_report(transaction_data: str, user_interaction: str) -> str: 
    """Generate monthly report from the transactions data"""
    messages = [
        (
            "system",
            "You are a helpfull assistant that can help to generate monthly report from the transactions data"
        ),
        ('human', f'Transaction Data: {transaction_data}\n User Instruction: {user_interaction}'),
    ]

    response = llm.invoke(messages)
    return response.content