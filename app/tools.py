from langchain_core.tools.retriever import create_retriever_tool
from langchain_core.tools import Tool, StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from pandasai.connectors import SqliteConnector
from pandasai import SmartDataframe
import pandas as pd
import sqlite3
from datetime import datetime, timedelta


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-001",
    temperature=0,
)

def current_datetime_tool(query: str) -> str:
    """Return the current date and time based on location"""
    now = datetime.datetime.now()
    return f"The current date and time is: {now.strftime('%Y-%m-%d %H:%M:%S')}"    

def recomendation_savings(transaction_data: str, user_interaction: str) -> str:
    """Generate recommendation savings from the transaction data or struk belanja"""
    messages = [
        (
            "system",
            "You are a helpfull assistant that can help to generate recommendation savings from the transaction data or struk belanja"
        ),
        ('human', f'Transaction Data: {transaction_data}\nUser Instruction: {user_interaction}'),
    ]

    response = llm.invoke(messages)
    return response.content

def get_data_transaction():
    """Get the user transaction data"""
    conn = sqlite3.connect("data/finance.db")
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    conn.close()
    transaction_data = df.to_string()
    
    return transaction_data


def visualization_tools(query: str) :
    """Generate visualization from transaction data. This will return a image of the visualization. the path is saved in exports/charts/temp_chart.png"""
    connector = SqliteConnector(
        config={
            'database': 'data/finance.db',
            'table': 'transactions'
        }
    )

    df = SmartDataframe(connector, config={'llm': llm})

    response = df.chat(f"{query}")

    return response 

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


