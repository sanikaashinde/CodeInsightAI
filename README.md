# CodeInsight AI

CodeInsight AI is an intelligent static code analysis platform built with Python and Streamlit.

## Features

- Source code analysis
- Project/ZIP analysis
- Security vulnerability detection
- Cyclomatic complexity analysis
- Code smell detection
- Code quality scoring
- Project structure analysis
- Dependency analysis
- Analysis history
- AI-powered code summary
- User authentication
- Configurable analysis settings

## Tech Stack

- Python
- Streamlit
- SQLite
- AST-based static analysis
- Google Gemini AI

## Project Structure

CodeInsightAI/
├── app/
│   ├── components/
│   └── pages/
├── core/
│   ├── analysis/
│   ├── auth.py
│   ├── parser/
│   └── utils/
├── data/
├── uploads/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md

## Run Locally

Install dependencies:

pip install -r requirements.txt

Start the application:

streamlit run main.py

## AI Configuration

Create a `.env` file and add your Gemini API key:

GEMINI_API_KEY=your_api_key_here

Do not commit the `.env` file to GitHub.

## Author

Sanika Shinde
