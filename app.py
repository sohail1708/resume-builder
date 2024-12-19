import getpass
import os
from langchain_groq import ChatGroq

# Set the GROQ API key
os.environ["GROQ_API_KEY"] = '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'

# Initialize the LLM model
llm = ChatGroq(model="llama3-8b-8192")