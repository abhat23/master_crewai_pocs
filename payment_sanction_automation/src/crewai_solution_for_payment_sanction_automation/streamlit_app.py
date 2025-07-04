# app.py
import streamlit as st
from crew import CrewaiSolutionForPaymentSanctionAutomationCrew
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="CrewAI Streamlit", layout="centered")

st.title("🤖 CrewAI Streamlit App")
st.markdown("Interact with your Crew of AI agents.")

topic = st.text_input("Enter a topic to research and summarize:", "Generative AI in Healthcare")

if st.button("Run Crew"):
    with st.spinner("Agents at work..."):
        inputs = {
                'topic': topic
        }
        result = CrewaiSolutionForPaymentSanctionAutomationCrew().crew().kickoff(inputs=inputs)
        st.success("Crew finished the task!")
        st.markdown("### 📄 Output")
        st.markdown(result)
