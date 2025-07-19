from flask import Flask, request, jsonify, render_template
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
import os
import sys
import io
import re

load_dotenv(override=True)

api_key = os.environ.get('GROQ_KEY')
print(api_key)

def clean_terminal_codes(text):
    return re.sub(r'\x1b\[[0-9;]*m', '', text)

app = Flask(__name__)

# Web Search Agent setup
web_search_agent = Agent(
    name="Web Search Agent",
    role="search web",
    model=Groq(id="llama-3.3-70b-versatile", api_key=api_key),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tools_calls=True,
    markdown=True
)

# Finance Agent setup
finance_agent = Agent(
    name="Finance Agent",
    role="analyze finance data",
    model=Groq(id="llama-3.3-70b-versatile", api_key=api_key),
    tools=[YFinanceTools(stock_price=True, stock_fundamentals=True, company_news=True)],
    instructions=["Use tables to display the data"],
    show_tools_calls=True,
    markdown=True
)

# Multi-Aid Agent setup
multi_aid_agent = Agent(
    name="Multi-Aid Agent",
    role="assisting users with multiple needs",
    model=Groq(id="llama-3.3-70b-versatile", api_key=api_key),
    teams=[web_search_agent, finance_agent],
    instructions=["Always include sources", "Use table to display the data"],
    show_tools_calls=True,
    markdown=True
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask-bot', methods=['POST'])
def ask_question():
    question = request.json.get('question')

    if not question:
        return jsonify({"error": "No question provided"}), 400

    original_stdout = sys.stdout
    sys.stdout = io.StringIO()

    multi_aid_agent.print_response(question, stream=True)

    captured_response = sys.stdout.getvalue()

    sys.stdout = original_stdout

    cleaned_response = clean_terminal_codes(captured_response)

    return jsonify({"response": cleaned_response.strip()})

if __name__ == '__main__':
    app.run(debug=True)
