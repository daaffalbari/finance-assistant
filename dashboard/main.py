import streamlit as st
import requests 

api_url = 'http://localhost:8000/chat'


def get_response(query, history_input, history_output):
    payload = {
        'query': query,
        'history_input': history_input,
        'history_output': history_output,      
    }
    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            response_data = response.json()
            return response_data['response'], response_data['total_tokens']
        else:
            return f"Error: Status Code {response.status_code}, Details: {response.json()}"
    except Exception as e:
        return f"Error: {str(e)}"


st.title('Finance Assistant')

with st.sidebar:
    st.header('Upload Your Data')
    transaction_file = st.file_uploader('Transaction File', type=['csv'])
    shopping_list = st.file_uploader('Shopping List', type=['pdf'])


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if query := st.chat_input("Masukan pesan Anda di sini"):
    st.chat_message("user", avatar="🧑‍💻").markdown(query)

    history_input = [msg['content'] for msg in st.session_state.messages if msg['role'] == 'user']
    history_output = [msg['content'] for msg in st.session_state.messages if msg['role'] == 'assistant']

    st.session_state.messages.append({"role": "user", "content": query})

    response, total_tokens = get_response(query, history_input, history_output)

    with st.chat_message("assistant", avatar="🦖"):
        st.write(response)
        st.write(f"Total Tokens: {st.session_state.tokens + total_tokens}")

    st.session_state.messages.append({"role": "assistant", "content": response})