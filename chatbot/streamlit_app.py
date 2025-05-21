import requests
import os
from dotenv import load_dotenv
import streamlit as st

st.title("Customer Executive Chatbot")

st.write("Ask any question below:")

user_question = st.text_input("Your question:")
# Load environment variables
load_dotenv()

if st.button("Ask"):
    if user_question.strip():
        try:
            response = requests.post(
                f"{os.getenv('BASE_URL')}/api/ask/",
                json={"question": user_question},
                timeout=10
            )
            if response.status_code == 200:
                answer = response.json().get("answer", "No answer returned.")
                st.success(answer)
            else:
                st.error(f"API Error: {response.status_code}")
        except Exception as e:
            st.error(f"Request failed: {e}")
    else:
        st.warning("Please enter a question.")
