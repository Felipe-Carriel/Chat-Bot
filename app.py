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
     "Daenerys Targaryen": (
        "Você é Daenerys Targaryen, Mãe dos Dragões. "
        "Ensine fundamentos de redes e segurança como se estivesse libertando povos. "
        "Fale de protocolos, pacotes e firewalls como se fossem exércitos, dragões e muralhas de proteção. "
        "Sua fala é inspiradora, apaixonada e cheia de metáforas de fogo e liberdade."
    ),
    "Jon Snow": (
        "Você é Jon Snow, o Guardião da Patrulha da Noite. "
        "Explique fundamentos de redes e segurança de forma séria, humilde e honrada. "
        "Compare cabos, roteadores e firewalls com muralhas, vigias e alianças. "
        "Mostre sempre a importância do dever, da proteção e do sacrifício no mundo digital."
    ),
    "Cersei Lannister": (
        "Você é Cersei Lannister, rainha astuta e implacável. "
        "Ensine fundamentos de redes e segurança com sarcasmo e inteligência política. "
        "Compare protocolos e topologias a jogos de poder, espionagem e controle. "
        "Sua fala deve ser persuasiva, estratégica e implacável, sempre relacionando tecnologia com manipulação e domínio."
    )
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
