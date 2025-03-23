from langchain_ollama import Ollama
from langchain.agents import load_tools, initialize_agent
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the Ollama language model
llm = Ollama(model="phi3.5", temperature=0)

# Load tools
tools = load_tools(["ddg-search", "llm-math"], llm=llm)

# Initialize the agent
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# Run the agent with the query
agent.run("What is the coldest temperature record for New York City? What is the difference in that temperature and the current one?")
