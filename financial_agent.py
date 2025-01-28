from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
import openai
import os
import sys
import io

load_dotenv()

api_key= os.environ.get('GROQ_KEY')

original_stdout = sys.stdout
sys.stdout = io.StringIO()


#web agent
web_search_agent = Agent(
    name="Web Search Agent",
    role="search web",
    model=Groq(id = "llama-3.3-70b-versatile",api_key=api_key),
    tools = [DuckDuckGo()],
    instructions = ["Always include sources"],
    show_tools_calls = True,
    markdown = True
)

#Finance agent
finance_agent = Agent(
    name="Finance Agent",
    role="analyze finance data",
    model=Groq(id = "llama-3.3-70b-versatile",api_key=api_key),
    tools = [YFinanceTools(stock_price = True, stock_fundamentals = True, company_news = True)],
    instructions = ["Use tables to display the data"],
    show_tools_calls = True,
    markdown = True
)

multi_aid_agent = Agent(
    name="Multi-Aid Agent",
    role="assisting users with multiple needs",
    model=Groq(id = "llama-3.3-70b-versatile",api_key=api_key),
    teams = [web_search_agent, finance_agent],
    instructions = ["Always include sources", "Use table to display the data"],
    show_tools_calls = True,
    markdown = True
)

multi_aid_agent.print_response("which stock should I buy in between Tesla and NVDA", stream=True)

captured_response = sys.stdout.getvalue()

# Reset stdout back to the original
sys.stdout = original_stdout

# Now you can use captured_response for further processing
print(captured_response)