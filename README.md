MedScan AI
A high-aesthetic, medical-document-analysis web application built with Streamlit and Groq-hosted vision models (qwen/qwen3.6-27b). It allows users to upload photos of medications or lab reports to receive clear, structured, and plain-language clinical breakdowns.

Features
AI Vision Integration: Leverages Groq's high-performance vision endpoint to interpret medical documents and prescription labels accurately.

Plain-Language Summaries: Breaks down complex medical jargon into easy-to-understand explanations for users without a medical background.

Modern UI Design: Custom blue-themed layout with Google Fonts (Outfit, Plus Jakarta Sans), high-contrast result containers, and a polished user experience.

Robust Error Handling: Built-in retry logic for API rate limits and automatic removal of internal model reasoning (<think> tags).

Tech Stack
Frontend: Streamlit

Backend / AI: Groq API (qwen/qwen3.6-27b)

Image Processing: Pillow (PIL)

HTTP Requests: Requests

Project Structure
Plaintext
med-report-simplifire/
│
├── .streamlit/
│   └── secrets.toml       # Local configuration for API keys
├── app.py                 # Streamlit frontend user interface
├── gemini_service.py      # Backend API communication and image processing
└── requirements.txt       # Project dependencies
Setup & Installation
Clone the repository or open your project folder in VS Code.

Create and activate a virtual environment:

Bash
python -m venv venv
Windows (CMD): venv\Scripts\activate.bat

Windows (PowerShell): .\venv\Scripts\Activate.ps1

Mac / Linux: source venv/bin/activate

Install dependencies:

Bash
pip install -r requirements.txt
Configure your API Key:

Create a folder named .streamlit in your project root.

Inside .streamlit, create a file named secrets.toml.

Add your Groq API key:

Ini, TOML
GROQ_API_KEY = "your_actual_groq_api_key_here"
Run the application locally:

Bash
streamlit run app.py
