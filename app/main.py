from fastapi import FastAPI, HTTPException
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import ChatVertexAI
from langchain_google_vertexai import VertexAIEmbeddings
from langchain.tools import tool
from langchain_chroma import Chroma
from langchain_community.utilities import SQLDatabase
from langchain_community.document_loaders import PyPDFLoader
from langchain import hub
from langchain.utilities import SQLDatabase
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType

from langchain_core.tools.retriever import create_retriever_tool
from langchain_core.tools import Tool, StructuredTool

import vertexai
import os
import pandas as pd
import sqlite3
import datetime

_ = load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION")

vertexai.init(project=PROJECT_ID, location=LOCATION)

LANGCHAIN_TRACING_V2= os.getenv('LANGCHAIN_TRACING_V2')
LANGCHAIN_ENDPOINT= os.getenv('LANGCHAIN_ENDPOINT')
LANGCHAIN_API_KEY= os.getenv('LANGCHAIN_API_KEY')
LANGCHAIN_PROJECT= os.getenv('LANGCHAIN_PROJECT')

llm = ChatVertexAI(
    model="gemini-1.5-pro-001",
    temperature=0,
)


def save_file(uploaded_file, upload_dir):  
    if uploaded_file is not None:  
        file_path = os.path.join(upload_dir, uploaded_file.name)  
        with open(file_path, 'wb') as f:  
            f.write(uploaded_file.getbuffer())  
        return file_path  
    return None  



def extract_receipt(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    embeddings = VertexAIEmbeddings(
        model_name="text-multilingual-embedding-002"
    )

    vector_store = Chroma.from_documents(
    docs,
    embeddings,
    collection_name="receipts",
    persist_directory='data/'
    )   

    reciept_retriever = vector_store.as_retriever(search_kwargs={"k": 1})

    return reciept_retriever


def transaction_parser(transaction_file):
    docs = pd.read_csv(transaction_file)
    docs.to_string()

    conn = sqlite3.connect("data/finance.db")
    df = pd.read_sql_query("SELECT budget, rules FROM budget_categories", conn)
    conn.close()

    template_prompt = """
    Your task is to check the transactions have a categories or not. If the transaction dont have a category, you can assign a category to the transaction.
    In category have a rules, if the transaction have a keyword in the rules, you can assign the category to the transaction.

    here is the list of transactions:
    {transaction}

    Here is the list of categories:
    {categories}

    please answer in the following format json. always answer in the following format.
    {{
        "date": <date>,
        "category": <category>,
        "amount": <amount>,
        "description": <description>
    }}
    """

    prompt = ChatPromptTemplate.from_template(template_prompt)
    output_parser = JsonOutputParser()

    chain = prompt | llm | output_parser

    response = chain.invoke({
        "transaction": docs,
        "categories": df
    })

    transaction_clean = pd.DataFrame(response)

    return transaction_clean


def export_transaction_clean_to_db(transaction_clean):
    conn = sqlite3.connect("data/finance.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        date DATE,
        amount REAL,
        description TEXT,
        category TEXT
    )
    """)
    conn.commit()
    
    transactions_df['date'] = pd.to_datetime(transactions_df['date'], errors='coerce')
    transactions_df = transactions_df.dropna(subset=['date']) 
    transactions_df['date'] = transactions_df['date'].dt.strftime('%Y-%m-%d')  
    
    transactions_df.to_sql('transactions', 
                          conn, 
                          if_exists='append', 
                          index=False)

    return 'Data has been exported to database'


app = FastAPI()


@app.get('/')
def read_root():
    return {
        'message': 'Hello World'
    }

@app.get('/chat')
async def chat():
    return {
        'message': 'Chat'
    }