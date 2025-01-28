# Financial Agentic AI

This project is a **multi-agent financial AI system** designed to provide real-time responses to financial queries. The system operates by integrating multiple AI agents and external APIs to fetch and process information dynamically. It uses **PhiData** for handling structured datasets, **Groq** for computational optimization, and real-time search capabilities via DuckDuckGo and Yahoo Finance.

---

## Functionality

1. **Multi-Agent AI System:** Combines different AI agents to handle diverse financial tasks like data lookup, analysis, and query answering.
2. **Real-Time Data Fetching:** Retrieves live financial data from sources such as Yahoo Finance and DuckDuckGo search engine.
3. **Dynamic Query Processing:** Accepts user input in natural language, processes it through an advanced NLP pipeline, and generates contextualized financial insights.

---

## Development Stack

### Core Technologies:
- **Backend:** Python with Flask for handling API routes and business logic.
- **Data Handling:** PhiData for managing and processing structured data.
- **Computation:** Groq for high-performance optimization during multi-agent interactions.

### APIs and Tools:
- **Search API:** DuckDuckGo for fetching real-time search results.
- **Finance API:** Yahoo Finance for stock and market-related queries.
- **Frontend:** HTML, CSS, and JavaScript for creating an interactive terminal-like user interface.

---

## How It Works

1. **User Query:** Users interact with the terminal interface to ask financial questions in plain English.
2. **Agent Execution:** The query is processed by the **multi-aid-agent** module, which utilizes:
   - **Search Agent:** Performs real-time web searches.
   - **Data Agent:** Retrieves structured financial data.
   - **Analysis Agent:** Analyzes and summarizes the retrieved information.
3. **Response Generation:** The system combines results from all agents and generates a coherent response displayed in the terminal interface.

---

## Key Features

- **Real-Time Search:** Fetches the latest and most relevant data from the web.
- **Multi-Source Integration:** Combines data from structured and unstructured sources for comprehensive insights.
- **Optimized AI Workflow:** Utilizes Groq’s high-performance infrastructure for multi-agent collaboration.

---
