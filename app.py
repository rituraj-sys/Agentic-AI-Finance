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

# Load environment variables from .env file
load_dotenv()

# Get API key for GROQ model
api_key = os.environ.get('GROQ_KEY')

# Define the function to clean escape sequences
def clean_terminal_codes(text):
    # Remove any ANSI escape sequences
    return re.sub(r'\x1b\[[0-9;]*m', '', text)

# Initialize Flask app
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

# Route for serving the HTML page
@app.route('/')
def index():
    return render_template('index.html')  # Your HTML file should be named 'index.html'

# Route to handle questions asked by the user
@app.route('/ask-bot', methods=['POST'])
def ask_question():
    # Get the question from the POST request
    question = request.json.get('question')

    if not question:
        return jsonify({"error": "No question provided"}), 400

    # Redirect stdout to capture the response
    original_stdout = sys.stdout
    sys.stdout = io.StringIO()

    # Generate the response for the question
    multi_aid_agent.print_response(question, stream=True)

    # Capture the response from the redirected stdout
    captured_response = sys.stdout.getvalue()

    # Reset stdout back to the original
    sys.stdout = original_stdout

    # Clean the response to remove terminal codes
    cleaned_response = clean_terminal_codes(captured_response)

    # Return the cleaned response in the JSON response
    return jsonify({"response": cleaned_response.strip()})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
