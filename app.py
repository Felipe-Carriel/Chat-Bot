import streamlit as st
import os
from dotenv import load_dotenv
from google import genai


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("⚠️ Defina a variável de ambiente GEMINI_API_KEY no seu .env")
else:
   
    client = genai.Client(api_key=API_KEY)


st.set_page_config(page_title="Chatbot de Redes", page_icon="💻", layout="centered")
st.title("🤖 Chatbot de Fundamentos de Redes e Segurança")


personas = {
    "Professor exigente de redes": "Você é um professor exigente de redes e segurança. Responda de forma técnica e cobre raciocínio do aluno.",
    "Hacker arrependido": "Você é um hacker arrependido que agora ensina redes e segurança para evitar que os alunos cometam erros.",
    "Analista de segurança experiente": "Você é um analista de segurança de redes experiente, com explicações claras, exemplos práticos e dicas do mercado."
}


persona_escolhida = st.selectbox("Escolha a personalidade do assistente:", list(personas.keys()))


if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])


if prompt := st.chat_input("Pergunte sobre Redes e Segurança..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

   
    contexto = personas[persona_escolhida]
    chat_history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])

    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{contexto}\nHistórico:\n{chat_history}\nResponda a última pergunta do usuário."
    )

    
    resposta = response.text

    
    st.chat_message("assistant").markdown(resposta)
    st.session_state.messages.append({"role": "assistant", "content": resposta})
