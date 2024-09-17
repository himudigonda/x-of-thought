import streamlit as st
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from prompts import basic_prompt, cot_prompt, got_prompt

@st.cache_resource
def get_llm():
    """
    Retrieve and cache the Ollama language model instance for use in the application.

    Returns:
        Ollama: An instance of the Ollama language model configured with a specific model version.
    """
    return Ollama(model="llama3.1:8b-instruct-q4_K_M")

# Initialize the language model
llm = get_llm()

# Initialize language model chains for different types of prompts
basic_chain = LLMChain(llm=llm, prompt=basic_prompt)  # Basic question-answer chaining
cot_chain = LLMChain(llm=llm, prompt=cot_prompt)     # Chain of Thought for detailed reasoning
got_chain = LLMChain(llm=llm, prompt=got_prompt)     # Graph of Thoughts for complex reasoning paths
