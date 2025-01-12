# LangGraph Practice

A project exploring LangGraph for building stateful multi-agent applications.

## Overview

This repository contains experiments and practice implementations using LangGraph, a library for creating structured, multi-agent workflows. LangGraph enables the creation of complex agent interactions and stateful applications using language models.

## Project Structure

- `agent_flow.png` - Visualization of the agent interaction flow
- `main.py` - Main application entry point (CLI version)
- `app.py` - Flask web interface
- `nodes.py` - Agent definitions and behaviors
- `agent_state.py` - State management
- `.env` - Environment configuration (required for API keys)

## Requirements

- Python 3.x
- OpenAI API key

## Installation

1. Clone this repository
2. Create and activate a virtual environment:
   ```bash
   # For Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # For macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   # First, remove any conflicting packages
   pip uninstall langchain langchain-core langchain-openai langgraph langchain-text-splitters langgraph-checkpoint -y

   # Then install all required packages
   pip install --upgrade langchain langgraph langchain-openai openai python-dotenv flask graphviz IPython
   ```

4. Set up your environment:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to `.env`

## Usage

### CLI Version
Run the command-line interface:
```bash
python main.py
```

### Web Interface
Run the Flask web application:
```bash
# For Windows
python app.py

# For macOS/Linux
export FLASK_APP=app.py
flask run
```

Then open your web browser and navigate to:
- http://localhost:5000 or
- http://127.0.0.1:5000

The system will present a web interface for selecting and executing tasks using the multi-agent workflow.

## License

(Add license information)